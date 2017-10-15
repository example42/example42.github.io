---
layout: blog
title: Tip of the Week 42 - Puppet Tasks in PSICK
---

At [PuppetConf2017](https://puppet.com/community/events/puppetconf/puppetconf-2017) the [bolt](https://puppet.com/products/puppet-bolt) task runner was released and made public.

Bolt uses the concept of Puppet tasks to allow workflow based system management, which was missing in Puppet since ages.

Puppet itself uses the declarative state configuration model, describing the final state of a system. With declarative description it was always a pain adding workflow based configurations like application updates or running maintenance tasks only at specific times. Bolt fills this gap.

With bolt one can run any kind of:

  - copying files to a system
  - run any remote command
  - run any script
  - run a Puppet task
  - run a Puppet plan

Connection to remote systems is done either via ssh or WinRM. Other connectors can be added to bolt upstream development. At the moment there is no API available to add additional connectors to bolt via some kind of bolt plugin.
The ssh access must be configured in advance prior being able to make use of bolt. Access can be configured as unprivileged user using sudo commands. Bolt just needs to know which credentials to use.

Credentials for ssh can be placed in ```~/.ssh/config```. Credentials for Windows systems are provided on command line using the ```--user``` and the ```--password``` parameter.

Which systems bolt should connect to must be provided on cli with ```--nodes``` parameter. As of now, no node groups can be specified.

## Running remote commands

Running remote commands is easy. Just tell bolt which remote command to execute:

    bolt command run 'yum -y update' --nodes www.domain.com,mail.domain.com

For Windows system the nodes must be given using the winrm URI:

    bolt command run 'puppet resource service puppet-agent ensure=running' --nodes winrm://win.domain.com,server.domain.com --user Administrator --password <password>

## Running scripts

Bolt is able to use a local script, copy it to the mentioned nodes and run it there:

    bolt script run ~/update_system.sh --nodes www.domain.com,mail.domain.com

## Writing and running tasks

## Writing und running plans

Martin Alfke

