---
layout: blog
title: Puppet Evaluation Error. Error while evaluating a Resource Statement - Unknown resource type
---

So you got the **Error while evaluating a Resource Statement, Unknown resource type** with Puppet and are searching for solutions?

You are lucky, because right now we are going to see what it means, why it happens and how to solve it.

## TL;DR

The module that provides the referred Unknown resource type is not available where your Puppet code is compiled.

Find the module you need in the **metadata.json** file of the module where the code fails (use the provided path).

Solve by adding the module to your `Puppetfile`, or running the `puppet module install` command.


### Decomposing the "Unknown resource type" Puppet error message  [JUNIOR]

Your error message may look like (we are going later to see which parts can be different for you):

    Error: Could not retrieve catalog from remote server: Error 500 on SERVER: Server Error: Evaluation Error: Error while evaluating a Resource Statement, Unknown resource type: 'concat' (file: /etc/puppetlabs/code/environments/production/modules/openvpn/manifests/config.pp, line: 6, column: 5) on node lab.psick.io

Here's how to decompose it:

    Error: Could not retrieve catalog from remote server: Error 500 on SERVER: Server Error: Evaluation Error: Error while evaluating a Resource Statement 

This is your Puppet agent throwing an Error, saying that it was not able to get the catalog of the resources to apply from the server. Then it shows the server's 500 error related to problems while evaluating a resource statement in the code:

    Unknown resource type: 'concat' 

This is the specific message, where the 'concat' resource type can and will be different, and gives the key information for solving it: Puppet is looking for a resource type, here 'concat', and it doesn't find it.

    (file: /etc/puppetlabs/code/environments/production/modules/openvpn/manifests/config.pp, line: 6, column: 5)

Another key information: where Puppet failed to compile our code. In a normal client-server infrastructure, the file path is on the Puppet server's filesystem (path may be different, what matters is that this is the file to check). If you use the puppet apply command, there's no server involved and the path is local.
    
    on node lab.psick.io

This is your client node where Puppet agent was run.


### A few Puppet basic principles. [BEGINNER]

Puppet manages any kind of computer related item, it uses its own language, written in files like the /etc/puppetlabs/code/environments/production/modules/openvpn/manifests/config.pp of the above example, where we can declare what are the resources we want to manage on our system(s) (lab.psick.io).

Puppet is shipped with some core resource types like 'package', 'service', 'file', 'user', etc. We use them to manage, guess what, packages, services, files, and users on Operating Systems like Windows, Linux, MacOS. For example code as follows automates the installation of the nginx package and manages its service on any node where is used:

```puppet
    package { 'nginx':
      ensure => present,
    }
    service { 'nginx':
      ensure => running,
      enable => true,
    }
```

Puppet is used typically to automate the management of configurations on multiple servers or desktop systems, but can be used to manage virtually anything which is IT related: network devices, cloud resources, etc.

This is possible thanks to Puppet's extensible and modular structure.

Additional resource types can therefore be found in Puppet modules which are shared on sites like GitHub and on a public repository called the [Forge](https://forge.puppet.com).

Whatever the name, in Puppet language, we always declare a resource type with the following syntax:

```puppet
    resource_type { 'title':
      parameters,
    }
```

Our problem here is that in line 6 column 5 in the /etc/puppetlabs/code/environments/production/modules/openvpn/manifests/config.pp file on our server, we have a resource declaration like 

```puppet
    concat { '/etc/default/openvpn':
      owner => root,
      group => 0,
      mode  => '0644',
      warn  => true,
    }
```

that uses the resource 'concat' which is not available, because it's not a native resource type, shipped with puppet itself, and we don't have the module that provides the concat resource.


### How to solve Unknown resource type errors [JUNIOR]

The quick answer is to install the module that contains the resource type you are trying to use, and the quick way to find it is to look at the dependencies of the module which is using the missing resource.

Puppet modules can require other modules, in this case the 'openvpn' module on this example requires an additional module which provides the 'concat' resource.

The dependencies of every module are defined in the `metadata.json` file, at the root of the module directory, and indeed in our /etc/puppetlabs/code/environments/production/modules/openvpn/metadata.json we have the following:

    {
      "name": "puppet-openvpn",
      "version": "10.2.1",
      "author": "Vox Pupuli",
      [...]
      "dependencies": [
        {
          "name": "puppetlabs/concat",
          "version_requirement": ">= 4.1.0 < 8.0.0"
        },
        {
          "name": "puppetlabs/stdlib",
          "version_requirement": ">= 4.25.0 < 9.0.0"
        }
      ]
    }

The important information here is:

- we are using the module puppet/openvpn (Here 'puppet' is the user name on the Forge of the Vox Pupuli community of modules authors)
- This module depends on 2 additions modules: puppetlabs/concat and puppetlabs/stdlib, they are both from the 'puppetlabs' Forge user, which is the Puppet company itself) 

