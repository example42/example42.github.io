---
layout: blog
title: Tip of the Week 51 - Acceptance testing on a control-repository using beaker in combination with vagrant and docker
---

Beaker has become the de-facto standard utility for Puppet code acceptance testing.

Like the figure from [The Muppet Show](https://en.wikipedia.org/wiki/Beaker_(Muppet)) the Puppet tooling "...is a magnet for disaster".
In this specifc case we want to find out whether a catalog can be applied to a system successfully.
In additiona to that the Muppet figure has even more qualification for breaking things: "he routinely experiences mishaps such as being blown up, electrocuted, eaten by large monsters, or afflicted with awkward side effects caused by Dr. Bunsen Honeydew's experiments. Beaker communicates in a nervous, high-pitched squeak that sounds like "Mee-mee-mee mee"" (quote taken from Wikipedia Beaker Muppet - see link above).

I also like the name for the tool, as we sometimes re-use the "Mee-mee-mee" to a person telling you that something is not working.

### Beaker installation

Puppet beaker allows for unattanded CI based testing and acts as a frontend for Vagrant, AWS, Google Compute, VMware/Vsphere, Docker and others. Please see the [beaker documentation on hypervisors](https://github.com/puppetlabs/beaker/tree/master/docs/how_to/hypervisors) for additional information.

Within this posting I want to explain how we at example42 use beaker for acceptance testing in control-repositories like [PSICK](https://github.com/example42/psick).

Installing beaker is usually done by adding a few lines to your Gemfile:

    # Beaker
    group :acceptance do
      gem 'beaker'
      gem 'beaker-rspec'
      gem 'beaker-hiera'
      gem 'beaker-puppet_install_helper'
    end

All standard beaker hypervisor extensions are a dependency to the beaker gem. Please note that beaker uses the [fog libraries](https://github.com/fog/fog) for cloud access which causes a long list of dependencies.

### Beaker nodesets

Next we need to add node descriptions providing information on operating system and releases to run tests on.
These are placed into the `spec/acceptance/nodesets/` folder.

Here we usually see the first difference between acceptance tests on control-repositories versus acceptance testing on modules:

Within modules one wants to test, whether the single code base is working as expected on all supported operating systems. For a control-repository one wants to test multiple different system roles on a few operating systems.

Let's continue testing control-repositories on CentOS 7. The nodeset configuration consists of the following two files:

First we generate the nodeset for testing on docker:

    # spec/acceptance/nodesets/default.yml
    HOSTS:
      centos7-box:
        platform: el-7-x86_64
        hypervisor: docker
        docker_cmd: '["/usr/sbin/init"]'
        docker_image_commands:
          - 'yum install -y crontabs initscripts iproute openssl sysvinit-tools tar wget which ss'
          - 'systemctl mask getty@tty1.service'
        docker_preserve_image: true
        mount_folders:
          controlrepo:
            host_path: .
            container_path: /tmp/production
            opts: ro
    CONFIG:
      type: foss

Now we add the nodeset for testing on vagrant:

    # spec/acceptance/nodesets/vagrant.yml
    HOSTS:
      centos-7-x64:
        roles:
          - agent
        platform: el-7-x86_64
        box: centos/7
        hypervisor: vagrant
        mount_folders:
          controlrepo:
            host_path: ../../../
            container_path: /tmp/production
            opts: ro
    CONFIG:
      type: foss


### Beaker running instance preparation

The images we are using do not have puppet agent package installed. Installation and preparation of the started images is configured in the `spec/spec_helper_acceptance.rb` file:

    # spec/spec_helper_acceptance.rb
    require 'beaker-rspec'
    require 'beaker/puppet_install_helper'
    
    # Instal PC1 puppet 4 agent packages
    run_puppet_install_helper
    
    RSpec.configure do |c|
      # Readable test descriptions
      c.formatter = :documentation
      # preare each system after starting the image:
      hosts.each do |host|
        # remove obsolete global hiera.yaml
        on(host, '/usr/bin/test -f /etc/puppetlabs/puppet/hiera.yaml && /bin/rm -f /etc/puppetlabs/puppet/hiera.yaml || echo true')
        # remove existing production environment
        on(host, '/usr/bin/test -d /etc/puppetlabs/code/environments/production && /bin/rm -fr /etc/puppetlabs/code/environments/production || echo true')
        # re-create production environment directory
        on(host, '/usr/bin/test ! -d /etc/puppetlabs/code/environments/production && mkdir -p /etc/puppetlabs/code/environments/production || echo true')
        # copy control-repo
        on(host, 'cp -r /tmp/production/{.git,environment.conf,hiera.yaml,hieradata,manifests,site,modules}  /etc/puppetlabs/code/environments/production/')
      end
    end

### Beaker serverspec tests

Next one can add serverspec tests for specific roles:

    # spec/acceptance/puppetmaster_spec.rb
    require 'spec_helper_acceptance'

    describe 'puppetmaster' do
      let(:manifest) {
        <<-EOS
          include role::puppetmaster
        EOS
      }
      it 'should run forst time with changes and without errors' do
        result = apply_manifest(manifest, :catch_failures => true)
        expect(@result.exit_code).to eq 2
      end
      it 'should run a second time without changes' do
        result = apply_manifest(manifest, :catch_changes => true)
        expect(@result.exit_code).to eq 0
      end
      # here one can add more serverspec tests
    end

Now we need to changes the default beaker acceptance testing rake task as we want to run tests on a control-repository.

    # Rakefile
    # beaker is designed to run all tests on multiple nodes
    # we have another usecase: run single tests on one host, then next test on new fresh host
    Rake::Task[:beaker].clear
    RSpec::Core::RakeTask.new(:beaker) do |config|
      puts 'dont use beaker, use beaker_roles:<role> or all_roles instead'
      abort
    end

    # iterate over acceptance tests and create namespaced rake tasks
    namespace :beaker_roles do
      # find all acceptance tests
      Dir.glob("spec/acceptance/*_spec.rb") do |acceptance_test|
        # find role part of file name
        test_name = acceptance_test.split('/').last.split('_spec').first
        RSpec::Core::RakeTask.new(test_name) do |t|
          t.rspec_opts = ['--color']
          t.pattern = acceptance_test
        end
      end
    end

### Running beaker and acceptance tests

Now we can run the acceptance tests:

    bundle exec rake beaker_roles:puppetmaster

This command only uses the `default.yml` nodeset.
If we want to use the `vagrant.yml` nodeset we must tell beaker to do so by providing an environment variable:

    BEAKER_set=vagrant bundle exec rake beaker_roles:puppetmaster

In addition to `BEAKER_set` there are some other useful environment variables:
Usually beaker deletes the container/virtual machine after running tests (even after failed tests). To keep the instance alive just add `BEAKER_destroy=no` environment variable.

If one needs more information on what is happening during beaker running, it is possible to enable debug mode by specifiying `BEAKER_debug=true`

Happy testing on your control-repository.

example42 wishes everybody a happy christmas.

Martin Alfke
