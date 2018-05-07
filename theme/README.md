# docs-theme

A Jekyll-based site for documentation. It provides a central interface for internal
and external access to structured documentation written in a lightweight
markup format (Markdown) and stored in public and private GitHub repositories.

While the other repositories host the content for the documentation, docs-theme
contains the Jekyll-based templates that style, structure, and deploy the website.

## Requirements

Installation of Jekyll is required to build and edit the site locally. Ruby
version 2.2.5 or above is required for installation of Jekyll.

The site will need documentation files for the docs-theme repository to format.
Therefore, at least one documentation GitHub repository is required to associate
with the docs-theme repository (see the [processing-manual repository](https://github.com/RockefellerArchiveCenter/processing-manual) for
an example).

In order to pull the most up-to-date data from the documentation repositories
to the docs-theme repository, a docs-build script must be deployed (see
[docs-build](https://github.com/RockefellerArchiveCenter/docs-build) for more
information on using the script and on correctly setting up a config file for a
documentation repository that is prepared to link with a docs-theme repository)

## Installation

1. Download or clone this repository.
`git clone http://github.RockefellerArchiveCenter/docs-theme`

2. Using your computer's command line, navigate to the directory where the site
  is located on your computer
`example for PC: cd documents/GitHub/docs-theme`

3. Generate the site locally on your computer with the command:
`jekyll serve`

4. Enter the link http://localhost:4000 in your browser to view the site on your
computer

## Usage

You can adjust the config.yml file cloned from the docs-theme repository for
personal needs:

    Site settings
    title: docs.rockarch.org
    description: "A central platform for the documentation of the Rockefeller Archive Center"
    baseurl: # the subpath of your site, e.g. /blog

    Build settings
    markdown: kramdown

    Local settings for building the site
    public: true
    type: theme

Variable type:theme should remain to distinguish theme repository from
documentation repositories.

## How it works

The site uses a directory of Jekyll-based layouts to create a cohesive structure
and theme.

Layouts are written in HTML and are chiefly composed from a separate directory
of Jekyll-based includes and one default layout template. They are styled with
both Bootstrap and custom CSS and are rendered with the Liquid template language.

The layout directory formats the various documentation files stored in the
individual GitHub repositories and thereby creates the site's central interface for
access to documentation. This process is achieved through the use of layout
variables in the documentation files' YAML front matter and the deployment of the
docs-build webhook application.    

## Contributing

Pull requests accepted!

## Authors

Hillel Arnold  
Hannah Sistrunk  
Katie Martin  
Darren Young  

## License

Code is released under an MIT License. See [LICENSE](https://github.com/RockefellerArchiveCenter/docs-theme/blob/master/LICENSE)
for more information.
