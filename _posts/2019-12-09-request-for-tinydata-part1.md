---
layout: blog
title: Puppet Tip 107 - Request for Tiny Data - Part 1
---

This is the first of a 4 part call for Tiny Data.

Before talking about Tiny data we have to mention what uses it:

### Tiny Puppet (tp)

If you know something about example42, you should know that we developed [Tiny Puppet](https://github.com/example42/puppet-tp){:target="_blank"} (tp), a Puppet module which allows to manage potentially **any application** on any **Operating System**.

What exactly, currently Tiny Puppet can manage?

**Any application** that can be installed via a Puppet **package** resource.

On What Operating Systems?

- Mostly **Linux** (RedHat, Debian, Suse and derivatives)
- But also **Solaris**, **BSDs** and **Darwin** (with brew-cask)
- And potentially also **Windows** (with Chocolatey).

What you can use it for?

- Quickly install, test, show logs of the managed applications, from the shell
- Manage applications installation and configuration in Puppet manifests. such as
  - Local profiles, with our code, our files and logic 
  - Possibly, optionally, in component modules, to benefit from tp integrations
  - Ready for Hiera use collections, like the [tp-profiles],

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

This can be useful when **we know how to configure our application**, and we want a quick way to puppettize it without getting lost in finding the right component modules with its bunch of dependencies, in a way the allows us to concentrate just on the data to customise, which, for the above example, could be Hiera data as follows:

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

### Request for Tiny Data!

So, is there any app you would like to be managed via Tiny Puppet?

**Let us know**, in any way (tweet, comment, email, voice...).

We will **give our answer**.
