---
layout: blog
title: Tip of the Week 72 - Puppet [custom] data types
---

One of the most powerful features introduced with Puppet 4 is the new type system.

For every variable or parameter in Puppet can be defined the type of data we can expect for it.

We typically use the type system to validate the kind of data expected for classes or defines parameters.

For example, Puppetlabs' ntp module has the ntp class which has parameters like these:

    class ntp (
      Boolean $broadcastclient,
      Stdlib::Absolutepath $config,
      Optional[Stdlib::Absolutepath] $config_dir,
      String $config_file_mode,
      Optional[String] $config_epp,
      Enum['running', 'stopped'] $service_ensure,
      Variant[Boolean, Integer[0,1]] $tos_cohort,
      ...

These few lines give us a good idea of how flexible the type system is, and how it can be extended and customised.

Besides the most common data types like:

- ```Boolean``` (matches a boolean value, either ```true``` or ```false```, without quotes otherwise they become Strings)
- ```String``` (matches any string)
- ```Hash``` (matches an hash (an unordered list of key values))
- ```Array``` (matches an ordered array of elements)
- ```Integer``` (matches a integer number)

Puppet has natively many more useful data types:

- ```Optional``` allows to accept a valid value (of the data type specified in square brackets) or an undef value.
- ```Enum``` accepts a list of strings, as defined, separate by comma, in the square brackets.
- ```Variant``` accepts different data types, separated by comma. In the above example a Boolean or an Integer from 0 to 1.

For a more extensive list of the native data types you can  heck the [official documentation](https://puppet.com/docs/puppet/5.5/lang_data.html).

In the above code fragment, we can see an "unusual" data type: ```Stdlib::Absolutepath```, this is a case of a custom data type, defined in the [stdlib](https://github.com/puppetlabs/puppetlabs-stdlib/blob/master/types/absolutepath.pp) module, under the path ```types/absolute.pp``` with content as follows:

    type Stdlib::Absolutepath = Variant[Stdlib::Windowspath, Stdlib::Unixpath]

What's nice here is that we can compose and use different data types, even custom ones (as ```Stdlib::Windowspath``` and ```Stdlib::Unixpath```) and ship them directly in a module.

For example, in our psick module we have created, under ```types/ensure.pp``` a ```Psick::Ensure``` data type which we use to manage the ensure parameter of a package resource, its content looks like:

    type Psick::Ensure = Variant[Enum['present', 'absent', 'installed','latest'],Pattern[/\d+(\.\d+)*/]]

This accepts either a string as defined in Enum, or a Regular expression matching version numbers.

Another interesting data type is ```Struct``` which allows to validate the type of each value of the keys of an Hash.

We use it in Tiny Puppet, to validate the list of settings which can be used to override an application's tinydata:

Here is is, as defined in tp module's [types/settings.pp](https://github.com/example42/puppet-tp/blob/master/types/settings.pp):

    type Tp::Settings = Struct[{

      Optional[package_name] => Variant[String,Array],
      Optional[package_ensure] => String,
      Optional[package_provider] => String,

      Optional[service_name] => Variant[String,Array],
      Optional[service_enable] => Boolean,
      Optional[service_ensure] => Enum['running', 'stopped'],

      Optional[process_name] => String,
      Optional[process_extra_name] => String,
      Optional[process_user] => String,
      Optional[process_group] => String,

      Optional[config_file_path] => Stdlib::Absolutepath,
      Optional[config_file_owner] => String,
      Optional[config_file_group] => String,
      Optional[config_file_mode] => String,

      Optional[config_dir_path] => Stdlib::Absolutepath,
      Optional[config_dir_owner] => String,
      Optional[config_dir_group] => String,
      Optional[config_dir_mode] => String,
      Optional[config_dir_recurse] => Boolean,

      Optional[log_file_path] => Stdlib::Absolutepath,
      Optional[pid_file_path] => Stdlib::Absolutepath,
      Optional[init_file_path] => Stdlib::Absolutepath,
      Optional[log_file_path] => Stdlib::Absolutepath,

      Optional[conf_dir_path] => Stdlib::Absolutepath,
      Optional[data_dir_path] => Stdlib::Absolutepath,
      Optional[plugins_dir_path] => Stdlib::Absolutepath,
      Optional[modules_dir_path] => Stdlib::Absolutepath,

      Optional[tcp_port] => Variant[String,Integer],
      Optional[udp_port] => Variant[String,Integer],

      Optional[nodaemon_args] => String,
      Optional[dockerfile_prerequisites] => String,

      Optional[package_prerequisites] => Array,
      Optional[tp_prerequisites] => Array,
      Optional[exec_prerequisites] => Hash,
      Optional[exec_postinstall] => Hash,

      Optional[repo_package_url] => String,
      Optional[repo_package_provider] => String,
      Optional[repo_url] => String,
      Optional[repo_namel] => String,
      Optional[key] => String,
      Optional[key_url]=> String,
      Optional[include_src] => String,

      Optional[apt_repos] => String,
      Optional[apt_key_server] => String,
      Optional[apt_key_fingerprint] => String,
      Optional[apt_release] => String,
      Optional[apt_pin] => String,
      Optional[yum_priority] => String,
      Optional[yum_mirrorlist] => String,
      Optional[zypper_repofile_url] => String,

    }]

Note that each key an be optional (so the parameter passed can be an hash with any of the above keys) and must adhere to the defined type, either native or custom, like ```Stdlib::Absolutepath```.

We find the Struct type particularly useful when using the [templates + options hash pattern](https://www.example42.com/2014/10/29/reusability-features-every-module-should-have/).

Another very useful data type is ```Sensitive``` which, when used, hides the relevant value from being shown in reports and logs.

You can use it to manage single values (and avoid to see them in reports) or for whole files, when using the ```content``` argument for a file resource:

    file { '/etc/secret':
      content => Sensitive(template("${module_name}/secret.erb")),
    }

In this way even if the content of the file changes in a Puppet run, you won't see it and its diff with potential sensitive information.

There's a lot more to talk about data types, and it's definitively worth reading the official documentation and giving a look to the ones provided by [puppetlabs-stdlib](https://github.com/puppetlabs/puppetlabs-stdlib/tree/master/types) module, as they cover some quite common use cases (```Stdlib::Ip_address```, ```Stdlib::HTTPSUrl```, ```Stdlib::MAC``` to name a few).

Give a type to your data, it makes your code more robust and reliable.

Alessandro Franceschi
