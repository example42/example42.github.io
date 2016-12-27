---
layout: blog
title: Tip of the Week [2] - Anatomy of a Puppet control-repo
---

For years Puppeteers have struggled to find a way to organize their Puppet code to manage their infrastructures in an optimal way, following the evolution of Puppet itself and its ecosystem.

Many different approaches were taken some worked better, some worse, but there was not actually a single, common approach.

Now things are different. There are established tools to manage Puppet data ([Hiera](https://docs.puppet.com/hiera/)), deployment of external modules ([r10k](https://docs.puppet.com/pe/latest/r10k.html) or [Librarian Puppet](https://github.com/voxpupuli/librarian-puppet)) and a standard place where to place everything ([directory environments](https://docs.puppet.com/puppet/latest/environments_configuring.html)).

A Puppet control-repo is a [git] repository that contains the files you expect to have in your directory environment which provide whatever you need to manage your infrastructure, that is:

  - The ```manifests``` directory where are placed the first files that the Puppet server parses when compiling catalogs for clients. Here you typically have the ```site.pp``` file (but other manifests with different names can be seamlessly added) where you can set top scope variables, resource defaults, and eventually have node statements to define what classes should be included in your nodes (nodes classification can be done in several different ways, using ```node``` is just one of them).

  - The ```hieradata``` directory which contains Hiera data files. The name of the directory is completely arbitrary, even if this is a sort of standard de facto. This same directory could not even exists in the unlikely case you are not using Hiera, or if you use Hiera with backends which don't store data in normal (typically yaml or json) files. Some people, not me, prefer to place Hiera data in a separated dedicated repository, so you might have it outside the control-repo.

  - The ```modules``` directory contains Puppet modules. Typically you don't place themselves directly in your control-repo but define them in the ```Puppetfile``` and then deploy them with either r10k or Librarian Puppet.

  - You will probably have to develop custom modules (your role and profile modules, your site specific ones). You can decide to place them in dedicated repositories, and add them to your Puppetfile, or keep them in your same control-repo. In this case it makes sense to place them in a separated directory, such as ```site```, in order to differentiate external modules, defined in the Puppetfile, from the local ones.

  - The ```environment.conf``` file, which configures your environment: where the modules are placed, the caching timeout and eventually a script that returns a custom configuration version.

You can find an [essential skeleton for a control-repo](https://github.com/puppetlabs/control-repo), from Puppet.

You can also give a look to [example42 control-repo](https://github.com/example42/control-repo), which provides much more. Maybe too much.

It's based on a node-less classification, without role classes (profiles to include are defined in Hiera), a LOT of sample profiles with relevant sample Hiera data, deep integrations with Docker and Vagrant for code testing and a set of tools, optionally integrated with Fabric, to manage the whole Puppet code development, testing and deployment workflow.

For more information about example42 control-repo, give a read to [this blog post](http://www.example42.com/2016/05/11/a-modern-puppet4-control-repo/) or just look at its documentation and files: whatever are your Puppet skills you may find something useful there, after all it's the result of 10 years of Puppet experience.

Alessandro Franceschi
