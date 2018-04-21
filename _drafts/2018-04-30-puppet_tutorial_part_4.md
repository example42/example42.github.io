---
layout: blog
title: Tip of the Week 70 - example42 Puppet Tutorial - Part 4
---

### example42 Puppet Tutorial - Part 4

This is the fourth post of a series of articles covering an introduction to Puppet.

In the [first post](https://www.example42.com/2018/04/09/puppet_tutorial_part_1/) I started with Puppet agent installation and how to use Puppet and Facter to analyze your system. Next topics have been the introduction to the Puppet programming language (DSL), how to setup the central Puppet master and how to connect Puppet agents to the Puppet master.

The [second posting](https://www.example42.com/2018/04/16/puppet_tutorial_part_2/) covered cover Puppet modules, code logic and variables and how to add external facts to your systems. Besides this I introduced parameters and the concept of separating code and data by using hiera.

Th [third part](http://example42.com/blog) explained how to make use of upstream Puppet libraries when describing your own infrastructure, how to best classify nodes and where to place the code.

In this posting I will combine what I have shown and explain how to make use of the example42 [PSICK control repository](https://github.com/example42/psick.git), the [PSICK module](https://github.com/example42/puppet-psick.git) and the [PSICK hieradata](https://github.com/example42/psick-hieradata).

* Table of content
{:toc}

#### The PSICK Control Repository

Yes, you can start from scratch, with an empty control-repository. I wonder why you want to take the burdon to do everything by yourself when there is already Open Source work which you just need to adapt to your infrastructure.

The [PSICK control repository](https://github.com/example42/psick.git) contains:

- Puppet node classification
- Unit and acceptance tests (rspec-puppet, beaker)
- CI/CD integration (GitLab, Jenkins, Travis, Danger)
- Developer support (editorconfig, Vscode, RuboCop, Codacy)
- Setup automation (Hardware, Vagrant, Fabric, Docker)

Your main starting point is `manifests/site.pp` here you check for trusted facts variables, set defaults for different operatingsystems, manage the noop mode and classify all nodes using the [example42 PSICK puppet module](https://github.com/example42/puppet-psick.git).

Next important file is hiera.yaml - the environment level hiera configuration file. Here you see that data and data management is split into two different repositories. The main reason is that we see data management changes as dangerous. Whith this setup you can provide different access to data.
Besides this you learn that we have enabled hiera-eyaml from scratch.
***Please note that you must create your keys:***

    pushd /etc/puppetlabs/puppet
    /opt/puppetlabs/puppet/bin/eyaml createkeys
    popd

Next you want to verify whether our provided default hierarchies can also be used on your platform. (This is the list from most generic to most specific)

- Common
- Zone
- Zone-stage
- Nodes

#### The PSICK Module (Library)

Within the PSICK module you will find an infrastructure library based on [example42's tiny-puppet](http://tiny-puppet.com/) and many standard Puppet modules.
Next you will see modules which are used by specifc profiles.

Please note that we use profiles only from the [Roles & Profiles pattern](https://puppet.com/docs/pe/latest/r_n_p_full_example.html).

In the module main class (`init.pp`) we provide parameters for global PSICK settings (e.g. noop mode and first_run), then you will find information regarding your management network. Last parameter block (general endpoints and variables) is used for your infrastructure and stages.

At the end of the file you will see the verification for first_run. If this is not needed or already done, you will see three contain functions for three different deployment levels:

|Level|Description|
|---|---|
|Pre|prepare system, e.g. network, repositories,...|
|Base|basic setup, mail, ssh, sudo, logging, ntp,...|
|Profiles|the usecase for the system, e.g. webserver, db, loadbalancer, imap, CI server,...)|

Here you might want to review, whether everything you need is already there. You only need to add your own implementation profiles to the control repository.

#### The PSICK hieradata

As you have ssen, we fully rely on hiera config v5 (Data in Modules, Data in Environments).

Basically everything can be enabled or disabled and configured by changing hieradata only. Try to stick to this pattern as long as possible.

Start writing your own production code after you have understood Puppet Modules, Profiles and PSICK well enough to ensure good code stability and maintainability.

Martin Alfke
