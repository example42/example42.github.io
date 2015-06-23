---
layout: blog
title: Rethinking modules - Part 1
tags: puppet, modules, standardization, higher abstraction
---

I'm somehow obsessed by Puppet modules, it must be a rare syndrome, and I hope self awareness is the first step towards its cure.

I've passed years developing modules, trying to find ways to make them useful, usable and reusable. Most of the times I wrote them while working on specific Puppet projects, trying to figure out how they could be used in different circumstances. 

I've redefined my opinions on how to design them over time, following the evolution of Puppet, the best practices of the moment, the feedback I received from other users and my own personal experience.

I have to say that I'd definitively do things in different ways if I had to start from scratch, now.

I'd dare to say that I would not write almost any of the 91 modules published on the [Forge](https://forge.puppetlabs.com/example42) and the, even more, present on [Github](https://github.com/example42). Their maintenance cost is simply unbearable for the spare time of a single person, even with the great contributions from a lot of people.

Something has to change. This post, divided in two parts, is about how Puppet modules might change. At least **my** Puppet modules.

On this first part I'm going to express my opinion on some points:

- What are the reusability features a module should have
- The distintion between application modules and higher abstraction modules
- What are the challenges and reusability options for higher abstraction modules

### Modules reusability features

I've tried to figure out what could be the features a module should have in order to be considered reusable. I might be a bit extreme on this point, but according to me a reusable module should provide:

- Support for different Operating Systems
- By default deploy a neutral setup, honoring the underlying OS default settings
- Support for different configuration approaches, such as:
  - Complete files provided as ERB templates ( ```content => template($template) ``` ) 
  - Complete files from a fileserver ( ```source => puppet:///modules/... ``` )
  - Single lines in files managed by **Augeas** or other settings based defines
  - Files built assembling fragments with **concat**
  - Complete configuration directories
- Support for different usage behaviors, such as:
  - Option to decide if configuration changes should trigger services restarts or not
  - Options to activate debug or audit modes
  - Options to provide custom classes, to be used as alternatives to the default subclasses, to manage dependencies or components of the module
- Support for custom names and paths for the managed resources (Package and Service name, files paths, and so on)
- Support for alternate installation options (via native packages, upstream sources and so on)

Many of these features were introduced in the Example42 NextGen modules, using different modules blueprints: full featured templates for the generation of different kind of applications' modules.

I'd consider these the common reusability features a module should have: a shared baseline that any great reusable module should have.

Then there are all the other application specific resources and features that can be added and can help in making users' life easier and the module more accomplished.

For example we can have custom types and defines that manage single elements of an application, such as: ```apache::vhost``` or ```mysql::grant```, or classes that configure specific components of the module.

Also, in many cases, the module's classes expose parameters that allow the configuration of specific application settings. These parameters are generally used in ERB templates to shape configuration files as needed or to configure the application's components, behavior or relationship with other applications and services.

The kind and amount of such custom parameters may vary, a lot.

My current opinion is that besides, eventually, some very core, useful and basic parameter for specific applications (For example: ```syslog_server``` , ```dns_servers```) it should be enough to expose a single parameter where users can provide a hash with any specific configuration setting the application may have. Such a hash should be used with a proper template to manage any kind of configuration.

The benefit is clear, we preserve the possibility to manage our infrastructure via bare data, without the need to add and update the module's classes with application specific parameters.


### Higher abstraction modules

Application modules (also called "component" modules) should follow a Single Responsibility Principle, dealing only with resources directly related to the managed application.

Still in our infrastructures we have many applications that interoperate and have to be configured to reflect a consistent setup which involves different configurations for different applications to be assembled together. 

The Roles and Profiles pattern is an example of how we can work at a higher abstraction layer, using different component modules to setup whole stacks of applications which may run on separated systems.

I think that application modules should not be opinionated, at least in their default functionalities.
They should provide resources to manage different configuration needs, without enforcing any specific implementation. An application module should be considered as a library, an interface to the configuration of the underlying application. Something that does just a specific thing and it does it well, in a predictable way.

