---
layout: blog
title: Tip of the Week 56 - Running acceptance tests on different Puppet versions with PSICK
---

Example42's [psick control-repo](https://github.com/example42/psick) has several features which allows user to manage most of the typical infrastructure tasks easily.

PSICK has a set of unit and acceptance tests already built in. Usually we want to test the Puppet version we have running in infrastructure and we want to test functionality with newer versions.

### Unit Testing

Handling different Puppet versions on unit testing is done by reading an environment variable from [Gemfile](https://github.com/example42/psick/blob/production/Gemfile#L39).
[rspec puppet](http://rspec-puppet.com/) uses the Puppet version installed by bundler to compile and check catalogs.

Running unit tests for different Puppet versions is easy:

    export PUPPET_GEM_VERSION='4.10.9'
    bundle install --path vendor
    bundle exec rake spec

Now let's test Puppet 5:

    export PUPPET_GEM_VERSION='5.3.3'
    bundle update puppet
    bundle exec rake spec

Unsetting the PUPPET_GEM_VERSION environment variable will use the latest Puppet version from rubygems.

### Acceptance Testing

Acceptance testing is different.

At PSICK we offer the possibility to use [Docker containers](https://github.com/example42/psick/blob/production/spec/acceptance/nodesets/docker.yml) or [Vagrant instances](https://github.com/example42/psick/blob/production/spec/acceptance/nodesets/vagrant.yml) for acceptance tests run by beaker. In both solutions the Puppet agent must be installed inside the instance. Usually we want to use the version we have running in our infrastructure.

The beaker-puppet helper offers a new way on specifying Puppet versions to install. At PSICK we re-use the pattern from unit testing by specifying the PUPPET_GEM_VERSION environment variable:

    export PUPPET_GEM_VERSION='4.10.8'
    bundle install --path vendor
    bundle exec rake beaker_roles:psick

Now we want to test latest Puppet 5 version:

    export PUPPET_GEM_VERSION='~> 5'
    bundle update puppet
    bundle exec rake beaker_roles:psick

The magic is in [PSICK spec/spec_helper_acceptance.rb](https://github.com/example42/psick/blob/production/spec/spec_helper_acceptance.rb#L9) where we check for the Puppet version installed by bundler and pass proper attributes to beaker's `install_puppet_agent_on` method.

Happy hacking,

Martin Alfke

