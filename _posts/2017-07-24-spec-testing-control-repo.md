---
layout: blog
title: Tip of the Week 30 - Spec Testing a Puppet control-repository
---

Spec tests are a common way to test whether your Puppet code either has no errors causing the compiler to stop or whether your Puppet code does things in the right way.
Usually spec tests are done at different levels:

1. Lint testing
1. Unit Testing
1. Acceptance Testing

Lint tests check if the Puppet code follows the Puppet [style guide](https://docs.puppet.com/puppet/5.0/style_guide.html).
Within unit tests we use [rspec-puppet](https://rspec-puppet.com). Rspec-puppet compiles a Puppet catalog in a sandbox and checks if the catalog is compiled successfully and contains all required resources.
Acceptance tests are used to deploy a machine, apply the Puppet code and verify system settings. For acceptance testing we use [beaker](https://github.com/puppetlabs/beaker/wiki) which is a wrapper around [vagrant](https://www.vagrantup.com/) or [docker](https://www.vagrantup.com/) and [serverspec](http://serverspec.org/).

Lint tests are easy to deploy and run. All you need is the following files:
- Gemfile
- Rakefile

We are re-using the puppetlabs_spec_helper gem as this brings most what we need.

    # Gemfile
    source ENV['GEM_SOURCE'] || "https://rubygems.org"
    gem 'puppetlabs_spec_helper'

    # optional lint extensions (see https://voxpupuli.org/plugins/#puppet-lint)
    gem 'puppet-lint-appends-check',
    :git => 'https://github.com/voxpupuli/puppet-lint-appends-check.git',
    :require => false
    gem 'puppet-lint-classes_and_types_beginning_with_digits-check',
      :git => 'https://github.com/voxpupuli/puppet-lint-classes_and_types_beginning_with_digits-check.git',
      :require => false
    gem 'puppet-lint-empty_string-check',
      :git => 'https://github.com/voxpupuli/puppet-lint-empty_string-check.git',
      :require => false
    gem 'puppet-lint-file_ensure-check',
      :git => 'https://github.com/voxpupuli/puppet-lint-file_ensure-check.git',
      :require => false
    gem 'puppet-lint-leading_zero-check',
      :git => 'https://github.com/voxpupuli/puppet-lint-leading_zero-check.git',
      :require => false
    #gem 'puppet-lint-numericvariable', # has issues with new puppet-lint release
    #    :git => 'https://github.com/fiddyspence/puppetlint-numericvariable.git',
    #    :require => false
    gem 'puppet-lint-resource_reference_syntax',
      :git => 'https://github.com/voxpupuli/puppet-lint-resource_reference_syntax.git',
      :require => false
    gem 'puppet-lint-spaceship_operator_without_tag-check',
      :git => 'https://github.com/voxpupuli/puppet-lint-spaceship_operator_without_tag-check.git',
      :require => false
    gem 'puppet-lint-trailing_comma-check',
      :git => 'https://github.com/voxpupuli/puppet-lint-trailing_comma-check.git',
      :require => false
    gem 'puppet-lint-undef_in_function-check',
      :git => 'https://github.com/voxpupuli/puppet-lint-undef_in_function-check.git',
      :require => false
    gem 'puppet-lint-unquoted_string-check',
      :git => 'https://github.com/voxpupuli/puppet-lint-unquoted_string-check.git',
      :require => false
    gem 'puppet-lint-variable_contains_upcase',
      :git => 'https://github.com/fiddyspence/puppetlint-variablecase.git',
      :require => false
    gem 'puppet-lint-version_comparison-check',
      :git => 'https://github.com/voxpupuli/puppet-lint-version_comparison-check.git',
      :require => false

Within the Rakefile you must enable the puppet-lint rake task:

    # Rakefile
    require 'puppetlabs_spec_helper/rake_tasks'

In the spec/spec_helper.rb file we enable the puppetlabs_spec_helper module spec helper:

    # spec/spec_helper.rb
    require 'puppetlabs_spec_helper/module_spec_helper'


Puppet-lint will check for a manifests and modules directory to read puppet manifests and checks for style guide.

But within a control-repository the files to test are not inside the modules directory, but inside the site directory. As we can not overwrite this default behavior we generate a new lint rake task in the Rakefile:

    # Rakfile
    require 'puppetlabs_spec_helper/rake_tasks'

    exclude_paths = %w(
      vendor/**/*
      spec/**/*
      modules/**/*
      pkg/**/*
      tests/**/*
    )

    Rake::Task[:lint].clear
    PuppetLint::RakeTask.new(:lint) do |config|
      # Pattern of files to ignore
      config.ignore_paths = exclude_paths
      # Pattern of files to check, defaults to `**/*.pp`
      config.pattern = ['manifests/**/*.pp', 'site/**/*.pp']
      # List of checks to disable
      config.disable_checks = ['140chars', 'relative', 'class_inherits_from_params_class']
      # Should the task fail if there were any warnings, defaults to false
      config.fail_on_warnings = true
      # Print out the context for the problem, defaults to false
      #config.with_context = true
      # Log Format
      #config.log_format = '%{path}:%{line}:%{check}:%{KIND}:%{message}'
    end

Unit tests need to know where to find the upstream modules which we have in Puppetfile within the control-repo.
We don't fetch these from upstream source as this would need to have Puppetfile and .fixtures.yml files synced or either one automatically generated.

Instead we have chosen to re-use the modules which must be installed using r10k:

    r10k puppetfile install -v

Within the spec/spec_helper.rb file we set the modulepath to 'site' and 'modules':

    fixture_path = File.expand_path(File.join(__FILE__, '..', 'fixtures'))

    RSpec.configure do |c|
      c.module_path = File.join(fixture_path, 'modules/site') + ':' + File.join(fixture_path, 'modules/r10k')
      c.manifest_dir = File.join(fixture_path, '../../manifests')
      c.manifest = File.join(fixture_path, '../../manifests/site.pp')
      c.hiera_config = File.join(fixture_path, '../../hiera.yaml')
      c.fail_fast = true
    end

The .fixtures.yml just ensures that all directories are in place:

    fixtures:
      symlinks:
          site: "#{source_dir}/site"
          r10k: "#{source_dir}/modules"

Now rspec-puppet needs a test. The most simple one just checks if a catalog is successfully created:

    # spec/classes/profile_apache_spec.rb
    describe 'profile::apache' do
      context 'catalog compile' do
        it { should compile.with all_deps }
      end
    end

Next we want acceptance tests. Usually beaker was created to run acceptance tests on modules.
Modules have a multiple tests running on supported operating systems. Beaker reuses a VM it has created for all tests.

Within a control-repo we want a fresh state on every test, as we have single tests which should run on a fresh os every time.

First we need the beaker gem:

    # Gemfile
    group :system_tests do
      gem 'beaker'
      gem 'beaker-rspec'
    end

In Rakefile we disable the default beaker task. Next we generate a new task which will iterate over our acceptance tests:

    # Rakefile
    Rake::Task[:beaker].clear
    RSpec::Core::RakeTask.new(:beaker) do |config|
      puts 'dont use beaker, use beaker_roles:<role> or all_roles instead'
      abort
    end

    namespace :beaker_roles do
      Dir.glob("spec/acceptance/*_spec.rb") do |acceptance_test|
        test_name = acceptance_test.split('/').last.split('_spec').first
        RSpec::Core::RakeTask.new(test_name) do |t|
          t.rspec_opts = ['--color']
          t.pattern = acceptance_test
        end
      end
    end

To allow all tests running in parallel we generate a multitask in Rakefile:

    all_roles = []
    Rake.application.in_namespace(:beaker_roles) do |beaker_roles_namespace|
      beaker_roles_namespace.tasks.each do |beaker_roles_tasks|
        all_roles << beaker_roles_tasks
      end
    end
    multitask :all_roles => all_roles

All this is already part of [PSICK](https://github.com/example42/psick)

We wish successful unit and integration tests on your control-repositories.

Martin Alfke
