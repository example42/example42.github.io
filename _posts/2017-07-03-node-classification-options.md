---
layout: blog
title: Tip of the Week 27 - Puppet node classification options
---

When using a Puppet Agent - Puppet Master setup it is required that the Puppet Master has information about classes which a node should receive.
This process is called Node Classification.

There are several possible ways on how to do this. This posting will cover several different options

1. Node Classification in Puppet environment manifests
1. Node classification in Hiera
1. Node classification on external sources

## Node Classification in Puppet environment manifests

The most cenvenient way to classify nodes is using Puppet environment manifests data.
This is the default behavior for any Puppet Open Source installation.

It uses the manifests directory structure which is located on the root of a Puppet Environment code basis.

    /etc/puppetlabs/code/environments/production
       |- manifests/
       |     |- site.pp
       |     |- infrastructure/
       |     |    |- internal_servers.pp
       |     |    \- workstations.pp
       |     \- servers.pp
       \- modules/

The site.pp file is parsed first. Any other files and directory are parsed in directory globbing order.
Usually the site.pp file is used to declare resource defaults and has a fallback default node classification.

    # /etc/puppetlabs/code/environments/production/manifests/site.pp
    # file backup should be local on node. backup file should be next to replaced file and has the fileending .puppet_backup
    File {
      backup => '.puppet_backup',
    }
    # On windows we use chocolatey as dfault provider
    if $facts['os']['family'] == 'windows' {
      Package {
        provider => 'chocolatey',
      }
    }

    # default node should always fail
    node default {
      fail("Missing node classification for node ${trusted['certname']}")
    }

All other nodes are then placed into other files or directories.
It is common best practice to classify nodes either by their business use case (role) or by implementation classes (profiles)

    node 'www01.example.com' {
      include role::company_website
    }
    node 'mail.example.com' {
      include profile::infrastructure::security
      include profile::infrastructure::ldap_client
      include profile::mail::postfix::mda
      include profile::mail::cyrus
    }

## Node classification in Hiera

Another possible solution is using hiera data. Usually the hiera lookup is added to site.pp - either in a default node or at global position.

    # /etc/puppetlabs/code/environments/production/manifests/site.pp
    # profiles are read as array from hiera on all matching hierarchies
    $profiles = lookup('profiles', Array, [], 'deep')
    
    # use Puppet 4 lambda for array iteration and declare each profile
    $profiles.each |String $profile| {
      include "profile::${profile}"
    }

The hiera lookup mentioned in the example above checks all valid hierarchies from a node and collects all findings of the 'profiles' key into an array.
Think about the following example:

    # common.yaml
    profiles: []

    # (%{datacenter}) - infrastructure.yaml
    profiles:
      - 'infrastructure::security'
      - 'infrastructure::ldap_client'
    
    # (%{application}) - mailserver.yaml
    profiles:
      - 'mail::postfix::mda'
      - 'mail::cyrus'

## Node classification on external sources

The next possible solution is to use an external source. In Puppet this is called an ENC (external node classifier).
An ENC needs some configuration on Puppet Server:

    # /etc/puppetlabs/puppet/puppet.conf
    [master]
    node_terminus = exec
    external_nodes = <full path to executable script>

Don't forget to restart your Puppet Server process to activate the new settings.
The external node script can be anything (perl, ruby, python, compiled C++ code) and must be executable by the user running the Puppet Server (puppet on Open Source, pe-puppet on Puppet Enterprise).

Please be careful when using remote data sources like databases, webservers, CMDB. The Puppet Server will access the remote systems every time a node requests a catalog. On larger installations this can lead to many requests against remote systems. It is best practice to use local stored data only.

The ENC script must produce YAML or JSON or empty output.

     classes:
       - profile::infrastructure::security
       - profile::infrastructure::ldap_client
       - profile::mail::postfix::mda
       - profile::mail::cyrus

There is one more thing which an ENC is capable of: environment enforcement.

Different to the manifests based node classification - which already takes part inside the Puppet compiler - the ENC is running prior the compiler.
Additional information on this topic can be found at [TOW 15](http://www.example42.com/2017/04/10/environment-enforcement/).

Martin Alfke
