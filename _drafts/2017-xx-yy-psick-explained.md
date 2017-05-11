---
layout: blog
title: Tip of the Week XXX - PSICK explained
---

Getting started with PSICK:

0. Prepare your master:

    mkdir -p /etc/puppetlabs/code/environment/
    git clone https://github.com/example42/psick /etc/puppetlabs/code/environments/production
    cd /etc/puppetlabs/code/environments/production
    git checkout development

1. If you have no Puppet 4 already installed:

    sudo bin/puppet_install.sh

Installs Puppet 4 from Puppet Inc. repositories.

2. Prepare your Puppet

    bin/puppet_setup.sh

Installs required gems and fetches remote modules with r10k.
The list of modules can be modified in ```Puppetfile```.

3. Choose your hiera version

    # For hiera 3 format (classic)
    ln -sf /etc/puppetlabs/code/environments/production/hiera3.yaml /etc/puppetlabs/puppet/hiera.yaml

    # For hiera 5 format
    ln -sf /etc/puppetlabs/code/environments/production/hiera.yaml /etc/puppetlabs/puppet/hiera.yaml

4. Understanding classifying your nodes

Node classification is based on 3 top scope variables:

    $::role - Node role
    $::env  - Node environment
    $::zone - Data center, region (optional)

These are used in hiera in the following order:

    - node trusted.certname in nodes/
    - role-env in role/
    - role in role/
    - zone in zone/
    - common

5. Classify your master

PSICK provides examples on how to classify your node. PSICK also supports automation of Puppet Master infrastructure.
Adopt settings from hieradata/nodes/puppet.lab.psick.io.yaml

    # hieradata/nodes/<master fqdn>.yaml
    ---
      profiles:
          - profile::puppet::pe_aio_server
          - profile::puppet::pe_code_manager

6. run puppet on manifests/site.pp

    puppet apply manifests/site.pp --modulepath=./site:./modules


Martin Alfke