So, in order to use the puppet/openvpn module we also need the puppetlabs/concat and puppetlabs/stdlib modules.

### Some info about where Puppet code lives [JUNIOR]

In our example the missing resource is on the file `/etc/puppetlabs/code/environments/production/modules/openvpn/manifests/config.pp`, this whole path has a meaning and you need to know it if you work with Puppet:

- **/etc/puppetlabs/code/environments/** is the default value for the **$environmentpath** configuration entry. Where the different Puppet environments are stored.
- **production** is the name of a Puppet environment, the default value
- **modules** is the default directory where an environment stores its modules
- **openvpn** is the name of the module that contains the config.pp file
- **manifests** is the directory in every module, where we place our Puppet code in manifests: files with .pp extension written in Puppet Domain Specific Language (DSL).
- **config.pp** is the manifest with Puppet code where we declare the resource which failed.

So the metadata.json with info about the dependency modules is to searched at the root of our openvpn module: `/etc/puppetlabs/code/environments/production/modules/openvpn`.

The modules listed under "dependencies" in the metadata.json file are what we need and we need them in the right place, more precisely in the Puppet's **$modulepath** : a configuration entry which displays a colon-separated list of directories where Puppet searches for modules.

Oh, incidentally, you can show all Puppet's configuration entries with the command:

```bash
    puppet config print all
```

and the specific one that matters here, the modulepath, where Puppet looks for modules:

```bash
    $ sudo puppet config print modulepath
    /etc/puppetlabs/code/environments/production/modules:/etc/puppetlabs/code/modules:/opt/puppetlabs/puppet/modules
```

So all we need to do is to install the missing modules.

### Installing modules [JUNIOR]

We can install additional modules in various ways which depends on how is managed Puppet code on our systems.

#### Using the Puppetfile 

If we are using a Puppet server, it's likely and advisable that in your company you are managing the full content of the **/etc/puppetlabs/code/environments/** dir with r10k (in puppet Open Source) or Code Manager (in Puppet Enterprise), so you should never manually touch any file there: a deployment procedure, eventually driven by a CI/CD tool, will do it for you

In this case any new external module should be listed in your control-repo's Puppetfile.

The control repo is a single git repository which contains a Puppet environment.

When it is deployed by tools like r10k or CodeManager, commonly used in Puppet world, for each branch of the control repo a Puppet environment is created in the **$environmentpath**.

When an environment is deployed two things happen:

- The content of the control-repo relevant branch (for example production) is copied/synced to its **/etc/puppetlabs/code/environments/production** directory.
- The modules listed in the control-repo's Puppetfile are deployed under the **modules** subdir of the environment/branch: **/etc/puppetlabs/code/environments/production/modules**.

In the Puppetfile our missing modules can be added as follows:

    mod 'puppetlabs/concat', '7.2.0'
    mod 'puppetlabs/stdlib', '8.4.0'

The version names, and the actual syntax can be seen on the module's page on the Forge.

#### Using the puppet module install command

If you are using Puppet in apply mode, without any Puppet server involved, or (blames on you!) you manage your manifests directly, on your servers's /etc/puppetlabs/code/environments/ dir, you can install the needed modules by using the Puppet module command.

It automatically installs the latest version of the defined modules (using the format: forge_user/module_name or forge_user-module_name) and their eventual dependencies:

    $ sudo puppet module install puppetlabs/concat
    $ sudo puppet module install puppetlabs/stdlib

To list the installed modules use:

    $ sudo puppet module list

Note than while the puppet module install command automatically installs every dependency, you have to specify them all in the Puppetfile.


### Common cases of Unknown resource type errors and remedies [INTERMEDIATE]

So, I hope it's clear that any kind of Puppet Unknown resource type error can be solved by adding the missing module which provides the resource we are trying to use.

The best approach is just to check the dependencies in the metadata.json file as just described, but, if you are copying random code from the Internet or working with legacy modules without the metadata.json file to check, you may find useful the reference here.


As a reference, we list here some common resource types and the relevant modules which provide them, with an extra bit of information which is worth knowing.

| Resource Type | Module |
| --- | --- |
| concat | puppetlabs/concat |
| archive | puppet/archive |
| line_line | puppetlabs/stdlib |
| anchor | puppetlabs/stdlib |
| vcsrepo | puppetlabs/vcsrepo |
| ini_setting | puppetlabs/inifile |
| ini_subsetting | puppetlabs/inifile |
| firewall | puppetlabs/firewall |
| firewallchain | puppetlabs/firewallchain |

In Puppet 6.0 some built-in resource types have been moved to separated "core" modules. Normally you can ignore them as they are included in the puppet-agent package, still if you have a Unknown resource type error with any of the following resources, here are the relevant modules which provide them:

