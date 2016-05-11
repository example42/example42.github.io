---
layout: blog
title: A modern Puppet 4 control repo
---

A few weeks ago we introduced version 4 of example42 Puppet modules with a radical change in the [reference repository](https://github.com/example42/control-repo) layout.

We've started to work on a **Puppet 4 only compatible** control-repo setup and we explored alternatives or optimizations to current best practices.

The term "control-repo" is relatively recent in Puppet world but its function has been common for a while: a single place where we manage our whole Puppet setup: our data, our code, the public modules we use.

Needless to say that a good stating control-repo is vital to a sane Puppet setup.

What we present here is a sample modern, rich featured, opinionated and customizable Puppet control repo with:

  - Sample Hiera structure and data, using hiera-eyaml

  - Local profiles optimized for Puppet 4 usage.

  - Use of experimental Puppet 4 optimized modules based on new design principles

  - Multiple, easily customizable, Vagrant environments, where to test the same control-repo code

  - Docker integration: Data driven build images configuration and control-repo testing environments

  - Fabric integration for Puppet code development, testing and deployment

  - Tiny Puppet usage for extremely compact, consistent and readable code

You can give it a try with:

    git clone git://github.com/example42/control-repo.git
    cd control-repo
    r10k puppetfile install -v

The starting code and data organization and nodes classification is intended to be adapted ad customized according to different needs. By default in ```manifests/site.pp``` it's used a node-less classification based on 3 top scope variables, ```$::role```, ```$::env```, ```$::zone```: they can be set as facts (as done in the provided Vagrant environments) or via an External Node Classifier.

We don't use role classes: the profiles to include in each node are defined via Hiera, using the ```profiles``` key. The sample hierarchy in ```hiera.yaml``` uses data in ```hieradata```.

In the local site profile class we manage the baseline of resources common to all nodes, and role specific ones.

The public modules installed via r10k are from various sources, not only example42 ones.

The control-repo code is far from being complete, we are experimenting design patterns for modules and this is an ongoing process. Just consider that you can, and actually should, decide what to use and what to change in the code, the data and the classification logic: the existing base code allows any customization in a totally data driven way.

### Control repo testing

You can test the control repo code and data while you develop or in your Continuous Integration pipeline.

We provide both Vagrant and Docker based testing environments and some Fabric tasks to work with them.

To install the required vagrant plugins:

    fab vagrant.setup

To see the status of the Vagrant environments in ```vagrant/environments``` (there are different ones for different purposes):

    fab vagrant.status

To start and provision a Vagrant vm do something like (or run the relevant Vagrant commands in the chosen environment):

    fab vagrant.up:vm=dev-local-docker-host-01
    fab vagrant.provision:vm=dev-local-docker-host-01

To build locally Docker images for different OS (using the data in ```hieradata/role/docker_multios_build.yaml```)

    fab docker.multios_build

To test a role on a Docker instance with puppet-agent preinstalled:

    fab docker.provision:puppetrole=tpweb,image=centos-7


Developments on this control-repo and the example42 modules are going to proceed while we explore patterns for Puppet infrastructures based on Puppet 4 and beyond.

Stay tuned, wonderful things happening here.
