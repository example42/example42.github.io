---
layout: blog
title: Tip of the Week 75 - What you need to know about Puppet facts. Part 2 - Custom facts
---

In the [first post](https://www.example42.com/2018/05/28/what-you-need-to-know-about-puppet-facts-part-1-core_facts/) of this series about Facter, we introduced its basic features and we talked about **Core facts**, the ones shipped directly with Facter and available whenever we use Puppet.

In this post we will see more details about facts that we can write in Ruby by ourselves for whatever purpose we may have.

### Custom facts

Custom facts are shipped with Puppet modules, if we use already Puppet it's likely we are already using some custom fact present in one of the public modules we might be using.

They are written in Ruby language and have to be placed in the directory ```lib/facter``` of a module.

The most simple example of a fact is one that just executes a command and shows its output:

    Facter.add('connected_users') do
      setcode do
        Facter::Core::Execution.execute('/usr/bin/who | wc -l')
      end
    end

This fact is called ```collected_users```, this is the argument passed to the ```Facter.add``` method.

Whatever code we want to run in order to calculate the value of this fact, has to stay inside the ```setcode``` statement. In this case we just want to run a shell command, and we use the dedicated ```Facter::Core::Execution.execute``` method for this (which takes care of wrapping our command as needed). The argument passed here is the command we want to execute (```/usr/bin/who | wc -l```).

The output of this command is the value of our collected_users fact.

In order to ship and use this fact, we have to place the above piece of Ruby code in a file called ```lib/facter/collected_users.rb``` of a module.

If we have such a module in the ```$modulepath``` of our Puppet Server (for example the directory ```/etc/puppetlabs/code/modules``` for modules available to all Puppet environments, or ```/etc/puppetlabs/code/environments/production/modules``` for modules available for the, default, production Puppet environment), this fact would be automatically copied to each client, **before** running the catalog request. This means that the fact is immediately available to the client and can be used straight on in our Puppet manifests.

This automatic copy of each custom fact (and other elements) of a module is called **pluginsync** and we actually see it happening when we run Puppet, with an output like:

    Info: Using configured environment 'production'
    Info: Retrieving pluginfacts
    Notice: /File[/opt/puppetlabs/puppet/cache/lib/facter/connected_users.rb]/ensure: defined content as '{md5}d4cfb32bbc71e8d738004e584b0ac8bf'
    [...]

which is telling us that the connected_users.rb fact present in the ```lib/facter``` directory of one of our modules has been copied to the ```/opt/puppetlabs/puppet/cache/lib/facter/``` directory of the client.

Note that custom facts are **not** visible when we run the ```facter``` command from the local cli. We need to specify ```-p``` (```--puppet```) argument, or, recommended starting from Facter 3, use instead the ```puppet facts``` command:

    root@client:~# facter connected_users

    root@client:~# facter -p connected_users
    1

    root@puppet:~# puppet facts | grep connected_users
    "connected_users": "1",

#### Facts confinement

What's wrong about the fact we just wrote, if we work in a multi OS environment?

It runs a shell command which is available under Linux / Unix, but this is what happens when we run it under Windows:

    Info: Retrieving plugin
    Notice: /File[C:/ProgramData/PuppetLabs/puppet/cache/lib/facter/connected_users.rb]/ensure: defined content as '{md5}d4cfb32bbc71e8d738004e584b0ac8bf'
    Info: Loading facts
    Error: Facter: error while resolving custom fact "connected_users": execution of command "/usr/bin/who | wc -l" failed: command not found.

and we don't unnecessary (in this case not blocking) errors, right?

Facter allows us to use the ```confine``` statement, which restricts the execution of the fact only on systems that match the given condition, based on another fact.

For example, to confine our ```connected_users``` fact to run only on Linux we can use the ```kernel``` core fact:

    Facter.add('connected_users') do
      **confine :kernel => 'Linux'**
      setcode do
        Facter::Core::Execution.execute('/usr/bin/who | wc -l')
      end
    end

#### Facts within Facts

We can refer use the values of other facts inside our custom facts code.

For example we can assign to a local variable, the value of a fact with:

    k = Facter.value(:kernel)

#### Facts precedence

We can have multiple ```Facter.add``` statements with the same name, they can have different confinements so that we can resolve the possible values of a fact using different code and logic.

We can also have different entries for the same confinement group, in this case we need a way to decide what's the actual value to use for a fact, and here come handy the concept of Facts's weight which defines the wight to give to a give, if we have valid values for two different fact names, the one with higher weight "wins" and provides the relevant value.

A good example of usage if ```confine``` and ```has_weight``` is the code of the core fact ```virtual``` in Ruby (so in Facter version 2, as the equivalent in version 3 is written in C++). This can be seen  [here](https://github.com/puppetlabs/facter/blob/2.x/lib/facter/virtual.rb).

Note that we have, in the ```virtual.rb``` file, multiple blocks like:

    Facter.add("virtual") do
      confine :kernel => 'XXX
      confine: :XXX => 'XXX'
      has_weight XXX
    end

their combination is used to provide the final value of the virtual fact for different OS and different Hypervisors.

### Structured facts



Alessandro Franceschi
