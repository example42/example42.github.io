---
layout: blog
title: Preparing for Tiny Puppet 1.0
---

[Tiny Puppet](http://github.com/example42/puppet-tp) is a Puppet module that abstracts application management.

It provides a set of Puppet defined types to manage installation and configuration of potentially any application on any Operating System (```tp::install```, ```tp::conf```, ```tp::dir```... ).

When Tiny Puppet was released Puppet 4 was still not available, so all its code is compatible with Puppet 3 (and actually also with Puppet 4 and Puppet 2). Yet the power of the future parser is undeniable so we started to make some Puppet 4 only versions of the main tp defines, adding a ```4``` suffix to them (```tp::install4```, ```tp::conf4```, ```tp::dir4```... ).

Now we are approaching the release 1.0 of Tiny Puppet and a relevant choice has to be done: should we keep on preserving old parser compatibility or jump hands and feet on the future (parser?)

We decided to jump, so starting from version 1.x the standard tp defines are going to be compatible only with Puppet 4. Puppet 3 compatible defines will have the ```3``` suffix (```tp::install3```, ```tp::conf3```, ```tp::dir3```... ), and, to ease migration on current codebase, they are already available.

So, summing up, the current version of tp (0.9.x) has this layout for defines:

    tp::install  # Works on Puppet 2, 3 and 4
    tp::install3 # Works on Puppet 2, 3 and 4, the same of of tp::install
    tp::install4 # Optimized for Puppet 4 (doesn't work on earlier versions)

When tp 1.x will be released, in mid November, we want to switch this naming as follows:

    tp::install  # Optimized for Puppet 4 (doesn't work on earlier versions)
    tp::install3 # Works on Puppet 2, 3 and 4 the same of tp::install from 0.x

The current code and documentation refer to the pre 1.x layout: this will be changed at 1.0.0 release.

If you are using Tiny Puppet 0.x and have Puppet 4 you have probably nothing to do, the new functions work as before, a few, rarely used,  parameters will be removed

If you have a Puppet 3 environment you should start to use defines with the 3 suffix (renaming functions like ```tp::conf``` to ```tp::conf3```), in order to be able to seamlessly upgrade to tp 1.x when released.

If you are still not using Tiny Puppet, give it a try. It can do a lot of useful things for you, and, we think it will be able to do much more with the powers of Puppet 4.
