---
layout: blog
title: Tip of the Week 42 - Puppet Tasks in PSICK
---

At [PuppetConf2017](https://puppet.com/community/events/puppetconf/puppetconf-2017) the [bolt](https://puppet.com/products/puppet-bolt) task runner was released and made public.

Bolt uses the concept of Puppet tasks to allow workflow based system management, which was missing in Puppet since ages.

Puppet itself uses the declarative state configuration model, describing the final state of a system. With declarative description it was always a pain adding workflow based configurations like application updates or running maintenance tasks only at specific times. Bolt fills this gap.

With bolt one can runny kind of:

  - any remote command
  - any script
  - a Puppet task
  - a Puppet plan

Connection to remote systems is done either via ssh or WinRM. Other connectors can be added to bolt upstream development. At the moment there is no API available to add additional connectors to bolt via some kind of bolt plugin.

Which systems bolt should connect to must be provided on cli with ```--nodes``` parameter. As of now, no node groups can be specified.

Martin Alfke

