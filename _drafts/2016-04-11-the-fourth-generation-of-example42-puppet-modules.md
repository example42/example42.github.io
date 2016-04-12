---
layout: blog
title: The 4th generation of example42 Puppet modules
---

Example42 Puppet modules have been around since 2009, they have lived different generations.

It's time for a new one, the 4th generation. Almost a revolution.

Let me give an historical perspective.

The [first generation of example42 Puppet modules](https://github.com/example42/puppet-modules/tree/1.0) introduced a set of features that were quite uncommon for the times:

  - Support of multiple OS, based on the params.pp pattern

  - Possibility to remove (decommission) the resources managed by the module

  - Abstraction and automation of firewalling and monitoring (Optional)

  - Awesome (IMHO) integration with Puppi 1.0 (Optional)

The reference layout of this first generation was done in pre Puppet 2.6 times, when there weren't parametrized classes and the modules ecosystem was basically a collection of OS specific recipes.

With Puppet 2.x many things changed and modules' classes could finally have parameters that allow much wider customizations. At the [beginning of 2012](http://www.example42.com/2012/01/03/the-next-generation-of-example42-puppet-modules/) started the release of the [second version](https://github.com/example42/puppet-modules/tree/2.0) of modules, the *NextGen* edition. They were far more advanced and featured:

  - Alternative ways to manage configurations (templates, static files, whole dirs... )

  - Extreme customization options (for example it was possible to manage Puppet Enterprise with the normal OSS puppet module, handling all the different packages names and paths)

  - A standard parameters set, common across modules

  - Better separation of custom site code from module

  - Use of skeletons for quick creation of full featured modules

  - The params_lookup() function, provided by the Puppi module. Used for each class parameter. It partly  anticipated the behavior of Puppet 3's Hiera data bindings and actually permitted even more flexible lookup options.

In this occasion independent git repos for each module were introduced and the main [puppet-modules](https://github.com/example42/puppet-modules) repo linking them as submodules.

Support for Puppi 2 was introduced, but ultimately failed, since Puppi 2 was never finished.

NextGen modules have been used for several years, across different Puppet versions and, I like to think, have in some parts influenced some design patterns in other modules.

In the meantime the modules ecosystem was getting better and better and it was impossible for a single person, mostly working on his free time, to deliver quality comparable to the best modules around.

It started a somehow decaying phase, where Puppet and its modules continued to grow, but work on Example42 modules became stale: the NextGen modules were starting to feel their age.

With the intention to [change this tendency](http://www.example42.com/2013/09/27/talking-about-evolution/) it was opened an example42 [GitHub organisation](http://www.example42.com/2014/10/13/example42_goes_org/) with different maintainers taking care of specific modules.

The plan was to work on a [third generation](https://github.com/example42/puppet-modules/tree/3.0) of modules without the params_lookup dependency (since it was somehow redundant having Puppet 3 data bindings) and have a more modern layout. It was launched the [stdmod initiative](https://github.com/stdmod) with the intention of introducing naming standards in Puppet chaotic modules world.

StdMod and this third generation never really took off, most of the modules are still based on the 2.0 layout and I personally failed in supporting properly the community and the contributors on GitHub.

In the meantime it was started the work on [Tiny Puppet](http://www.tiny-puppet.com) which somehow embodies all the standard features of example42 modules in a single module based on an external data module, where it's easy to add support for new OS and applications.

So we arrive at current times, with an aged set of modules (most of them were designed even before the release of Puppet 3, four years ago), lack of proper motivation to support them, and better alternatives around.

Time to take radical decisions for our fourth generation of Puppet modules:

  - A huge amount of modules have been deprecated. For specialized tasks there are better alternatives around, for common package, service, files management Tiny Puppet can do the same.

  - The repository layout has been overhauled: from a collection of submodules to a Puppet **control-repo** with a Puppetfile (with Example42 and third party modules), sample local roles and profiles, sample Hiera data

  - Vagrant and (soon) Docker environments are added to the repo for testing Puppet code and data.

  - The repository is now more suitable as a starting, point for a flexible and decently structured Puppet infrastructure.

Work has just begun, a modules set is developed over time. Most of the current modules are still in their "NextGen" layout and all of them should work on Puppet 2, 3 and 4.

We are considering how to evolve: if to follow the backwards compatibility we always wanted to preserve, in terms of supported Puppet versions, or if to drop completely Puppet 3 support and design the new versions of the modules using the most advanced techniques that come with the Future parser.

In the next months we will see how this generation evolves and I have reasons to believe that it will be luckier than the previous also because something has changed in the meantime: there a company behind example42, not just a single person.

Per Aspera ad Astra

Alessandro Franceschi
