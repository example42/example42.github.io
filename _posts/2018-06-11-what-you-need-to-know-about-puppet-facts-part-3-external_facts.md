---
layout: blog
title: Tip of the Week 76 - What you need to know about Puppet facts. Part 3 - External facts
---

This week continues our journey inside what's worth knowing about Facter.
In the [first post](https://www.example42.com/2018/05/28/what-you-need-to-know-about-puppet-facts-part-1-core_facts/) we introduced its basic features and the **Core facts**, in the [second post](https://www.example42.com/2018/06/04/what-you-need-to-know-about-puppet-facts-part-2-custom_facts/) we described how to write custom facts in Ruby language.

Now we are going to give a look to an even easier way to create custom facts: **external facts**


### External facts

They have been introduced in Facter 1.7, inheriting a similar functionality that was proposed via the **stdlibe** module.

External facts can be texts in ini file, yaml or json format, or simply commands or scripts, written in any language for which is available a local interpreter, that respectively contain or return key-values.

Writing an external file is as easy as placing a file like ```/etc/facter/facts.d/myfact.txt``` with a content like:

    myfact=myfactvalue

The same fact can be placed in a Yaml file called ```/etc/facter/facts.d/myfact.yaml``` and have content like:

    ---
    myfact: myfactvalue

Or be a Json file like ```/etc/facter/facts.d/myfact.json``` with content like:

    {
      "myfact": "myfactvalue"
    }

Note that actually the name of these files has not to be the same of the fact, what's important is the content of the txt, or json or yaml, the name of the key being the name of the fact.

We can have even more than one fact definition in a single file, and it's trivial to write **structured facts** (check previous posts for explanations) in Yaml or Json files:

    ---
    classification:
      role: webserver
      env: prod
      zone: dc1

### Executable Facts

External facts can be also expressed as the output of a command, on Unix derivatives it's enough to have an executable file under ```/etc/facter/facts.d/``` that outputs the name of the facts and its value (in ini like style: ```name=value```):

    #!/usr/bin/env bash
    echo connected_users=$(/usr/bin/who | wc -l | tr -d ' ')

Any language can be used to write external facts as executables, but it's required to specify the path of the interpreter to use (here bash) in the first line, with a shebang (```#!```).

On Windows executable facts can be placed in files with the following extensions:

- ```.com``` or ```.exe``` for binary executables
- ```.bat``` or ```.cmd``` for batch scripts
- ```.ps1``` for PowerShell scripts

Up to now we mentioned the directory ```/etc/facter/facts.d``` but actuslly FGacter looks for external facts in different directories. On Unix/Linux they can be placed under:

    /opt/puppetlabs/facter/facts.d/
    /etc/puppetlabs/facter/facts.d/
    /etc/facter/facts.d/

On Windows they can be placed under:

    C:\ProgramData\PuppetLabs\facter\facts.d\

When running Puppet as a non privileged user, external facts are looked in:

    <HOME DIRECTORY>/.facter/facts.d/

Contrary to **custom facts** written in Ruby, which can be seen from the command-line only by running ```facter -p```, external facts are visible, as **core facts** just by running ```facter```.

### Shipping external facts

As we have seen, it's enough to place a file in one of the mentioned directories to create an external fact.

This can be done during the nodes' provisioning, and might be a way to define how different can be our nodes in our infrastructure according to facts values like role, env, zone, datacenter, application or similar.

We can also ship external facts directly in our modules: as the ```lib``` directory of modules (ciontaining Puppet types and provides, ruby facts and functions) is automatically distributed to clients via Puppet **pluginsync** mechanism, the content of the directory ```facts.d``` of a module is also copied to clients, and the external facts there are evaluated since the very first Puppet run.

Note that any external file placed in a module's ```facts.d``` directory is copied as is to every client, so there's no way to ship different facts with different values to different clients.

The obvious consequence is that generally in modules the shipped external facts are executables, that and run and compute their values on the clients.

We can also shop external facts via Puppet using the ```file``` resource and placing a file in one of the available dirs for external facts. In this case the content of such file can be derived from a template and be different according to our nodes, but note that if we follow this approach, the relevant facts are available only starting from the second Puppet run, as the first one is needed to create them (no pluginsync is involved in this case).


Alessandro Franceschi
