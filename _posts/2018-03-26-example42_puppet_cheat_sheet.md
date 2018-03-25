---
layout: blog
title: Tip of the Week 65 - The example42 Puppet cheat sheet
---

Yes, we know, there is a famous Puppet cheat sheet available at docs.puppet.com

This is my personal collection of different Puppet DSL items, which I usually generate at each official Puppet Fundamentals training.
Now I found the time to paste them into a blog posting and add information on code logic and hiera.

### Puppet DSL

#### Resource type declaration:

    type { 'title':
      param => 'value',
    }

#### Class definition:

    class <name> (
      DataType $param1,           # this parameter must be provided upon declaration
      DataType $param2 = 'value',
    ) {
      # Puppet DSL code
    }

#### Class declaration using a function:

    include <name>  # no ordering, the mentioned class will be somewhere ein the catalog
    require <name>  # strict ordering, the class must be finished prior continuing
    contain <name>  # local ordering, the class must be finished within the class where the contain function is used

#### Class declaration using class as resource type:

    class { '<name>':
      param1 => 'value',
    }

#### Self defined resource type definition:

    define <name> (
      DataType $param1,
      DataType $param2 = 'value',
    ){
      # Puppet DSL
      # all resource type declaration must use the $title variable
      # older Puppet code uses $name instead of $title
    }

#### Self defined resource type declaration:

    <name> { 'title':
      param1 => 'value',
    }


### Puppet DSL code logic

#### Case statement:

    case $test_variable {
      'value1': {         # specific value
        # Puppet DSL
      }
      /regexp/: {         # regular expression
        # Puppet DSL
      }
      'value2', 'value3': {  # multiple values
        # Puppet DSL
      }
      default: {          # fall back value - optional
        # optional, Puppet DSL
      }
    }

#### If statement:

Variant 1: Boolean or existing variable:

    if $test_variable {
      # Puppet DSL
    } else {  # else is optional
      # Puppet DSL
    }

Variant 2: test content of variable:

    if $test_variable == 'content' {
      # Puppet DSL
    }

Variant 3: test content on regular expression:

    if $test_variable ~= /regexp/ {
      # Puppet DSL
    }

#### Selector:

Please use selectors sparsely as they very fast lead to hard to read Puppet code!

    $result_var = $test_var ? {
      'value1' => 'return_val1',
      'value2' => 'return_val2',
      default  => 'return_val3',
    }


### Puppet DSL lambda functions

#### Iterating over an array:

    $var = [ 'element1', 'element2' ]
    $var.each |DataType $key| {
      type { $key:
        param => 'value',
      }
    }

#### Iterating over a hash:

    $var = {
      'key1' => {
        'var1' => 'val1',
        'var2' => 'val2',
      },
      'key2' => {
        'var1' => 'val1',
      },
    }

    $var.each |DataType $key, DataType $val| {
      type { $key:
        * => $val,
    }

### Puppet and Hiera 5

#### Explicit lookup

    class foo {
      $data = lookup('key', DataType, <merge behavior>, <default value>)
    }

DataType, <merge behaviour> and <default value> are optional

merge behavior:

    'first'   # returns the first occurrence of 'key'
    'unique'  # returns an array of all occurrences of 'key' with duplicates removed
    'hash'    # returns a hash of all occurrences of 'key', duplicates hash keys are taken from highest priority
    'deep'    # returns a hash of all occurrences of 'key', duplicate hash keys are merged

#### Automatic data lookup

    class foo (
      DataType $data = 'value' # identical to $data = lookup('foo::data', DataType, 'first', 'value')
    ) {
    }

Puppet will automatically query hiera for the key `'foo::data'`

### Puppet and Resource ordering

#### Ordering with meta parameters

Variant 1: require and subscribe

    package { 'foo':
      ensure => present,
    }
    file { '/etc/foo/foo.conf':
      ensure  => file,
      require => Package['foo'],
    }
    service { 'foo':
      ensure    => running,
      subscribe => File['/etc/foo/foo.conf'].
    }

Variant 2: before and notify

    package { 'foo':
      ensure => present,
      before =: File['/etc/foo/foo.conf'],
    }
    file { '/etc/foo/foo.conf':
      ensure => file,
      notify => Service['foo'],
    }
    service { 'foo':
      ensure => running,
    }

Variant 3: resource chaining

    package { 'foo':
      ensure => present,
    }
    file { '/etc/foo/foo.conf':
      ensure => file,
    }
    service { 'foo':
      ensure => running,
    }

    Package['foo'] -> File['/etc/foo/foo.conf'] ~> Service['foo']

or multiline:

    Package['foo']
    -> File['/etc/foo/foo.conf']
    ~> Service['foo']

### Puppet Module

A module is a directory structure inside the `$modulepath`.

    <modulepath>/
      \- <modulename>
           |- manifests/
           |    |- init.pp
           |    |- subclass.pp
           |    \- folder/
           |        \- subclass.pp
           |- files/
           |    \- staticfile.conf
           |- templates/
           |    \- dynamic_config_file.epp
           |- facts.d/
           |    \- external_facts.yaml
           |- types/
           |    \- datatype.pp
           |- functions/
           |    \- puppetfunction.pp
           |- lib/
           |    |- facter/
           |    |    \- custom_facts.rb
           |    \- puppet/
           |        |- functions/
           |        |    \- puppet4function.rb
           |        |- parser/
           |        |    \- functions/
           |        |        \- puppetfunction.rb
           |        |- type/
           |        |    \- custom_type.rb
           |        \- provider/
           |             \- custom_type/
           |                 \- custom_provider.rb
           \- spec/


Happy hacking,

Martin Alfke