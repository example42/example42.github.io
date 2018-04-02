---
layout: blog
title: Tip of the Week 66 - Example42 Puppet modules status update
---

A quick update on the status of example42's Puppet works.

We released our [first set](https://github.com/example42/control-repo-archive/tree/1.0) of Puppet modules ten years ago, in 2008, at Puppet 0.24 times, looking at them now I can't prevent from smiling slighly embarassed: they had some unique features for the times (decommissining support, multi OS support by design, first attempt to separate common code from local implementation) but look definitively naive now.

Two years later, in 2010, when current Puppet version was 2.6, we released our [Next Gen](https://github.com/example42/puppet-modules-nextgen) set of modules, a completely rewritten army of modules with a somehow revolutionary feature: each class parameter value was looked up by the ```params_lookup``` function, which looks for values on Hiera and top scope variables. Note this was done before the release of Puppet 3 and automatic data binding on Hiera.

The ```params_lookup``` function is provided by the [puppi](https://github.com/example42/puppi) module, which is therefore required in the modulepath (but you don't need to include it). The modules had also optiona dependency of our monitor and firewall modules, to automatically manage monitoring and firewalling of the managed applications. All this has probably contributed to the wrong idea, which I heard too often around, that these modules couldn't be cherry picked but had to be taken as a whole set. Well, that' not true, all you need to use any nextgen module is the module itself and puppi in the modulepath.

Next Gen modules had several other feautures aimed to improve their reusability: parameters to define and override almost any variable used for package and service names, file paths, permissions and so on, parameters to control how to provide configuration files (as templates or sourced static files), and a lot of other common features (modules were generated from a common blueprint and then customised for the relevant application).

Those modules still mostly work now on Puppet 5 (minor fixes might be necessary in some parts) and are basically most of the current example42 ones you see on the [forge](https://forge.puppet.com/example42).

Also, most of them are currently deprecated: we are not actively working on them, for years, and receive and accept PRs to fix issues or ensure support on latest Puppet versions.

Even if they mostly do their work, we would not recommend them anymore: our suggestion for migration is either to choose a more updated module from other authors or enter the Tiny Puppet / PSICK world (more details later on this)

Some of the modules designed at "NextGen" times (problems with names like this is wondering what comes after the "next" gen...) are still supported and maintained either directly by Example42 of by some other mainteiners. The most relevant ones are apt, yum, puppi and the network module.

The latter is actually the reason I'm writing this post: my personal view on the module is somehow erratic, even if it's currently the only example42 Puppet module with the "Approved" label (when Puppet introduced Approved modules we were already deprecating most of our ones), I've given little attention and love to it for years, to the point that at some point I wanted to look for external maintainers and, in case no one were found, even deprecate it.

Some comments and discussions ([here](https://github.com/example42/puppet-network/pull/214#issuecomment-377794933) and [here](https://github.com/example42/puppet-network/issues/222)) on GitHub have forced us to reconsider this decision.

The network module might be the only reason you know example42 and maybe the only example42 module you are using, despite our past efforts on dozens of, now deprecated, modules and the current one on unconventional modules that most people probably don't understand or consider useful ([tp](https://github.com/example42/puppet-tp) and [psick](https://github.com/example42/puppet-psick)).

So we decided to keep on maintaining the network module and actually dedicate it much more time and resources than in the past.

Here's a short list, to sum up what is our current stance on the Puppet modules we have written and our plans for them:

- [network](https://github.com/example42/puppet-network). We'll keep on supporting it, with more effeort than in the last years. Short term goal is to improve documentation and flush PRs and tickets, longer term is to evaluate how to upgrade it (module comes from the "nextgen" era, it has been adapted to avoid puppi dependencies but it's still based on old Puppet language). It's working on all Puppet versions from 2.x to latest.

- [puppi](https://github.com/example42/puppi) has not received support for years but still does its job. It has 3 main functions:

  - provide the params_lookup function, which is now used only on the deprecated nextgen modules (but still works on Puppet 5)
  - provide shell commands to check the status of the managed applications (```puppi check```, ```puppi log```, ```puppi info```), which are now ideally replaced by Tiny Puppet commands (```tp test```, ```tp log```)
  - provide Puppet defines and shell commands to manage deployment of applications using different workflows defines in Puppet language (```puppi deploy $app```, ```puppi rollback $app```). We find this functionality still valid and somehow underrated (in the IT shop when puppi was written 8 years ago, it's still successfully used to seamlessly deploy hundreds of different applications) and in the future we might consider the opportunity to write a new puppi version which concentrates only on applications deployments.

- Other Example42 modules on the forge and GitHub. They are all deprecated (there's a deprecation notice at the beginning of the README) or maintained by third party supporters. We might give some support to them, especially the most used ones, in terms of possibility to run on recent Puppet versions and OS, but we still consider them a dead end, as they are already replaced by much more modern PSICK profiles.

- [tp](https://github.com/example42/puppet-tp). Tiny Puppet, coupled with PSICK module or used in your profiles, can replace ALL the old example42 modules. We are not actively working on new Tiny Puppet features as it currently does all we need. The companion [tinydata](https://github.com/example42/tinydata) module, with data for different applications on different OS is regularly updated with new or fixed data. We plan to keep on using them in the foreseeable future.

- [psick](https://github.com/example42/puppet-psick). Psick, the module, the [control-repo](https://github.com/example42/psick) and the separated sample [hieradata module](https://github.com/example42/psick-hieradata) is currently where we concentrate most of our Puppet developments. If you want to have an idea of how, in 2018, we design our Puppet infrastructures, give it a look and, please, before judging or dismissing it be sure to understand it ;-)

Finally, after years of solitary development (believe it or not, besides external contributions coming via PRs, most of the development of *all* these modules was done by me in slices of spare time), as example42 we have decided to dedicate more resources to the maintenance of our public Puppet works.

So if you are an example42 user and/or know and possibly like what we do, and want to be paid for development of our Open Source modules, contact us, we have a lot of work to do and are in the condition of involving more people on it.

Alessandro Franceschi
