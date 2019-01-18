#!/usr/bin/env python
# pulls files and builds sites

import yaml
from json import loads
from os import chdir, makedirs, listdir, symlink
from os.path import join, isdir, isfile, islink, normpath, abspath, dirname
from posix import remove
from shutil import copyfile, copytree, rmtree
import subprocess

# base path for the build script
base_path = normpath(abspath(join(dirname(__file__))))

with open(join(base_path, 'config.json'), 'r') as cfg:
    config = loads(cfg.read())

site_root = config.get('site_root')
repositories = config.get('repositories')
public_site = config.get('public_site')
private_site = config.get('private_site')


def get_updates(repository_name):
    # If the repository exists, update the data
    if isdir(join(site_root, repositories, repository_name)):
        chdir(join(site_root, repositories, repository_name))
        print "pulling from "+repository_name
        subprocess.call("git pull", shell=True)


def create_structure(src, target, site):
    if isdir(target):
        rmtree(target)
    if isfile(target):
        remove(target)
    try:
        makedirs(join(site_root, site['root'], site['build']))
    except OSError:
        # dir exists
        pass
    copytree(src, target)


def build_site(site):
    base_url = join(site_root, site['root'])
    chdir(base_url)
    print "Jekyll building at " + base_url
    subprocess.call("/usr/local/rvm/gems/ruby-2.1.8/wrappers/jekyll build --source %s --destination %s" % (site['staging'], site['build']), shell=True)
    for repo in repositories:
        print repositories
        subprocess.call("node {base_path}/create-index.js {build_dir}/{repo}/search-data.json {build_dir}/{repo}/search-index.json".format(base_path=base_path, build_dir=repositories['build'], repo=repo), shell=True)

def build_structure(directory):
    with open(join(site_root, repositories, directory, '_config.yml')) as f:
        yaml_config = yaml.load(f)
        if yaml_config['public']:
            sites = [public_site, private_site]
        else:
            sites = [private_site]
        update_docs_structure(directory, sites)


def link_site(site):
    target = site['link']
    if isfile(target) or islink(target):
        remove(target)
    if isdir(target):
        rmtree(target)
    symlink(join(site_root, site['root'], site['build']), target)


def update_docs_structure(name, sites=[], *args):
    print "*** building documentation ***"
    for site in sites:
        site_staging_dir = join(site_root, site['root'], site['staging'])
        data_file = join(site_root, site_staging_dir, '_data', name + '.yml')
        out = subprocess.Popen(["git log -1 --format=%ci"], stdout=subprocess.PIPE, shell=True)
        date = out.communicate()[0]
        # this file is used to generate the site home page
        if not isdir(join(site_staging_dir, '_data')):
            makedirs(join(site_staging_dir, '_data'))
        copyfile(join(site_root, repositories, name, '_config.yml'), data_file)
        with open(data_file) as f:
            yaml_config = yaml.safe_load(f)
        yaml_config['updated'] = date.rstrip()
        yaml_config['slug'] = name
        yaml_config['github_repo'] = 'https://github.com/RockefellerArchiveCenter/{0}'.format(name)
        with open(data_file, 'w') as f:
            yaml.safe_dump(yaml_config, f, default_flow_style=False)
        create_structure(join(site_root, repositories, name), join(site_staging_dir, name), site)


def update_theme_structure(name, sites=[], *args):
    print "*** building theme ***"
    for site in sites:
        create_structure(join(base_path, name), join(site_root, site['root'], site['staging']), site)


def main():
    update_theme_structure('theme', [public_site, private_site])
    for d in listdir(join(site_root, repositories)):
        get_updates(d)
        build_structure(d)
    for site in [public_site, private_site]:
        build_site(site)
        if site.get('link'):
            link_site(site)

main()
