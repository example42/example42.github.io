---
layout: blog
title: Tip of the Week 98 - Psick profiles. Part 2 - Setting proxy server and hostname
---

On the [first post](){:target="_blank"} of our series on Psick profiles we introduced the psick module and had an overview of its reusable profiles.

In this post we are starting to review some handy psick profiles:

- `psick::proxy` to configure proxy settings, on Linux system startup scripts, on gem and pip environments and in repo configurations for apt and yum

- `psick::hostname` to manage / enforce the system's hostname both on Linux and Windows


## Managing proxy settings with psick::proxy

To use it just include the class in your manifests (remember that):

    include psick::proxy

or classify with the ENC of choice.

Then, hiera configuration can be as follows:

    psick::proxy::proxy_server:
      host: proxy.example.com
      port: 3128
      user: john    # Optional
      password: xxx # Optional
      no_proxy:
        - localhost
        - "%{::domain}"
        - "%{::fqdn}"
      scheme: http   # 

If you have included the psick class, you can set the same values using the general psick::servers hash, as this is the default value for the psick::proxy::proxy_server:

    class psick::proxy ( [...]
      Optional[Hash] $proxy_server     = $::psick::servers['proxy'],
    [...]

The above example has the same effect of:

    psick::servers:
      proxy:
      host: proxy.example.com
      port: 3128

You can customise the components for which proxy should be configured, here are the default params:

Manage presence of proxy settings:

    psick::proxy::ensure: present

Configure proxy settings for system's gem environment:

    psick::proxy::configure_gem: true

Configure proxy settings for Puppet's gem environment:

    psick::proxy::configure_puppet_gem: true

Configure proxy settings for PIP environment:

    psick::proxy::configure_pip: true

Configure proxy settings for system. Exporting http_proxy variables in profile.d:

    psick::proxy::configure_system: true

Configure proxy settings on package management tool (yum and apt supported):

    psick::proxy::configure_repo: true


## Managing the hostname with psick::hostname

Another profile for common use cases is psick::hostname which manages the server's hostname both on Linux and Windows.

It allows to set or reinforce hostname, fqdn and domain in local system configuration files on Linux and Windows.

Class defaults are as follows:

    class psick::hostname (
      String                $host                 = $::hostname,
      Variant[Undef,String] $fqdn                 = $::fqdn,
      Variant[Undef,String] $dom                  = $::domain,
      String                $ip                   = $::ipaddress,
      Boolean               $update_hostname      = true,
      Boolean               $update_host_entry    = true,
      Boolean               $update_network_entry = true,
      Boolean               $update_cloud_cfg     = false,
      Boolean               $no_noop              = false,
    ) {

The update booleans have effect only on Linux and control where we want to set the hostname:

- On /etc/hostname and via the hostname command (`update_hostname`)

- With Puppet's host resource (`update_host_entry`)

- On /etc/sysconfig/network (only on RHEL derivatives) (`update_network_entry`)

- On /etc/cloud/cloud.cfg.d/99_preserve_hostname.cfg (requires cloud config) (`update_cloud_cfg`)

On Windows if $update_hostname is true and hostname is not the same configured, the `netdom renamecomputer` command is run.

Usage is the usual, include in manifests (ie: in role classes):

    include psick::proxy

Or via any other classification option you use.

Configuration via hiera can be as follows:

    psick::hostname::host: my_host
    psick::hostname::fqdn: my_host.my_domain
    psick::hostname::dom: my_domain
    psick::hostname::ip: "%{::ipaddress}"


These are two of the several psick profiles for common uses. They are less complete than dedicated modules but can do most of the expected work without the need of additional modules, other than psick, keeping the whole psick philosofy of giving choice on what profiles to use and what to configure with them.


Alessandro Franceschi
