---
layout: blog
title: Puppet 4 - Examples - Data Types
---

Puppet 4 has some new functionality. Within the next few blog posts I will give some examples on how to use the new functionality.
The first post covers the new Data Type system.

Let's assume that you want to have a parameterized ssh class where users of your module might choose whether the server side should be installed.

    class ssh (
      $server = true,
    ){
      ...
      if $server {
        ...
      }
      ..
    }


And now we use the module:

    class { 'ssh':
      server => 'false',
    }

In this example Puppet will verify the String 'false' which will result in a boolean value of 'true'.
This is not what we expected.

To avoid further misuse of the module we can add Data Types:

    class ssh (
      Boolean $server = true,
    ){
      ...
      if $server {
        ...
      }
      ...
    }

If we now use the same class declaration from above we will receive the following error message:

    Error: Expected parameter 'server' of 'Class[Ssh]' to have type Boolean, got String at ssh.pp:2 on node puppetmaster.example.net

What Data Types are available?

Puppet has Core Data Types and Abstract Data Types.

The Core Data Types are the following:

    String
    Integer
    Float
    Numeric
    Boolean
    Array
    Hash
    Regexp
    Undef
    Default

Integers are identified by a number (with or without minus sign) and no decimal point.

    Integer $var1 = 1
    Integer $var2 = -3 

Floats are identified by having a decimal point

    Float $var3 = 1.0
    Float $var4 = 0.2

Please note that you need to provide the trailing 0

Most of the other Data Types explain themselves.

The Default Data Type is something special:

The Default Data Type can be used in case statements and selectors:

    $real_server = $server ? {
      Boolean => $server,
      String  => str2bool($server),
      Default => true,
    }

Besides specifying the Data Types one can also specify Ranges of validity:

    class ssh (
      Integer[1,1024] $listen_port = 22,
    ){
      ...
    } 
    
This will check that $listen_port is set to an Integer value within 1 and 1024 and will fail if the boundary limits are not met.

The Abstract Data Types are the following:

    Scalar
    Collection
    Variant
    Data
    Pattern
    Enum
    Tuple
    Struct
    Optional
    Catalogentry
    Type
    Any
    Callable

One will mostly use Abstract Types which are built upon other Data Types.

e.g. you want to express the Data Types of the content of an Array or an Hash:

    class ntp (
      Array[String] $ntp_servers = ['pool.ntp.org'],
    ){
      ...
    }

A more complex example which takes a hash map:

    $hash_map = {
      'ben'   => {
        uid   => 2203,
        home  => '/home/ben',
      },
      'jones' => {
        uid   => 2204,
        home  => 'home/jones',
      }
    }
    
    class usermanagement (
      Hash[String, Struct[{ uid => Integer, home => Pattern[/^\/.*/]}]] $hash
    ) {
      $keys = keys($hash)
      $keys.each |$single_key| {
        users::define{ $single_key:
          uid  => $hash[$single_key]['uid'],
          home => $hash[$single_key]['home'],
        }
      }
    }
    
    define users::define (
      Integer          $uid,
      Pattern[/^\/.*/] $home,
    ){
      notify { "User: ${title}, UID: ${uid}, HOME: ${home}": }
    }
    
    class { 'usermanagement':
      hash => $hash_map,
    }

In case that one would like to allow certain words only, the Enum Data Type can be easily used:

    class ssh (
      Enum['*','::1','127.0.0.1'] $listen_ip = '*',
    ){
      ...
    } 

The Optional Data Type describes parameters which can be set to undef.

The next posting will cover Puppet 4 functions. 
