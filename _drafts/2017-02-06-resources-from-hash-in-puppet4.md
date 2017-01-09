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
        provider => 'foo',
      }
      create_resources('user', $data, $default)
    }

Great abstraction, but what happens really?

How abaout using Puppet 4 capability of dealing with data?

    class my_great_class (
      Hash $data = {}
    ){
      $data.each |String $key, Hash $value| {
        $ensure = pick($value['ensure'], 'present')
        $provider = pick($value['provider'], 'foo')
        user { $key:
          ensure   => $ensure,
          provider => $provider,
          *        => $value,
        }
      }
    }

Martin Alfke
