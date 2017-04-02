---
layout: blog
title: Tip of the Week 14 - Puppet Continuous Integration with GitLab
---

[GitLab](https://gitlab.com) is a versatile Open Source tool to manage your code repositories.

It's often used on premise to host private code projects, something like a private GitHub.

We often use it to host our Puppet code and we have started to appreciate its multiple features, one of them is the integrated CI engine.

It's incredibly easy to use and powerful, you can design your CI pipeline in a file called ```.gitlab-ci.yml``` at the root directory of your control repo. GitLab will automatically interpret it whenever there are changes in your repo code, and try to use **GitLab CI runners** (agents running on, typically, separated servers where are run the actual CI operations).

Let's see how this file is structured, samples are from example42's [PSICK](https://github.com/example42/psick/blob/production/.gitlab-ci.yml), where the control-repo is tested in various ways on different phases.

Give a look at the [official documentation](https://docs.gitlab.com/ce/ci/) for more details on GitLab CI.

First, on ```.gitlab-ci.yml```, you define the stages of your pipelines, in the order you want them to be executed (note you can have more pipelines for your project, to use in different conditions (for example when there are changes at specific git branches) so not all stages you list here have to be in the same pipeline):

    stages:
      - checks
      - version_check
      - specs
      - diffs
      - sitedoc
      - integration
      - live_runs
      - merge_request
      - promote
      - rollout
      - postcheck

Then you define the jobs to do, they have a stage assigned, and for each of them you can run scripts, manage behavior, assign with tags a specific CI runner, and define on which branch they should be run.

    # Run Syntax Checks on Feature/Personal Branch and Development branch:
    # All branches excluded production and testing
    syntax:
      stage: checks                    # This is a stage previously defined
      before_script: "bin/gitlab_before.sh"     # A script to run before the tests
      script: "bin/puppet_check_syntax_fast.sh" # The actual test script, its
                                                # exit code defines jobs status
      tags:             # If you tag a job you force it to run on specific
        - test_puppet   # CI runners
      except:           # This defines the branches on which to NOT run the job
        - testing
        - production
      only:             # This defines the branches on which RUN the job
        - branches
      cache:            # On the runner you can cache specific directories
        untracked: true
        paths:
          - modules/    # Paths are relative to the git repo, here we cache
                        # the directory where external modules are placed via r10k

For each job, you have a similar syntax, and you can add options, for example to allow failures on a job (the pipeline is not interrupted in case of errors in the job):

    # Puppet lint tests.
    lint:
      stage: checks
      before_script:                # You can run multiple scripts using an
        - "bin/gitlab_before.sh"    # array like this
      script: "bin/puppet_lint.sh"
      cache:
        untracked: true
        paths:
        - modules/
      tags:
        - test_puppet
      except:
        - testing
        - production
      only:
        - branches
      allow_failure: true   # The job can fail without blocking the pipeline

You can have also manual steps, which are not automatically performed in the pipeline, and can be triggered manually from GitLab web interface:

    # Do Vagrant run. Start the machine, run the tests, halt the machine.
    # This will use a .vagrant dir under $HOME of the users so that
    # it will not be deleted accidentally  by gitlab-runner
    vagrant_checks:
      stage: integration
      before_script:
        - "bin/gitlab_before.sh"
      script:
        - "bin/vagrant_node_test.sh centos7.ci ci setup"
        - "bin/vagrant_node_test.sh centos7.ci ci drift"
      after_script:
        - "bin/gitlab_after.sh"
        - "bin/vagrant_node_test.sh centos7.ci ci halt"
      cache:
        untracked: true
        paths:
        - modules/
        - tests/
      allow_failure: true
      tags:
        - test_puppet
      only:
        - development
      when: manual       # This step can be run manually

In our sample we use customer scripts to automate Merge Requests and Accept from different branches.
In this example code is promoted automatically, if there weren't unallowed failures in the previous steps, from development to testing branch:

    # Development to testing merge request creation
    merge_request_testing:
      stage: merge_request
      script: "bin/gitlab_create_merge_request.rb development testing"
      tags:
        - deploy_puppet
      only:
        - development

    # Automatic Accept merge request from Development to testing
    merge_accept_testing:
      stage: promote
      script: "bin/gitlab_accept_merge_request.rb development testing"
      only:
        - development
      tags:
        - deploy_puppet
      when: on_success   # Do this only if there are no failures in the pipeline

Once merged in testing we can trigger Puppet runs on real servers and check the server's status:

    # On testing branch
    run_puppet_on_testing:
      stage: live_runs
      before_script:
        # Trigger remote Puppet runs via puppet job
        - "bin/puppet_job_run.sh testing"
        # Trigger remote Puppet runs via Rundeck
        #  - "bin/rundeck_job_run.sh testing"
      script:
        - "bin/puppetdb_env_query.sh testing" # Query PuppetDB for last run status
      tags:
        - deploy_puppet
      when: on_success
      only:
        - testing
      allow_failure: true

The actual deployment of Puppet code on the Puppet Server can be performed as a normal job too, achieving, if wanted, a Continuous Deployment solution.

In our case we use PE Code Manager or GitLab hooks to automatically deploy the Puppet control-repo code when there are changes in a branch, so, basically, Puppet code deployment to production is done whenever a change is merged in the production branch.

A nice touch, which can be automated too, is the generation on the control-repo documentation using puppet strings and publish it directly on GitLab pages:

    pages:
      stage: sitedoc
      script:
        - rm -rf doc public .yardoc
        - puppet strings generate site/\*\*/manifests/\*.pp site/\*\*/manifests/\*\*/\*.pp site/\*\*/manifests/\*\*/\*\*/\*.pp site/\*\*/functions/\*\*/\*.pp manifests/\*.pp
        - mv doc public
      tags:
        - deploy_puppet
      artifacts:
        paths:
        - public
        expire_in: '30 day'
      only:
        - production

These are just examples of what you can do in a pipeline for Continuous Integration of your Puppet code.

The workflow design, the stages, jobs and implementation are something that have to be adapted to each context, we are still exploring alternative approaches in terms of things to check (other jobs involve using catalog diff, tests on docker vms, spec tests...) and in the logic of the git workflow.

The approach used here, with Merge Requests from development to testing to production, may have better alternatives. Any suggestion?

Alessandro Franceschi
