---
layout: blog
title: Tip of the Week 8 - Using Puppet Resource References the right way
---

    class phpmyadmin {
      package { 'phpmyadmin':
        ensure  => present,
        require => Service['apache'],
      }
    }

What is wrong with this code?

You have build a hidden dependency between the phpmyadmin class and the class which declares the Apache Service resource.

Why is this bad?

You can never use the class phpmyadmin standalone. The phpmyadmin class should be a Technical Component Class which can be used alone or in any other combination of classes. Besides this: you are forcing the users of your class to have phpmyadmin running on Apache webserver only.

How should this be done right?

Use local Resource References.

    class phpmyadmin {
      package { 'phpmyadmin':
        ensure => present,
      }
    }
    class apache {
      service { 'apache':
        ensure => running,
      }
    }
    class profile::phpmyadmin {
      contain apache
      contain phpmyadmin
      Class['apache'] -> Class['phpmyadmin']
    }

You can check your code for non-local Resource References by using the lint extension [reference_on_declaration_outside_of_class-check](https://github.com/voxpupuli/puppet-lint-reference_on_declaration_outside_of_class-check).

Martin Alfke
