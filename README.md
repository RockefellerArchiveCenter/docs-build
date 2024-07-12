# docs-build

Theme file along with a Python script which retrieves updates for documentation
repositories, and builds internal and external-facing sites. Requires at
least one documentation repository (see [processing-manual](https://github.com/RockefellerArchiveCenter/processing-manual)).

[![Build Status](https://app.travis-ci.com/RockefellerArchiveCenter/docs-build.svg?branch=base)](https://app.travis-ci.com/RockefellerArchiveCenter/docs-build)

## Quick Start

A Dockerfile for local development (`Dockerfile-local`) is included in this repository so you can quickly spin up a sample site on your computer. With git and Docker installed, run:

    git clone https://github.com/RockefellerArchiveCenter/docs-build.git
    docker-compose build
    docker-compose up

The public docs site (which includes all the repositories listed under the `public`
key in `repositories.yml`) will be available in your browser at `http://localhost:4000`.

## Usage

## Adding or Removing Repositories

Repositories can be added or removed from either the public or private site by
updating `repositories.yml`. Only the sites listed under the `public` or `private`
key will be built for each site, so make sure to add publicly-available Repositories
to both the `public` and `private` lists.

You will also need to make sure the repositories
have some necessary configuration files:
- Jekyll configuration files (see [Documentation Repository Configuration](#documentation-repository-configuration))
- GitHub Actions file to publish update notifications to AWS Simple
Notification Service (SNS) (see [GitHub Action Configuration](#github-action-configuration))

Last, you will need to ensure that the repository has access to the following
Organization Secrets in Github:
- AWS_DOCS_ACCESS_KEY_ID
- AWS_DOCS_ACCOUNT_ID
- AWS_DOCS_REGION
- AWS_DOCS_SECRET_ACCESS_KEY
- AWS_DOCS_SNS_TOPIC


### Theme

The site uses a Jekyll-based theme to create a cohesive structure and
customizable interface. These files are located in the `theme/` directory.

Layouts are written in HTML and are chiefly composed from a separate directory
of Jekyll-based includes and one default layout template. They are styled with
both Bootstrap and custom CSS and are rendered with the Liquid template language.

The layout directory formats the various documentation files stored in the
individual GitHub repositories and thereby creates the site's central interface for access to documentation. This process is achieved through the use of layout variables in the documentation files' YAML front matter.

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

## Documentation Repository Configuration

In order to build the full documentation site, the following variables must be
available in a file named `_config.yml` located the root directory of each
documentation repository. These files should be valid [YAML](http://yaml.org).

    public: true
    title: "Collection Policy"
    description: "The main collecting areas of the Rockefeller Archive Center."
    pages:
      - ["Rockefeller Archive Center Collection Policy", "index"]

`public` indicates whether or not the documentation should be public. Values
should be either `true` or `false` (booleans, not strings).

`title` is the official title of the documentation, which will be displayed on
the home page of the site.

`description` is a statement of what the documentation is. This text will become the description meta tag for the site, which is displayed in search-engine results, so keep it short and snappy.

`pages` is a list of lists of the pages included in this site. The first value
in each list is the name, and the second is the filename of the page (without the
extension). These values are used when building tables of contents.

Other variables can be included in this config file if desired.

## GitHub Action Configuration
In order to deliver update notifications to Amazon SNS (which will trigger a build of the site), a GitHub Actions file named `.github/workflows/publish_sns.yml` needs to be created and populated with the following content:

```
name: Publish to SNS
on:
  push:
    branches:
      - base
      - development

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Publish SNS Notification
      uses: nothingalike/sns-publish-topic@v1.6
      with:
        MESSAGE: ${{ toJSON(github) }}
        TOPIC_ARN: "arn:aws:sns:${{ secrets.AWS_DOCS_REGION }}:${{ secrets.AWS_DOCS_ACCOUNT_ID }}:${{ secrets.AWS_DOCS_SNS_TOPIC }}"
      env:
        AWS_REGION: ${{ secrets.AWS_DOCS_REGION }}
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_DOCS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_DOCS_SECRET_ACCESS_KEY }}
```

To test this configuration, you can trigger a workflow run from the GitHub interface.

## Visual regression testing for theme

The repository includes [BackstopJS](https://github.com/garris/BackstopJS) to test visual changes to the site theme by comparing a set of reference images for different screen sizes. Anytime the CSS styles are changed, use BackstopJS to test locally:

1. Install BackstopJS dependency: `yarn install`
2. Build and run the site using the steps in the [Quick Start section](#quick-start) above.
3. In another terminal, run the BackstopJS tests: `yarn backstop-test`.
4. Review the results in the browser and look at the diff of any failed tests.
5. To update the reference image files with the results of the last test images use: `yarn backstop-approve`. Subsequent tests will be compared against these updated reference files.
6. Commit any updated reference images to the repository so that future tests will be compared against the most recent images.

To add or update reference images, edit the scenarios in `backstop.json` and run `yarn backstop-reference`.

## Contributing

Pull requests accepted!

## Authors

Hillel Arnold
Hannah Sistrunk
Katie Martin
Darren Young

## License

This code is released under an [MIT License](LICENSE).
