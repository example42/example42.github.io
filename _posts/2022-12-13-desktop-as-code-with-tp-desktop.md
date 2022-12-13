---
layout: blog
title: Desktop as Code with TP Desktop
---

We manage via code the configurations of servers, cloud resources and infrastructures.

Are we doing the same with our desktop setups, on our laptop, desktop, remote VDI?

Do we manage as code the usual files we have, or would like to have, in our home configurations on remote servers?

You may wonder what's the benefit of adding the complexity of developing configurations that are applied one time and are usually managed manually.

Well, let's see if any of these use cases may be of interest for us:

- We do not setup our desktop only once. We do it whenever we buy or reinstall a new computer, we are going to do that until the end of our life, on all our current and future computers and systems.
- We may have the programs we always want installed, and maybe even configure them, on different Operating Systems (Linux, Windows, MacOS)
- We man have to manage our homes directories, configuring bash, git, vim, ssh, authorized_keys, etc, either on our local desktop or on remote servers
- We may have to handle sensitive data in a safe way (ssh keys, cloud credentials, applications passwords), in a repeatable, reliable and programmatic way (well, it's just Yaml).


## Introducing tp desktop

If any of the above use cases might be of interest for you, you may want to check out **tp desktop**, a tool that allows you to manage your desktop as code.

Technically tp desktop is a combination of the example42-tp Puppet module (version 3.7.0 or later) and a simplified Puppet control repository: a git repository where you can store your desktop code.

Prerequisites are just:

- Puppet, just the package, used in apply mode (without the need of a central server and a local service)
- Git, used to clone and update the tp-desktop control repository

And hey, even if you don't know or like Puppet don't worry, with tp-desktop you will work only with Yaml files.

All the complexities and powers of Puppet's language are hidden (but still available, if you know how to master puppets).


## Installation

To install tp desktop, you need to have the Puppet and Git commands available, so just install them as you would normally do on your system:

    rpm|apt|zypper|brew install puppet

If you want to install the latest Puppet package you can just run this installation script:

    wget -O - https://bit.ly/installpuppet | sudo bash

With Puppet installed, you can install example42's tp module with the following command:

    sudo puppet module install example42/tp

Then all you can setup tp, adding the tp command to your system:

    sudo puppet tp setup

If you need to install git, you can do it directly with the tp command line:

    sudo tp install git

The tp command has various options that allow you to install, test, troubleshoot and get info on the applications Tiny Puppet can manage (technically every possible application for which there's a downloadable package).

But here we are discussing how to manage our desktop as code, and this can be done initializing a new desktop git repository, where you can start to configure your desktop configurations:

    tp desktop init

This clones the [tp-desktop](https://github.com/example42/tp-desktop) git repository under a directory named tp_desktop (don't rename it!), just enter there and run the available tp desktop commands:

    cd tp_desktop

Now you can start to work with your desktops configurations. You can list the ones available by default (you can/should modify them or add new ones according to your needs):

    tp desktop list

There are several things that can go wrong with a young tool that aims to make it easy to manage every possible application on different platforms, so if you find any issue first give a look to the ERRORS.md file and then feel free to open an issue on [tp](https://github.com/example42/tp).

First important caveat worth underlining is that at the moment the tp command line doesn't work on Windows systems, we will get there, you can already manage Windows resources with the example42-tp module, but the tp cli command is still not available.


## Creating your own desktop configurations

You can create your own desktop configurations by adding new files to the **tp_desktop/data/desktops** directory. Here there are simple Yaml files you can edit to manage packages to install or files to create, using the tp Puppet module.

You have several options available here, for who knows Puppet, technically you are just configuring via Hiera the parameters of the tp class, tp_desktop is a simplified Puppet control-repo and tp desktop apply just runs puppet apply manifests/site.pp with the proper parameters.

The simplest way to define the list of applications to install is as follows, edit a new file like data/desktops/my_desktop.yaml and something like:

    ---
    tp::installs:
      - code
      - docker
      - packer
      - terraform

You can install the above applications (tp will take care of managing the right package and eventual extra repositories for your OS) with:

    sudo tp desktop apply my_desktop

You can create all the desktop files you need and apply them on the systems of your choice.

Nobody prevents you from using different desktop files on the same system, or use the same file on different systems, applying different sets of configurations as needed.

Just be aware that the configurations added in  **data/desktops/desktop_name.yaml** are applied when you run **tp desktop apply desktop_name**, while the configurations added in **data/common.yaml** are applied to every desktop, so you are expected to set there only general settings which are good for all your OS and desktops / home environments.


## Managing your home directory and more... 

Tp desktop can be used not only to manage the applications you want to install on your computer, but also your configuration files on a system.

A desktop configuration as follows:

    ---
    tp::dirs:
      /home/myuser/:
        source: 'puppet:///modules/mydata/home'
        recurse: remote

allows you to manage the contents of your home directory (**/home/myuser** in the example, change as needed) with the contents of the files under the directory **site/mydata/files/home** of your tp_desktop repository (technically, mydata is a Puppet module, tp::dir is a wrapper around the Puppet file resource and shares some of its parameters).

You may wonder what's the advantage of having this overhead just to manage the contents of a directory, well we are just scraping the surface of what you can do with tp desktop.

Let's review here what you can do with it, leaving to further posts or the documentation the details of how to do it:

- Install any application on any Operating System (as described earlier), handling eventual upstream repositories

- Manage the contents of full directories with status configuration files (as just described)

- Manage the contents of configuration files, using templates and variables defined in the desktop configurations

    tp::confs:
      /home/myuser/.gitconfig:
        source: 'puppet:///modules/mydata/home/.gitconfig'
      

- Manage the contents of directories based on a remote git repositories
- Clone the git repos of the applications you want (just name the application, tp knows where to look for the sources)
- Encrypt passwords and sensitive files (like ssh private keys or tokens) and safely store them, in encrypted format in a git repository
- Leverage on the **tp log**, **tp test**, **tp info**, **tp debug**, **tp version** commands, available for every application installed via tp, to get info, troubleshoot and test the functionality of the applications you've installed.

tp desktop is in beta now, without Windows cli support.

With the release of Tiny Puppet 4.0 an evolved version is expected with:

- **tp desktop** 1.0, with Windows cli support
- **tp source** command, define and task, to clone apps' git sources
- **tp image** command, define and task, to deploy the app's official container
- **tp debug** command, define and task to troubleshoot apps
- **tp version** command, define and task which shows apps' version
- improved **tp info** command, define and task to get info on apps
- **TinyData 1.0** with updated data for recent OS and the new settings used by the above commands

Alessandro Franceschi

