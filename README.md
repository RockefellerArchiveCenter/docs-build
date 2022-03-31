# docs-build

Theme file along with a Python script which retrieves updates for documentation
repositories, and builds internal and external-facing sites. Requires at
least one documentation repository (see [processing-manual](https://github.com/RockefellerArchiveCenter/processing-manual)).

![Build Status](https://travis-ci.org/RockefellerArchiveCenter/docs-build.svg?branch=base)](https://travis-ci.org/RockefellerArchiveCenter/docs-build)

## Quick Start

A Dockerfile for local development (`Dockerfile-local`) is included in this repository so you can quickly spin up a sample site on your computer. With git and Docker installed, run:

    git clone https://github.com/RockefellerArchiveCenter/docs-build.git
    docker-compose build
    docker-compose up

The public docs site will be available in your browser at `http://localhost:4000`.

## Usage

## Adding or Removing Repositories

Repositories can be added or removed from either the public or private site by
updating `repositories.yml`. You will also need to make sure the repositories
have the necessary configuration files
(see [Documentation Repository Configuration](#documentation-repository-configuration))
and configure a webhook to trigger a build of the site
(see [GitHub Webhooks](#github-webhooks)).


### Theme

The site uses a Jekyll-based theme to create a cohesive structure and
customizable interface. These files are located in the `theme/` directory.

Layouts are written in HTML and are chiefly composed from a separate directory
of Jekyll-based includes and one default layout template. They are styled with
both Bootstrap and custom CSS and are rendered with the Liquid template language.

The layout directory formats the various documentation files stored in the
individual GitHub repositories and thereby creates the site's central interface for
access to documentation. This process is achieved through the use of layout
variables in the documentation files' YAML front matter.

## Deployment

This site is intended to be deployed as an AWS Lambda which pushes updates
to an S3 bucket from where they can be served.

### Environment Variables

The following environment variables must be present in order for this deployment pattern to work effectively:
- `GH_TOKEN` - a GitHub Personal Access Token which has the necessary permissions
  to clone private repositories. Make sure this  has the scope org:read as well.
- `GH_SECRET` - a secret key associated with the GitHub Webhook.
- Environment variables for S3 buckets to which files will be uploaded. These
  should be formatted as {BRANCH}_{AUDIENCE}_BUCKET_NAME:
  - `DEVELOPMENT_PRIVATE_BUCKET_NAME`
  - `BASE_PRIVATE_BUCKET_NAME`
  - `BASE_PUBLIC_BUCKET_NAME`
- `REGION_NAME` - the AWS region in which the S3 buckets are located.
- `ACCESS_KEY` - an Access Key for an IAM user that has the necessary permissions to upload files to the bucket.
- `SECRET_KEY` - the Secret Key for an IAM user with the necessary permissions to upload files to the bucket.

### GitHub Webhooks

In order to trigger deployments, a webhook which listens for `push` events should
be added to a GitHub repository. This webhook should point at the AWS API Gateway
endpoint tied to the Lambda task.

A Secret should be added in the webhook configuration, the value of which should
match the `GH_TOKEN` environment variable from the preceding section.

## Documentation Repository Configuration

In order to build the full documentation site, the following variables must be
available in a file named `_config.yml` located the root directory of each
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

## Contributing

Pull requests accepted!

## Authors

Hillel Arnold  
Hannah Sistrunk  
Katie Martin  
Darren Young  

## License

This code is released under an [MIT License](LICENSE).
