---
layout: blog
title: Tip of the Week 15 - Environment enforcement
---

Think about the following situation:

You have a node running in development environment.
A user logs in and runs ```puppet agent --test --environment production```.

What will happen: the node will receive production ready code.
This is OK... but... what if you use the environment to also pass data like passwords, users, accounts to your nodes?

In this case the development system will have all production data and users are happy that they now can connect to your production database.

If you would not like to allow this, you have to make use of an external nodes classifier (ENC).

An ENC is configured within the master section of puppet.conf file. It is called **external** as it does work prior the master starts catalog compilation.

ENC usage is configured as follows:

    # /etc/puppetlabs/puppet/puppet.conf
    [master]
      node_terminus = exec
      external_nodes = bin/enc_cat.sh

What does the enc_cat.sh script do? An external nodes classifier using the exec terminus is called with the node cert name as argument and returns yaml syntax.

Foreman, Puppet Enterprise Console are common examples of ENC, they provide a custom script for ```external_nodes``` which queries the relevant API.

In the above example the command is a simple bash script that just cats yaml files (either with the name of the node passed as argument, or a default one):

    # bin/enc_cat.sh
    #!/bin/bash
    repo_dir="$(dirname $0)/.."
    script_dir="$(dirname $0)"
    . "${script_dir}/functions"

    host=$1
    if [ -f "${repo_dir}/bin/enc_cat/${host}.yaml" ]; then
      cat "${repo_dir}/bin/enc_cat/${host}.yaml"
    else
      cat "${repo_dir}/bin/enc_cat/default.yaml"
    fi

Within the enc_cat directory one places yaml files. Either host specific or a default. If the ENC has no file to return, the node will be classified using manifests node syntax only.

A default.yaml file can look like the following (the same format is what is expected by the ENC scripts for Foreman, PE Console or any other ENC):

    # enc_cat/default.yaml
    ---
      environment: production
      classes:
        - profile::base::pre
      parameters:
        - env: development
        - role: default

To pin a node to a specific environment, the first line is required:

    environment: development

This value is used by the Puppet server to determine whether a node should be in a specific environment and verifies node environment setting. If the nodes setting does not match the Puppet server will switch the catalog compilation based upon the environment from ENC.

When using [PSICK](https://github.com/example42/psick) the above essential enc_cat is already available and can be easily activated in puppet configuration file.

Martin Alfke
