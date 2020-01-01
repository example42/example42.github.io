---
layout: blog
title: Tip of the Week XX - Hiera nested lookups
---

The Puppet data backend (hiera) allows you set data for site specific differences in your infrastructure.

For example you can have multiple datacenters where DNS, NTP, SNMP and backup are different, or you have a development stage which uses a different database server than the production stage.

Usually you check your infrastructure for differences and then use Facter data to build layers of Hiera data.

But what if you need the same data in several hiera keys?

Fot example you want to set the db connection settings like user/password for databases and webservers.

This is where we can make use of nested hiera lookups.

* Table of content
{:toc}

## Hiera nested lookups

Hiera lets you run an additional hiera lookup inside of hiera data.

This allows you to specify shared information once only, instead of adding the same information several times:

An example:

    profile::app::db::auth
      'app1':
        user: 'app1'
        password: '$\.fgeetd'

    profile::app::web::auth:
      'app1':
        user: 'app1'
        password: '$\.fgeetd'


## The "lookup" and "hiera" lookup

Instead of managing the same information on several places, we can ask hiera to run another lookup to fetch the required data:

    profile::app::db::auth
      'app1':
        user: "%{lookup('app1_user')}"
        password: %{lookup('app1_user_pass')}"

    profile::app::web::auth:
      'app1':
        user: "%{lookup('app1_user')}"
        password: %{lookup('app1_user_pass')}"

    app1_user: 'app1'
    app1_user_pass: '$\.fgeetd'

Instead of "lookup" you can also specify "hiera".

Please note that "lookup" and "hiera" nested lookups will only return string based values.

If you specify a non existing key, hiera will fail and return an error.

You can have multiple layers of nested lookups. That means that you run a lookup on a key, which does again run lookup.

You have to be aware that Hiera will fail, if you build loops. Hiera will detect these and return an error.

## The "alias" lookup

What if you don't need string, but other data types like boolean, array or hash to be returned by a nested lookup?

In this case you can use the "alias" lookup:

    profile::app::db::default_packages: "%{alias('default_packages')}"

    profile::app::web::default_packages: "%{alias('default_packages')}"

    default_packages:
      - 'tree'
      - 'net-utils'

Please note, that you can not add additional data to an "alias" lookup.

## The "literal" lookup

Consider the situation in which you donot like hiera to interpolate the percent (%) sign.

In this case you can use the "literal" lookup:

    profile::app::web::server_name_string: "%{literal('%')}{SERVER_NAME}"

This will return the value `%{SERVER_NAME}`.

## The "scope" lookup

The "scope" function interpolates variables.

The following two examples are identical:

    profile::app::web:stage: "%{facts.app_stage}"

    profile::app::web:stage: "%{scope('facts.app_stage')}"

As you also use the simple interpolation, the "scope" lookup is not really needed.

Happy hacking on hiera,
Martin Alfke

