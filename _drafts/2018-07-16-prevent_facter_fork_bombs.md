---
layout: blog
title: Tip of the Week 81 - Facter fork bombs and timeouts - what are they, how to prevent them
---

On [April 11th 2018 we wrote about external facts](https://www.example42.com/2018/06/11/what-you-need-to-know-about-puppet-facts-part-3-external_facts/). Within the mentioned posting we explained the possibilities you have and that you can use executables (like shell scripts) which will allow you to add individual facts.

What we have not talked about is the facter fork bomb which you can run into easily.

* Table of content
{:toc}

## Facter fork bomb

What is the facter fork bomb? A fork bomb means that the same process executes itsef over and over again.

### Facter fork bomb example

Consider the following external facter shell code:

    #!/bin/bash
    $osfamily=$(facter -p os.family)
    case $osfamily in
      'RedHat')
      ;;
      'SLES')
      ;;
      'Debian')
      ;;
    esac

### Facter fork bomb explanation

You want to return different values, depending on the os.family facts.
But what will happen:

Facter executes the shell script. The shell script itself executes facter, which will exectute the shell script, which will execute facter,.....

Welcome to your first facter fork bomb. Within a couple of seconds your system will be unusable, running on high load and eating memory.

### Facter fork bomb prevention

Never use the facter binary in an external, executable fact.
If you really must use a fact, then please consider writing a custom fact in Ruby.

Here you can easily use facter.value to access available facts.

## Facter timeouts

Another issue which can occur is that facter takes a hugh amount of time to collect facts. Sometimes this can be related to an external or custom fact where you try to connect to a non-performance system collecting data.

### Facter timeout example

Consider your 200 nodes to query information e.g. from LDAP or a remote database.

See the following code example:

    #!/bin/bash
    $role=$(ldapsearch -b 'cn=role, cn=$(hostname) ou=Servers, dc=example42, cd=com' -h ldapmaster.example42.com -l 3600
    echo "role=$role"

What happens if your LDAP server is not available, slowly responding of available over a highly saturated network link?

Facter will take long time to collect all information.
This can even lead to a timeout.

### Facter timeout prevention

Don't access remote systems from facter. Either the remote system can not deal well with the amount of requests or single nodes can not access the remote system.

Each external (executable) fact must use local resources only.

Happy hacking,
Martin Alfke
