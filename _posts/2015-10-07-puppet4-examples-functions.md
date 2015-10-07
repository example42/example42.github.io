---
layout: blog
title: Puppet 4 - Examples - Functions
---

Puppet 4 has some new functionality. Within the next few blog posts I will give some examples on how to use the new functionality.

The [first post](http://www.example42.com/2015/09/09/puppet4-examples-data-types/) covered the new Data Type system.

This second post covers the new Function API.

In Puppet 3 functions had limitation like

  - no type checking
  - unique naming required

Puppet 3 functions had to be placed in a module in ```lib/puppet/parser/functions```

This has changed in Puppet 4. Functions now live in ```lib/puppet/functions```

Inside this functions directory other subdirectories can be used, to provide namespaces for functions.

e.g. in module resolver:

    # lib/puppet/functions/resolver/resolve.rb
    Puppet::Functions.create_function(:'resolver::resolve') do
      ...
    end

This allows module specific functions with the same name as other functions (e.g. v3 functions from stdlib).

In fact this is not the same name. It is the same filename.

The resolve function should return the Puppet master fqdn in case no argument is given.

Hint: this functionality requires the `socket` gem.

We now extend the function:

    # lib/puppet/functions/resolver/resolve.rb
    require 'socket'
    Puppet::Functions.create_function(:'resolver::resolve') do
      def resolve
        Socket.gethostname
      end
    end

*Please note: the def uses the function short name without the namespace !*

With Puppet 3 we had to have multiple functions returning different data depending on the provided arguments.

With Puppet 4 we now have a possibility to check for arguments data type and execute according function parts only.

First we need to write dispatch definitions which will evaluate the given data type.

We will continue with the last example:

    # lib/puppet/functions/resolver/resolve.rb
    require 'socket'
    Puppet::Functions.create_function(:'resolver::resolve') do
      dispatch :no_param do
      end
      def no_param
        Socket.gethostname
      end
    end

Note that we now make use of the dispatch when running specific parts of the function.

One can have multiple dispatch sections e.g. for different data types.

We want to make use of this by adding tow more resolve calls:

  - when provided with an IP address, it should return the hostname
  - when provided with a hostname, it should return the IP address

Hint: This functionality requires the rubygem `resolv`.

    # lib/puppet/functions/resolver/resolve.rb
    require 'socket'
    require 'resolv'
    Puppet::Functions.create_function(:'resolver::resolve') do
      dispatch :ip_param do
        param 'Pattern[/^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/]', :ip
      end
      dispatch :fqdn_param do
        param 'Pattern[/^([a-z0-9\.].*$/]', :fdqn
      end
      dispatch :no_param do
      end

      def ip_param(ip)
        Resolv.getname(ip)
      end
      def fqdn_param(fqdn)
        Resolv.getaddress(fqdn)
      end
      def no_param
        Socket.gethostname
      end
    end

We now can make use of the function in a manifest:

    $localname = resolver::resolve()
    notify { "Without argument resolver returns local hostname: ${localname}": }

    $remotename = resolver::resolve('google.com')
    notify { "With argument google.com: ${remotename}": }

    $remoteip = resolver::resolve('8.8.8.8')
    notify { "With argument 8.8.8.8: ${remoteip}": }

When declaring a manifest with this code inside, the following result will show up:

    Notify[Without argument resolver returns local hostname: puppetmaster]
    Notify[With argument google.com: 216.58.216.142]
    Notify[With argument 8.8.8.8: google-public-dns-a.google.com]

This function now fully relies upon working DNS resolution.
One might want to add some sanity checks around the resolv and socket ruby code.

The next posting will cover Puppet 4 EPP template engine.

