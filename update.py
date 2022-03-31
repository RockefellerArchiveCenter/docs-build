#!/usr/bin/env python

import json
import mimetypes
import os
import subprocess
from datetime import datetime
from shutil import copyfile, copytree, rmtree

import boto3
import yaml


def copy_dir(src, target):
    if os.path.isdir(target):
        rmtree(target)
    copytree(src, target)


def call_command(command):
    try:
        c = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        while True:
            line = c.stdout.readline().rstrip()
            if not line:
                break
            print(line)
    except Exception as e:
        print(f'Error calling `{" ".join(command)}`: {e}')


class UpdateRoutine:
    def run(self, audience, branch, deploy=True):
        with open('repositories.yml') as f:
            repositories_config = yaml.safe_load(f)
        site = Site()
        site.update_theme()
        site.stage(repositories_config[audience], branch, audience)
        site.build()
        if deploy:
            site.upload(audience, branch)
        return f'Update process for {audience} {branch} site completed at {datetime.now()}'


class Site:
    def __init__(self):
        self.staging_dir = '/tmp/staging/'
        self.build_dir = '/tmp/build/'
        self.repositories_dir = '/tmp/repositories/'

    def update_theme(self):
        copy_dir('theme', os.path.join(self.staging_dir))

    def stage(self, repositories, branch, audience):
        os.makedirs(os.path.join(self.staging_dir, '_data'))
        for repo in repositories:
            self.current_repo = repo
            repo_path = os.path.join(self.repositories_dir, self.current_repo)
            repo_url = (f'https://github.com/RockefellerArchiveCenter/{self.current_repo}.git'
                        if audience == 'public' else
                        f'https://{os.environ.get("GH_TOKEN")}@github.com/RockefellerArchiveCenter/{self.current_repo}.git')
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
        call_command(['/usr/local/rvm/gems/ruby-2.6.6/wrappers/jekyll', 'build',
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
        s3 = boto3.resource(
            service_name='s3',
            region_name=os.environ.get('REGION_NAME'),
            aws_access_key_id=os.environ.get('ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('SECRET_KEY'))
        for root, dirs, files in os.walk(self.build_dir):
            for f in files:
                mtype, _ = mimetypes.guess_type(os.path.join(root, f))
                s3.meta.client.upload_file(
                    os.path.join(root, f),
                    os.environ.get(
                        f'{branch.upper()}_{audience.upper()}_BUCKET_NAME'),
                    os.path.join(
                        root.replace(
                            self.build_dir,
                            '').lstrip('/'),
                        f),
                    ExtraArgs={'ContentType': mtype if mtype else 'application/json'})


def main(event, context):
    if event:
        audience = 'private' if event.get(
            'repository', {}).get('private') else 'public'
        branch = event.get('ref', '').replace('refs/heads/', '')
        if branch not in ['base', 'development']:
            return {
                'statusCode': 200,
                'body': json.dumps(f"Branch {branch} is not eligible to be built")
            }
        message = UpdateRoutine().run(audience, branch)
        if audience == 'public':
            UpdateRoutine().run('private', branch)
            message = f'Update process for public and private {branch} sites completed at {datetime.now()}'
        return {
            'statusCode': 200,
            'body': json.dumps(message)
        }
    else:
        return UpdateRoutine().run('private', 'base', False)
