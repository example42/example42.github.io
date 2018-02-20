---
layout: blog
title: Tip of the Week 60 - Anatomy of a Puppet control-repo compared to PSICK
---

Note: This is an updated and improved version of the [Tip of the Week 2 - Anatomy of a Puppet control-repo](2017-01-09-anatomy-of-a-puppet-control-repo.md).

A Puppet control-repo is a [git] repository that contains the files you expect to have in your directory environment (for example ```/etc/puppetlabs/code/environments/production``` for the default production environment) which provides whatever you need to manage your infrastructure.


### The standard control-repo

A control repo is typically composed of:

  - The ```manifests``` directory where are placed the first files that the Puppet server parses when compiling catalogs for clients. Here you typically have the ```site.pp``` file (but other manifests with different names can be seamlessly added) where you can set top scope variables, resource defaults, and eventually have node statements to define what classes should be included in your nodes (nodes classification can be done in several different ways, using the ```node``` statement is just one of them).

  - The ```hieradata``` (or ```data```) directory which contains Hiera data files. The name of the directory is completely arbitrary, even if these are a sort of standard de facto. This same directory could not even exists in the unlikely case you are not using Hiera, or if you use Hiera with backends which don't store data in normal (typically yaml or json) files. Hiera data can also be placed in a separated dedicated repository, eventually a "fake module" to load via ```Puppetfile``` so you might have it outside the control-repo, and have different people who might access the Hiera data and the control-repo code.

  - The ```hiera.yaml``` file configures the Hiera backed and the hierarchies to use for the environment

  - The ```modules``` directory contains Puppet modules. Typically you don't place themselves directly in your control-repo but define them in the ```Puppetfile``` and then deploy them with either r10k or Librarian Puppet.

  - You will probably have to develop custom modules (your role and profile modules, your site specific ones). You can decide to place them in dedicated repositories, and add them to your Puppetfile, or keep them in your same control-repo. In this case it makes sense to place them in a separated directory, such as ```site```, in order to differentiate external modules, defined in the Puppetfile, from the local ones.

  - The ```environment.conf``` file, which configures your environment: where the modules are placed, the caching timeout and eventually a script that returns a custom configuration version.

You can find an [essential skeleton for a control-repo](https://github.com/puppetlabs/control-repo), from Puppet.


### The PSICK additions

Example42's [PSICK](https://github.com/example42/psick) is a Puppet control repo with superpowers. It contains all the above directories and something more:

- The ```vagrant``` directory contains different Vagrant environments with the relevant toolset that can be used to locally test the same control-repo. They are fully customizable by editing the ```config.yaml``` file in each Vagrant environment.

- Files for building Docker images locally are under the ```docker``` directory.

- [Fabric](http://www.fabfile.org) tasks are defined in the ```fabfile``` directory.

- Documentation is stored under ```docs```

- The ```bin``` directory contains several scripts for various Puppet master activites. Many of them can be invoked via Fabric or are used in the CI pipelines.

- The files ```.gitlab-ci.yml```, ```Jenkinsfile``` and ```.travis.yml``` are used to configure CI pipelines for Puppet code on different tools

- ```Rakefile```, ```Gemfile``` and the ```spec/``` directory are needed to run control-repo unit and integration tests

- ```Dangerfile``` configures the [Danger](https://danger.systems) bot based which automatically send comments based on control-repo changes

- ```metadata.json``` was added to be able to use pdk within the control-repo.

- ```psick``` command can be used to create a new control-repo based on the Puppet standard (and essential) one, or example42's big, fat, rich, psick one.

Besides these additions, PSICK can be used as a normal Puppet control repo, and it fully follows its conventions and rules.

Alessandro Franceschi
