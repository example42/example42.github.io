---
layout: blog
title: Tip of the Week 5 - RSpec Testing on existing Puppet code
---

Many Puppet code bases are pure Puppet code without unit or integration testing.

Most maintainers of such a code base fear the work for adding tests to their code.

But what is it that you as a maintainer would like to achieve? Normally you are happy when you can check whether your Puppet code still compiles on a newer Puppet version.

Just adding this kind of unit tests is easy and depends on your code layout:

  - do you have repository per module
  - do you have one monolithic repository

Let's go for the first solution:

You need a Gemfile, a Rakefile, a .fixtures.yml and a spec/spec_helper.rb file.

The Gemfile can be short:

    # Gemfile
    source 'https://rubygems.org'
    gem 'puppetlabs_spec_helper'
    gem 'puppet', ENV['PUPPET_GEM_VERSION'] || '~> 4'

Yu can even omit the puppet gem and you get the latest version automatically. In our example you have the option to specify other versions via environment variables:

    export PUPPET_GEM_VERSION='~> 3'

The Rakefile can be even shorter:

    # Rakefile
    require 'puppetlabs_spec_helper/rake_tasks'

The .fixtures.yml describes the naming scheme of your module and adds additional required modules for spec testing in a sandbox.

    # .fixtures.yml
    fixtures:
      repositories:
        stdlib: "https://github.com/puppetlabs/puppetlabs-stdlib.git"
      symlinks:
        put your class name here: "#{source_dir}"

The spec_helper.rb file must be located in the spec Directory and has the following content:

    # spec/spec_helper.rb
    require 'puppetlabs_spec_helper/module_spec_helper'

Next you want to test your module. We assume that the module has one class only. Put class tests inside the ```spec/classes``` directory. The test file must end with ```_spec.rb``` to allow rspec-puppet to find the test.

    # spec/classes/init_spec.rb
    require 'spec_helper'
    describe 'put your class name here' do
      describe 'on test osfamily' do
        let(:facts) do
          { :osfamily => 'put the os you want to test here' }
        end
        context 'with default options' do
          it { is_expected.to compile.with_all_deps }
        end
      end
    end

The second approach (one monolithic repository just needs adoption of all symlinks in the .fixtures.yml file.

e.g.

    # .fixtures.yml
    fixtures:
      symlinks:
        my_ntp:    "#{source_dir}/modules/ntp"
        my_apache: "#{source_dir}/modules/my_apache"
        mysql:     "#{source_dir}/modules/mysql"
        ...

Everything else works similar.

Now you need to install the Gemfile extensions. First you want to ensure that you have a corresponding, [supported Ruby version](https://docs.puppet.com/guides/platforms.html#ruby-versions) installed.
In case that the OS vendor does not offer the correct version from repositories you might want to reconcider installing ruby into your home directory by using [rvm](http://rvm.io/) or [rbenv](http://rbenv.org/).

Switch into the repository directory where the Gemfile is located and install the extensions using bundler:

    bundle install

Extra tip: if you dont like to mess up your ruby installation you can also specify a path where the extensions will be installed:

    bundle install --path vendor

Now you can run the rake task:

    bundle exec rake spec

Please note that in this simple case you want to run the tests on the same os as your infrastructure. Testing on e.g. a Windows or OS X workstation requires additional fact and Puppet code mocks.

But how to write full tests when no time is given for this task?

Please check the [retrospec](https://github.com/nwops/puppet-retrospec) tool which will parse your Puppet code and generate the tests automagically for you.

Martin Alfke
