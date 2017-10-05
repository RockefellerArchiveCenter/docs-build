#!/usr/bin/env python
# pulls files and builds sites

import sys
import yaml
from json import loads
from os import chdir, makedirs, listdir
from os.path import join, isdir, isfile, normpath, abspath, dirname
from posix import remove
from shutil import copyfile, copytree, rmtree
from subprocess import call

# base path for the GitHub Webhook handling application
base_path = normpath(abspath(join(dirname(__file__), '..')))

with open(join(base_path, 'config.json'), 'r') as cfg:
    config = loads(cfg.read())

with open(sys.argv[1], 'r') as jsf:
  payload = loads(jsf.read())

site_root_dir = config.get('site_root_dir')
repository_dir = config.get('repository_dir')
staging_dir = config.get('staging_dir')
build_dir = config.get('build_dir')
public_site_dir = config.get('public_site_dir')
private_site_dir = config.get('private_site_dir')
repository_name = payload['repository']['name']
repository_url = payload['repository']['ssh_url']

def get_updates():
    # If the repository exists, update the data
    if isdir(join(repository_dir, repository_name)):
        chdir(join(repository_dir, repository_name))
        print "pulling from "+repository_name
        call("git pull", shell=True)
    # If the repository doesn't already exist, make a directory and pull down the data
    else:
        makedirs(join(repository_dir, repository_name))
        chdir(repository_dir)
        print "cloning "+repository_name
        call("git clone " + repository_url, shell=True)

def create_structure(target, site, name):
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

    copytree(join(repository_dir, name), target)

def build_site(base_url, source, destination):
    chdir(base_url)
    print "building at " + base_url
    print "jekyll build --source %s --destination %s" % (source, destination)
    call("jekyll build --source %s --destination %s" % (source, destination), shell=True)
    # set file permissions and ownership if necessary

def build(directory):
    with open(join(repository_dir, directory, '_config.yml')) as f:
        yaml_config = yaml.load(f)
        if yaml_config['type'] == 'docs':
            if yaml_config['public'] == True:
                sites = [public_site_dir, private_site_dir]
            else:
                sites = [private_site_dir]
            update_docs(directory, sites)
        if yaml_config['type'] == 'theme':
            update_theme(directory, [public_site_dir, private_site_dir])

def update_docs(name, sites = [], *args):
    print "*** building documentation ***"
    for site in sites:
        site_staging_dir = join(site_root_dir, site, staging_dir)
        # this file is used to generate the site home page
        if not isdir(join(site_staging_dir, '_data')):
            makedirs(join(site_staging_dir, '_data'))
        copyfile(join(repository_dir, name, '_config.yml'), join(site_staging_dir, '_data', name + '.yml'))

        create_structure(join(site_staging_dir, name), site, name)

        build_site(join(site_root_dir, site), staging_dir, build_dir)

def update_theme(name, sites = [], *args):
    print "*** building theme ***"
    for site in sites:
        site_staging_dir = join(site_root_dir, site, staging_dir)

        create_structure(site_staging_dir, site, name)

    for s in listdir(repository_dir):
        if isdir(join(repository_dir, s)):
            with open(join(repository_dir, s, '_config.yml')) as f:
                yaml_config = yaml.load(f)
                if yaml_config['type'] == 'docs':
                    if yaml_config['public'] == True:
                        sites = [public_site_dir, private_site_dir]
                    else:
                        sites = [private_site_dir]
                    for site in sites:
                        copytree(join(repository_dir, s), join(site_root_dir, site, staging_dir, s))

    for site in sites:
        build_site(join(site_root_dir, site), staging_dir, build_dir)

def main():
    get_updates()
    build(repository_name)

main()
