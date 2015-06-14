---
layout: blog
title: Reusability features every module should have
---

The quality of Puppet modules is constantly increasing, for each relevant application there's a good module to manage it.

They may have different structures, feature sets, OS coverage and naming conventions (:-I) but most of the times the better modules around do their work.

Still, often, also in some of the most popular modules, I desperately miss a few basic features that would allow me to use them without being forced to make a local fork.

Whenever we have to modify a public module to adapt it to our needs, we have a reusability failure IMHO.

The good news is that a few very and easy to apply principles may improve dramatically our modules' reusability without the need of a local fork.

They are not rocket science, just common sense and more or less established patterns. Let's review them.


#### Expose a parameter to change the used templates. Always.

Wherever we use an erb template in our module to populate the content of a managed file, we should add a parameter that allows our users to provide their own custom template.

The reason is simple, in most of the cases we simply can't provide a fitting template for the configuration needs of everyone.

So, whenever we have in a module something like:

    file { '/etc/redis/redis.conf':
      content => template('redis/redis.conf.erb'),
    }

We can expose in the class or the define that contains this file declaration a parameter that allows customisation of the template.

For the above example, a quick, safe, and backwards compatible fix is as easy as:

    class redis (
      $config_file_template = 'redis/redis.conf.erb',
    ) {

      file { '/etc/redis/redis.conf':
        content => template($config_file_template),
      }
    }


#### Expose a parameter for a generic configuration hash

What and how many parameters should a module expose?

We may try to expose plenty of parameters to configure any possible configuration setting of our application, or we can expose only the "most important" ones, the ones that are more frequently changed, leaving room for ambiguity and arbitrary choices.

We can also expose a single parameter where users can pass an hash of custom and arbitrary data, for whatever usage they may think about.

Such a parameter is generally paired with the template one we have just seen.

Let's just add it to our class:

    class redis (
      $config_file_template = 'redis/redis.conf.erb',
      $options_hash         = { },
    ) {

      file { '/etc/redis/redis.conf':
        content => template($config_file_template),
      }

    }

Now our users can have (Hiera) data where they can define whatever they want:

    ---
      redis::config_file_template: 'site/redis/redis.conf.erb'
      redis::options_hash:
        port: '12312'
        bind: '0.0.0.0'
        masterip: '10.0.42.50'
        masterport: '12350'
        slave: true

The template to use for redis.conf is taken from a custom local site module (so no modification is needed on the "public" redis module) and in this template we can access the $options_hash variable.

A sample fragment of the file ```$MODULEPATH/site/templates/redis/redis.conf.erb``` might be like:

    port <%= @options_hash['port'] %>
    bind <%= @options_hash['bind'] %>
    <% if @options_hash['slave'] == true -%>
    slaveof <%= @options_hash['masterip'] %> <%= @options_hash['masterport'] %>
    <% end -%>

Users can actually provide any kind of data in such an hash, and use it in their templates as preferred. They can use it for application's configuration options, to manage triggers with booleans or to pursue any other purpose that fits their needs.

Is such a generic hash a catch all solution that might replace all or most parameters used only to populate the contents of our templates?

Well, eventually.

Let's look at the next step.


#### Provide defaults for the options_hash

I may understand the eyebrow of the module author reading this and wondering how to provide a working and useful setup out of the box with just a generic hash which is empty by default.

Actually what's empty can be filled with default values, exactly like the default values we place in parameters.

We can, for example, set default values in this way:

    class redis (
      $config_file_template = 'redis/redis.conf.erb',
      $options_hash         = { },
    ) {

    # Default configuration values  
      $options_defaults = {
        port     => '6379',
        bind     => $::ipaddress,
        slave    => false,
        timeout  => '0',
      }

      # We use the merge function from stdlib to override the defaults with users' values
      $options=merge($options_defaults, $options_hash)

    }

Now we can provide in our module a default configuration template that is highly customisable via the ```$options_hash``` parameter, with the extra benefit of providing good sample reference for users' custom templates.

Our module's ```$MODULEPATH/redis/templates/redis.conf.erb``` should, obviously, use the computed ```$options``` variable which is the result of the merging of users' data with our defaults:

    port <%= @options['port'] %>
    bind <%= @options['bind'] %>
    <% if @options['slave'] == true -%>
    slaveof <%= @options['masterip'] %> <%= @options['masterport'] %>
    <% end -%>

Now we have the best of two worlds:

- Very few parameters (two) are enough to set any configuration value for the managed application

- In our modules we can set default values that are used to provide sane and working configurations out of the box

- Module's users can manage any configuration element in their (Hiera) data. The level of detail is up to users and their needs.

Up to now we have seen how we can improve users' customisation of the content of the managed files.

Let's give a look to a final hint that can literally save our modules' integrity (in terms of possibility to be used without changes) in many situations.


#### Place extra resources in dedicated sub classes. Allow users to change them.

A few months ago I expressed my [opinions](http://www.example42.com/2014/05/31/rethinking-modules-part-1/) on the common ambiguity we currently have with Puppet modules about what they should and should not do.

This is basically due to a not clear distinction we make in application component modules, which are expected to be the single responsibility point to manage that application, and higher abstraction modules, like profiles and [stacks](https://github.com/alvagante/puppet-stack_logstash/blob/master/manifests/init.pp) (Stacks are an approach to higher level modules I started to use as an alternative to profiles).

What should a wordpress module do? Install only the wordpress files? Configure the webserver? Configure the backend database?

If we consider it a component module it should just download the wordpress code and eventually manage its configuration file. If we want to work at an higher level, it should configure the web frontend, the database credentials and make everything work out of the box.

This is the first thing that users expect from a module.

The second one is the ability to adapt the module to custom needs.

Often, authors, place resources that refer to some external application, in a dedicated subclass.

For example ```wordpress::apache``` might be used to configure apache as frontend, alternative to a ```wordpress::nginx``` or whatever. In these cases it's generally available a parameter that allows the choice of the webserver to use.

That's fine but I'd go further. For every subclass of a module, that groups resources somehow related to other modules, there should be a parameter that allows users to provide a custom version of that class.

Most of the modules dependencies conflicts can be solved with such an approach.

Let's see an example with something as easy as:

    class wordpress (
      $webserver_class = '::wordpress::apache',
    ) {

      if $webserver_class {
        include $webserver_class
      }
    }

Small note with Puppet 4 the above code would not work as expected if we set an empty string as value for ```$webserver_class```, a possible alternative could be something like:

    if $webserver_class
    and $webserver_class != '' {
      include $webserver_class
    }

If our users want to use a different implementation of Apache (they may use a different, not compatible, module) or a different webserver, they can simply provide the name of the class to use with data like:

    ---
      wordpress::webserver_class: '::site::wordpress::apache'

and define this class in the own site module, so have the file ```$MODULEPATH/site/manifests/wordpress/apache.pp``` with a content like:

    class ::site::wordpress::apache {
      # Anything needed to configure Apache as desired  
    }

This approach can be followed for other cases, for example, if we need to configure additional repositories to manage the installation of packages, we can con confine them in a dedicated class, or if we want to provide automatic firewalling or monitoring features with the module, we might place them in dedicated classes that allow our users to manage these features within their infrastructure.

I bet you have not read anything really new to you in this post, still there a lot of modules from expert authors that don't follow these simple patterns which are not expensive and intrusive (excluding the third point, which is somehow more opinionated an questionable).

So, if you write and publish public Puppet modules, do yourself, your users, and me a favour, embrace these suggestions, we will have all a better Puppet life.


Alessandro Franceschi
