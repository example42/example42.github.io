---
layout: blog
title: Tip of the Week 33 - Testing a control-repo with Vagrant
---

When we develop our Puppet code it's useful to have the possibility to test the effect of what we are doing on real systems, running Puppet on them, using our code under development, and seeing what happens without the need to commit anything.

Traditional testing methods based on spec tests don't verify the actual effect of our code on systems (they analyse the generated catalog to verify if it has the expected resources), we need to run real code on real operating systems.

Vagrant is the perfect tool for this and we can use it in our Puppet development setup.

We've [already talked](#http://www.example42.com/2017/05/08/a-psick-vagrant-experience/) about how we use Vagrant on [PSICK](https://github.com/example42/psick/), Example42's sample Control repo [generator], but that's a rather complex setup, with multiple Vagrant environments, a simple to use configuration file to use for each one of them, and multiple approaches to Puppet run.

If you want all the work done, just use PSICK, or copy from it the ```vagrant``` directory and the script ```bin/puppet_install.sh``` (used to install Puppet in certain VMs).

Let's review here, instead, the basic principles and what has to be done to setup Vagrant testing from within our control-repo.

First we have to create a ```Vagrantfile```, here we can configure one of more VMs to work on.

Then we have to decide how we want to run Puppet within the VMs, we have different options here:

  - (1) Run Puppet in ```apply``` mode, without using any Puppet Server. This is the simplest approach (we don't need a dedicated Puppet server to point to) but it fully simulates our real server setup , without further efforts, only if the following conditions are met:

    - We are not using an External Node Classifier or we can simulate in the Vagrant environment what the ENC provides (classes to include, parameters to set)

    - We don't rely on PuppetDB to manage resources in our catalog, that is we don't use exported resources and we don't use functions, like ```puppetdb_query``` that interrogate PuppetDB directly. If we are in these conditions we have to provide some workaround for machines running in Vagrant.

  - (2) Run Puppet in ```agent``` mode, using a Puppet Master running in our Vagrant environment. This is a valid alternative, which may cope with PuppetDB but may presents a few additional challenges:

    - If we use an ENC on our live Puppet Server, we must configure accordingly our Vagrant Puppet Server

    - We have to mount on the Vagrant Puppet Server our local control-repo, so that the files it serves come directly from the host where we are developing (in this case is absolutely necessary to disable catalog caching in ```environment.conf```).

On PSICK you can see both approaches used in different Vagrant environments under ```vagrant/environments```.

Other alternatives, like running Vagrant in agent mode pointing to an existing external Puppet Server, may be tried, as long as it's preserved the basic principle of being able to test our code before committing it (so we should either develop directly on the Puppet Server, using a dedicated environment, our mount there via NFS or similar, our local development directory).

Let's concentrate on the *apply* scenario, as using puppet agent implies that we are able to setup a Puppet Server on Vagrant which reproduces the same conditions we have on the real infrastructure.

Besides the apparent limitations, listed earlier, such approach is possible in many different cases, as long as we care of:

  - Setting with provisioning a script either [external facts](https://github.com/example42/psick/blob/production/vagrant/bin/vagrant-setfacts.sh) or [trusted facts](https://github.com/example42/psick/blob/production/vagrant/bin/vagrant-settrustedfacts.sh)  before running Puppet, if they are needed to classify nodes or are used in our ```hiera.yaml``` hierarchies.

  - Running Puppet in apply mode passing all the arguments we need to point our local Hiera data, and use the modules in the control-repo. For example [this one](https://github.com/example42/psick/blob/production/vagrant/bin/papply.sh).

  - Be sure we have, on our VMs all the gems and tools needed to compile a catalog, so Puppet, of course, and eventual extra gems ([example](https://github.com/example42/psick/blob/production/vagrant/bin/vagrant-setup_papply.sh))

  - Mount on the VM (better if in Read Only mode) the control repo directory we are developing on, under ```/etc/puppetlabs/code/environments/production``` (or link the "usual" /vagrant directory or change the puppet apply command to point to the correct local path).

  - Have the modules listed in our ```Puppetfile``` deployed on our development workstation (it's enough to run ```r10k puppetfile install``` from the main control-repo directory to populate accordingly its ```modules``` subdirectory)

  - If we use Hiera-eyaml and we don't want to place our private key on developers' workstations, we can just override eventual encrypted data in common Hiera files with unencrypted data, in the Hiera layers specific for development hostnames or for a ```devel``` tier.

  - If we use exported resources or functions that query PuppetDB, provide exceptions when the code is evaluated under Vagrant (usually this can be done checking if the value of the ```virtual``` fact matches ```Virtualbox```, as this is the most comment hypervisor used in Vagrant.)

Generally testing code under Vagrant in Puppet apply mode is easier and doesn't require particular workarounds when our control-repo is *self-contained*: it contains all the information we need to classify and configure nodes, eventually basing it on facts that can be easily added, as we've seen it before, during Vagrant provisioning.


Alessandro Franceschi
