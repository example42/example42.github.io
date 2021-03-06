---
layout: blog
title: Tip of the Week 25 - Control Repo documentation
---

The current method to manage documentation in Puppet code is based on [puppet strings](https://github.com/puppetlabs/puppet-strings).

We can install it as a gem:

    puppet resource package puppet-strings provider=puppet_gem

and then, from within the main directory of a module we can generate the module documentation just by running:

    puppet strings

Puppet strings uses [Yard](http://yardoc.org), a Ruby Documentation Tool that parses comments with defined @tags in the code and creates documentation based on them.

For example,we can document a class by adding lines as the following at the beginning of its manifest:

    # @summary This class manages the general hardening of a system.

    # The class provides, as params, the names of the classes to include in
    # order to manage specific hardening activities.
    #
    # @example Define all the available hardening classes. Set a class name to an
    #          empty string to avoid to include it
    #   profile::hardening::pam_class: '::profile::hardening::pam'
    #   profile::hardening::packages_class: '::profile::hardening::packages'
    #   profile::hardening::services_class: '::profile::hardening::services'
    #   profile::hardening::tcpwrappers_class: '::profile::hardening::tcpwrappers'
    #   profile::hardening::securetty_class: '::profile::hardening::securetty'
    #   profile::hardening::network_class: '::profile::hardening::network'
    #
    # @param pam_class Name of the class to include to manage PAM
    # @param packages_class Name of the class where are defined packages to remove
    # @param services_class Name of the class to include re defined services to stop
    # @param securetty_class Name of the class where /etc/securetty is managed
    # @param tcpwrappers_class Name of the class to include to manage TCP wrappers
    # @param network_class Name of the class where some network hardening is done

There are various tags which Yard automatically detects and uses to compose documentation, here is the [full list](http://www.rubydoc.info/gems/yard/file/docs/Tags.md#List_of_Available_Tags), the most used for Puppet are:

  - @summary - A brief summary of what the class does
  - @param <param_name> - The description of what  parameter does. Puppet strings automatically detects the accepted Type for the param (if set in the class) and the default value (currently the default value is not shown if we use data in module and values are set in hiera's Yaml files)
  - @example - To should usage examples. Outour will be shown in a monospaced font.
  - @return - In functions, defines what the function returns.

Puppet strings can parse and create documentation for manifests (classes, user defines, functions in Puppet DSL), types and providers, and any piece of ruby code in our files.

The use case for a single module shown before generates the documentation for that module files and uses the README.md one as content for the main page.

When we want to generate documentation for a whole control repo, we need to pass some more options. If we have our local modules in the ```site``` directory and we want to generate documentation only for them, we can run a command like:

    puppet strings generate site/**/**/*{.pp\,.rb} site/**/**/**/*{.pp\,.rb}

This can generate something like the [PSICK documentation](http://puppet.pages.lab.psick.io/psick/) that we automatically generate in our PSICK Puppet CI pipelines.

It's possible to use files different than README.md as text for the main page (in the above case the same README.md file used by puppet strings is generated by composing different [fragments of documentation](https://github.com/example42/psick/tree/production/docs)), to have the output in different formats and to customise Yard in various ways.

To specify extra options for documentation generation we have two alternatives:

  - Use the provided [rake task](https://github.com/puppetlabs/puppet-strings#rake-tasks)
  - Add a ```.yardopts``` file to the main directory of the control-repo. Check [here](https://rubydoc.tenderapp.com/kb/getting-started-with-rubydocinfo/setting-up-a-yardopts-file) for further info.

Documentation is always a multi facets giant to face, when we write code: We hate to write it, but still we want it when we need it and we want it to be complete and updated.

At the same time it take time to write it, it takes time to keep it updated and it's really hard to make it complete, easy to follow and fitting for different kind of users with different knowledge.

If it's written in a dedicated, separated place (a Wiki, a document file somewhere, an email(!?)... ) it's probably doomed to become obsolete a few days after it has been written. Having in code comments that can be used to generate contextual, "live" documentation is a pattern present is practically any language.

We have it on Puppet too, it's flexible and nice enough to be worth using and, staying where the code stays, it can help us in making it updated and current.

Generating it for the whole control-repo, instead of a single module, during the delivery pipeline of our Puppet code base is just a simple step which we can add while putting together the different dots that draw our Puppet infrastructure.

Alessandro Franceschi
