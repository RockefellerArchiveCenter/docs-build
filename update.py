#!/usr/bin/env python
# pulls files and builds sites

import subprocess
import sys
import yaml
from json import loads
from os import chdir, makedirs, listdir
from os.path import join, isdir, isfile, normpath, abspath, dirname
from posix import remove
from shutil import copyfile, copytree, rmtree
from subprocess import call

# base path for the build script
base_path = normpath(abspath(join(dirname(__file__))))

with open(join(base_path, 'config.json'), 'r') as cfg:
    config = loads(cfg.read())

site_root_dir = config.get('site_root_dir')
repository_dir = config.get('repository_dir')
staging_dir = config.get('staging_dir')
build_dir = config.get('build_dir')
public_site_dir = config.get('public_site_dir')
private_site_dir = config.get('private_site_dir')


def get_updates(repository_name):
    # If the repository exists, update the data
    if isdir(join(site_root_dir, repository_dir, repository_name)):
        chdir(join(site_root_dir, repository_dir, repository_name))
        print "pulling from "+repository_name
        call("git pull", shell=True)


def create_structure(src, target, site):
    if isdir(target):
        rmtree(target)
    if isfile(target):
        # in case someone put something (like a softlink) in its place
        remove(target)
    try:
        makedirs(join(site_root_dir, site, build_dir))
    except OSError:
        # dir exists
        pass
    copytree(src, target)


def build_site(base_url, source, destination):
    chdir(base_url)
    print "Jekyll building at " + base_url
    call("/usr/local/rvm/gems/ruby-2.1.8/wrappers/jekyll build --source %s --destination %s" % (source, destination), shell=True)
    call("node %s/create-index.js %s/search-data.json %s/search-index.json" % (base_path, destination, destination), shell=True)


def build_structure(directory):
    with open(join(site_root_dir, repository_dir, directory, '_config.yml')) as f:
        yaml_config = yaml.load(f)
        if yaml_config['type'] == 'docs':
            if yaml_config['public']:
                sites = [public_site_dir, private_site_dir]
            else:
                sites = [private_site_dir]
            update_docs_structure(directory, sites)


def update_docs_structure(name, sites=[], *args):
    print "*** building documentation ***"
    for site in sites:
        site_staging_dir = join(site_root_dir, site, staging_dir)
        data_file = join(site_root_dir, site_staging_dir, '_data', name + '.yml')
        # this file is used to generate the site home page
        if not isdir(join(site_staging_dir, '_data')):
            makedirs(join(site_staging_dir, '_data'))
        copyfile(join(site_root_dir, repository_dir, name, '_config.yml'), data_file)
        with open(data_file) as f:
            yaml_config = yaml.safe_load(f)
        yaml_config['slug'] = name
        yaml_config['github_repo'] = 'https://github.com/RockefellerArchiveCenter/{0}'.format(name)
        with open(data_file, 'w') as f:
            yaml.safe_dump(yaml_config, f, default_flow_style=False)
        create_structure(join(site_root_dir, repository_dir, name), join(site_staging_dir, name), site)


def update_theme_structure(name, sites=[], *args):
    print "*** building theme ***"
    for site in sites:
        site_staging_dir = join(site_root_dir, site, staging_dir)
        create_structure(join(base_path, name), site_staging_dir, site)


def main():
    update_theme_structure('theme', [public_site_dir, private_site_dir])
    for d in listdir(join(site_root_dir, repository_dir)):
        get_updates(d)
        build_structure(d)
    for site in [public_site_dir, private_site_dir]:
        build_site(join(site_root_dir, site), staging_dir, build_dir)


main()
