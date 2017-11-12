---
layout: blog
title: Tip of the Week 46 - Checking config files before applying them
---

Lately I've rediscovered an option of Puppet's **file** resource that can be incredibly useful and, surprisingly, doesn't seem to be widely used.

Since Puppet 4.6 the file resource type has the [validate_cmd](https://puppet.com/docs/puppet/latest/type.html#file-attribute-validate_cmd) attribute, which allows to run a command to check the syntax of a file before actually applying it to the system.

For example we can write:

    file { '/etc/nginx/nginx.conf':
      content      => 'This can be wrong',
      validate_cmd => 'nginx -t -c %',
    }

to make Puppet run the specified ```validate_cmd``` on the file we are trying to provide, which is referenced by the ```%``` sign (can be configured with the ```validate_replacement``` attribute).

Needless to say that this is extremely useful to prevent accidental failures in managed systems due to incorrect syntax (or incomplete values, due to missing variables) in the provided configuration files for the managed applications.

This is what happens in a Puppet run when we try to provide a file with a wrong syntax for which is defined the ```validate_cmd``` attribute:

    Notice: /Stage[main]/Psick::Nginx::Tp/Tp::Conf[nginx]/File[/etc/nginx/nginx.conf]/content:
    --- /etc/nginx/nginx.conf	2017-02-11 21:00:57.000000000 +0000
    +++ /tmp/puppet-file20171111-22472-s7ino5	2017-11-11 16:33:57.380255495 +0000
    @@ -1,85 +1 @@
    -user www-data;
    [....]
    -#}
    +something wrong
    \ No newline at end of file

    Info: Computing checksum on file /etc/nginx/nginx.conf
    Info: /Stage[main]/Psick::Nginx::Tp/Tp::Conf[nginx]/File[/etc/nginx/nginx.conf]: Filebucketed /etc/nginx/nginx.conf to puppet with sum 907bbf7d1cb3f410d8d6d4474a984b86
    Error: Execution of 'nginx -t -c /etc/nginx/nginx.conf20171111-22472-12tbrva' returned 1: nginx: [emerg] unexpected end of file, expecting ";" or "}" in /etc/nginx/nginx.conf20171111-22472-12tbrva:1
    nginx: configuration file /etc/nginx/nginx.conf20171111-22472-12tbrva test failed
    Error: /Stage[main]/Psick::Nginx::Tp/Tp::Conf[nginx]/File[/etc/nginx/nginx.conf]/content: change from '{md5}907bbf7d1cb3f410d8d6d4474a984b86' to '{md5}d9729feb74992cc3482b350163a1a010' failed: Execution of 'nginx -t -c /etc/nginx/nginx.conf20171111-22472-12tbrva' returned 1: nginx: [emerg] unexpected end of file, expecting ";" or "}" in /etc/nginx/nginx.conf20171111-22472-12tbrva:1
    nginx: configuration file /etc/nginx/nginx.conf20171111-22472-12tbrva test failed
    Notice: /Stage[main]/Psick::Nginx::Tp/Tp::Install[nginx]/Service[nginx]: Dependency File[/etc/nginx/nginx.conf] has failures: true
    Warning: /Stage[main]/Psick::Nginx::Tp/Tp::Install[nginx]/Service[nginx]: Skipping because of failed dependencies
    Notice: Applied catalog in 11.07 seconds

Puppet shows the diff of the file but it doesn't actually change it, as the validate command has returned an error (any exit code different from 0).

Since the file resource has failed, also the dependent resources, as the nginx service, are skipped.

On the system the original file and the relevant service have remained untouched.

We have just added such functionality to [Tiny Puppet](https://github.com/example42/puppet-tp/commit/209e9c811881c4dd8c5443fde2183f3225daded0), now, whenever there's the relevant Tiny Data for an application, the ```tp::conf``` defines runs a validate command for the files it provides.

Configuration on Tiny Data is easy, check [this commit](https://github.com/example42/tinydata/commit/2b07697e8d246c6a6583a3f083330eae76209bc8) for an example.

Note that it's possible, in Tiny Data, either to define a single string containing the validation script, or an hash, where is possible to define what command to run for what configuration file type.

For example, the ```httpd -t -f %``` command can be used only with the main Apache configuration file (base_file = 'config'), as it would fail with configuration fragments as can be virtual hosts definitions.

Expect more TinyData to appear in the future to add configuration validation to applications managed by Tiny Puppet, and, please, feel free to send Pull Requests to TinyData, similar to the one linked earlier, to add support to new applications.

Alessandro Franceschi
