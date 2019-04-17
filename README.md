# docs-build

Theme file along with a Python script which retrieves updates for documentation
repositories, and builds internal and external-facing sites. It can be set to
run at a specified time (for example on a nightly basis) using cron. Requires at
least one documentation repository (see [processing-manual](https://github.com/RockefellerArchiveCenter/processing-manual)).

## Quick Start

A Docker container is included in this repository so you can quickly spin up a sample site on your computer. With git and Docker installed, run:

    git clone https://github.com/RockefellerArchiveCenter/docs-build.git
    git submodule update --init --recursive
    cd docs-build
    docker-compose up

The docs site will be available in your browser at `http://localhost:4000` with three sets of example documentation contained as submodules in the `/repositories` directory.

This container is also useful for development purposes. If you've made changes to files and want to regenerate the site, you can run `docker-compose exec docs python update.py`.

## Install

    git clone https://github.com/RockefellerArchiveCenter/docs-build.git
    cd docs-build
    ./install.sh

`./install.sh` will install all the necessary dependencies, and also creates SSH keys which enable the application to interact with Github.

## Setup

Copy or move `_config.yml.example` to `_config.yml`. You may need to modify some
of the configs in this file in order to build the site correctly for your needs.

You can configure what the application does by copying the sample config file
`config.json.sample` to `config.json` and adapting it to your needs. The structure
of that file looks like this:

    {
        "site_root": "/var/www",
        "repositories": "repositories",
        "public_site": {
          "root": "public",
          "staging": "staging",
          "build": "build",
          "link": "link"
        },
        "private_site": {
          "root": "private",
          "staging": "staging",
          "build": "build",
          "link": "link"
        }
    }

`repositories`: Sets base directory into which repositories will be pulled from
Github.

`site_root`: Configures the root directory for the site.

`public_site` and `private_site`: Objects containing configs to be set for each site.

`root`: Sets the root directory for the site, which will be nested underneath `site_root_dir`.

`staging`: Configures the staging directory to which directories will be copied
before the build process, which will be nested below the `root` directory for that site.

`build`: Configures the directory into which the final sites will be built,
which will be nested below the `root` directory for that site.

`link`: Configures an optional symbolic link target. Useful if you want to build
your site somewhere other than a web accessible directory on your server.

## Build Script

`update.py` is the script that pulls the updated data from GitHub, and then
rebuilds the site using Jekyll. It handles build processes for documentation and
theme repositories differently.

#### Repository Configuration

In order to work correctly, `build_sites.py` expects that the following variables
will be available in a file named `_config.yml` located the root directory of a
documentation repository. These files should be valid [YAML](http://yaml.org).

    public: true
    tags:
      - "policy"
      - "preservation"
      - "appraisal"
      - "mission"
    title: "Collection Policy"
    description: "The main collecting areas of the Rockefeller Archive Center."
    pages:
      - ["Rockefeller Archive Center Collection Policy", "index"]

`public` indicates whether or not the documentation should be public. Values
should be either `true` or `false` (booleans, not strings).

`tags` are a list of tags you wish to associate with the documentation.

`title` is the official title of the documentation, which will be displayed on
the home page of the site.

`description` is a short description of what the documentation is, the audience
it is intended for, and what it helps that audience do. This text will be
displayed on the home page of the site.

`pages` is a list of lists of the pages included in this site. The first value
in each list is the name, and the second is the filename of the page (without the
extension). These values are used when building tables of contents.

Other variables can be included in this config file if desired.

#### Repository Structure

The application will create a directory (configured in `config.json` as described above) containing subdirectories (based on repository name) for each documentation repository. Based on the default values supplied in `config.json.sample` that structure would be:

    /repositories/
      ∟public/
        ∟documentation files
      ∟private/
        ∟documentation files

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

The build process copies directories and files from the repository directory to a new structure before executing the Jekyll build structure.

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

## Contributing

Pull requests accepted!

## Authors

Hillel Arnold  
Hannah Sistrunk  
Katie Martin  
Darren Young  

## License

This code is released under an [MIT License](LICENSE).
