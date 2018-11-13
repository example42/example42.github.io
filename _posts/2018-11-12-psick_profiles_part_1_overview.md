---
layout: blog
title: Tip of the Week 98 - Psick profiles. Part 1 - Overview
---

We have already talked in our blog about the PSICK project, both the [control-repo](https://github.com/example42/psick){:target="_blank"} and the [Puppet module](https://github.com/example42/puppet-psick){:target="_blank"}.

Here and in our next posts we will get deeper in how to use the reusable profiles of the Psick module.

## Prerequisites

Psick is a module you can get from the forge, if you install it form the command line all its dependencies are resolved:

    puppet module install example42-psick

When used inside a control repo, you need to explicitly state its dependencies in your Puppetfile:

    mod 'puppetlabs-stdlib', :latest
    mod 'example42/psick', :latest
    mod 'example42/tp', :latest
    mod 'example42/tinydata', :latest

In a production environment we will likely specify fixed and tested versions, the current latest version of the above modules are:

    mod 'puppetlabs-stdlib', :5.1.0
    mod 'example42/psick', :0.5.8
    mod 'example42/tp', :v2.3.1
    mod 'example42/tinydata', :v0.3.2

Some psick modules can support other third party component modules, refer to each psick class documentation for details on additional prerequisite modules.

## Usage

Once you have psick among your modules you can include any of its profiles using whatever method you have to classify nodes.

You have to include first the main psick class, which is safe and harmless as it does nothing by default but act as entrypoint for some common variables used by psick profiles.

Usage inside manifests then can be like:

    include psick
    include psick::<profile>

You can consider psick classes as reusable profiles: they have the characteristic of a profile as they wrap resources from other modules to accomplish specific functions, but they are conceived in a way that they can be reused and adapted to different (common) use cases.

You can cherry pick and use the ones you want instead of writing a custom profile (which might eventually need an additional component module and its dependencies) for every case where a psick profile fits your situation.

Usage of psick profiles is similar to the one of classes from existing modules: you classify nodes with the relevant class name, and then use hiera to configure it via it's parameters.

## Base and applications profiles

Psick comes with a wide like of base profiles for common settings, here are the most significant ones:

  - psick::hosts - Manage /etc/hosts
  - psick::motd - Manage /etc/motd and /etc/issue
  - psick::nfs - Manage NFS client and server
  - psick::sudo - Manage sudo configuration
  - psick::sysctl - Manage sysctl settings
  - psick::firewall - Manage firewalling
  - psick::openssh - tp profile and keygen define
  - psick::hardening - Manage system hardening
  - psick::network - Manage networking
  - psick::puppet - Manage Puppet components
  - psick::users - Manage users
  - psick::time - Manage time and timezones

There are also several other application specific profiles, where it's generally possible to choose what module to use to manage the actual application (if a popular public module or Tiny Puppet):

  - psick::ansible - Manage Ansible installation
  - psick::aws - Manage AWS client tools and VPC setup
  - psick::bolt - Manage Bolt installation
  - psick::docker - Docker installation and build tools
  - psick::foreman - Foreman installation
  - psick::git - Git installation and configuration
  - psick::gitlab - GitLab installation and config
  - psick::mariadb - Manage Mariadb
  - psick::mysql - Manage Mysql
  - psick::mongo - Manage Mongo
  - psick::php - Manage php and modules
  - psick::oracle - Manage Oracle prereq and setup
  - psick::sensu - Manage Sensu

## tp profiles

TP profiles in psick are profiles which are generated automatically, they all share the same structure (and parameters)  offering a consistent user interface. They, of course, use Tiny Puppet defines (tp::install and tp::conf) to manage the relevant applications.

All tp profiles in psick have names like ```psick::<app>::tp```, and are generated with pdk using this [template](https://github.com/example42/pdk-module-template-tp-profile).

You can generate a new tp profile, by running on the psick module:

    bin/bin/tp_profile.generate.sh nginx

will create the class `psick::nginx::tp`

On the upstream psick module, currently, only a [limited list](https://github.com/example42/puppet-psick/blob/master/bin/tp_profile_mass_update.txt) of application have their own tp profile. Feel free to request more application specific tp profiles.

TP encourages the usage of the template + options hash pattern, ad has some generic templates usable for common file structures. So, for example, to manage openssh with psick , we can:

    include psick::openssh::tp

by default a tp profile installs the relevant application but doesn't configure it. In order to manage configuration files you have to set parameters as follows (in this example we use a generic template where each key value of the options hash is written as `<key> <value>` which is a valid format for OpenSSH confiuration):

    psick::openssh::tp::resources_hash:
      tp::conf:
        openssh:
          template: 'psick/generic/spaced.erb'
          options_hash:
            Protocol: 2
            PermitRootLogin: 'no'
            Subsystem: 'sftp /usr/libexec/openssh/sftp-server'

Here, by including the ```psick::openssh::tp``` profile we have Openssh package installed and the relevant service started. We configure it using the ```resources_hash``` parameter, common in all tp profiles, where for each configuration file to manage via ```tp::conf```, or whole directories to manage with ```tp::dir```, we specify name, and content (by using parameters like ```source```, ```content```, ```template``` or ```epp```) and a custom ```options_hash``` where any parameter, referred in the used template, looked up in deep merge mode, can be managed via Hiera.

The whole logic of the tp profiles is to expose parameters that allow to directly configure tp defines via Hiera.

If you know exactly how to configure your application, and its setup is based on a standard package + configuration files + service pattern, then tp, either used within your profiles on via a psick tp profile, can be a solid alternative to the usage of a dedicated component module.

## Conclusion

This is the first post of a series about the profiles shipped with the psick module.

After this general introduction we are going, in the next posts, to see more details on how to use these profiles for common system configurations.

Alessandro Franceschi
