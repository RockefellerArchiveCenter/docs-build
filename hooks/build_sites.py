#!/usr/bin/env python
# pulls files and builds sites

# TODO
# test setup file
# add next steps to setup file
# sort out git credentialing
# script for theme updating
# consider using existing config file
# update readme

import sys
import json
import yaml
from os import chdir, makedirs, listdir
from os.path import join, isdir, isfile
from posix import remove
from shutil import copyfile, copytree, rmtree
from subprocess import call
from ConfigParser import ConfigParser, NoSectionError

# use existing config file?
config = ConfigParser()
config.read('local_settings.cfg')

# with open(sys.argv[1], 'r') as jsf:
#   payload = json.loads(jsf.read())

root_dir = config.get('Directories', 'root')
repository_dir = join(root_dir, config.get('Directories', 'repositories'))
staging_dir = config.get('Directories', 'staging')
build_dir = config.get('Directories', 'build')
public_dir = config.get('Directories', 'public')
private_dir = config.get('Directories', 'private')
# repository_name = payload['repository']['name']
repository_name = "theme"
# repository_url = payload['repository']['ssh_url']

def get_updates():
    # If the repository exists, update the data
    if isdir(join(repository_dir, repository_name)):
        chdir(join(repository_dir, repository_name))
        # call("git pull")
    # If the repository doesn't already exist, make a directory and pull down the data
    else:
        makedirs(join(repository_dir, repository_name))
        chdir(join(repository_dir, repository_name))
        # call("git pull")
        # call("git clone " + repository_url)

def create_structure(target, site, name):
    if isdir(target):
        rmtree(target)
    if isfile(target):
        # in case someone put something (like a softlink) in its place
        remove(target)

    try:
        makedirs(join(root_dir, site, build_dir))
    except OSError:
        # dir exists
        pass

    copytree(join(repository_dir, name), target)

def build_sites(directory):
    with open('_config.yml') as f:
        yaml_config = yaml.load(f)
        if yaml_config['type'] == 'docs':
            if yaml_config['public'] == True:
                sites = [public_dir, private_dir]
            else:
                sites = [private_dir]
            build_docs(directory, sites)
        if yaml_config['type'] == 'theme':
            build_theme(directory, [public_dir, private_dir])

def build_docs(name, sites = [], *args):
    print "*** building documentation ***"
    for site in sites:
        site_staging_dir = join(root_dir, site, staging_dir)

        # this file is used to generate the site home page
        if not isdir(join(site_staging_dir, '_data')):
            makedirs(join(site_staging_dir, '_data'))
        copyfile(join(repository_dir, name, '_config.yml'), join(site_staging_dir, '_data', name + '.yml'))

        create_structure(join(site_staging_dir, name), site, name)

        chdir(join(root_dir, site))

        #staging --> build
        print "building" + site
        # call("jekyll build --source %s --destination %s" % (config.get('Directories', 'staging'), config.get('Directories', 'build')))

        # set file permissions and ownership if necessary

def build_theme(name, sites = [], *args):
    print "*** building theme ***"
    for site in sites:
        site_staging_dir = join(root_dir, site, staging_dir)

        create_structure(site_staging_dir, site, name)

    for s in listdir(repository_dir):
        if isdir(join(repository_dir, s)):
            with open(join(repository_dir, s, '_config.yml')) as f:
                yaml_config = yaml.load(f)
                if yaml_config['type'] == 'docs':
                    if yaml_config['public'] == True:
                        sites = [public_dir, private_dir]
                    else:
                        sites = [private_dir]
                    for site in sites:
                        copytree(join(repository_dir, s), join(root_dir, site, staging_dir, s))

    for site in sites:
        chdir(join(root_dir, site))

        #staging --> build
        print "building " +site
        # call("jekyll build --source %s --destination %s" % (config.get('Directories', 'staging'), config.get('Directories', 'build')))

        # set file permissions and ownership if necessary

def main():
    get_updates()
    build_sites(repository_name)

main()
