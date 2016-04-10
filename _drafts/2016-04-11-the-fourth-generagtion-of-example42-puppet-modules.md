---
layout: blog
title: The 4th generation of example42 Puppet modules
---

We, as example42, have written Puppet modules for years and we started to release them to the public in 2009.

The [first generation of example42 Puppet modules](https://github.com/example42/puppet-modules/tree/1.0) introduced a set of features that were quite uncommon for the times:

  - Support of multiple OS, based on the params.pp pattern

  - Possibility to remove (decommission) the resources managed by the module

  - Abstraction and automation of firewalling and monitoring

  - Awesome, out of the box (but optional) integration with Puppi 1.0

The reference layout of this first generation was done in pre-Puppet 2.6 times, when there weren't parametrized classes and the modules ecosystem was basically a collection of OS specific recipes.

With Puppet 2.x many things changed and modules' classes could finally have parameters that allow much wider customizations. At the [beginning of 2012](http://www.example42.com/2012/01/03/the-next-generation-of-example42-puppet-modules/) we started to release our [second version](https://github.com/example42/puppet-modules/tree/2.0) of modules, the *NextGen* edition. They were far more advanced and featured:

  - Alternative ways to manage configurations (templates, static files... )

  - Extreme customization options (for example it was possible to manage Puppet Enterprise with the normal OSS puppet module, handling all the different packages names and paths)

  - A standard parameters set, common across modules

  - Better separation of custom site code from module

  - The params_lookup() function, provided by the Puppi module, which anticipated the behavior of Puppet 3's Hiera data bindings and actually permitted even more flexible lookup options.

The soft dependency on the Puppi module (just for the presence of the params_lookup function), and the concept that having a whole modules set didn't mean that you had to take them all or nothing, have been points that we failed to explain properly.

In this occasion we started to have independent git repos for each module and the main [puppet-modules](https://github.com/example42/puppet-modules) one linking them as submodules.

We wanted also to introduce support for Puppi 2 and we failed, since Puppi 2 was never finished.

Still I think we provided a solid set of modules which have been used for years with several different Puppet versions, 4 included, and, I like to think, has in some parts influenced some design patterns on other modules.

In the meantime the modules ecosystem was getting better and better and it was impossible for a single person, mostly working on his free time, to deliver quality comparable to the best modules around.

It started a somehow decaying phase, where Puppet and its modules continued to grow, but work on Example42 modules became stale: the NextGen modules were starting to feel their age.

We tried to [change this tendency](http://www.example42.com/2013/09/27/talking-about-evolution/) opening an example42 [GitHub organisation](http://www.example42.com/2014/10/13/example42_goes_org/) and having Maintainers taking care of specific modules.

We wanted to start to work on a [third generation](https://github.com/example42/puppet-modules/tree/3.0) of modules where we wanted to get rid of the params_lookup dependency (since it was somehow redundant having Puppet 3 data bindings) and have a more modern layout. We tried also to launch the [stdmod initiative](https://github.com/stdmod) hoping the help introducing some naming standards in Puppet chaotic modules world.

StdMod and this third generation never really took off, most of its modules are still based on the 2.0 layout and we failed to support properly our community and contributors.

In the meantime we started to work on [Tiny Puppet](http://www.tiny-puppet.com) which somehow embodies all the standard features of our modules in a single module and allows far more ambitious evolutions.

So we arrived at these times, with an aged set of modules (most of them were designed even before the release of Puppet 3, four years ago), lack of proper motivation to support them, and better alternatives around.

We took some big decisions for our fourth generation of Puppet modules:

  - We deprecated a huge amount of modules. You can use Tiny Puppet or other modules to manage the relevant applications.

  - We changed radically the repository layout: from a collection of submodules to a Puppet **control-repo** with a Puppetfile, local site profiles, hiera data, a Vafgrant environment for testing the same local code and everything you need to setup from scratch a reliable, flexible and well structured Puppet infrastructure. To be honest the whole controlrepo code was taken from another project of ours, but we plan to improve and optimise it.

Work has just begun, a modules set is developed over time. Most of the current modules are still in their "NextGen" layout and all of them should work on Puppet 2, 3 and 4.

We are considering how to evolve: if to follow the backwards compatibility we always wanted to preserve, in terms of supported Puppet versions, or if to drop completely Puppet 3 support and design the new versions of the modules using the most advanced techniques that come with the Future parser.

In the next months we will see how this generation evolves and I have reasons to believe that it will be luckier than the previous also because something has changed in the meantime: there a company behind example42, not only a single person.

Per Aspera ad Astra

Alessandro Franceschi
