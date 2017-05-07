---
layout: blog
title: Tip of the Week 19 - A PSICK Vagrant experience
---

[PSICK](http://github.com/example42/psick) is an opinionated Puppet control-repo with a lot of integrations and tooling to support the Puppeteer during development, testing and operations.

One of the most useful integration is the one with **Vagrant**.

We can **test our current local changes** to Puppet code and data in several different Vagrant environments and VMs.

Under ```vagrant/environments``` we have various Vagrant environments, fully customisable, where Puppet can be run in agent or apply mode testing directly the effect of our changes on the repo.

Here we can test different Operating Systems and Puppet setups, with Puppet Enterprise (PE), OSS Puppet or The Foreman masters.

But first, we need to setup a few things.

## Our new control-repo

PSICK is both a control-repo by itself and a generator (at the moment very rough) of control-repos.

To create a control-repo for our new, wonderful, green field **acme** project we can:

    git clone https://github.com/example42/psick
    cd psick
    ./psick create

This command allows us to create a new control-repo in a new directory. It asks some questions:

- the path (absolute or relative to the dir containing psick) where we want to create it

- if we want to create a bare minimal control-repo or a full featured one, which is the exact copy of the current psick files.

- if we want to automatically make the first commit on the brand new control-repo with all the added files.

Output is something like:

    ### PSICK is going to create a brand new control-repo ###

    # Specify the path where you want to create your new Puppet control-repo
    Provide the full absolute path or the name of a dir that will be created under /Users/al/tmp
    Press [ENTER] when done.

**acme**

    # Choose how you want to create your new control-repo
    1- Create a full featured control-repo based on current PSICK
    2- Create a minimal control-repo with only the bare minimal files
    Note that you will be able to add or remove components later.
    Make your choice:

 **1**

    # Copying all files from psick to /Users/al/tmp/acme

    # Initialising git in the new directory
    Initialized empty Git repository in /Users/al/tmp/acme/.git/
    # Showing current status of the new git repo
    On branch production

    Initial commit

    Untracked files:
      (use "git add <file>..." to include in what will be committed)

            .codacy.yaml
            .gitignore
            .gitlab-ci.yml
            [...]
            vagrant/

    nothing added to commit but untracked files present (use "git add" to track)
    # NOTE: master branch has been renamed to production for Puppet compliance

    # Do you want to make a first commit on the new repo?
    Press 'y' to commit all the existing files so to have a snapshot of the current repo
    Press anything else to skip this and take your time to review and cleanup files before your first commit

**y**

    [production (root-commit) 1c7c6c8] First commit: Snapshot of origin     https://github.com/example42/psick (fetch) originhttps://github.com/example42/psick (push)
     607 files changed, 107764 insertions(+)
     create mode 100644 .codacy.yaml
     create mode 100644 .gitlab-ci.yml
     [...]

    ### Congratulations! Setup of the new control-repo finished ###
    # To start to work on it: cd /Users/al/tmp/acme
    # Keep updated the psick repo, and use the psick command to update or add componenent to your control-repo

So now we can move in the created dir, in my test case:

    cd /Users/al/tmp/acme
    git log
    git status

and setup our control repo following the instructions.

### Prerequisites installation

If we still haven't Puppet installed, we can install it (more or less on any Linux) with:

    sudo bin/puppet_install.sh

Consider that many parts of PSICK use Puppet latest features, optimal would be Puppet version 4.10 or later.

Remember, as is, PSICK is intended to be used for greenfield setups or migrations: we are not supposed to use it on existing Puppet control-repo, if not for inspiration, or some code or ideas grabbing.

Once a decent Puppet is in place, we have to deploy the modules via r10k, if not already installed, we can install it and some other useful gems with:

    bin/puppet_setup.sh

If we have **r10k** already installed, we can just run:

    r10k puppetfile install -v

Setup is done, now we can start to play around. Under the ```vagrant``` directory we have most of the Vagrant related stuff.

We need Vagrant, Virtual Box and some plugins. We can install them all (with the option to skip single steps) with:

    bin/vagrant_setup.sh

We can install the recommended vagrant plugins with:

    vagrant plugin install vagrant-cachier
    vagrant plugin install vagrant-vbguest
    vagrant plugin install vagrant-hostmanager
    vagrant plugin install vagrant-triggers

And, if we want to test a Puppet Enterprise based environment (such as ```pe```, ```demo```, ```lab```)

    vagrant plugin install pe_build


## Time to play

Once Vagrant is setup with the needed dependencies, we can create some VM.

    cd vagrant/environments/ostest
    vagrant status

Output here is quite interesting, note all OS work flawlessly out of the box, though.

    al@mule ostest [production] $ vagrant status
Current machine states:

    centos7.ostest.psick.io             not created (virtualbox)
    centos6.ostest.psick.io             not created (virtualbox)
    ubuntu1604.ostest.psick.io          not created (virtualbox)
    ubuntu1404.ostest.psick.io          not created (virtualbox)
    ubuntu1204.ostest.psick.io          not created (virtualbox)
    debian8.ostest.psick.io             not created (virtualbox)
    debian7.ostest.psick.io             not created (virtualbox)
    suse12.ostest.psick.io              not created (virtualbox)
    suse11.ostest.psick.io              not created (virtualbox)
    opensuse-tumbleweed.ostest.psick.io not created (virtualbox)
    opensuse-42-1.ostest.psick.io       not created (virtualbox)
    alpine3.ostest.psick.io             not created (virtualbox)
    fedora23.ostest.psick.io            not created (virtualbox)
    cumulus.ostest.psick.io             not created (virtualbox)
    windows2012-ostest                  not created (virtualbox)
    windows2008-ostest                  not created (virtualbox)

We try a Centos 7 vm:

    vagrant up centos7.ostest.psick.io

The ```ostest``` environment uses **puppet apply** to test our local code, mounted on the selected VM.

Puppet run can be triggered either via a command like:

    vagrant provision centos7.ostest.psick.io

Or, from within the VM, as root:

    vagrant ssh centos7.ostest.psick.io
    vm $ sudo su -
    vm # /etc/puppetlabs/code/environments/production/bin/papply.sh

The same concept applies for other VMs and for the other environments under ```vagrant/environments```, some of them use Puppet Enterprise or Foreman, serving directly our code to client VMs running in **puppet agent** mode.

In some cases, further steps may be required, local documentation should help.

Don't expect everything to work out of the box flawlessly, combinations of OS, roles and data are many and not all tested.
Please report bugs and eventually Pull Requests on Github.

## Customising

The existing Vagrant environments can be customised, by editing the ```config.yaml``` file in each dir.
Give a look to [this document](https://github.com/example42/psick/blob/production/docs/vagrant.md) for  details on how to tune the Vagrant environments.

Now we can enjoy our Puppet environment, start to develop and customise our control repo starting from the data in ```hieradata```, the local code under ```site``` the external modules to add to ```Puppetfile```, the classification logic in ```manifests/site.pp``` and ```hiera.yaml```.

And, most of all, we can immediately test our code in several different systems which may emulate our infrastructure servers.

Alessandro Franceschi
