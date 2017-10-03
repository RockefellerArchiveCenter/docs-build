# docs-build

A Python WSGI application to handle GitHub webhooks for internal and external facing documentation websites. Based on [Python Github Webhooks](https://github.com/carlos-jenkins/python-github-webhooks) developed by [@carlos-jenkins](https://github.com/carlos-jenkins/)

## Install

    git clone https://github.com/RockefellerArchiveCenter/docs-build.git
    cd docs-build
    ./install.sh

`./install.sh` will install all the necessary dependencies, and also set SSH keys which enable the application to interact with Github.

## Setup

You can configure what the application does by copying the sample config file
`config.json.sample` to `config.json` and adapting it to your needs:

    {
        "github_ips_only": true,
        "enforce_secret": "",
        "return_scripts_info": true
        "hooks_path": "/.../hooks/"
        "repository_dir": "/repositories",
        "site_root_dir": "/docs",
        "public_site_dir": "public",
        "private_site_dir": "private",
        "staging_dir": "staging",
        "build_dir": "build"
    }

`github_ips_only`: Restrict application to be called only by GitHub IPs. IPs whitelist is obtained from
 [GitHub Meta](https://developer.github.com/v3/meta/) ([endpoint](https://api.github.com/meta)). Default: `true`.

`enforce_secret`: Enforce body signature with HTTP header `X-Hub-Signature`. See `secret` at [GitHub WebHooks Documentation](https://developer.github.com/v3/repos/hooks/). Default: `''` (do not enforce).

 `return_scripts_info`: Return a JSON with the `stdout`, `stderr` and exit code for each executed hook using the hook name as key. If this option is set you will be able to see the result of your hooks from within your GitHub hooks configuration page (see "Recent Deliveries"). Default: `true`.

 `hooks_path`: Configures a path to import the hooks. If not set, it'll import the hooks from the default location (/.../docs-build/hooks)

 `repository_dir`: "/repositories",

 `site_root_dir`: "/docs",

 `public_site_dir`: "public",

 `private_site_dir`: "private",

 `staging_dir`: "staging",

 `build_dir`: "build"

## Build Hook

Docs, theme, YAML config file, build structure

## Adding Hooks

It is possible to add additional webhooks by creating additional scripts in the hooks directory as configured above. Scripts will be executed in the following order:

    hooks/{event}-{name}-{branch}
    hooks/{event}-{name}
    hooks/{event}
    hooks/all

The application will pass to the hooks the path to a JSON file holding the payload for the request as first argument. The event type will be passed as the second argument. For example:

    hooks/push-myrepo-master /tmp/sXFHji push

Hooks can be written in any scripting language as long as the file is executable and has a shebang. A simple example in Python could be:

    #!/usr/bin/env python
    # Python Example for Python GitHub Webhooks
    # File: push-myrepo-master

    import sys
    import json

    with open(sys.argv[1], 'r') as jsf:
      payload = json.loads(jsf.read())

    ### Do something with the payload
    name = payload['repository']['name']
    outfile = '/tmp/hook-{}.log'.format(name)

    with open(outfile, 'w') as f:
        f.write(json.dumps(payload))

Not all events have an associated branch, so a branch-specific hook cannot fire for such events. For events that contain a pull_request object, the base branch (target for the pull request) is used, not the head branch.

The payload structure depends on the event type. Please review [GitHub documentation on payload structure](https://developer.github.com/v3/activity/events/types/).

## Deploy

### Apache

To deploy in Apache, just add a ``WSGIScriptAlias`` directive to your
VirtualHost file:

    <VirtualHost *:80>
        ServerAdmin you@my.site.com
        ServerName  my.site.com
        DocumentRoot /var/www/site.com/my/htdocs/

        # Handle Github webhook
        <Directory "/var/www/site.com/my/python-github-webhooks">
            Order deny,allow
            Allow from all
        </Directory>
        WSGIScriptAlias /webhooks /var/www/site.com/my/python-github-webhooks/webhooks.py

    </VirtualHost>

You can now [register the hook](https://developer.github.com/webhooks/creating/#setting-up-a-webhook) in your Github repository settings. Make sure you select Content type: `application/json` and set the URL to the URL
of your WSGI script. For example, using the Apache deployment above it would be:

    http://my.site.com/webhooks


## Test your deployment

To test your hook you can use the [GitHub REST API](https://developer.github.com/v3/) with `curl`:

    curl --user "<youruser>" https://api.github.com/repos/<youruser>/<myrepo>/hooks

Take note of the test_url.

    curl --user "<youruser>" -i -X POST <test_url>

You should be able to see any log error in your webapp.


## Debug

When running in Apache, the `stderr` of the hooks that return non-zero will be logged in Apache's error logs. For example:

    sudo tail -f /var/log/apache2/error.log

Will log errors in your scripts if printed to `stderr`.

You can also launch the Flask web server in debug mode at port `5000`.

    python webhooks.py

This can help debug problem with the WSGI application itself.


## License

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

   <http://www.apache.org/licenses/LICENSE-2.0>

   Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.

## Credits

Based on Based on [Python Github Webhooks](https://github.com/carlos-jenkins/python-github-webhooks) developed by [@carlos-jenkins](https://github.com/carlos-jenkins/), which is a reinterpretation and merge of:

-   [github-webhook-wrapper](https://github.com/datafolklabs/github-webhook-wrapper)
-   [flask-github-webhook](https://github.com/razius/flask-github-webhook)