So, by default, a component module should just install the relevant application and start it's service, where present, with default settings. It should then offer a simple to use, coherent and robust interface to the application configuration. Such as the reusability features outlined previously.

On the other hand, a higher abstraction module, has to be opinionated. It must provide a working setup, so it has to manage files and configurations in some specific way, as decided by the author.

This is what many have done for a long time in their infrastructures: component modules, either public or written locally, have been used by custom internal "site" classes, where we've managed the composition of the services provided to the nodes of the infrastructure.

In some cases public, shared, modules where forked and modified locally, in other cases people (rightly, IMHO), have preferred to keep unaltered in a dedicated directory these public modules.

Sometimes a component module wants to do too much, and tries to manage resources related to other applications, which are needed for a complete and working setup. Here is where the Single Responsibility Principle is broken and the distinction between component and higher abstraction modules gets blurred.

The reason is that just recently the difference from component and higher abstraction modules, such as profiles, has started to be defined.


### Reusable higher abstraction modules

Up to know we have not seen may public examples of profile modules that can be adapted to different cases.

How much flexibility such a module might offer depends exclusively on the author's ambition to widen alternative options of his module.

Let's see an example of an higher abstraction module.

A Wordpress module is a (apparently simple) case. It's the typical borderline case, as it should just install WordPress, but in order to provide a working setup we have to configure the component modules of Apache, Php and Mysql in a very precise way managing Mysql grants, Apache virtualhosts and Php settings.

Here, we should actually have two different modules:

- The component module, that just installs and configures WordPress
- The higher abstraction module, that manages the whole infrastructure needed to provide a WordPress site.

Let's concentrate on the latter. Such a module, or class, might expose parameters that allow to set high level settings (virtualhost names, database credentials...) but it has to be opinionated on the setup, from the same core choice on the web server and database backend to use, to content of the actual configuration files delivered.

To offer better reusability options, it might expose parameters to manage which component to use, for example allowing users the option to use Nginx and PostgreSQL, instead of Apache and MySQL. It also could allow the possibility to compose the deployment of its various components on different, separated, servers and eventually add features to manage reverse proxies, load balancers or caching servers. 

All such reusability options definitively augment the complexity of the module to a point that we might question if it's worth the effort.

Still at least some composition options are just needed, an example of a wordpress profile that installs all its components on a single server might be useful for training purposes but is almost useless in a modern, mid size, setup.

I hope to see sooner or later some examples of reusable profiles. To test and validate the idea (reusability, composition on multiple servers) I've make this, essential, [logstash stack](https://github.com/example42/puppet-stack/blob/master/manifests/logstash.pp) which is actually in production on at least a site.

Besides the specific implementation, I think that a reusable higher abstraction module should provide:

- Support for different Operating Systems, where possible
- By default a working setup, based on opinionated choices about what components to use and how to configure them
- Support for alternate templates. For each application for which a configuration file is managed via a template, users should be able to provide their own alternative one
- Parameters that allow configuration of high level settings
- Optional support for monitoring and firewalling classes, with the possibility for users to override the default classes for these tasks, if present
- Optional support for different components (for example: different web servers, database backends and so on)
- Compositioning options, that allow users to install the needed components on different nodes adapting to different infrastructures.

The last point is particularly important as is the key for real reusability and, at the same time, introduces new challenges that raise the complexity of the module and opens new questions on the module's usage patterns.

I think that what is still missing, in the current Puppet modules' ecosystem, are two fundamental points:

- Patterns to extend reusability of higher abstraction layer modules (as described in this post)
- Standardization in the component application modules

I suppose and hope we will see proposals and suggestions on how reusability patterns will be extended to higher abstraction modules, maybe clarifying the naming (here sometimes I talked about "reusable profiles", even if profiles, as originally described in Craig Dunn's post, are not so similar to the reusable abstraction modules discussed here).

As for the second point, a possible approach on how to face the standardization of the component modules, or even rethink the whole concept of component modules, is going to be presented in the second part of this post. 
