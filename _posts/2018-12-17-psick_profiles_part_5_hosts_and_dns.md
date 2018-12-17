---
layout: blog
title: Tip of the Week 102 - Psick profiles. Part 5 - Managing /etc/hosts and DNS
---

Our tour of the ready to use profiles of the psick module continues this week with management of DNS entries for the resolver, and of the content of /etc/hosts file.

These are the previous posts of this series:

- [Part 1 - Overview](https://www.example42.com/2018/11/12/psick_profiles_part_1_overview/){:target="_blank"} of the psick module and its reusable profiles.

- [Part 2 - Proxy and Hostname](https://www.example42.com/2018/11/19/psick_profiles_part_2_proxy_and_hostname_settings/){:target="_blank"} settings with psick profiles.

- [Part 3 - OpenSSH](https://www.example42.com/2018/12/03/psick_profiles_part_3_openssh/){:target="_blank"} settings, keys, configs management.

- [Part 4 - Users](https://www.example42.com/2018/12/10/psick_profiles_part_4_users/){:target="_blank"} management.


## Managing /etc/hosts

Psick module provides 3 different classes to manage the contents of `/etc/hosts`:

- `psick::hosts::file`: Manage /etc/hosts via a file resource

- `psick::hosts::dynamic`: Manage /etc/hosts dynamically using exported resources

- `psick::hosts::resource`: Manage /etc/hosts content via Puppet native `host` resource type

### Using `psick::hosts::file`

This class just manages /etc/hosts as a file, you can customise the template to use for the content of this file and an array of entries to add to it.

To use this approach, just classify your nodes with with profile:

    include psick::hosts::file

Then it can be configured via Hiera with the following settings:

The erb template to use to manage the content of /etc/hosts (default value is `psick/hosts/file/hosts.erb`):

    psick::hosts::file::template: profile/hosts/hosts.erb

The ip address (default is the value of `$::psick::primary_ip` which defaults to the fact `$::networking['ip']`), the short hostname (defaults to fact `$::hostname`) and the domain (defaults to fact `$::domain`) to use to identify the local node in /etc/hosts:

    psick::hosts::file::ipaddress: 10.12.13.14
    psick::hosts::file::domain: example42.com
    psick::hosts::file::hostname: my_server

An array of custom extra lines to add to `/etc/hosts` (default: []), each element of the array should contain the expected text in each extra line:

    psick::hosts::file::extra_hosts:
    - 10.12.13.15	puppet puppet.example42.com
    - 10.12.13.20	other_server other_server.example42.com

### Using `psick::hosts::dynamic`

This class manages /etc/hosts automatically and dynamically: each server managed by Puppet exports its own host entry (via Puppet `host` resource) and collects the ones of all the other nodes.

The class provides options to customise IP and alias to export for a node, if to actually export the host entry and a special "magic var" which can be used to divide nodes in different groups (within each group hosts' entries are exported and collected).

This class is alternative to the others, it requires Store configs enabled on the Puppet Server (so, consequently, the usage of PuppetDB in not too ancient setups) and can be used with a simple:

    include psick::hosts::dynamic

In small setups this could be enough to have /etc/hosts automatically managed with all the entries of all the nodes.

It's possible anyway to customise some entries. For example the ip address (default `$::ipaddress`) and the array of aliases (default `[ $::hostname` ] to use when exporting the local host's info):

    psick::hosts::dynamic::dynamic_ip: 10.12.13.14
    psick::hosts::dynamic::dynamic_alias:
      - my_server
      - my_server.example42.com
      - my_server_other_alias

It's also possible to control if and how to export and collect the node's host entry.

It's possible to set a string that allows to group together nodes: all nodes having this magic var set collect and export host resources only for nodes using the same magic var:

    psick::hosts::dynamic::dynamic_magicvar: intranet

If we don't want to collect in any place the host entry of a node we can set, for it (default value is false, so each node exports a valid and collectable host resource):

    psick::hosts::dynamic::dynamic_exclude: true

Since /etc/hosts entries are managed via exported `host` Puppet resources, it's also possible to specify an Hash of custom additional entries to add to the host file. This makes sense if we want to add references to hosts or devices not managed by Puppet. The syntax of the hash to use maps the available arguments of the host resource (`puppet describe host` for a full list):

    psick::hosts::dynamic::extra_hosts:
      firewall.example42.com:
        ip: 10.12.13.1
        target: /etc/hosts # (Default)
        host_aliases:
          - firewall
          - fw.example42.com
      san.example42.com:
        ip: 10.12.13.250
        host_aliases:
          - san


### Using `psick::hosts::resource`

This is the third alternative to manage /etc/hosts. It's just a wrapper that exposes an Hiera controllable entry point for Puppet `host` resource. This is alternative to the previous profiles and has to be classified as the others:

    include psick::hosts::resource

Configuration the is done via an Hash of hosts resources similar to what we have seen for `psick::hosts::dynamic::extra_hosts`:

    psick::hosts::resource::hosts:
      firewall.example42.com:
        ip: 10.12.13.1
        target: /etc/hosts # (Default)
        host_aliases:
          - firewall
          - fw.example42.com
      san.example42.com:
        ip: 10.12.13.250
        host_aliases:
          - san

## Managing DNS resolver.

To manage the contents of `/etc/resolver` you can use the `psick::dns::resolver` profile. Classify it with something equivalent to :

    include psick::dns::resolver

And then configure on Hiera both the template to use and its entries.

To manage the template to use (default is 'psick/dns/resolver/resolv.conf.erb') and the actual path of the resolver file (default is '/etc/resolv.conf'):

    psick::dns::resolver::resolver_path: /etc/resolv.conf
    psick::dns::resolver::resolver_template: profile/resolver/resolv.conf.erb

To manage the actual typical configuration settings of resolv.conf:

    psick::dns::resolver::nameservers:
      - 1.1.1.1
      - 8.8.8.8
    psick::dns::resolver::options:
      - attempts: 2
      - timeout: 2
      - rotate
    psick::dns::resolver::search:
      - example42.com
      - lab.example42.com  
    psick::dns::resolver::domain: example42.com
    psick::dns::resolver::sortlist:
      - 130.155.160.0/255.255.240.0
      - 130.155.0.0

That's all for today. As we have seen, for the most common use cases, on Linux systems, Psick provides ready to use profiles to manage the content of /etc/hosts and /etc/resolv.conf without the need of fetching dedicated modules.

Have fun with Puppet, Life, Universe and Everything.

Alessandro Franceschi
