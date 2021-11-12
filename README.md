# docs-build

Theme file along with a Python script which retrieves updates for documentation
repositories, and builds internal and external-facing sites. It can be set to
run at a specified time (for example on a nightly basis) using cron. Requires at
least one documentation repository (see [processing-manual](https://github.com/RockefellerArchiveCenter/processing-manual)).

![Build Status](https://travis-ci.org/RockefellerArchiveCenter/docs-build.svg?branch=base)](https://travis-ci.org/RockefellerArchiveCenter/docs-build)

## Quick Start

A Docker container is included in this repository so you can quickly spin up a sample site on your computer. With git and Docker installed, run:

    git clone https://github.com/RockefellerArchiveCenter/docs-build.git
    cd docs-build/repositories
    git submodule add https://github.com/RockefellerArchiveCenter/docs-guide.git
    docker-compose up

The public docs site will be available in your browser at `http://localhost:4000` and the private site will be available at `http://localhost:4001`. This will include the RAC's Documentation Site Guide to Managing Content as an example piece of documentation. To include additional sets of documentation, you will need to add them as submodules in the `repositories/` subdirectory. Refer to the [Adding Repositories](#adding-repositories) section of this document.

## Setup

### Update configuration files

Copy or move `theme/_config.yml.example` to `theme/_config.yml`. You may need to modify some
of the configs in this file in order to build the site correctly for your needs.

Then, configure the site build by copying the sample config file
`config.json.sample` to `config.json` and adapting it to your needs. The structure
of that file looks like this:

    {
        "site_root": "/home/docs",
        "repositories": "docs-build/repositories",
        "public_site": {
          "root": "public",
          "staging": "staging",
          "build": "build",
          "link": "/var/www/external"
        },
        "private_site": {
          "root": "private",
          "staging": "staging",
          "build": "build",
          "link": "/var/www/internal"
        }
    }

`repositories`: Sets base directory into which repositories will be pulled from
Github using git submodules. This directory must be a subdirectory of the root
directory of this repository.

`site_root`: Configures the root directory for the site.

`public_site` and `private_site`: Objects containing configs to be set for each site.

`root`: Sets the root directory for the site, which will be nested underneath `site_root_dir`.

`staging`: Configures the staging directory to which directories will be copied
before the build process, which will be nested below the `root` directory for that site.

`build`: Configures the directory into which the final sites will be built,
which will be nested below the `root` directory for that site.

`link`: Configures an optional symbolic link target. Useful if you want to build
your site somewhere other than a web accessible directory on your server.

### Install dependencies

In order to use the script which updates the site, you will need to install some
system dependencies:

- Python 3.6
- Ruby 2.6.6
- Jekyll 4.0.0

In addition, several Python packages need to be installed. Ideally you should
set a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to isolate these dependencies. Once you've done that, the quickest way to install dependencies is
to use `pip`:
```
pip install -r requirements.txt
```

## Build Script

`update.py` is the script that pulls the updated data from GitHub, and then
rebuilds the site using Jekyll. It handles build processes for documentation and
theme repositories differently.

#### Documentation Repository Configuration

In order to work correctly, `build_sites.py` expects that the following variables
will be available in a file named `_config.yml` located the root directory of a
documentation repository. These files should be valid [YAML](http://yaml.org).

    public: true
    category: "collection development and management"
    tags:
      - "policy"
    title: "Collection Policy"
    description: "The main collecting areas of the Rockefeller Archive Center."
    pages:
      - ["Rockefeller Archive Center Collection Policy", "index"]

`public` indicates whether or not the documentation should be public. Values
should be either `true` or `false` (booleans, not strings).

`categories` indicate what archival life cycle category(s) applies to the documentation. Categories enable filtering of documentation items on homepage. Values should be `"collection development and management"`, `"preservation"`, `"arrangement and description"`, and/or `"reference and outreach"`.

`tags` are used to describe what type of documentation the item is. Values should be either `"policy"` or `"workflow"`.

`title` is the official title of the documentation, which will be displayed on
the home page of the site.

`description` is a statement of what the documentation is. This text will become the description meta tag for the site, which is displayed in search-engine results, so keep it short and snappy.

`pages` is a list of lists of the pages included in this site. The first value
in each list is the name, and the second is the filename of the page (without the
extension). These values are used when building tables of contents.

Other variables can be included in this config file if desired.


#### Theme

The site uses a Jekyll-based theme to create a cohesive structure and
customizable interface. These files are located in the `theme/` directory.

Layouts are written in HTML and are chiefly composed from a separate directory
of Jekyll-based includes and one default layout template. They are styled with
both Bootstrap and custom CSS and are rendered with the Liquid template language.

The layout directory formats the various documentation files stored in the
individual GitHub repositories and thereby creates the site's central interface for
access to documentation. This process is achieved through the use of layout
variables in the documentation files' YAML front matter.

#### Build Structure

The build process copies directories and files to a "staging" structure before executing the Jekyll build, which generates HTML files and places them in their final location.

Assuming the values in `config.json.sample` above, the final structure would be:

    /var/www/
      ∟public/
        ∟staging/
          ∟files to be built
        ∟build/
          ∟generated site
      ∟private/
        ∟staging/
          ∟files to be built
        ∟build/
          ∟generated site

The `build` directory for the public and private sites contain the final sites that need to be served up via Apache or some other method.

#### Adding Repositories

Documentation repositories are managed as [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules). To add a new repository, from the root of this repository navigate into the `repositories/` directory:

      cd repositories/

Then run the following command, substituting `submodule_url` with a URL for a repository on GitHub, such as `https://github.com/rockefellerArchiveCenter/processing-manual`:

      git submodule add [submodule url]

If you want to see how things look immediately, you can trigger the build process by running `update.py`

## Docker image

The Dockerfile in the root of this repository provides an easy way to get up and
running, and allows for easy local development. The image built from this file
is used in the Compose file as well as in the continuous integration pipeline.

To publish changes to this image, first build it locally:

      docker build -t rockarch/docs-build-base .

And then push the built image to Docker Hub:

      docker push rockarch/docs-build-base:latest


## Contributing

Pull requests accepted!

## Authors

Hillel Arnold  
Hannah Sistrunk  
Katie Martin  
Darren Young  

## License

This code is released under an [MIT License](LICENSE).
