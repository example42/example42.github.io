---
layout: blog
title: Tip of the Week 65 - The example42 Puppet cheat sheet
---

Yes, we know, there is a famous Puppet cheat sheet available at docs.puppet.com

This is my personal collection of different Puppet DSL items, which I usually generate at each official Puppet Fundamentals training.
Now I found the time to paste them into a blog posting and add information on code logic and hiera.

### Puppet DSL

A resource type declaration:

    type { 'title':
      param => 'value',
    }

A class definition:

    class <name> (
      DataType $param1,           # this paramter must be provided upon declaration
      DataType $param2 = 'value',
    ){
      # Puppet DSL code
    }

A class declaration using a function:

    include <name>  # no ordering, the mentioned class will be somwher ein the catalog
    require <name>  # strict ordering, the class must be finished prior continuing
    contain <name>  # local ordering, the class must be finished within the class where the contain function is used

A class declaration using class as resource type:

    class { '<name>':
      param1 => 'value',
    }

A self defined resource type definition:

    define <name> (
      DataType $param1,
      DataType $param2 = 'value',
    ){
      # Puppet DSL
      # all resource type declaration must use the $title variable
      # older Puppet code uses $name instead of $title
    }

A self defined resource type declaration:

    <name> { 'title':
      param1 => 'value',
    }



### Puppet DSL code logic

A case statement:

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

An if statement:

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

A selector:

Please use selectors sparesely as they very fast lead to hard to read Puppet code!

    $result_var = $test_var ? {
      'value1' => 'return_val1',
      'value2' => 'return_val2',
      default  => 'retuen_val3',
    }


### Puppet DSL lambda functions

Iterationg over an array:

    $var = [ 'element1', 'element2' ]
    $var.each |DataType $key| {
      type { $key:
        param => 'value',
      }
    }

Iterating over a hash:

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

Explicit lookup

    class foo {
      $data = lookup('key', DataType, <merge behavior>, <default value>)
    }

DataType, <merge behavior> and <default value> are optional

merge behavior:

    'first'   # returns the first occurence of 'key'
    'unique'  # returns an array of all occurences of 'key' with duplicates removed
    'hash'    # returns a hash of all occurences of 'key', duplicates hash keys are taken from highest priority
    'deep'    # returns a hash of all occurences of 'key', duplicate hash keys are merged

Happy hacking,

Martin Alfke

