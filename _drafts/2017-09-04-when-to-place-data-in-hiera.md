---
layout: blog
title: Tip of the Week 36 - When to place data in hiera
---

When Puppet Inc. released hiera, we gained the possibility to seaprate data from code.

Prior hiera we used logic patterns like ```if``` and ```case``` to identify differences in our platform and configurations.
With hiera we started using the hiera lookup function to fetch data based on a hierarchy where we specify differences of our platform. This lead to cleaner, better maintainable code.

Now people started putting data no longer into their code, which lead to huge hiera data files and hard to maintain hierarchies.

The biggest problem is to identify when to put data in hiera and when to keep data in code.
Puppet did a [blog post](https://puppet.com/blog/hiera-data-and-puppet-code-your-path-right-data-decisions) a couple of weeks ago, describing the problem and providing a workflow to identify where data should be placed.

I mostly agree with Gary's posting and decisions. There is just one minor issue I see with his approach: the posting does not talk about hiera data namespaces.

Generally you start with the question: is this data different among the platform?

If you must confess that data is identical anywhere you will not put this data into hiera, but keep it inside the profile:

    # site/profile/manifests/login/ssh.pp
    class profile::login::ssh {
      class { 'ssh':
        permit_root_login => 'no',
      }
    }

If you must use the variable from multiple places, it is recommended to assign the data to a variable and use this variable instead:

    # site/profile/manifests/data.pp
    class profile::data {
      $delete_unmanaged_accouts_and_keys = true,
    }


    # site/profile/manifests/login/ssh.pp
    class profile::login::ssh {
      include profile::data
      class { 'ssh':
        permit_root_login => 'no',
        purge_keys        => $profile::data::delete_unmanaged_accounts_and_keys,
      }
    }

    # site/profile/manifests/users.pp
    class profile::users {
      include profile::data
      class { 'profile::users::static':
        delete_unmanaged => $profile::data::delete_unmanaged_accounts_and_keys,
      }
    }

Next question is whether data can be calculated on a simple logic. In this case you will place the logic into the profile:

    # site/profile/manifests/login/ssh.pp
    class profile::login::ssh {
      include profile::data
      $case $::location {
        'dmz': {
          $manage_firewall = true
        }
        default: {
          $manage_firewall = false
        }
      }
      class { 'ssh':
        permit_root_login => 'no',
        purge_keys        => $profile::data::purge_ssh_auth_keys,
        manage_firewall   => $manage_firewall
      }
    }

No comes the point where I differ from Gary's posting:

In all other cases make your profile a parameterized profile. Whether you want to specify a sane default value is up to you.

    
    # site/profile/manifests/login/ssh.pp
    class profile::login::ssh (
      Integer $port = 22,
      Array   $allow_groups,
    ){
      include profile::data
      $case $::location {
        'dmz': {
          $manage_firewall = true
        }
        default: {
          $manage_firewall = false
        }
      }
      class { 'ssh':
        permit_root_login => 'no',
        purge_keys        => $profile::data::purge_ssh_auth_keys,
        manage_firewall   => $manage_firewall
      }
    }

Within hiera one can now use the profile namespace to place data:

    profile::login::ssh::port: 2222
    profile::login::ssh::allow_groups:
      - 'admin'
      - 'backup'

example42 wished everybody fun and success with Puppet and hiera.

Martin Alfke
