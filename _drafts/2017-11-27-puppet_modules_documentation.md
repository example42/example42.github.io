---
layout: blog
title: Tip of the Week 48 - Puppet modules documentation
---

Modules' documentation is useful to understand what a module does and how it does it. We can access to it usually by reading the README, directly on the Forge or GitHub page, and eventually looking directly at the inline documentation in manifests.

### Puppet Strings

As you are probably aware there a tool, [**Puppet strings**](https://github.com/puppetlabs/puppet-strings) which is able to automatically generate documentation for a module.

It's based on the [Yard](http://yardoc.org/) tool and can generate docs in various formats.

To install Puppet strings:

    puppet resource package rgen provider=puppet_gem
    puppet resource package puppet-strings provider=puppet_gem

To generate the documentation for a module, move inside the module main directory and run:

    /opt/puppetlabs/puppet/bin/puppet strings generate **/*{.pp\,.rb} **/**/*{.pp\,.rb}

This will parse all the .rb and .pp files in the module and generate html documentation under the ```doc``` directory of the module.

### Puppet documentation server

Instead of running the ```puppet strings``` command on every change, it is also possible to have the strings server checking for changes and rendering documentation upon file changes.

Just change to your control repository and run the strings server:

    /opt/puppetlabs/puppet/bin/puppet strings server --modulepath=./modules:./site

This will spin up a webservice which is accessible on port 8808: ```http://localhost:8808```

We recommend to **not** have this web server running on the puppet master. Spin up a new server which will get code updates via git hooks or CI pipelines.

### puppetmodule.info

Yard can act as a server and show directly the html pages generated. There's a web site which relies on this and show Puppet strings based documentation for most of the Puppet public modules on the Forge and GitLab.

Give a visit to [www.puppetmodule.info](http://www.puppetmodule.info), site created by Dominic Cleal from The Foreman team.

Here you can see the documentation for virtually any module you will find yourself using, the site is able to generate on request the documentation for modules it hasn't yet processed.

So on this site you can look how documented modules [appear](http://www.puppetmodule.info/modules/example42-psick) and search modules and contents as needed.

### Control repo documentation

In [Psick](https://github.com/example42/psick) we use Puppet strings also to generate the documentation of the whole control-repo.

[This](http://puppet.pages.lab.psick.io/psick/) is Psick's puppet strings generated documentation (it includes README with merged texts from the psick control-repo and the classes and defines from the psick module). It is automatically generated during the CI pipeline we run on GitLab, relevant lines are [here](https://github.com/example42/psick/blob/production/.gitlab-ci.yml#L251).

As they say: it's not ready until it's documented.

### How to use puppet strings in your puppet code?

Every class and define must start with the documentation prior class or define definition. Documentation is marked as comments using the hash character (#).

    # The demo setup class
    #
    # This is an example of using documentation in a class or define
    #
    # @summary this is the redered summary of the class or define
    #
    # @example Show how people can make use of the class
    #   include demo_setup
    #
    # @param prod [Boolean] This parameter describes the stage or maturity level
    #   of the application. This text is longer, so we use newline for
    #   readability
    # @param port [Integer] Port on which the demo_setup must run
    #
    class demo_setup (
      Boolean $prod = true,
      Integer $port = 1025,
    ){
      # Puppet code
    }

Strings can also render documentation from types and providers:

    Puppet::Type.newtype(:demo_setup) do
      desc <<-DESC
    The type for the demo_setup
    @example Show usage for the type
      demo_setup { 'application':
        prod => true,
        port => 8880,
      }
    DESC

      newparam(:prod) do
        desc 'Stage to run in'
        # ...
      end
    end


Alessandro Franceschi
