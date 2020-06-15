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

## PSICK

Clone the PSICK repository, switch to `terraform` directory.
Add file `secrets.auto.tfvars` with the following keys:

- hcloud\_token - add your API token from Hetzner Cloud
- sshkey - provide the ssh deploy private key file (e.g. `/home/tuxmea/.ssh/hetzner_deploy`)
- puppet\_version - Version of Puppet to use, defaults to 6. Possible values: 5 or 6
- control\_repo - The Git repository to use as control-repository. This repository must fullfil some requirements. Defaults to `https://github.com/example42/psick.git`
- machines - A hash of nodes which will bve created

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

## Your own control-repo

When using you own control-repository you want to be sure that you have the bootstrapping script for the infrastructure in `/bin/bootstrap/cloud_init.sh`.

This file gets executed by cloud provisioning.

Happy puppetizing and terraforming,

Martin

