---
layout: blog
title: Puppet Tip XXX - Unit and acceptance testing your Control Repository
---

When changing Puppet code in a control-repository or upgrading modules you want to ensure, that your code is still working and behaves as expected.
This is where you want to have at least unit tests or (even better) unit- and acceptance-tests.

When looking around the Puppet ecosystem you will find many different tools which are related to Puppet code testing:

- PDK
- Onceover
- Beaker
- Litmus

So which is the right one to use?

Within this posting we are going to explain how to add unit- and acceptance tests to your Puppet control-repo and the pro and cons of each of the mentioned tools.

* Table of content
{:toc}

# Unit Testing

Unit testing Puppet code is possible by using [rspec-puppet](https://rspec-puppet.com). Rspec-puppet will compile a catalog and parse the catalog for classes, types and parameters.
Compiling a catalog on a control-repo usually requires to have access to your hiera data.


## PDK - Puppet Development Kit

The Puppet Development Kit bundles everything needed to run unit tests and check code validity.
The purpose of PDK is to help people creating, writing and maintaining Puppet modules.

You can create a module structure based on PDK module template by running `pdk new module`. You must then answer some questions which are purely module related (like module name, license, author and supported operating system).
You can also specify your own PDK module template by providing a path to a directory or a git url.

Next you can create classes, defined types, tasks and custom types (using the new type/provider API, which is not compatible with Puppet 5).
For classes and defined types the `pdk new` command will create the file in manifests directory and a file describing the smallest possible unit test in spec directory.

But how to test a control repository using PDK?

When using the roles and profile pattern you will have two self created modules: profile and role module.
Usually we create these modules using PDK.

We first want to check how to test our profiles.

When it comes to unit testing, we must add dependencies to .fixtures.yml file which will then get installed into the spec/fixtures/modules directory. You can either specify all your modules in Puppetfile also in .fixtures.yml. But that means that you mus maintain the same information twice.

What we usually do: we configure rspec to also check other paths in spec/fixtures directory. Module installation from Puppetfile is done via CI running `r10k puppetfile install` Within .fixtures.yml file we add a symboilic link from modules to spec/fixtures/r10k.

Another topic comes up when we want to use the control-repo hiera data. Here we follow the same pattern by changing rspec-puppet hiera configuration to either make use of the control-repo hiera data or by switching to a unit test specific hiera configuration and data.

    # spec/spec_helper_local.rb


## OnceOver

# Acceptance Testing

## Litmus

## Beaker


Happy puppetizing and testing,

Martin Alfke

