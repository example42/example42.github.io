---
layout: blog
title: Puppet Tip XYZ - Deploying your Puppet Infrastructure at Hetzner Cloud
---

If you follow our development at GitHub you might have seen, that our [Puppet Infrastructure Construction Kit](https://github.com/example42/psick) has received some terraform additions.

This blog post explains how you can easily use this to deploy your Puppet Infrastructure at [Hetzner Cloud](https://cloud.hertzner.com).

Note: we use this setup for inhouse and remote workshop courses - therefore we deploy a puppet master, a gitlab server and have student1 to studentNN maschines.

* Table of content
{:toc}

# Preparation

## Hetzner Cloud

You must create an account and a project at Hetzner Cloud.
Create an API token key.
Add your login ssh key(s) and add a deploy ssh key (without passphrase) to your project.

## Local machine

Create a local SSH key used for cloud deployment (copying scripts to cloud instances and start them).
Please be aware that his key must not have a passphrase!

## PSICK

Clone the PSICK repository, switch to `terraform` directory.

    git clone https://github.com/example42/psick
    cd psick/terraform

Add file `secrets.auto.tfvars` with the following keys:

- hcloud\_token - add your API token from Hetzner Cloud
- sshkey - provide the ssh deploy private key file (e.g. `/home/tuxmea/.ssh/hetzner_deploy`)
- puppet\_version - Version of Puppet to use, defaults to 6. Possible values: 5 or 6
- control\_repo - The Git repository to use as control-repository. This repository must fullfil some requirements. Defaults to `https://github.com/example42/psick.git`
- machines - A hash of nodes which will be created with information on IP Address, Puppet Role, Server Type and Access Level

example file:

    # secrets.auto.tfvars
    hcloud_token = "12345678901234567890123456789012345678901234"
    sshkey = "/Users/mea/.ssh/hetzner_key"
    puppet_version = 5
    control_repo = 'https://github.com/example42/psick.git'
    machines = {
      'puppet' = { ip = '10.0.1.1', role = 'puppet', server_type = 'cx41', access_level = 'admin_keys' },
      'demo1'  = { ip = '10.0.1.2', role = 'demo',   server_Type = 'cx11', accces_level = 'all_keys'   }
    }

Note: access\_level is work in progress. At the moment we deploy all keys to all machines.

## Your own control-repo

When using you own control-repository you want to be sure that you have the bootstrapping scripts for the infrastructure:

- `bin/puppet_set_external_facts.sh`
- `bin/puppet_set_trusted_facts.sh`
- `bin/puppet_install.sh`
- `bin/bootstrap/cloud_init.sh`.

These files gets executed by cloud provisioning.

You can find the working files at our [Puppet Infrastructure Construction Kit](https://github.com/example42/psick)

## Running terraform

First check that all data is available:

    terraform plan

If no errors show up, you can initiate the deployment:

    terraform deploy

Happy puppetizing and terraforming,

Martin

