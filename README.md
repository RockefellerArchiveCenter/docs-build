# docs-build

A Python script which retrieves updates for documentation repositories and themes, and builds internal and external-facing sites. It can be set to run at a specified time (for example on a nightly basis) using cron. Requires a theme repository (see [docs-theme](https://github.com/RockefellerArchiveCenter/docs-theme) for an example) and at least one documentation repository (see [processing-manual](https://github.com/RockefellerArchiveCenter/processing_manual))

## Install

    git clone https://github.com/RockefellerArchiveCenter/docs-build.git
    cd docs-build
    ./install.sh

`./install.sh` will install all the necessary dependencies, and also set SSH keys which enable the application to interact with Github.

## Setup

You can configure what the application does by copying the sample config file
`config.json.sample` to `config.json` and adapting it to your needs:

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

`repositories`: Sets base directory into which repositories will be pulled from Github. See below for details

`site_root`: Configures the root directory for the site.

`public_site` and `private_site`: Objects containing configs which will be set for each site.

`root`: Sets the root directory for the site, which will be nested underneath `site_root_dir`.

`staging`: Configures the staging directory to which directories will be copied before the build process, which will be nested below the `root` directory for that site.

`build`: Configures the directory into which the final sites will be built, which will be nested below the `root` directory for that site.

`link`: Configures an optional symbolic link target. Useful if you want to build your site somewhere other than a web accessible directory on your server.

## Build Script

`update.py` is the script that pulls the updated data from GitHub, and then rebuilds the site using Jekyll. It handles build processes for documentation and theme repositories differently.

#### YAML Configuration

In order to work correctly, `build_sites.py` expects that the following variables will be available in a file named `_config.yml` located the root directory of a documentation or theme repository.

    public: true
    type: "docs"
    tags:
      - "processing"
      - "planning"
      - "project vitals"
    title: "Guide to Processing Collections at the RAC"
    description: "A manual for arranging and describing archival collections."
    pages:
      - ["About This Site", "index"]

`public` indicates whether or not the documentation should be public. Values should be either `true` or `false` (booleans, not strings).

`type` tells the application whether the repository is a documentation or theme repository, which helps it determine how to handle the build process.

`tags` are a list of tags you wish to associate with the documentation.

`title` is the official title of the documentation, which will be displayed on the home page of the site.

`description` is a short description of what the documentation is, the audience it is intended for, and what it helps that audience do. This text will be displayed on the home page of the site.

`pages` lists all the pages included in this site. The first value in the list is the name, and the second is the filename of the page (without extension). This is used in building tables of contents.

Other variables can be included in this config file if desired.

#### Repository Structure

The application will create a directory (configured in `config.json` as described above) containing subdirectories (based on repository name) for each documentation repository. Based on the default values supplied in `config.json.sample` that structure would be:

    /repositories/
      ∟my-docs-theme/
        ∟theme files
      ∟my-public-docs/
        ∟documentation files
      ∟my-private-docs/
        ∟documentation files

#### Build Structure

The build process copies directories and files from the repository directory to a new structure before executing the Jekyll build structure.

Assuming the values in `config.json.sample` above, the final structure would be:

    /var/www/
      ∟public/
        ∟staging/
          ∟theme files
          ∟my-public-docs
            ∟documentation files
        ∟build/
          ∟index.html
          ∟my-public-docs/
            ∟documentation.html
      ∟private/
        ∟staging/
          ∟theme files
            ∟my-public-docs/
              ∟documentation files
            ∟my-private-docs/
              ∟documentation files
        ∟build/
          ∟index.html
          ∟my-public-docs/
            ∟documentation.html
          ∟my-private-docs/
            ∟documentation.html

The `site_build_directory` for the public and private sites contain the final sites that need to be served up via Apache or some other method.

#### Adding Repositories

To add a repository, navigate to the root of the repositories directory, and then clone the repository you want to add:

      git clone git@github.com:DocumentationWriter/my-awesome-docs.github

If you want to see how things look immediately, you can trigger the build process by running `update.py`

## License

This code is released under an [MIT License](LICENSE)
