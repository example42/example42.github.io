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

### puppetmodule.info

Yard can act as a server and show directly the html pages generated. There's a web site which relies on this and show Puppet strings based documentation for most of the Puppet public modules on the Forge and GitLab.

Give a visit to [www.puppetmodule.info](http://www.puppetmodule.info), site created by Dominic Cleal from The Foreman team.

Here you can see the documentation for virtually any module you will find yourself using, the site is able to generate on request the documentation for modules it hasn't yet processed.

So on this site you can look how documented modules [appear](http://www.puppetmodule.info/modules/example42-psick) and search modules and contents as needed.

### Control repo documentation

In [Psick](https://github.com/example42/psick) we use Puppet strings also to generate the documentation of the whole control-repo.

[This](http://puppet.pages.lab.psick.io/psick/) is Psick's puppet strings generated documentation (it includes README with merged texts from the psick control-repo and the classes and defines from the psick module). It is automatically generated during the CI pipeline we run on GitLab, relevant lines are [here](https://github.com/example42/psick/blob/production/.gitlab-ci.yml#L251).

As they say: it's not ready until it's documented.

Alessandro Franceschi
