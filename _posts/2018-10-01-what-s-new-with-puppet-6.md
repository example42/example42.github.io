---
layout: blog
title: Tip of the Week 92 - What's new with Puppet 6
---

Puppet 6 has been released the 18th of September, Eric Sorenson announced the [new release](https://puppet.com/docs/puppet/6.0/release_notes.html) in [this blog post](https://puppet.com/blog/introducing-puppet-6).

This is a new major release because it contains some enhancements which are not backwards compatible, but for most of the cases they won't require you to do any major review of your Puppet code base: if it works with Puppet 4 it's likely to work also on Puppet 6.

Let's see what are the most interesting new features.

* Table of content
{:toc}

## [Backwards Incompatibility] Several types moved to dedicated modules

This is a long awaited cleanup: all the Nagios types, and some other [OS specific ones](https://puppet.com/docs/puppet/6.0/type.html#deprecated-types) are no more part of the core product or have been moved to modules.

Most of them are still shipped in the puppet-agent package, others are in maintained modules not included in the puppet agent and some have been moved to modules and been deprecated.

More precisely, the following types are included in supported modules on the forge and repackaged in puppet-agent, so nothing changes for end users:
`augeas cron host mount scheduled_task selboolean selmodule ssh_authorized_key sshkey yumrepo zfs zone zpool`.

These other types have been moved to module which are still supported by are not included in Puppet agent package, so if you use them you should add the relevant modules from the Forge: `k5login mailalias maillist`.

These types have been deprecated, they are moved to modules which are not going to be actively maintained and are not shipped with puppet-agent package: `computer interface macauthorization mcx router vlan` plus all the `nagios_*` types (all moved to [puppetlabs-nagios_core](https://forge.puppet.com/puppetlabs/nagios_core) module).

In general all the moved types are now placed in a puppetlabs module with `_core` suffix. Look here for a [rough list](https://forge.puppet.com/modules?utf-8=%E2%9C%93&page_size=25&sort=rank&q=core).

The core modules shipped with Puppet-agent are placed under `/opt/puppetlabs/puppet/modules` on \*nix and `$codedir/modules` on Windows, these paths are added to the default `basemodulepath` setting.

## [Backwards Incompatibility] New CA management on the puppetserver

Puppet CA support has been rewritten in Clojure and included in the puppetserver package, the old CA Ruby code has been removed. The new `puppetserver ca` command has been introduced to replace the previous `puppet cert` and `puppet ca` commands.

The `puppetserver ca` actions to manage certs are similar to the old `puppet cert` ones. Available actions are:

- `clean`: clean files from the CA for certificates
- `generate`: create a new certificate signed by the CA
- `setup`: generate a root and intermediate signing CA for Puppet Server
- `import`: import the CA’s key, certs, and CRLs
- `list`: list all certificate requests
- `revoke`: revoke a given certificate
- `sign`: sign a given certificate

## Puppet ssl command

The `puppet ssl` command has been introduced. It replaces `puppet certificate_request` (use `puppet ssl submit request`) and add subcommands like `puppet ssl verify` (verifies that local Puppet cert and key are valid) and `puppet ssl download_cert` (downloads a certificate for the local node).

## The Resource API

A [Resource API](https://puppet.com/docs/puppet/6.0/create_types_and_providers_resource_api.html) has been added, providing a new, recommended method to create custom types and providers. The Resource API is built on top of Puppet core and is easier, faster, and safer than the old types and providers method.

Writing new Puppet providers based on the Resource API is even simpler by using the `pdk new provider` commands with the puppet Development Kit.

Check the [reference](https://puppet.com/docs/puppet/6.0/about_the_resource_api.html) for more details.

## The "Deferred" data type

This is a quite interesting and long awaited feature. Up to now the sanest method to do something on the client based on some client's condition was to create a custom fact and use it as needed in the Puppet code.

The `Deferred` data type allows to call **Ruby** functions directly from the client before the catalog is applied (they are usually evaluated on the server). This is possible only with Ruby functions as they are already shipped to the client with pluginsync.

So it's now possible to write some special function in our modules (under `lib/puppet`) that we want to run on the client.

One of the expected use cases is to [support secret lookups](https://tickets.puppetlabs.com/browse/PUP-8711) at catalog application time via tools like Consul and Vault.

## Functions imported from stdlib

Some [functions](https://puppet.com/docs/puppet/6.0/function.html) from the Puppetlabs-stdlib module have been moved to core:

- the getvar() function has been moved from stdlib, a new get() one has been introduced.

- the sort() function has been moved from stdlib to core and now accepts a lambda for custom comparisons

- the mathematical functions abs(), ceil(), floor(), round(), min(), and max() are compatible with homonymous stdlib ones with the added feature to use a lambda with a custom compare.   

- upcase(), downcase(), capitalize(), camelcase(), lstrip(), rstrip(), strip(), chop(), chomp(), and size() and been moved to core and updated to the modern function API.

- New compare() function.

## Command puppet module build removed

The `puppet module build` command has been removed. To build and package modules [PDK](https://puppet.com/docs/pdk/) should be used.

## Conclusions

This is a list of the most important changes with Puppet 6, in our opinion.

As you have seen they are mostly related to consolidation, cleanup and enrichment of the language and the platform.

Upgrade from Puppet 5 is expected to be safe and painless for most of the cases. If you are using any of the types which have been moved to separated modules which are not shipped with puppet-agent, you will have to add them by yourself to your module path.

Thanks to David Schmitt from Puppet for the remarks about some incorrect statements in the first revision of this post.


Alessandro Franceschi
