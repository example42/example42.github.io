---
layout: blog
title: Tip of the Week 21 - Automated Puppet infrastructure setup
---

How often do you reinstantiate your Puppet server infrastructure?
How often do you upgrade your Puppet master and the agents?

Usually people set up the heart of their Puppet infrastructure in a manual way.

From our perspective this is an anti pattern when you manually manage the core of your automation.
We believe that autmating your automation allows you:
 - to better re-deploy your Puppet infrastructure
 - to manage your Puppet infrastructure by using Puppet
 - gain confidence that you can easily spin up everything from scratch after major outage

The example 42 PSICK control-repo now allows you to spin up either Puppet Enterprise or Puppet Open Source infrastructures in a fully automated way.

Getting started with PSICK to automate your Puppet Open Source Server setup on a bare OS installation

0. Get the code base:

    mkdir -p /etc/puppetlabs/code/environment/
    git clone https://github.com/example42/psick /etc/puppetlabs/code/environments/production
    cd /etc/puppetlabs/code/environments/production
    git checkout development

1. Install Puppet 4:

    bin/puppet_install.sh

This installs Puppet 4 from Puppet Inc. repositories.

2. Prepare your Puppet

    bin/puppet_setup.sh

Installs required gems and fetches remote modules with r10k.
The list of modules can be modified in ```Puppetfile```.

3. Understanding classifying your nodes

There are two possible options for node classification:

Option 1: using hiera data
Option 2: using trusted facts

Option 1 is enabled in ```manifests/site.pp``` per default.
Option 2 is available, but deactivated

Our intention is to make use of profiles within hiera for node classification.
Adding roles on top of profiles adds another layer of complexitiy which mostly is not required.
Profiles usually are parameterized classes which can fetch data from hiera using automatic data binding.

4. Classify your master

Adopt settings from hieradata/nodes/puppet.pos.psick.io.yaml

    # hieradata/nodes/<master fqdn>.yaml
    ---
      profiles:
          - profile::puppet::foss_server

5. run puppet to automate the Master setup

        bin/papply.sh

This builds you a fully operational monolithic Puppet master with PuppetDB, storeconfigs and reporting enabled.

But how to get your code improvements onto your fresh Puppet master?

This is where the profile parameters come into place:

The FOSS Puppet master profile allows you to set r10k configurations. At the moment we only support a single r10k repository.
Just add proper namespace keys to hiera:

    # hieradata/nodes/<master fqdn>.yaml
    profile::puppet::foss_master::r10k_remote_repo: 'git@gitlab.pos.psick.io:/repos/psick.git'

You can either specify this setting prior running step 5 or add the setting later and run puppet agent.

Summary for automated Puppet Open Source installation

1. add node classification information to hiera
2. place the repo on the new Puppet master
3. bin/puppet_install.sh
4. bin/puppet/setup.sh
5. bin/papply.sh


Martin Alfke
