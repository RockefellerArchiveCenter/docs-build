#!/usr/bin/env python

import yaml
from json import loads
import os
from shutil import copyfile, copytree, rmtree
import subprocess
from datetime import datetime


base_path = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__))))
with open(os.path.join(base_path, 'config.json.sample'), 'r') as cfg:
    config = loads(cfg.read())


def copy_dir(src, target):
    if os.path.isdir(target):
        rmtree(target)
    copytree(src, target)


def call_command(command):
    c = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = c.communicate()
    if len(output[1]):
        print("Error calling `{command}`: {output}".format(command=" ".join(command), output=output[1]))


class UpdateRoutine:
    def run(self):
        print("Update process started at {time}".format(time=datetime.now()))
        call_command(["git", "submodule", "init"])
        call_command(["git", "submodule", "update", "--remote"])
        for s in [config['public_site'], config['private_site']]:
            site = Site(s)
            site.update_theme()
            site.stage()
            site.build()
        print("Update process completed at {time}".format(time=datetime.now()))


class Site:
    def __init__(self, site_config):
        self.root = os.path.join(config['site_root'], site_config['root'])
        self.staging_dir = os.path.join(self.root, site_config['staging'])
        self.build_dir = os.path.join(self.root, site_config['build'])
        self.repositories_dir = os.path.join(config['site_root'], config['repositories'])
        self.site_config = site_config
        for d in [self.build_dir, os.path.join(self.staging_dir)]:
            if os.path.isdir(d):
                rmtree(d)
            os.makedirs(d)

    def update_theme(self):
        print("Updating theme")
        copy_dir(os.path.join(base_path, 'theme'), os.path.join(self.staging_dir))

    def stage(self):
        print("Staging site")
        os.makedirs(os.path.join(self.staging_dir, '_data'))
        for repo in os.listdir(self.repositories_dir):
            self.current_repo = repo
            self.current_repo_dir = os.path.join(self.repositories_dir, self.current_repo)
            if self.has_repo():
                data_file = os.path.join(self.staging_dir, '_data', self.current_repo + '.yml')
                copyfile(
                    os.path.join(self.current_repo_dir, '_config.yml'),
                    data_file)
                self.update_data_file(data_file)
                copy_dir(
                    os.path.join(self.current_repo_dir),
                    os.path.join(self.staging_dir, self.current_repo))

    def build(self):
        print("Building site")
        call_command(["/usr/local/rvm/gems/ruby-2.1.8/wrappers/jekyll", "build",
                      "--source", self.staging_dir, "--destination", self.build_dir])
        for repo in os.listdir(self.repositories_dir):
            self.current_repo = repo

    def has_repo(self):
        if not os.path.isdir(self.current_repo_dir):
            return False
        if self.site_config == config['public_site']:
            with open(os.path.join(self.current_repo_dir, '_config.yml')) as f:
                yaml_config = yaml.safe_load(f)
                return True if yaml_config['public'] else False
        elif self.site_config == config['private_site']:
            return True

    def update_data_file(self, data_file):
        updated_date = self.get_updated_date()
        with open(data_file) as f:
            yaml_config = yaml.safe_load(f)
        yaml_config['updated'] = updated_date.rstrip()
        yaml_config['slug'] = self.current_repo
        yaml_config['github_repo'] = 'https://github.com/RockefellerArchiveCenter/{0}'.format(self.current_repo)
        with open(data_file, 'w') as f:
            yaml.safe_dump(yaml_config, f, default_flow_style=False)

    def get_updated_date(self):
        out = subprocess.Popen(["git --git-dir={0}/.git show --format=%ci".format(self.current_repo_dir)], stdout=subprocess.PIPE, shell=True)
        return out.communicate()[0]


UpdateRoutine().run()
