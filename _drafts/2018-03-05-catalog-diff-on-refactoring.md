---
layout: blog
title: Tip of the Week 62 - Using catalog diff to check refactoring
---

Note: This is an updated version of the [Tip of the Week 4 - Existing code and Puppet 4](https://www.example42.com/2017/01/23/existing-code-on-puppet4/) dealing with octocatalog-catalog diff only.

## General

Refactoring Puppet code is a task which we usually have to do, especially when being at a customer with Puppet code with a long history.

There are several reasons for refactoring:

- Adopt to new best practices
- Migrate from Hiera config v3 to Hiera config v5
- Restructuring code to allow better code management

But how can you verify that the refactoring was done properly, so no changes on systems occur?

This is where catalog diff tools come into place.
Originally these tools have been created to allow smooth upgrade from Puppet 3 to Puppet 4 (like the [puppetlabs-catalog_diff](https://github.com/puppetlabs/puppetlabs-catalog_diff) or [octocatalog-diff](https://github.com/github/octocatalog-diff)).

## Installation

Both tools use a different approach. The puppetlabs-catalog_diff is installed as a puppet module, bringing a new puppet interface (command line option).

Installation can be done using the `puppet module install`command:

    puppet module install puppetlabs/puppetlabs-catalog_diff
    
After installation there is now a puppet cli command available:

    puppet catalog diff
    
The octocatalog-diff is delivered as a ruby gem. It needs ruby 2.0 or newer and can be installed using the `puppet gem` or - in case you have a sufficient ruby version - the `gem` command:

    /opt/puppetlabs/puppet/bin/gem install octocatalog-diff
    
The tool needs a loca Puppet agent installed and can be used on Linux and Mac OS. Windows is not supported.

## Configuration

The octocatalog diff tool needs a configuration file  (.octocatalog-diff.cfg.rb) unless you want to specify all parameters as command line options.

The configuration file can reside in different locations. Lookup for the file is done in the following order:

1. in local directory
2. in home directory
3. /usr/local/etc/octocatalog-diff.cfg.rb
4. /opt/puppetlabs/octocatalog-diff/octocatalog-diff.cfg.rb
5. /etc/octocatalog-diff.cfg.rb

The configuration covers 4 different parts:

1. Hiera
2. Node Classifier (ENC)
3. PuppetDB and
4. Puppet

#### Hiera

If you are already using Puppet 4.9 or later and when you have a hiera.yaml (config v5 format) in your environment root, Puppet will recognize the file by itself, so will octocatalog-diff do.

In this case you are good to skip the hiera settings and you are asked to NOT configure hiera settings in octocatalog-diff.

#### ENC

If you are using an external node classifier, you must tell octocatalog-diff about it. Puppet Enterprise uses the classifier API as ENC, which can be configured using a token or a whitelist.

If you are using token authentication against the Puppet Enterprise RBAC service, one needs to configure the following settings:

    octocatalog-diff \
      --pe-enc-url https://your.pe.console.server:4433/classifier-api \
      --pe-enc-token-file /path/to/token/file.txt \
      --pe-enc-ssl-ca /path/to/ca.crt \
      [other options]

If you are using a whitelisted SSL keypair the following options must be used:

    octocatalog-diff \
      --pe-enc-url https://your.pe.console.server:4433/classifier-api \
      --pe-enc-ssl-ca /path/to/ca.crt \
      --pe-enc-ssl-client-cert /path/to/client.crt \
      --pe-enc-ssl-client-key /path/to/client.key \
      [other options]

If you are using another ENC, you must pass the ENC file option:

      octocalaog-diff \
        -enc bin/enc.sh \
        [other options]

#### PuppetDB

PuppetDB can be used to staore latest node facts, exported resources and node catalogs and their reports.

In this specific case we are interested to receive the latest catalog from PuppetDB.

Octocatalog-diff only supports PuppetDB API v4 which means that you must run PuppetDB 2.3 or newer.

Usually Puppet Master is able to communicate with PuppetDB using a certificate whitelist. We can re-use this setting as this is the most secure way how to configure access to PuppetDB.

Octocatalog-diff must be configured to use proper certificates by using the following settings in configuration file:

    settings[:puppetdb_url] 'https://puppetdb.server:8081/
    settings[:puppetdb_ssl_ca] 'path to Puppet SSL CA file'
    settings[:puppetdb_ssl_client_cert] 'path to Puppet SSL certificate
    settings[:puppetdb_ssl_client_key] 'path to Puppet SSL key file'

If you prefer to set CLI options you can use the following form:

    octocatalog-diff \
      --puppetdb-url https://puppetdb.example.net:8081 \
      --puppetdb-ssl-ca FILENAME
      --puppetdb-ssl-client-cert FILENAME
      --puppetdb-ssl-client-key FILENAME

Access to PuppetDB must be grated by using the [PuppetDB SSL whitelist option](https://puppet.com/docs/puppetdb/5.1/configure.html#certificate-whitelist).

#### Puppet

Last but least, octocatalog-diff must know about the Puppet installation which it uses to compile a catalog. Note: the puppet-agent is sufficient. There is no need to install puppetserver on a system where you want to make use of octocatalog-diff.

    settings[:puppet_binary] = '/opt/puppetlabs/puppet/bin/puppet'

Please note, that octocatalog-diff must have the puppetdb-termini package installed in case that you also want to get exprted resources in a nodes catalog.

## Usage

Now you are able to verify your settings by running

    octocatalog-diff --config-test
    
Read the output carefully and see whether all settings are correct for your installation.

In normal (module) mode, octocatalog-diff will assume that the base for the catalog will be the origin/master branch on a git repository.
For control repository you want to change this by setting the `-f origin/productoin` CLI parameter.

Facts can be read from PuppetDB - if configured - or from a specifc facts file which gets added using the `--fact-file` option.

The nodes to test are provided using the `-n <nodename>` option

Additional descriptions and usage can be found in the [octocatalog-diff documentation](https://github.com/github/octocatalog-diff/tree/master/doc).

Happy hacking and refactoring using catalog diff verification.

Martin Alfke
