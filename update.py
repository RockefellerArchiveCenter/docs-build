#!/usr/bin/env python
# pulls files and builds sites

import yaml
from json import loads
import os
from shutil import copyfile, copytree, rmtree
import subprocess

# base path for the build script
base_path = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__))))

with open(os.path.join(base_path, 'config.json.sample'), 'r') as cfg:
    config = loads(cfg.read())

site_root = config.get('site_root')
repositories = config.get('repositories')
public_site = config.get('public_site')
private_site = config.get('private_site')


def get_updates(repository_name):
    # If the repository exists, update the data
    if os.path.isdir(os.path.join(site_root, repositories, repository_name)):
        os.chdir(os.path.join(site_root, repositories, repository_name))
        print "pulling from "+repository_name
        subprocess.call("git pull", shell=True)


def create_structure(src, target, site):
    if os.path.isdir(target):
        rmtree(target)
    if os.path.isfile(target):
        remove(target)
    try:
        os.makedirs(os.path.join(site_root, site['root'], site['build']))
    except OSError:
        # dir exists
        pass
    copytree(src, target)


def build_site(site):
    base_url = os.path.join(site_root, site['root'])
    os.chdir(base_url)
    print "Jekyll building at " + base_url
    subprocess.call("/usr/local/rvm/gems/ruby-2.1.8/wrappers/jekyll build --source %s --destination %s" % (site['staging'], site['build']), shell=True)
    for repo in os.listdir(os.path.join(site_root, repositories)):
        subprocess.call("node {base_path}/create-index.js {build_dir}/{repo}/search-data.json {build_dir}/{repo}/search-index.json".format(base_path=base_path, build_dir=site['build'], repo=repo), shell=True)


def build_structure(directory):
    with open(os.path.join(site_root, repositories, directory, '_config.yml')) as f:
        yaml_config = yaml.load(f)
        if yaml_config['public']:
            sites = [public_site, private_site]
        else:
            sites = [private_site]
    update_docs_structure(directory, sites)


def link_site(site):
    target = site['link']
    if os.path.isfile(target) or os.path.islink(target):
        os.remove(target)
    if os.path.isdir(target):
        os.path.rmtree(target)
    os.symlink(os.path.join(site_root, site['root'], site['build']), target)


def update_docs_structure(name, sites=[], *args):
    print "*** building documentation ***"
    for site in sites:
        site_staging_dir = os.path.join(site_root, site['root'], site['staging'])
        data_file = os.path.join(site_root, site_staging_dir, '_data', name + '.yml')
        out = subprocess.Popen(["git log -1 --format=%ci"], stdout=subprocess.PIPE, shell=True)
        date = out.communicate()[0]
        # this file is used to generate the site home page
        if not os.path.isdir(os.path.join(site_staging_dir, '_data')):
            os.makedirs(os.path.join(site_staging_dir, '_data'))
        copyfile(os.path.join(site_root, repositories, name, '_config.yml'), data_file)
        with open(data_file) as f:
            yaml_config = yaml.safe_load(f)
        yaml_config['updated'] = date.rstrip()
        yaml_config['slug'] = name
        yaml_config['github_repo'] = 'https://github.com/RockefellerArchiveCenter/{0}'.format(name)
        with open(data_file, 'w') as f:
            yaml.safe_dump(yaml_config, f, default_flow_style=False)
        create_structure(os.path.join(site_root, repositories, name), os.path.join(site_staging_dir, name), site)
        copyfile(
            os.path.join(site_staging_dir, 'search-data.json'),
            os.path.join(site_staging_dir, name, "search-data.json"))


def update_theme_structure(name, sites=[], *args):
    print "*** building theme ***"
    for site in sites:
        create_structure(os.path.join(base_path, name), os.path.join(site_root, site['root'], site['staging']), site)


def main():
    update_theme_structure('theme', [public_site, private_site])
    for d in os.listdir(os.path.join(site_root, repositories)):
        # get_updates(d)
        build_structure(d)
    for site in [public_site, private_site]:
        build_site(site)
        if site.get('link'):
            link_site(site)

main()
