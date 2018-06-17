---
layout: blog
title: Tip of the Week 77 - How to adopt the Puppet Developer Kit (PDK) to your code
---

PDK alows you to easily get unit tests for your puppet modules.

The Developer Kit is [available](https://puppet.com/download-puppet-development-kit) for Linux, OS X and macOS and Windows.

* Table of content
{:toc}

## What is inside?

In the PDK installation package you get some Puppet and Ruby versions installed into `/opt/puppetlabs/pdk`.
In version 1.5.0 you get Ruby 2.1.9 and 2.4.4 (installed into `/opt/puppetlabs/pdk/private/puppet/ruby/`)
Installation of Puppet versions is spread among the ruby versions. For Ruby 2.1.09 we have Puppet 4.7.1, 4.8.2, 4.9.4 and 4.10.11 (installed in `/opt/puppetlabs/pdk/private/puppet/ruby/2.1.0/gems/`). In Ruby 2.4.4 you find Puppet versions 5.0.1, 5.1.0, 5.2.0, 5.3.6, 5.4.0 and 5.5.1 (installed in `/opt/puppetlabs/pdk/private/puppet/ruby/2.4.0/gems/`)

Besides this git is bundled in version 2.14.2 in `/opt/puppetlabs/pdk/private/git`.

## Starting a new module

The Puppet Developer Kit is based on a module template. The template is bundled as a bare git repository in the installer and is located at `/opt/puppetlabs/pdk/share/cache/pdk-templates.git/`.

The module which is created by PDK uses Gemfile for installation of ruby extensions required for testing like rspec-puppet and provides CI configurations for [travis](http://travs-ci.org) and [GitLab CI runner](https://docs.gitlab.com/runner/).

### Generate the Module

The module creation process starts with asking several questions regarding the PuppetForge account name (you don't need one, it is just a name, which is prefixed to the module name), the author name, license and supported operating systems.

The creation is started by running

    pdk new module <modulename>
    
e.g.

    pdk new module demo
    pdk (INFO): Creating new module: demo

    We need to create the metadata.json file for this module, so we're going to ask you 4 questions.
    If the question is not applicable to this module, accept the default option shown after each question. You can modify any answers at any time by manually updating the metadata.json file.

    [Q 1/4] If you have a Puppet Forge username, add it here.
    We can use this to upload your module to the Forge when it's complete.
    --> mea

    [Q 2/4] Who wrote this module?
    This is used to credit the module's author.
    --> tuxmea

    [Q 3/4] What license does this module code fall under?
    This should be an identifier from https://spdx.org/licenses/. Common values are "Apache-2.0", "MIT", or "proprietary".
    --> Apache-2.0

    [Q 4/4] What operating systems does this module support?
    Use the up and down keys to move between the choices, space to select and enter to continue.
    --> RedHat based Linux, Debian based Linux, Windows (Use arrow or number (1-7) keys, pres--> RedHat based Linux, Debian based Linux, Windows

    Metadata will be generated based on this information, continue? Yes
    pdk (INFO): Module 'demo' generated at path '/Users/mea/Desktop/example42-blog/demo', from template 'file:///opt/puppetlabs/pdk/share/cache/pdk-templates.git'.
    pdk (INFO): In your module directory, add classes with the 'pdk new class' command.

### Generate module content

With PDK you can create classes, defined_types and tasks. Generating providers is an experimental feature at the moment.

    pdk new class demo
    pdk (INFO): Creating '/Users/mea/Desktop/example42-blog/demo/manifests/init.pp' from template.
    pdk (INFO): Creating '/Users/mea/Desktop/example42-blog/demo/spec/classes/demo_spec.rb' from template.

This generates a Puppet class and the according basic unit test file.

Creating a self defined Puppet resource type is similar:

    pdk new defined_type demo::foo
    pdk (INFO): Creating '/Users/mea/Desktop/example42-blog/demo/manifests/foo.pp' from template.
    pdk (INFO): Creating '/Users/mea/Desktop/example42-blog/demo/spec/defines/foo_spec.rb' from template.

Tasks are created by running:

    pdk new task run_demo
    pdk (INFO): Creating '/Users/mea/Desktop/example42-blog/demo/tasks/run_demo.sh' from template.
    pdk (INFO): Creating '/Users/mea/Desktop/example42-blog/demo/tasks/run_demo.json' from template.

As you can see, PDK creates you a stub file using `.sh` extension. The JSON file is the description of the task.

## Using PDK on existing module

## Adopting PDK to your code

PDK manages several files and will overwrite them when running `pdk update`.
This is especially for `Gemfile`, `Rakefile`, `spec/spec_helper.rb` and `spec/default_facts.yml`.

These files are managed and owned by PDK. But how to adopt these to your specific needs?

### Adding ruby gems

PDK does not include the hiera-eyaml gem.
If you want to run tests with eyaml, you must install the hiera-eyaml gem within PDK.
Installation of Ruby gems is done via `Gemfile`.
Any additional gem can be placed either in `~/.gemfile` or in `Gemfile.local`.
Please note that `Gemfile.local` is excluded from git in `.gitignore` file!

We usually remove that entry from `.gitignore` file and take care to again remove after `pdk update`.

### Adding your own code to spec_helper

Don't manage `spec/spec_helper.rb` directly.
Add your own rspec settings to `spec/spec_helper_local.rb` instead.

### Adding more facts

Don't manage `spec/default_facts.yml` directly.
Add your own facts to `spec/default_module_facts.yml` instead.


Happy hacking,
Martin Alfke
