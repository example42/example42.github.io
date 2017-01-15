---
layout: blog
title: Tip of the Week 9 - Building your own Puppet 4 Data Types
---

Puppet comes with a set of core data types like Integer, Float, String, Boolean.

But what if you have special needs? How to reimplement the stdlib functions like validate_absolute_path() or validate_ipv4()?

Puppet allows you to place your own build data types into a modules type directory:

    modulepath/
    \-  firewall/
         |- manifests/
         | \- init.pp
         |- lib/
         |  |- facter
         |  \- puppet
         |- facts.d
         \- types
            \- ipv4address.pp

Inside the types directory you can specify a new data type. This new data type is available in your module namespace:

    # firewall/types/ipv4address.pp
    type firewall::ipv4address = Pattern[/^((([0-9](?!\d)|[1-9][0-9](?!\d)|1[0-9]{2}(?!\d)|2[0-4][0-9](?!\d)|25[0-5](?!\d))[.]){3}([0-9](?!\d)|[1-9][0-9](?!\d)|1[0-9]{2}(?!\d)|2[0-4][0-9](?!\d)|25[0-5](?!\d)))(\/((([0-9](?!\d)|[1-9][0-9](?!\d)|1[0-9]{2}(?!\d)|2[0-4][0-9](?!\d)|25[0-5](?!\d))[.]){3}([0-9](?!\d)|[1-9][0-9](?!\d)|1[0-9]{2}(?!\d)|2[0-4][0-9](?!\d)|25[0-5](?!\d))|[0-9]+))?$/]

You can use any data type for building new ones.

Some combined data types are already available in [puppetlabs-stdlib](https://github.com/puppetlabs/puppetlabs-stdlib/tree/master/types) or [voxpupuli-tea](https://github.com/voxpupuli/puppet-tea).

Martin Alfke
