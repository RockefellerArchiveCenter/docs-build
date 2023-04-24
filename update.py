#!/usr/bin/env python

import json
import logging
import mimetypes
import os
import subprocess
from base64 import b64decode
from datetime import datetime
from shutil import copyfile, copytree, rmtree
from urllib.parse import unquote

import boto3
import yaml

RUBY_VERSION = "ruby-3.1.2"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def copy_dir(src, target):
    if os.path.isdir(target):
        rmtree(target, ignore_errors=True)
    copytree(src, target)


def call_command(command):
    try:
        subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    except Exception as e:
        print(f'Error calling `{" ".join(command)}`: {e}')


def decrypt_env_variable(key):
    ENCRYPTED = os.environ[key]
    return boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(ENCRYPTED),
        EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
    )['Plaintext'].decode('utf-8')


class UpdateRoutine:
    def run(self, audience, branch, deploy=True):
        if deploy:
            try:
                decrypt_env_variable(f'{branch.upper()}_{audience.upper()}_BUCKET_NAME')
            except KeyError:
                return f'No build destination for {audience} {branch} site'

        with open('repositories.yml') as f:
            repositories_config = yaml.safe_load(f)
        site = Site(audience)
        site.update_theme()
        site.stage(repositories_config[audience], branch, audience)
        site.build()
        if deploy:
            site.upload(audience, branch)
        return f'Update process for {audience} {branch} site completed at {datetime.now()}'


class Site:
    def __init__(self, audience):
        self.staging_dir = f'/tmp/staging/{audience}/'
        self.build_dir = f'/tmp/build/{audience}/'
        self.repositories_dir = '/tmp/repositories/'

    def update_theme(self):
        copy_dir('theme', os.path.join(self.staging_dir))

    def stage(self, repositories, branch, audience):
        logging.info(f'Staging {audience} site for {branch} branch')
        os.makedirs(os.path.join(self.staging_dir, '_data'))
        for repo in repositories:
            self.current_repo = repo.split("/")[-1]
            repo_path = os.path.join(self.repositories_dir, self.current_repo)
            repo_url = (f'https://github.com/{repo}.git'
                        if audience == 'public' else
                        f'https://{decrypt_env_variable("GH_TOKEN")}@github.com/{repo}.git')
            if os.path.isdir(repo_path):
                rmtree(repo_path)
            call_command([
                'git', 'clone',
                repo_url,
                repo_path,
                '--branch', branch])
            self.current_repo_dir = os.path.join(
                self.repositories_dir, self.current_repo)
            data_file = os.path.join(
                self.staging_dir, '_data', self.current_repo + '.yml')
            copyfile(
                os.path.join(self.current_repo_dir, '_config.yml'),
                data_file)
            self.update_data_file(data_file)
            copy_dir(
                os.path.join(self.current_repo_dir),
                os.path.join(self.staging_dir, self.current_repo))

    def build(self):
        logging.info(f'Building site.')
        call_command([f'/usr/local/rvm/gems/{RUBY_VERSION}/wrappers/jekyll', 'build',
                      '--source', self.staging_dir, '--destination', self.build_dir])

    def update_data_file(self, data_file):
        updated_date = self.get_updated_date()
        with open(data_file) as f:
            yaml_config = yaml.safe_load(f)
        yaml_config['updated'] = updated_date.rstrip()
        yaml_config['slug'] = self.current_repo
        yaml_config[
            'github_repo'] = f'https://github.com/RockefellerArchiveCenter/{self.current_repo}'
        with open(data_file, 'w') as f:
            yaml.safe_dump(yaml_config, f, default_flow_style=False)

    def get_updated_date(self):
        out = subprocess.Popen(
            [f'git --git-dir={self.current_repo_dir}/.git show --format=%ci'],
            stdout=subprocess.PIPE,
            shell=True)
        return out.communicate()[0]

    def upload(self, audience, branch):
        bucket_name = decrypt_env_variable(f'{branch.upper()}_{audience.upper()}_BUCKET_NAME')
        logging.info(f'Uploading site in {self.build_dir} to {bucket_name}.')
        s3 = boto3.client(
            's3',
            region_name=decrypt_env_variable('REGION_NAME'),
            aws_access_key_id=decrypt_env_variable('ACCESS_KEY'),
            aws_secret_access_key=decrypt_env_variable('SECRET_KEY'))
        for root, dirs, files in os.walk(self.build_dir):
            for f in files:
                mtype, _ = mimetypes.guess_type(os.path.join(root, f))
                s3.upload_file(
                    os.path.join(root, f),
                    bucket_name,
                    os.path.join(
                        root.replace(
                            self.build_dir,
                            '').lstrip('/'),
                        f),
                    ExtraArgs={'ContentType': mtype if mtype else 'application/json'})


def main(event=None, context=None):
    if event:
        """Code in this branch is executed in an AWS Lambda context."""
        message_data = json.loads(event['Records'][0]['Sns']['Message'])
        audience = 'private' if message_data['event'].get(
            'repository', {}).get('private') else 'public'
        branch = message_data['event'].get('ref', '').replace('refs/heads/', '')
        if branch not in ['base', 'development']:
            return {
                'statusCode': 200,
                'body': json.dumps(f"Branch {branch} is not eligible to be built")}

        message = UpdateRoutine().run(audience, branch)
        if audience == 'public':
            UpdateRoutine().run('private', branch)
            message = f'Update process for public and private {branch} sites completed at {datetime.now()}'
        logging.info(message)
        return {
            'statusCode': 200,
            'body': json.dumps(message)}


if __name__ == '__main__':
    main()
