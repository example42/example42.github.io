---
layout: blog
title: Puppet 4 - Examples - EPP Templates
---

Puppet 4 has some new functionality. Within the next few blog posts I will give some examples on how to use the new functionality.

The [first post](http://www.example42.com/2015/09/09/puppet4-examples-data-types/) covered the new Data Type system.

The [second post](http://www.example42.com/2015/10/07/puppet4-examples-functions/) covered the new function API.

This third post covers the new EPP template engine and the HEREDOC implementation.

In Puppet 3 all templates were written as ERB (embedded Ruby) templates.

All variables in ERB templates have either been looked up dynamically, or one needed to specify the scope for variable lookup.

In Puppet 4 a new template engine was introduced: EPP (embedded Puppet).

Within EPP templates varaibles are writtenin Puppet syntax - which means that variables can be specified by using the module/class namespace.

Example (sshd_config):

    <% if $ssh::port -%>
    Port <%= $ssh::port %>
    <% else -%>
    Port 22
    <% end -%>
    <% if $ssh::listen -%>
    ListenAddress <%= $ssh::listen %>
    <% else -%>
    ListenAddress 0.0.0.0
    ListenAddress ::
    <% end -%>

Besides this the array iteration also needs to be written in Puppet DSL code:

    <% if $ssh::port ~= Array -%>
    <% $ssh::port.each |$port| { -%>
    Port <%= $port %>
    <% } -%>
    <% end -%>

Additionally the EPP template now offers the possibility to make use of parameters (like parameterized classes).
Parameters in EPP have to be put in the beginning and are enclosed in EPP tag and a pipe sign.

    <% |  String $text, $Array $array, Boolean $bool |>
    <% if $string -%>
    Text from variable: <%= $string %>
    <% end -%>
    <% if $array -%>
    <% $array.each |$element| { -%>
    Array item: <%= $element %>
    <% } -%>
    <% end -%>
    <% if $bool -%>
    Bool value is true
    <% end -%>

Data for EPP parameters are set by the epp or inline_epp function. This function now can have two parameters:

  1. the content of the template (either as file or as variable
  2. a hashmap for parameters

Example:

```
  content => epp('test/example.epp', { text => 'foo', array => ['one', 'two'], bool => false }),
```

Parameterized templates are useful when the template serves different puprposes for different modules. The non parameterized template should be used when only used by one specific module.


===
HEREDOC

It has always been a pain having small config files in Puppet DSL - mostly due to having bad readable code:

    class my_motd {
      $content = "Welcome to <%= @fqdn %>
    This system is managed by Puppet.
    Changes will be overwritten on next Puppet Agent run."
    
      file { '/etc/motd':
        ensure  => file,
        content => inline_template($content),
      }
    }


In Puppet 4 we have a new way of having files being part of the code: HEREDOC.
First, let's migrate the example to heredoc and epp.

Hereddoc needs a tag (set in round brackets) - like Shell heredoc

    class my_motd {
      $content = @(EOF)
    Welcome to <%= $::fqdn %>
    This system is managed by Puppet.
    Changes will be overwritten on next Puppet Agent run.
    EOF

      file { '/etc/motd':
        ensure  => file,
        content => inline_epp($content)
      }
    }

Next we will make use of the fixed identation by using a pipe sign:

    class my_motd {
      $content = @(EOF)
        Welcome to <%= $::fqdn %>
        This system is managed by Puppet.
        Changes will be overwritten on next Puppet Agent run.
        | EOF
     
      file { '/etc/motd':
        ensure  => file,
        content => inline_epp($content),
      }
    }

Now we want to make use of the heredoc substitution. Substitution can be enabled by putting the tag in double quotes:

    class my_motd {
      $content = @("EOF")
        Welcome to ${::fqdn)
        THis system is managed by Puppet.
        Changes will be overwritten on next Puppet Agent run.
        | EOF
      
      file { '/etc/motd':
        ensure  => file,
        content => $content,
      }
    }

if you need escape sequences then you need to enable them at the heredoc tag:

    $content = @(EOF\tn)

THis enables tabular and newline escape sequences.


The next posting will deal with several ways on how to upgrade to Puppet 4.