| Resource Type | Module |
| --- | --- |
| mount | puppetlabs/mount_core |
| augeas | puppetlabs/augeas_core |
| zfs | puppetlabs/zfs_core |
| zpool | puppetlabs/zfs_core |
| yumrepo | puppetlabs/yumrepo_core |
| host | puppetlabs/host_core |
| selboolean | puppetlabs/selinux_core |
| selmodule | puppetlabs/selinux_core |
| zone | puppetlabs/zone_core |
| cron | puppetlabs/cron_core |
| scheduled_task | puppetlabs/scheduled_task|
| sshkeys | puppetlabs/sshkeys_core |
| mailalias | puppetlabs/mailalias_core |
| maillist | puppetlabs/maillist_core |
| nagios_* | puppetlabs/nagios_core |

The puppetlabs/nagios_core module provides the following, previously built in, types: nagios_command, nagios_contact, nagios_contactgroup, nagios_host, nagios_hostdependency, nagios_hostescalation, nagios_hostextinfo, nagios_hostgroup, nagios_service, nagios_servicedependency, nagios_serviceescalation, nagios_serviceextinfo, nagios_servicegroup and nagios_timeperiod.
 
There is a set of modules which implement common types using the Augeas tool. They are the so called Augeas Providers:

| Resource Type | Module |
| --- | --- |
| pam | herculesteam/augeasproviders_pam |
| shellvar | herculesteam/augeasproviders_shellvar |
| ssh_config | herculesteam/augeasproviders_ssh |
| sshd_config | herculesteam/augeasproviders_ssh |
| sshd_config_subsystem | herculesteam/augeasproviders_ssh |
| sshd_config_match | herculesteam/augeasproviders_ssh |
| sysctl | herculesteam/augeasproviders_sysctl |
| kernel_parameter | herculesteam/augeasproviders_grub |
| grub_config | herculesteam/augeasproviders_grub |
| grub_menuentry | herculesteam/augeasproviders_grub |
| grub_user | herculesteam/augeasproviders_grub |
| mounttab | herculesteam/augeasproviders_mounttab |
| pg_hba | herculesteam/augeasproviders_postgresql |
| syslog | herculesteam/augeasproviders_syslog |
| syslog_filter | herculesteam/augeasproviders_syslog |
| syslog | herculesteam/augeasproviders_syslog |
| puppet_auth | herculesteam/augeasproviders_puppet |
| nrpe_command | herculesteam/augeasproviders_nagios |
| apache_directive | herculesteam/augeasproviders_apache |
| apache_setenv | herculesteam/augeasproviders_apache |


If you use Puppet to manage Windows, you might need these resources and modules:

| Resource Type | Module |
| --- | --- |
| registry_key | puppetlabs/registry |
| registry_value | puppetlabs/registry |
| reboot | puppetlabs/reboot |
| dsc | puppetlabs/dsc_lite |
| acl | puppetlabs/acl |
| chocolateysource | puppetlabs/chocolatey |
| chocolateyfeature | puppetlabs/chocolatey |

As a general reference, if the missing resource type has a double colon in its name, (like: apache::vhost), then the name of the module HAS to be the first part before the double quotes (apache). Next problem would be to find the right apache module from the Forge, and that can take some time if it's not referenced in the metadata.json file.

If you bumped into code which is using example42's revolutionary Puppet modules, be aware of the following:

| Resource Type | Module |
| --- | --- |
| tp::install | example42/tp |
| tp::conf | example42/tp |
| tp::dir | example42/tp |
| tp::dir | example42/tp |
| tp::test | example42/tp |
| tp::info | example42/tp |
| psick::* | example42/psick |

* Any defined resource type (also called define) from the psick module, there are quite a few: psick::puppet::access, psick::puppet::module, psick::puppet::set_external_fact, psick::netinstall, psick::yum::repo, psick::yum::plugin, psick::rclocal::script, psick::profile::script, psick::sudo::directive, psick::network::route, psick::network::routing_table, psick::network::set_lo_ip, psick::network::interface, psick::network::rule, psick::network::validate_gw, psick::network::netplan, psick::network::netplan::interface, psick::bolt::project, psick::limits::limit, psick::limits::config, psick::nfs::export, psick::nfs::mount, psick::openssh::keypair, psick::openssh::keyscan, psick::openssh::keygen, psick::openssh::config, psick::systemd::unit_file, psick::java::install_tarball, psick::services::init_script, psick::services::systemd_script, psick::archive, psick::users::managed, psick::aws::cli::script, psick::git::config, psick::php::module, psick::php::pear::module, psick::php::pear::config, psick::sysctl::set, psick::chruby::gem, psick::tools::create_dir, psick::tools::gpgkey, psick::kmod::module.

## Conclusions

Hope this has been useful, thanks for reading. Let me know if you like similar posts on Puppet errors, I might do more of them.

If you need quick support for any Puppet related error or problem, just contact me via the link in the top right: if the solution is quick (as it would be the one for an error like this), it'll be without any cost or obligation.

If it's Puppet related, I know I can help, and I'm glad to.

Alessandro Franceschi

Twitter: @alvagante
GitHub: @alvagante
