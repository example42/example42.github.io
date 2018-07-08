---
layout: blog
title: Tip of the Week 80 - Update on example42 Puppet modules
---

TL;DR: We "un-deprecated" two more modules - by customer request.

* Table of content
{:toc}

## example42 Puppet modules in early 2018

In [April 2018 we talked about the status of example42 modules](https://www.example42.com/2018/04/02/example42_puppet_modules_status_update/). Within the mentioned posting we also gave a short historical summary (from 2008 to 2017) regarding example42 Puppet modules, underlying how most of the "NextGen" modules, written in 2010, were deprecated (even if most of them, written at Puppet 2.6 times, can still work under Puppet 5) and how most of their functionalities could be replaced by [tp](https://github.com/example42/puppet-tp) and [psick](https://github.com/example42/puppet-psick).

There are many good maintained modules available from [voxpupuli](https://github.com/voxpupuli) or [camptocamp](https://github.com/camptocamp), for example, and, when necessary, we collaborate with existing communities.

By that time we did the minimal updates needed to ensure functionality with Puppet 5 without using any of the modern Puppet implementations like lambda or data in modules.

We decided to only keep the [example42 puppet-network module](https://github.com/example42/puppet-network/). Due to the reason that the network module is an approved module on Puppet forge, and a few other modules who had a dedicated maintainer, as [apt](https://github.com/example42/puppet-apt)

## example42 Puppet modules in mid 2018

In July 2018 we have been at several customers and we learned that they are using two more modules: [puppet-rclocal](https://github.com/example42/puppet-rclocal/) and [puppet-zabbix_agent](https://github.com/example42/puppet-zabbix_agent), so we decided to keep on with their development, "un-deprecate" them, and work on the releases which make use of current Puppet syntax.

The puppet-rclocal module is already upgraded to make use of data in modules with hiera 5. A [new version](https://forge.puppet.com/example42/rclocal) has already been released to Puppet forge.

The [zabbix_agent](https://github.com/example42/puppet-zabbix_agent) module is under development at the moment. We removed dependencies to example42 firewall, monitor and puppi module, legacy of NextGen times, and we updated it to modern Puppet language.
A new version will be pushed to the Forge very soon.

## example42 Puppet modules in future

We are carefully reviewing any usage of our modules at customers. Generally we try to move customers to supported or approved modules (mostly from puppetlabs or voxpupuli).

We will keep our list of modules short and we try to get approved status for all example42 modules which are under actual development.

Happy hacking,
Martin Alfke
