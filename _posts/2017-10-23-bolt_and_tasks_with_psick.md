---
layout: blog
title: Tip of the Week 43 - Bolt and tasks with PSICK
---

The release of  [bolt](https://puppet.com/products/puppet-bolt) at last PuppetConf has stirred a lot of interest in Puppet community and in a very few days modules with tasks have started to appear on the Forge.

At example42 we have started to experiment with Bolt and have added relevant profiles and tasks to the [psick](https://github.com/example42/puppet-psick) module.

Let's see how to work with Bolt in PSICK.

First we need to install the psick module:

    puppet module install example42/psick

Or add it to the ```Puppetfile``` of our control-repo (we can use the [PSICK control-repo](https://github.com/example42/psick) or any other one):

    mod 'example42/psick', :latest

Then we have to classify our nodes with the psick class, it's enough something like

    include psick

Once the psick class is added to the catalog nothing happens, by default, but a huge amount of functionalities is a parameter away. If we use, as we should, Hiera to manage our data, and we have an [e]yaml backend, we can install bolt on a node (we need it only on the server from which we run commands) with data like:

    psick::base::linux_classes:
      bolt: 'psick::bolt'

    psick::bolt::is_master: true

Psick can also automatically manage ssh keys sharing between nodes and the creation of a bolt user on all the nodes, who can sudo bold commands. This is completely optional (we can connect with bolt directly using the root user and share authorised keys via other methods) but if we want everything done out of the box we can add, for all our nodes:

    psick::base::linux_classes:
      bolt: 'psick::bolt'

    psick::bolt::master: <bolt_master> # Bolt master is the fqdn of node where to set psick::bolt::is_master: true
    psick::bolt::keyshare_method: storeconfigs

We require storeconfigs enabled on our Puppet Server to automatically share ssh keys between the Master and the managed nodes.

It will take some Puppet runs, on the so called Bolt master and the managed nodes, to converge and distribute the ssh keys to use for bolt.

Once done, we can login on the Bolt master, as bolt user and from here we can run via Bolt commands, scripts, tasks and plans on any node of our Puppet infrastructure:

    [bolt@puppet ~]$ bolt command run uptime --n $(cat nodes/all) --user bolt

Psick creates automatically the file called ```nodes/all``` in the home of the bolt user (this is the default user psick uses for ssh connections both on master and managed nodes), with a csv of all the nodes of the infrastructure.

In the class ```psick::bolt::master``` is possible to create and customise different files for different nodes lists.

The psick module has some tasks too, the first one we've thought about when we have heard about Bolt:

  - ```psick::puppet_install``` installs Puppet agent on a remote node
  - ```psick::puppet_agent``` runs Puppet agent on a remote node (eventually specifying the Puppet master, the Puppet environment and if to run in noop or no-noop mode
  - ```psick::puppet_enable_noop``` configures noop mode on puppet.conf
  - ```psick::puppet_unlock``` removes lock files create by stale Puppet runs or by ```puppet agent --disable```
  - ```psick::system_update``` trigger the update of all packages of the system

We are quite sure this list is going to grow and the single tasks to be refined, but we think this list already covers some quite common needs.

To run one of Psick's tasks:

    bolt task run psick::puppet_unlock -n <node_fqdn> --modules <module_path> --user bolt

(Note, we don't have to specify ```--user bolt``` (the one used for SSH login) if we are running as bolt user locally. The examples in this post are done on vagrant servers and for some reasons the vagrant user is used by default to connect to remote servers, even if bolt is run as bolt user.)

To run puppet agent in noop mode using the integration environment on all nodes, a command like this is enough:

    bolt task run psick::puppet_agent noop=true environment=integration -n $(cat nodes/all) --modules <module_path> --user bolt

If you use psick, you have also the Tiny Puppet module installed, and this brings with it the ```tp::test``` task, which allows quick testing on the status of all the applications managed by Tiny Puppet in the whole infrastructure:

    bolt task run tp::test -n $(cat nodes/all) --modules <module_path> --user bolt

This is just the beginning of our exploration of Bolt and Puppet tasks (and plans!) in psick.

We see a huge potential in Bolt, it perfectly fits the part where Puppet was weaker than other tools like Ansible: remote commands execution, on demand, and, partly, orchestration.

We are sure a lot of interesting use cases and applications will arise in the near future and we are committed to play a lot with it inside and outside PSICK.


Alessandro Franceschi
