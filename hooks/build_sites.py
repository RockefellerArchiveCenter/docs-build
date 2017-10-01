#!/usr/bin/env python
# pulls files and builds sites

import sys
import json
import yaml
from os import chdir, mkdir, makedirs
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
repository_name = "test"
# repository_url = payload['repository']['ssh_url']


def build_sites(directory):
    with open('config.yml') as f:
        yaml_config = yaml.load(f)
        # Does it make sense to rely on whether or not the repository is private?
        if yaml_config['public'] == True:
            sites = [public_dir, private_dir]
        else:
            sites = [private_dir]
        build_site(directory, sites)

def build_site(name, sites = [], *args):
    for site in sites:
        site_staging_dir = join(root_dir, site, staging_dir)
        # this file is used to generate the home page
        if not isdir(join(site_staging_dir, '_data')):
            makedirs(join(site_staging_dir, '_data'))
        copyfile(join(repository_dir, name, 'config.yml'), join(site_staging_dir, '_data', name + '.yml'))

        if isdir(join(site_staging_dir, name)):
            rmtree(join(site_staging_dir, name))
        if isfile(join(site_staging_dir, name)):
            # in case someone put something (like a softlink) in its place
            remove(join(site_staging_dir, name))

        try:
            makedirs(join(root_dir, site, build_dir))
        except OSError:
            # dir exists
            pass

        copytree(join(repository_dir, name), join(site_staging_dir, name))

        chdir(join(root_dir, site))

        #staging --> build
        # print "jekyll build --source %s --destination %s" % (config.get('Directories', 'staging'), config.get('Directories', 'build'))
        # call("jekyll build --source %s --destination %s" % (config.get('Directories', 'staging'), config.get('Directories', 'build')))

        # set file permissions and ownership if necessary


# If the repository exists, update the data
if isdir(join(repository_dir, repository_name)):
    chdir(join(repository_dir, repository_name))
    # call("git pull")
    build_sites(repository_name)
# If the repository doesn't already exist, make a directory and pull down the data
else:
    mkdir(join(repository_dir, repository_name))
    chdir(join(repository_dir, repository_name))
    # call("git pull")
    # call("git clone " + repository_url)
    build_sites(repository_name)
