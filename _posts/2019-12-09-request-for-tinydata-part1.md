---
layout: blog
title: Puppet Tip 107 - Request for Tiny Data - Part 1 - Tiny Puppet (tp)
---

This is the **first** of **four** post series for our **Request for Tiny Data**.

We will clarify better at the end who can request what, first, we have to give some context, and explain **what uses Tiny Data**:

### Tiny Puppet (tp)

If you know something about example42, you should know that we developed [Tiny Puppet](https://github.com/example42/puppet-tp){:target="_blank"} (tp), a Puppet module which allows to manage potentially **any application** on any **Operating System**.

**What applications exactly Tiny Puppet can manage?**

The current list is **[always this](https://github.com/example42/tinydata/tree/master/data){:target="_blank"}**, but the right answer is: **Any application** that can be installed via a Puppet **package** resource, taking care, where necessary, of the configuration of the relevant package respository.

**On What Operating Systems?**

- Mostly **Linux** (RedHat, Debian, Suse and derivatives)
- But also **Solaris**, **BSDs** and **Darwin** (with brew-cask)
- And potentially also **Windows** (with Chocolatey).

**What do I need to achieve this?**

Puppet, the Tiny Puppet module and, guess what, the app tinydata.

**What you can use it for?**

- **Shell** usage: Use the `tp` command to quickly install, test, show logs of the managed applications
- **Puppet manifests** usage: Use `tp::install`, `tp::dir` and `tp::conf` defines to manage applications installation and configurations.

#### Usage in shell

Tiny Puppet is born and expected to be used in Puppet manifests, but it can actually work standalone, as a cli command.

It can be installed, via Puppet, with:
````
sudo puppet module install example42-tp
sudo puppet tp setup
````

After this we have at disposal the **tp** command, that we can use to install something:

````
sudo tp install sysdig
sudo tp install opera
sudo tp install puppetdb
````

We can also check if all the resources we installed via tp are running well:

````
tp test
tp test apache
````

Or show the live logs of all or the selected applications:

````
tp log
tp log nginx
````

#### Usage in Puppet manifests

The tp module provides the following defines:

- ```tp::install```. It installs an application and starts its service, by default
- ```tp::conf```. It allows to manage configuration files related to the app, handling dependencies
- ```tp::dir```. Manages the content of directories
- ```tp::test```. Allows quick and easy checking of the status of the application
- ```tp::repo```. Manages extra or upstream repositories for the application package

We can use them in Puppet manifests like:

  - Local **site profiles**, with our code, our files configured with our logic 
  - Possibly, optionally, in **component modules**, to benefit of tp cli integrations and OS coverage
  - Ready for Hiera use **profiles collections**, like the [tp-profile](https://github.com/example42/puppet-tp_profile){:target="_blank"} or the [psick module](https://github.com/example42/puppet-psick){:target="_blank"}.

Just to give you an idea, the following code:

    class profile::openssh (
      String $template = 'profile/openssh/sshd_config.erb',
      Hash $options    = {},
    ) {

      tp::install { 'openssh': }
      tp::conf { 'openssh':
        template     => $template,
        options_hash => $options,
      }
      # Alternative which does the same:
      # tp::conf { 'openssh':
      #   content => template($template),
      # }      
    }

will install the package, configure the file with the contents we want, manage the service (taking care of dependencies and different names and paths) for openssh.

The example used here for openssh can be done **virtually for all applications you can think about** (for which there's a package to install and the right tinydata).

This can be useful when **we know how to configure our application**, and we want a **quick way to puppettize** it without getting lost in finding the right component modules with its bunch of dependencies, in a way the allows us to concentrate just on the data to customise, which, for the above example, could be Hiera data as follows:

    profile::openssh::template: profile/openssh/sshd_config.erb
    profile::openssh::options:
      Protocol: 2
      PermitRootLogin: 'no'
      UsePAM: 'yes'
      TCPKeepAlive: 'yes'

Content of the template, to be placed in our profile module, could be something like what follows (plus all the necessary extra settings we may want to hard-code):

    # File managed by Puppet
    <% @options.each do |k,v| -%>
    <%= k %> <%= v %>
    <% end -%>

### Request for Tiny Data

So, this is Tiny Puppet, and anything want to manage with it we need its Tiny Data.

Is there any app that **you** would like to easily install and configure (via Tiny Puppet)?

**Let us know**, in any way (tweet, comment, email, voice...).

We will give an **example42 answer**.
