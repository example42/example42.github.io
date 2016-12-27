---
layout: blog
title: Puppet 4 - Examples - Data in Modules
---

Puppet 4 has some new functionality. Within the next few blog posts I will give some examples on how to use the new functionality.

The [first post](http://www.example42.com/2015/09/09/puppet4-examples-data-types/) covered the new Data Type system.

The [second post](http://www.example42.com/2015/10/07/puppet4-examples-functions/) covered the new function API.

The [third post](http://www.example42.com/2015/12/20/puppet4-examples-epp-template/) was about the new EPP template engine.

This fourth post covers the topic of Data in Modules.


In Puppet 3 hiera was fully integrated.
With hiera you were able to use a built-in way of separating code and data.

Besides this Puppet has an automatic data binding. This means, that upon declaration of parameterized classes Puppet automatically queries hiera for all parameters in the class namespace.
This allows people to more easy make use of upstream component modules.

The only problem was within hiera hierarchies and the amount of data which were put into hiera.
With hierarchies one had to think about a proper hierarchy which fits platform setup and application stacks.
When it comes to the amount of data one had to think about a way of keeping data in an easy to manage, structured way.

To allow data in modules to work, one needs to set configuration parameters.
Depending on data location this needs to be done in different locations.

It is possible to specify a global data provider. This needs to be done in puppet.conf file

```
  environment_data_provider = <provider>
```

It is possible to have data not in modules, but in environments - this is most likely a similar approach compared to standard hiera data in environments. It is possible to specify either the same or a different data provider. This needs to pe put in environment.conf file
```
  environment_data_provider = <provider>
```

Besides this it is possible to specify a module individual data provider. Modules normally do not have configuration files. But modules should have a metadata.json file.
The following has to be put into metadata.json:

```
  "data_provider": "<provider>",
```

Within puppet 4 the following data provider exist:

1. hiera - hiera (v4) lookup
1. function - data function lookup

Data provider and data location can be combined.
This leads to the following set of possible data solutions:

1. data in environments - using hiera provider
1. data in modules - using hiera provider
1. data in environments - using function provider
2. data in modules - using function provider

First we are looking at Data in Environments used in combination with the hiera data provider.

The ```hiera``` data provider is very easy to use when one already has hiera data per environment.
You can identify this by looking at your hiera.yaml file datadir setting:

```
  :datadir: "/etc/puppetlabs/code/environments/%{environments}/hieradata"
```




Example (sshd_config):

    <% if $ssh::port -%>
    Port <%= $ssh::port %>
    <% else -%>
    Port 22
    <% end -%>
    <% if $ssh::listen -%>
    ListenAddress <%= $ssh::listen %>
    <% else -%>
    ListenAddress 0.0.0.0
    ListenAddress ::
    <% end -%>


The next posting will deal with several ways on how to upgrade to Puppet 4.
