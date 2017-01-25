---
layout: blog
title: Tip of the Week 6 - Resources from Hash Data in Puppet 4
---

Puppet is always about abstraction. But please never forget maintainability, readability and simplicity [(K.I.S.S)](https://en.wikipedia.org/wiki/KISS_principle).

Nowadays we often see code like the following:

    class my_great_thing (
      $data = {},
    ){
      $default = {
        ensure   => present,
      }
      create_resources('user', $data, $default)
    }

Great abstraction, but what happens really?

When declaring the class my_great_thing, puppet compiler will automatically do a hier alookup for the key ```my_great_thing::data```.

Maybe the key-value looks like this:

    my_great_thing::data:
      'foo':
        home: '/home/foo'
        shell: '/bin/bash'
        uid: '1044'
        gid: '1044'
      'bar':
        home: '/home/bar'
        shell: '/bin/bash'
        uid: '1045'
        gid: '1045'

These data are not used with the ```create_resource``` function, which will generate two user resource types for the users foo and bar.

This is a quite hidden approach of what is done.

How about using Puppet 4 capability of dealing with data?

    class my_great_class (
      Hash $data = {}
    ){
      $data.each |String $key, Hash $value| {
        $ensure = pick($value['ensure'], 'present')
        user { $key:
          ensure   => $ensure,
          *        => $value,
        }
      }
    }

The most beautiful thing here is the splat operator ```* => $value,```.
This expands the $value subhash. Each key becomes the parameter and the according value becomes the parameter value.

Martin Alfke
