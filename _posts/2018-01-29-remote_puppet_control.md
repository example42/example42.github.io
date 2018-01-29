---
layout: blog
title: Tip of the Week 57 - All the ways to remotely trigger Puppet runs (with or without Puppet tasks)
---

Example42's [psick control-repo](https://github.com/example42/psick) has several features which makes easier the life of the Puppet administrator.

Since the release of [Puppet Tasks](https://puppet.com/resources/solution-brief/puppet-tasks) [several infrastructure commands](https://forge.puppet.com/example42/psick/tasks) have been added as tasks in the [psick module](https://github.com/example42/puppet-psick):

- psick::system_update - Update all packages on a system
- psick::puppet_unlock - Remove Puppet lockfiles
- psick::puppet_install - Install Puppet agent on a node
- psick::puppet_enable_noop - Enable noop option in Puppet agent config
- psick::puppet_agent - Run Puppet agent on a node

In this post we review the different ways we can use to remotely trigger a Puppet task and (in this case psick::puppet_agent but can be any task from any [module](https://forge.puppet.com/modules?with_tasks=true)):

1. Use the [bolt](https://github.com/puppetlabs/bolt) command (OSS)
2. Use the [puppet task](https://puppet.com/docs/pe/2017.3/orchestrator/running_tasks_from_the_command_line.html) command (PE)
3. Run Puppet tasks from Puppet Enterprise Web console
4. Directly interact with PE Orchestrator APIs

The above methods allow execution of any Puppet task, if we "just" want to trigger Puppet agent execution on a remote node, we have some other, more or less classic, additional options:

1. Run Puppet from PE Web Console for single nodes
2. Use MCollective
3. Use Ansible, Fabric or any other [unattended] remote execution tool
4. Run Puppet Use PCP broker and a custom PXP agent module

In the examples here we use a single target node, but can be defined use multiple nodes or the ones identified by a [PQL](https://puppet.com/docs/puppetdb/5.1/api/query/v4/pql.html) query.

## Tasks via bolt command line (OSS)

Bolt is the most direct tool we can use to remotely run Puppet tasks as it doesn't need any agent installed on the target node.

Syntax to run a given task (psick::puppet_agent) on a given node (git.lab.psick.io) accessed via ssh as specified user (bolt, but can any user on the remote node which has our local ssh public key added to its authorized_hosts):

    bolt task run psick::puppet_agent environment=host --modules /local/path/to/modules/ --user bolt remove -n git.lab.psick.io

    git.lab.psick.io:

    Info: Using configured environment 'host'
    Info: Retrieving pluginfacts
    Info: Retrieving plugin
    Info: Loading facts
    Info: Caching catalog for git.lab.psick.io
    Info: Applying configuration version 'af0e48e - PE File Sync Service, Mon Jan 15 21:41:10 2018 +0100 : code-manager deploy signature: 'da3956ed288ad2573fc8cec722330e5618514525''
    Notice: Applied catalog in 0.80 seconds

## Tasks via puppet task command (PE)

If we have Puppet Enterprise we can use the puppet task subcommand. Which requires [token based authentication](https://puppet.com/docs/pe/2017.3/rbac/rbac_token_auth_intro.html) and interacts directly with Puppet orchestrator APIs (on port 8143 on the PE Puppet Server):

    puppet task run psick::puppet_agent -n git.lab.psick.io

    Starting job ...
    New job ID: 395
    Nodes: 1

    Started on git.lab.psick.io ...
    Finished on node git.lab.psick.io
      STDOUT:
        Info: Using configured environment 'host'
        Info: Retrieving pluginfacts
        Info: Retrieving plugin
        Info: Loading facts
        Info: Caching catalog for git.lab.psick.io
        Info: Applying configuration version 'af0e48e - PE File Sync Service, Mon Jan 15 21:41:10 2018 +0100 : code-manager deploy signature: 'da3956ed288ad2573fc8cec722330e5618514525''
        Notice: Applied catalog in 0.73 seconds

    Job completed. 1/1 nodes succeeded.
    Duration: 11 sec

## Tasks via PE Web Console

From Puppet Enterprise 2017.3.0 onwards it's possible to select tasks from the modules available on the PE server. Click on the RUN - Task menu to access an easy to use web interface where to choose the tasks to run. Note that from the RUN - Puppet menu entry it's possible to trigger a Puppet run on a emote node using the native method based on PXP.

The list of Puppet Jobs executed (both tasks and puppet runs) are visible from the INSPECT - Jobs menu entry or via the command:

    puppet job show

For more details check the [official documentation](https://puppet.com/docs/pe/2017.3/orchestrator/running_tasks_in_the_console.html)


## Tasks via Orchestrator APIs

Finally we can query directly the PE[Orchestrator API](https://puppet.com/docs/pe/2017.3/orchestrator/orchestrator_api_v1_endpoints.html), which as with the puppet job command, requires a [token](https://puppet.com/docs/pe/2017.3/rbac/rbac_token_auth_intro.html) and proper [RBAC permissions](https://puppet.com/docs/pe/2017.3/rbac/managing_access.html).

The generated token has to be added to the http headers of our API calls.

Tasks have a specific API endpoint: the command endpoint.

Task parameters are added to the payload of the request. Affected nodes can be listed as array.

The following example shows how to build the `curl` command call:

    curl -k -X POST \
      -H "Content-Type: application/json" \
      -H 'X-Authentication:<token>' \
      https://<mom or compile master>:8143/orchestrator/v1/command/task \
      -d '{
        "environment" : "production",
        "task" : "psick::puppet_agent",
        "params" : {
          "noop" : true,
          "puppet_master" : "<compile master to use for this specific agent run>"
        },
        "scope" : {
          "nodes" : ["<node1>", "<node2>"]
        }
      }'

This will return the following Output:

    {
      "job" : {
        "id" : "https://<mom or compile master>:8143/orchestrator/v1/jobs/12",
        "name" : "12"
      }
    }

Read result from job:

    curl -k -X GET \
      -H 'X-Authentication:<token>' \
      https://<mom or compile master>:8143/orchestrator/v1/jobs/12

End of output while still running:

      "node_count" : 1,
      "node_states" : {
        "running" : 1
      }

End of output when finished:

      "node_count" : 1,
      "node_states" : {
        "finished" : 1
      }

Read node results:

    curl -k -X GET \
      -H 'X-Authentication:<token>' \
      https://<mom or compile master>:8143/orchestrator/v1/jobs/12/nodes

Output:

    {
      "items" : [ {
        "finish_timestamp" : "2018-01-24T14:41:14Z",
        "transaction_uuid" : null,
        "start_timestamp" : "2018-01-24T14:40:18Z",
        "name" : "<node1>",
        "duration" : 55.795,
        "state" : "finished",
        "details" : { },
        "result" : {
                  "_output" :
                  "\u001B[0;32mInfo: Using configured environment 'production'\u001B[0m\n
                  \u001B[0;32mInfo: Retrieving pluginfacts\u001B[0m\n
                  \u001B[0;32mInfo: Retrieving plugin\u001B[0m\n
                  \u001B[0;32mInfo: Loading facts\u001B[0m\n
                  \u001B[0;32mInfo: Caching catalog for <node1>\u001B[0m\n
                  \u001B[0;32mInfo: Applying configuration version '7a4be91 - Alessandro Franceschi, Sun Jan 14 18:15:44 2018 +0100 : run acceptance tests also for newer puppet versions (#220) (#221)'\u001B[0m\n
                  \u001B[mNotice: /Stage[main]/Psick::Dns::Resolver/File[/etc/resolv.conf]/content: \n
                  --- /etc/resolv.conf\t2018-01-24 14:31:51.428194104 +0000\n
                  +++ /tmp/puppet-file20180124-20270-1wxros6\t2018-01-24 14:40:44.602327849 +0000\n
                  @@ -1,3 +1,3 @@\n-# Generated by NetworkManager\n
                  -search pe.psick.io\n-nameserver 10.0.2.3\n
                  +#File managed by Puppet\n
                  +nameserver 8.8.8.8\n
                  +nameserver 8.8.4.4\n
                  \u001B[0m\n
                  \u001B[0;32mInfo: Computing checksum on file /etc/resolv.conf\u001B[0m\n
                  \u001B[0;32mInfo: FileBucket got a duplicate file {md5}b9dfc6d9764870be83fe35ecf2cfc5f3\u001B[0m\n
                  \u001B[0;32mInfo: /Stage[main]/Psick::Dns::Resolver/File[/etc/resolv.conf]: Filebucketed /etc/resolv.conf to puppet with sum b9dfc6d9764870be83fe35ecf2cfc5f3\u001B[0m\n
                  \u001B[mNotice: /Stage[main]/Psick::Dns::Resolver/File[/etc/resolv.conf]/content: \n
                  \u001B[0m\n\u001B[mNotice: /Stage[main]/Psick::Dns::Resolver/File[/etc/resolv.conf]/content: content changed '{md5}b9dfc6d9764870be83fe35ecf2cfc5f3' to '{md5}3ccdb679ea166bdf52104b3ae3a4499d'\u001B[0m\n
                  \u001B[mNotice: Applied catalog in 29.16 seconds\u001B[0m\n"
        },
        "latest-event-id" : 41,
        "timestamp" : "2018-01-24T14:41:14Z"
      } ],
      "next-events" : {
        "id" : "https://<node1>:8143/orchestrator/v1/jobs/14/events?start=42",
        "event" : "42"
      }
    }


## Remote Puppet agent run using other methods (not as tasks)

All the above cases can be applied to any task, but if we just need to remotely trigger a Puppet agent execution, various other ways are available.

We have already seen how it possible to trigger Puppet runs (not as tasks) from the PE Web Console, possible from the RUN - Puppet menu entry, or, for a specific node, directly from the details page (Run Puppet link).

It has been possible for long to run Puppet (and do a lot of other actions) via [MCollective](https://puppet.com/docs/pe/2017.3/managing_mcollective/invoking_mcollective_actions.html).

We can also use Ansible, Fabric, or other tools for orchestration or remote command execution.

On PSICK for example, this is possible, if using Fabric, with:

    fab puppet.agent:host=git.lab.psick.io

Finally it's potentially possible to trigger Puppet runs (and potentially other commands) directly via the PCP Broker and eventually a custom PXP Module.

ATTENTION: this solution is NOT working at the moment as the PCP broker is not yet opened and documented.

First we need a pxp-agent module on the nodes. An example can be found in the [pxp-agent repository](https://github.com/puppetlabs/pxp-agent/blob/master/modules/pxp-module-puppet.md) and this is actually basically the only existing one (and the one currently used under the hood when remote Puppet run is triggered from the PE Console Web interface).

For development purpose the module can be executed locally:

    sudo echo "{\"input\":{\"flags\":[\"--noop\", \"--server=puppet.pe.psick.io\"]}, \"configuration\" : {\"puppet_bin\" : \"/opt/puppetlabs/bin/puppet\"}}" | /etc/puppetlabs/pxp-agent/modules/puppet_agent run

The following is not working, as the API is unknown. Could be something similar to the following:

    curl -k -X POST \
      -H "Content-Type: application/json" \
      -H 'X-Authentication:0MDuxrsDQnQbzGn1P_4sWu4hgzg8AvQk0sebRuReGiZI' \
      https://puppet.pe.psick.io:8142/orchestrator/v1/command/task \
      -d '{
        "properties" : {
          "notify_outcome" : true,
          "module" : "puppet_agent",
          "action" : "run",
          "params" : {
            "flags" : [ "--noop" ]
          }
        },
        "required" : ["transaction_id", "notify_outcome", module", "action"],
        "additionalProperties" : false
      }'

We have a [ticket at Puppet open](https://tickets.puppetlabs.com/browse/PCP-830) for opening PCP broker API.

## Conclusion

As we have seen there are multiple ways to remotely trigger a Puppet agent execution from a central node and there are various ways to trigger a Puppet task to achieve the same result.

The ability to orchestrate Puppet execution can affect our choices on how we decide to manage how infrastructure via Puppet, allowing many combination of options, such as:

  - Normal Puppet agent running every [30] minutes + On request remotely triggered Puppet runs
  - Normal Puppet agents 30 minutes in noop mode + On request no-noop Puppet runs
  - Puppet runs triggered on Canary nodes during CI
  - Puppet runs only on request, without always running agents
  - Staged rollouts of configurations via remotely orchestrated Puppet runs.

Note that in most of the above examples we can see the result of the Puppet run only after it has ended and not in real-time.

Happy Puppet orchestration, with or without PSICK,

Martin Alfke

Alessandro Franceschi
