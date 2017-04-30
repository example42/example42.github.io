---
layout: blog
title: Tip of the Week 18 - Puppet debugger
---

Deep in its core, Puppet holds arcane codes that might be hard to understand.

We usually don't need to grasp Puppet inners in our daily activities, but at times it's necessary to explore what hides under the hoods.

[Puppet Debugger](https://github.com/nwops/puppet-debugger) by Corey Osman is a great tool that can help us whenever we need to get deeper in Puppet wonderlands.

We can install it as gem:

    gem install puppet-debugger

If Puppet is not installed, it's installed as a gem dependency, in the local user ruby environment. We can enter the Puppet debugger console running:

    puppet debugger

If Puppet is already installed, typically via a system package, you might have issues (I had), with the above command, probably due to mismatching library paths.

Once in the console, various commands are available:

    Ruby Version: 2.0.0
    Puppet Version: 4.10.0
    Puppet Debugger Version: 0.6.1
    Created by: NWOps <corey@nwops.io>
    Type "exit", "functions", "vars", "krt", "whereami", "facts", "resources", "classes",
         "play", "classification", "types", "datatypes", "benchmark",
         "reset", or "help" for more information.

So, we can start to play around, for example, by querying available info. Starting from facts:

    1:>> facts

    {
     "architecture"              => "x86_64",
     [...]
    }

The full local list of local facts is shown. Nothing new you can rightly say, but that's just the beginning, we can get the list of variables available in the scope:

    1:>> vars
    "Facts were removed for easier viewing"
    {
     "facts"        => "removed by the puppet-debugger",
     "module_name"  => "",
     "name"         => "main",
     "server_facts" => {
      "environment"   => "production",
      "serverip"      => "172.17.0.1",
      "servername"    => "lab.psick.io",
      "serverversion" => "4.10.0"
     },
     "title"        => "main",
     "trusted"      => {
      "authenticated" => "local",
      "certname"      => nil,
      "domain"        => nil,
      "extensions"    => {},
      "hostname"      => nil
     }
    }

Starting to be interesting eh? Now, there's more. Based on the modules available in the modulepath we can get the list of available functions, both puppet core ones and the ones from the modules.

    1:>> functions
    archive::artifactory_sha1
    archive::assemble_nexus_url
    archive::go_md5
    inifile::create_ini_settings
    noop::noop
    puppet-4.10.0::alert
    puppet-4.10.0::assert_type
    [...]
    stdlib::abs
    stdlib::any2array
    [...]

A list of the available datatypes, also the ones defined in modules:

    1:>> datatypes
    [
      [ 0] "Any",
      [ 1] "Array",
      [...]
      [41] "Stdlib::Unixpath",
      [42] "Stdlib::Windowspath",
      [...]
      [47] "Tp::Settings",
      [...]
    ]

A list of the Puppet types, both native and from modules:

1:>> types
    [
      [  0] "stage",
      [  1] "file",
      [  2] "exec",
      [...]
    ]

Things get even more interesting when you consider that the context in which puppet debugger operates when you lauch it is determined by ```modulepath``` and ```environmentpath``` Puppet variables. If you have your control repo in the environmentpath, or a link to it, you can gen a list of the classes that would be provided to your local node (this is possible when node classification is managed directly in the control-repo and is not delegated to an External Node Classifier):

    1:>> classes
    [
      [ 0] "settings",
      [ 1] "tools",
      [ 2] "profile::settings",
      [ 3] "profile::pre",
      [ 4] "profile::repo::generic",
      [...]
    ]

Even more intriguing is the list of the resources that you be applied to your node:

1:>> resources
Resources not shown in any specific order
[
  [ 0] "Stage['main']",
  [ 1] "Class['Settings']",
  [ 2] "Class['main']",
  [ 3] "Class['Tools']",
  [...]
  [15] "File['/usr/local/bin/facter']",
  [...]
]

Note that this information is relevant to the local node, based on the Puppet code in the default environment and the modulepath, but we can run Puppet debugger and get information about a third node.

In order to do this we should either run Puppet debugger on the Puppet Master or do it via a development workstation, as long as we set (either in puppet.conf or on the command line) the name of the Puppet server and we have locally the same code base we have on the server.

    puppet debugger -n node.my.domain

Finally, another neat feature of Puppet debugger is the benchmark command, which allows to evaluate how much time Puppet takes for its operations. For example, to see the performance of a function:

    1>> benchmark
    2:BM>> lookup('profiles',Array,'unique',[])
     => "Time elapsed 0.86 ms"
    3:BM>> tp_lookup('apache','settings','tinydata','merge')
     => [
      [0] {
             "conf_dir_path" => "/etc/httpd/conf.d",
          "config_dir_group" => "root",
      [...]
                  "tcp_port" => "80"
      },
      [1] "Time elapsed 29.73 ms"
    ]

It's possible to launch an instance of Puppet debugger directly inside a manifest, this allows to query the above info having as scope exactly what's available at in a specific part of a manifest.

In order to launch Puppet debugger on real code, we need the ```debug::break``` function from [nwops/puppet-debug](https://github.com/nwops/puppet-debug) module.

We can introduce in our code the function::

    class 'apache' (
     [...]
     ) {
       [...]
       debug::break({'run_once' => false})
     }

When the debug::break function is found, the compiler is interrupted, a Puppet debugger instance is opened, it has access to all the local scope variables (just type a $variable name to see its value), it shows where in the code the function has been called, and, it allows to skip to the next break function found during the catalog compilation.

Puppet debugger gives powerful insights on our Puppet code and how and where is evaluated and definitively deserves it place in the essential toolset of every Puppet engineer.

Alessandro Franceschi
