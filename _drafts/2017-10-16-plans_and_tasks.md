---
layout: blog
title: Tip of the Week 42 - Puppet plans and tasks
---

At [PuppetConf2017](https://puppet.com/community/events/puppetconf/puppetconf-2017) the [bolt](https://puppet.com/products/puppet-bolt) task runner was released and made public.

Bolt uses the concept of Puppet tasks to allow workflow based system management, which was missing in Puppet since ages.

Puppet itself uses the declarative state configuration model, describing the final state of a system. With declarative description it was always a pain adding workflow based configurations like application updates or running maintenance tasks only at specific times. Bolt fills this gap.

With bolt one can run any kind of:

  - upload files to a system
  - run any remote command
  - run any script
  - run a Puppet task
  - run a Puppet plan

Connection to remote systems is done either via ssh or WinRM. Other connectors can be added to bolt upstream development. At the moment there is no API available to add additional connectors to bolt via some kind of bolt plugin.
The ssh access must be configured in advance prior being able to make use of bolt. Access can be configured as unprivileged user using sudo commands. Bolt just needs to know which credentials to use.

Credentials for ssh can be placed in your ssh config file (```~/.ssh/config```). Credentials for Windows systems are provided on command line using the user (```--user```) and the password (```--password```) parameter.

Which systems bolt should connect to must be provided on cli with nodes (```--nodes```) parameter. As of now, no node groups can be specified.

## Upload files

Uploading files to a number of systems is easy:

    bolt file upload /local/file /remote/file --nodes www.domain.com,mail.domain.com

For Windows system the nodes must be given using the winrm URI:

    bolt file upload /local/file /remote/file --nodes winrm://win.domain.com,server.domain.com --user Administrator --password <password>

## Running remote commands

Running remote commands is easy. Just tell bolt which remote command to execute:

    bolt command run 'yum -y update' --nodes www.domain.com,mail.domain.com

## Running scripts

Bolt is able to use a local script, copy it to the mentioned nodes and run it there:

    bolt script run ~/update_system.sh --nodes www.domain.com,mail.domain.com

Please note that there is a difference to file upload: the script will be removed after execution.

## Writing and running tasks

Tasks are something different. Tasks are part of modules and are placed into the (```tasks```) directory. When running tasks with bolt, one must specify the task and the module name space and the module path:

    bolt task run <modulename>::<taskname> --nodes <node list> --modules <modulepath>

Additionally tasks may use parameters to switch action or behavior or to provde any kind of data.

e.g.

    bolt task run application::update_app apppath=/opt/app --nodes db.domain.com --modules ~/workspace/modules

The mentiones task (```application::update_app```) can be found within the application modules task directory in the update_app file.

    modules/
      \- application/
        \- tasks/
          \- update_app

A task must have an according .json file which documents the tasks and uses Puppet 4 data types on parameters:

    # modules/application/tasks/update_app.json
    {
      "description": "Update application",
      "supports_noop": false,
      "input_method": "environment",
      "parameters": {
        "apppath": {
          "description": "Path to application",
          "type": "Optional[String[1]]"
        }
      }
    }

Within the task the parameter is used as environment variable with PT_ prefix:

    # modules/application/tasks/update_app
    #!/usr/bin/env bash
    if [ -z "$PT_apppath" ]; then
      apppath=$PT_apppath
    else
      apppath='/opt/app'
    fi
    pushd $apppath
      git reset hard --master
      git fetch --all
      git pull origin master
    popd

When setting a parameter is mandatory, one can just use the task variable:

    #!/usr/bin/env bash
    updurl=$PT_updurl # will fail if no data was given
    pushd $apppath
      /opt/app/update.sh $updurl
    popd


When having many parameters it will become a nightmare to provide all on command line. One can place parameters and their valies to a .json file;

    # params.json
    {
      "updurl": "git@git.domain.com/application.git",
      "apppath": "/opt/app"
    }

Now you just must tell bolt that it should use the params.json file:

    bolt task run application::update_app --nodes db.domain.com --modules ~/workspace/modules --params @params.json

## Writing und running plans

Plans combine multiple plans. Think about the following problem:

Update of an application requires you to do the following steps:

  - disable node on loadbalancer
  - wait for last request to be served
  - update application
  - restart web server
  - check functionality
  - re-enable node on loadbalancer

Plans are - similar to tasks - part of a module and located in the (```plans```) directory.

    modules/
      \- application/
        \- plans/
          \- update.pp

we use the above mentioned example and generate a puppet plan:

    # modules/application/plans/update.pp
    plan application::update (
      String $lbserver  = 'lb.domain.com',
      String $maxtime   = '60',
      String $updurl    = 'ssh://git@git.domain.com/application.git',
      String $apppath   = '/opt/app',
      String $chkscript = '/opt/app/bin/check',
    ){
      # 'execute' tasks
      run_task('application::disable_node', $lbserver)
      run_task('application::wait_last_conn', $maxtime)
      run_task('application::update_app', $updurl, $apppath)
      run_task('application::restart_app', $maxtime)
      run_task('application::check_app', $chkscript)
      run_task('application::enable_node', $lbserver)
    }

Usually we want error handling in plans. Please check [writing plans](https://puppet.com/docs/bolt/0.5/writing_plans.html#handling-plan-function-results) for details.

Now the bolt plan command can be used:

    bolt plan run application::update --modules <modulepath> 

Check the [task docs](https://puppet.com/docs/bolt/0.5/writing_tasks.html) and [plan docs](https://puppet.com/docs/bolt/0.5/writing_plans.html) on additional topics like

  - enable no-op mode on tasks
  - use different plan execution functions:
    - commands, scripts or other plans, uploading files
  - input and output of tasks
  - using tasks input and output from and to plans
  - converting scripts to tasks

Happy hacking on bolt.

Martin Alfke
