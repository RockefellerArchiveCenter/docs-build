#!/usr/bin/env python
# pulls files and builds sites

import sys
import json
import yaml
from os import chdir, mkdir
from os.path import join, isdir
from posix import remove
from shutil import copyfile, copytree, rmtree
from subprocess import call
from ConfigParser import ConfigParser, NoSectionError

# use existing config file?
config = ConfigParser()
config.read(local_settings.cfg)

with open(sys.argv[1], 'r') as jsf:
  payload = json.loads(jsf.read())

repository_dir = config.get('Directories', 'repositories')
repository_name = payload['repository']['name']
repository_url = payload['repository']['ssh_url']

# If the repository exists, update the data
if isdir(join(repository_dir, repository_name)):
    chdir(join(repository_dir, repository_name))
    call("git pull")
    build_sites(repository_name)
# If the repository doesn't already exist, make a directory and pull down the data
else:
    mkdir(join(repository_dir, repository_name))
    chdir(join(repository_dir, repository_name))
    call("git pull")
    call("git clone " + repository_url)
    build_sites(repository_name)

def build_sites(directory):
    with open('config.yml') as f:
        yaml_config = yaml.load(f)
        # Does it make sense to rely on whether or not the repository is private?
        if yaml_config['public'] = 'true':
            sites = [config.get('Directories', 'public'), config.get('Directories', 'private')]
        else:
            sites = [config.get('Directories', 'private')]
        build_site(directory, sites)

def build_site(name, sites = [], *args):
    for site in sites:
        # We are still in repository/name
        # this file is used to generate the home page
        copyfile('config.yml', join(site, config.get('Directories', 'staging'), 'data', name + '.yml'))

        if isdir(join(site, config.get('Directories', 'staging'), name)):
            rmtree(join(site, config.get('Directories', 'staging'), name))
        if isfile(join(site, config.get('Directories', 'staging'), name)):
            # in case someone put something (like a softlink) in its place
            remove(join(site, config.get('Directories', 'staging'), name))

        try:
            makedirs(config.get('Directories', 'build'))
        except OSError:
            # dir exists
            pass

        copytree(join(repository_dir, name), join(site, config.get('Directories', 'staging'), name))

        chdir(site)

        #staging --> build
        call("jekyll build --source %s --destination %s" % config.get('Directories', 'staging'), config.get('Directories', 'build'))

        # set file permissions and ownership if necessary
