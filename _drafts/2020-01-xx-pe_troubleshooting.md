---
layout: blog
title: Puppet Tip 114 - Managing Puppet Enterprise: Part 2 - Log Files 
---

In the previous blog post we have seen what are the main services present in a Puppet Enterprise (PE) server, here we are going to give a look at their logs.

All Puppet Enterprise log files are under the `/var/log/puppetlabs` directory.

Here there are different subdirectories and log files for each single component.

* Table of content
{:toc}


## Puppet Server: /var/log/puppetlabs/puppetserver/

Directory `/var/log/puppetlabs/puppetserver` contains the logs of the Puppet Server component. 

### /var/log/puppetlabs/puppetserver/puppetserver.log

This is probably the most important and used log file of Puppet Enterprise. It contains information on all the Puppet Server activities:

- When a catalog is compiled for a client
- Eventual warnings or errors during the compilation of a catalog
- The Commands submitted to PuppetDB (replace_facts, replace_catalog, store_report)
- Information about the Code deployment activities

This log should be analysed to troubleshoot the following issues:

- Code Deployments failures (from the logs it's possible to verify if code has been successfully deployed and, in case of errors, the underlying reason)
- Recurring warnings on catalog compilations (WARNings, are generally not an issue but should be reviewed regularly and possibly cleaned up)
- Catalog compilation ERRORs, which prevent the Master from sending a valid catalog to clients

You can change Puppet Server's logging behavior by editing `/etc/puppetlabs/puppetserver/logback.xml`, and you can specify a different Logback config file in global.conf.  See:  https://puppet.com/docs/puppetserver/6.1/config_file_logbackxml.html for details.
 
 
Logs relevant to catalog compilation look like this:

    2019-01-14T10:57:48.774Z WARN  [qtp223287217-100574] [puppetserver] Puppet Unknown variable: '::nisdomainname'. (file: /etc/puppetlabs/code/environments/production/modules/network/manifests/global.pp, line: 49, column: 15)

Format is:

- Datetime
- Log level (INFO, WARN, ERROR...) The default log level is **INFO**, and Puppet Server sends nothing to syslog.
- An unique identifier for each catalog compilation (in the example is qtp223287217-100574): use it with `grep` to identify all the messages related to a single client catalog compilation. This is useful on busy Puppet Masters where logs related to different clients are mixed on puppetserver.log. So, for example, to have the full list of log messages related to the above sample line run: `grep qtp223287217-100574 /var/log/puppetlabs/puppetserver/puppetserver.log` 
- The name of the involved puppetserver subsystem (always [puppetserver] in logs concerning Puppet runs
- The actual log message

#### Sample Puppet catalog compilation log.

Here's a sample log of all the activities related to a single client catalog compilation:

    2019-01-14T11:27:47.616Z INFO  [qtp223287217-100708] [puppetserver] Puppet 'replace_facts' command for node1.example.com submitted to PuppetDB with UUID 2d4b60f5-1853-42b4-8d01-d5604af34ebc

This line refers to the command **replace_facts** sent to PuppetDB by the Server. It's the first activity done by the server when it rreceives catalog compilation requests: it copies to PuppetDB all the updated client facts and then it uses them when compiling the catalog.

    2019-01-14T11:27:48.313Z WARN  [qtp223287217-100708] [puppetserver] Puppet Unrecognized escape sequence '\/' (file: /etc/puppetlabs/code/environments/production/modules/logging/manifests/logrotate.pp, line: 151, column: 128)
    2019-01-14T11:27:48.313Z WARN  [qtp223287217-100708] [puppetserver] Puppet Unrecognized escape sequence '\/' (file: /etc/puppetlabs/code/environments/production/modules/logging/manifests/logrotate.pp, line: 151, column: 128)
    2019-01-14T11:27:48.313Z WARN  [qtp223287217-100708] [puppetserver] Puppet Unrecognized escape sequence '\/' (file: /etc/puppetlabs/code/environments/production/modules/logging/manifests/logrotate.pp, line: 151, column: 128)
    2019-01-14T11:27:50.152Z WARN  [qtp223287217-100708] [puppetserver] Puppet Unknown variable: '::nisdomainname'. (file: /etc/puppetlabs/code/environments/production/modules/network/manifests/global.pp, line: 49, column: 15)

All the above warning have been produced by the Puppet Server while compiling the client's catalog based on the client facts and the currently deployed Puppet code and Hiera data.

Warnings like `'Unrecognized escape sequence'` can usually be ignored as they might be due to necessary escape (\) chars used in commands or Windows path referred in Puppet manifests. In some cases they are hard to fix as we might actually need such escape chars in that shape, in other cases some workarounds can be tried. 

Warnings like `'Puppet Unknown variable'` should deserve some more attention. They happen when we try to use in Puppet code a variable which is not set. In some cases this is due to lazy checks on variables existence, in other they might be due to a missing value for other, unwanted reasons. In any case they are worth a check and a fix, even if they might not actually be a problem.

If you have the Puppet parameter `strict_variables` set to `true` all the above `'Puppet Unknown variable'` warnings would cause a catalog compilation failure.

    2019-01-14T11:27:50.892Z INFO  [qtp223287217-100708] [puppetserver] Puppet Inlined resource metadata into static catalog for node1.example.com in environment production in 0.01 seconds

This entry states that Puppet has generated metadata for file resources with a puppet:/// source. This happens when [static catalogs](https://puppet.com/docs/puppet/6.0/static_catalogs.html) are used (as default in recent Puppet versions) and the contents of files with the source argument are directly placed in the catalog instead of being requested by the client to the server when the catalog is applied.

In short words: you will always see this line when static catalogs are used.

    2019-01-14T11:27:50.892Z INFO  [qtp223287217-100708] [puppetserver] Puppet Compiled static catalog for node1.example.com in environment production in 3.12 seconds

This line states that the Server has successfully compiled the catalog for the client (here node1.example.com) and that it took 3.12 seconds.

Use a command like: `grep 'Puppet compiled' /var/log/puppetlabs/puppetserver/puppetserver.log` to have a quick overview of the catalog compilation times (the same information is available via the PE console anyway).

    2019-01-14T11:27:50.892Z INFO  [qtp223287217-100708] [puppetserver] Puppet Caching catalog for node1.example.com

This means that the server has started to send the catalog back to the client.

    2019-01-14T11:27:51.241Z INFO  [qtp223287217-100708] [puppetserver] Puppet 'replace_catalog' command for node1.example.com submitted to PuppetDB with UUID 24849581-5ca3-489d-ad19-3860a6bd141d

At the same time, the Puppet Server, as it did for facts, sends the catalog also to PuppetDB (only the last version of the catalog and facts is stored on PuppetDB). This allows us to query PuppetDB for each resource on each client, and, for example, have the possibility to view each node's graph on the PE console.

    2019-01-14T11:28:09.045Z INFO  [qtp223287217-100708] [puppetserver] Puppet 'store_report' command for node1.example.com submitted to PuppetDB with UUID 70b67f83-d796-41df-97c2-3f5f4fbb051c

This is the last log line concerning a single Puppet run, it's shown some time after the previous ones and it indicates that the Puppet Server has sent the content of the Puppet run report received from the client after the local catalog application.


#### Sample code deployment log (with success)

This is a sample output of a log puppetserver.log during the deployment of Puppet code via Code Manager.

    2019-01-14T11:25:54.294Z INFO  [qtp1096095702-961] [p.c.app] Queuing deploy for environment production
    2019-01-14T11:25:54.333Z INFO  [deploy-pool-1] [p.c.core] Attempting to deploy environment 'production'...

The above lines appear as soon as a Code Manager deployment is triggered, either via a webhook or the command line.

The next lines appear only after the code has been successfully deployed or failed. They may appear some minutes later.

    2019-01-14T11:29:44.794Z INFO  [deploy-pool-1] [p.c.core] Successfully staged environment 'production':

This happens when the code has been successfully deployed to the `/etc/puppetlabs/code-stating` directory.

    2019-01-14T11:29:47.778Z INFO  [clojure-agent-send-off-pool-1796] [p.e.s.f.file-sync-versioned-code-core] Running pre-commit hook command: /opt/puppetlabs/server/bin/generate-puppet-types.rb
    2019-01-14T11:29:47.956Z INFO  [clojure-agent-send-off-pool-1796] [p.e.s.f.file-sync-storage-core] Committing staging directory /etc/puppetlabs/code-staging to file sync storage service
    2019-01-14T11:29:48.064Z INFO  [clojure-agent-send-off-pool-1796] [p.e.s.f.file-sync-storage-core] Committing submodules in directory 'environments' for repo :puppet-code
    2019-01-14T11:29:48.065Z INFO  [clojure-agent-send-off-pool-1796] [p.e.s.f.file-sync-storage-core] Committing submodule :production
    2019-01-14T11:29:51.432Z INFO  [clojure-agent-send-off-pool-1796] [p.e.s.f.file-sync-storage-core] Committing the following changes:
    Added Files: modules/data/hiera/hosts/node1.example.com.yaml, modules/data/hiera/hosts/node2.example.com.yaml, modules/data/hiera/hosts/node4.example.com.yaml, modules/data/hiera/hosts/node3.example.com.yaml, modules/profile/hiera/hosts/ ...(10 of 256 files shown)
    Removed Files: modules/profile/manifests/options.pp, modules/hiera/host/lnp6d1gitrdb03.example.com.yaml ...(10 of 44 files shown)
    Changed Files: .r10k-deploy.json, modules/profile/files/context.xml ...(10 of 620 files shown)

This is the list of the changes occurred on the deployed control-repo files (this specific deployment has been done after several days, so many files have changed. Usually they are much less)

    2019-01-14T11:29:51.606Z INFO  [clojure-agent-send-off-pool-1796] [p.e.s.f.file-sync-storage-core] Completed commit in submodule at environments/production
    2019-01-14T11:29:51.607Z INFO  [clojure-agent-send-off-pool-1796] [p.e.s.f.file-sync-storage-core] Committing repo /etc/puppetlabs/code-staging
    2019-01-14T11:29:51.608Z INFO  [clojure-agent-send-off-pool-1796] [p.e.s.f.file-sync-storage-core] Committing the following changes:
    Added Files:
    Removed Files:
    Changed Files:
    Added Submodules:
    Updated Submodules: production
    2019-01-14T11:29:51.610Z INFO  [clojure-agent-send-off-pool-1796] [p.e.s.f.file-sync-storage-core] Completed commit of repo :puppet-code
    2019-01-14T11:29:51.721Z INFO  [deploy-pool-1] [p.c.file-sync] committed environment production with environment commit 'e59927f2c0f92c3af375642f69d016d88b10c9ea' and code commit '82aa94684fb1abc6f07b7ae74c11635f7e2be209'
    2019-01-14T11:29:51.842Z INFO  [deploy-pool-1] [p.c.core] Finished deploy attempt for environment 'production'.

This message confirms that the code has been successfully deployed to the `/etc/puppetlabs/code` directory

    2019-01-14T11:29:54.524Z INFO  [clojure-agent-send-off-pool-1796] [p.e.s.f.file-sync-client-core] Fetching ':production' to e59927f2c0f92c3af375642f69d016d88b10c9ea
    2019-01-14T11:29:55.504Z INFO  [clojure-agent-send-off-pool-1796] [p.e.s.f.file-sync-client-core] New latest commit: e59927f2c0f92c3af375642f69d016d88b10c9ea
    2019-01-14T11:29:55.506Z INFO  [clojure-agent-send-off-pool-1796] [p.e.s.f.file-sync-client-core] Fetching ':puppet-code' to 82aa94684fb1abc6f07b7ae74c11635f7e2be209
    2019-01-14T11:29:55.532Z INFO  [clojure-agent-send-off-pool-1796] [p.e.s.f.file-sync-client-core] New latest commit: 82aa94684fb1abc6f07b7ae74c11635f7e2be209
    2019-01-14T11:29:55.642Z INFO  [clojure-agent-send-off-pool-1796] [p.e.s.f.file-sync-client-core] Forcefully syncing live directory at /etc/puppetlabs/code for repository :puppet-code

The above messages notify that the code has been synced to the other compile master or replica servers, if they exist.

    2019-01-14T11:29:57.741Z INFO  [clojure-agent-send-off-pool-1796] [p.s.j.puppet-environments] Marking environment 'production' as expired.
    2019-01-14T11:29:57.741Z INFO  [clojure-agent-send-off-pool-1796] [p.s.j.puppet-environments] Marking environment 'production' as expired.
    2019-01-14T11:29:57.741Z INFO  [clojure-agent-send-off-pool-1796] [p.s.j.puppet-environments] Marking environment 'production' as expired.
    2019-01-14T11:29:57.741Z INFO  [clojure-agent-send-off-pool-1796] [p.s.j.puppet-environments] Marking environment 'production' as expired.

When code is successfully deployed the relevant environment cache is flushed, so that Puppet Server ensures that an updated code is used to compile catalogs.

### /var/log/puppetlabs/puppetserver/puppetserver-access.log

This log contains all the http requests done from clients to the Puppet Server (remember, all communications from clients to server's port 8140 is via https).

Log format is similar to a normal web server log and may give useful information. A sample line looks like:

    10.199.33.29 - - [14/Jan/2019:13:51:13 +0000] "GET /puppet/v3/file_metadata/modules/pe_infrastructure/puppet-infrastructure?environment=production&links=manage&checksum_type=md5&source_permissions=ignore HTTP/1.1" 200 267 "-" "Puppet/6.0.4 Ruby/2.5.1-p57 (x86_64-linux)" 133

With the following fields:

- The client host IP address
- The remote log name (usually not set, so you see a -)
- The user name (not set, so -)
- The datetime
- The http request method (always GET, except when clients sends the puppet run reports, via a PUT)
- The requested URL (endpoint) on the server with the arguments passed (after the ? sign) and the protocol used (alway HTTP/1.1)
- The http status code (200 for any correct connection, 304 for cached replies, 5xx for server errors, 4xx for authentication/access errors)
- The response's content lenght in bytes
- The referer (always - here)
- The client user agent (here you can see the client's Puppet version)

This logfile format and place is configured in `/etc/puppetlabs/puppetserver/request-logging.xml` 

Even if this log contains useful and interesting information about the http traffic on the server, it's not commonly used, as the puppetserver.log gives better, application level, insights.
Could be used, anyway, to generate statistics with tools that parse normal http access logs.

### /var/log/puppetlabs/puppetserver/code-manager-access.log

This log contains the logs of all the http requests made to the codemanager component. It shows a line for each attempted code deployment. Format is similar to the puppetserver/access.log one. Note that a 200 status code here doesn't involve necessarily a successful code deployment, but that a deployment activity has been successfully queued.
 
### /var/log/puppetlabs/puppetserver/puppetserver_gc.log.0.log

This log contains information about Garbage Collection on the JVM the Puppet Server is running on. Refer to docs like https://dzone.com/articles/understanding-garbage-collection-log for more details on how to interpret the output.

Note that messages like [GC (Allocation Failure) are relatively normal and, per se, not a sign or a failure. Proper analysis of these logs might be done to optimise and fine-tune JVM memory settings for the Puppet server. 

Check [https://puppet.com/docs/puppetserver/6.1/tuning_guide.html](https://puppet.com/docs/puppetserver/6.1/tuning_guide.html) for details on tuning PuppetServer.


## PuppetDB: /var/log/puppetlabs/puppetdb/

The directory `/var/log/puppetlabs/puppetdb/` contains the PuppetDB logs.

### /var/log/puppetlabs/puppetdb/puppetdb.log

This log contains all PuppetDB application logs. In particular, you can see here:

- All the commands submitted to Puppetdb
- The sync activities between the Master and the Replica Puppet DB servers
- PuppetDB internal activities such as flushing of stale reports, purging of deactivated nodes and database garbage collection events

A command log looks like:

    2019-01-14T14:20:37.836Z INFO  [p.p.command] [16827-1547475637809] [24 ms] 'replace facts' command processed for node3.example.com

Here we can see:
- The Datetime
- The log level
- The Component involved
- An unique ID
- The time spent in ms for the operation
- The PuppetDB command
- The certname for which the command was issued

Format, location, and rotation of this log is configured in `/etc/puppetlabs/puppetdb/logback.xml`.

#### /var/log/puppetlabs/puppetdb/puppetdb-access.log

Similarly to the `puppetserver-access.log`, this one contains http requests done to PuppetDB. It has the same combined log format and just gives an idea of the http traffic, without details on what happens at the application level.

Format, location, and rotation of this log is configured in `/etc/puppetlabs/puppetdb/request-logging.xml`.

#### /var/log/puppetlabs/puppetdb/puppetdb_gc.log.0.current

This log contains information about Garbage Collection on the JVM the PuppetDB is running on. What has been written about puppetserver_gc.log.0.current applies also here.

Check https://puppet.com/docs/puppetdb/5.1/maintain_and_tune.html for details on PuppetDB tuning.


## Console Services: /var/log/puppetlabs/console-services/

The directory contains `/var/log/puppetlabs/console-services/` the logs of PE Console, the web application we use to view and operate on Puppet Enterprise.

### /var/log/puppetlabs/console-services/console-services.log

This log contains console application logs. In particular you can see here:

- Autentication and user access attempts 
- Notices about sync of deployed Puppet classes to display in the Node classifier
- Eventual application stack traces

Use this log to troubleshoot issues related to access to web console or with class updates (when class deployed on the puppetserver environment dir are not visible on the console).

You don't see here details on the pages accessed by users.

Format, location, and rotation of this log is configured in `/etc/puppetlabs/console-services/logback.xml`.

### /var/log/puppetlabs/console-services/console-services-access.log

Similarly to the other access logs, this one contains http requests done to Puppet Console. It has the same combined log format and gives a better idea of the pages visited by the Console users.

Format, location, and rotation of this log is configured in `/etc/puppetlabs/console-services/request-logging.xml`.

### /var/log/puppetlabs/console-services/console-services-api-access.log

Similarly to the above one, this logs contains requests to the console API. In particular it's possible to see here http requests related to Jobs and Classifier activities.

It's configured in `/etc/puppetlabs/console-services/request-logging-api.xml`.

### /var/log/puppetlabs/console-services/console-services_gc.log.0.current

This log contains information about Garbage Collection on the JVM the PE Console is running on. What has been written about the other gc logs applies also here.

Check https://puppet.com/docs/pe/2019.0/config_console.html for details on configuring and tuning the PE console.


## Nginx: /var/log/puppetlabs/nginx/

Directory `/var/log/puppetlabs/nginx/` contains the logs of the NGINX webserver that acts as revers proxy to the PE Console.

### /var/log/puppetlabs/nginx/access.log

Typical web server access logs, contains basically the same requests found in `/var/log/puppetlabs/console-services/console-services-access.log` with the difference that here is possible to see the clients' IP (on console-services-access.log all the requests come from 127.0.0.1 which is this Nginx reverse proxy).

### /var/log/puppetlabs/nginx/error.log

Error logs of the NGINX proxy. Generally not much to see here, check it if you want to troubleshoot issues about which there are no traces in other places.


## Puppet Enteprise Installer: /var/log/puppetlabs/installer/

The directory `/var/log/puppetlabs/installer/` contains the logs produced by the Puppet Enterprise installer, used both to install and upgrade a PE instance. They basically contain the output of the puppet-enterprise-installer script, when executed. File names are based on the creation date.


## Orchestration Services: /var/log/puppetlabs/orchestration-services/

The directory `/var/log/puppetlabs/orchestration-services/` contains the logs of PE orchestration service, responsible for managing and scheduling jobs (remote Puppet runs, jobs and plans) execution.

### /var/log/puppetlabs/orchestration-services/orchestration-services.log

This log contains the orchestration service application logs. In particular you can see here:

- Minimal info about created job IDs
- Notices about deletion of old jobs and plans
- Eventual application services stack traces

Use this log to troubleshoot issues related to application orchestration.

Format, location, and rotation of this log is configured in `/etc/puppetlabs/orchestration-services/logback.xml`.

### /var/log/puppetlabs/orchestration-services/orchestration-services-access.log

Similarly to the other access logs, this one contains http requests done to Puppet orchestration service.

Format, location, and rotation of this log is configured in `/etc/puppetlabs/orchestration-services/request-logging.xml`.

### /var/log/puppetlabs/orchestration-services/orchestration-services-api-access.log

Similarly to the above one, this log contains requests to the orchestration API. In particular, it's possible to see here http requests related to Jobs and Classifier activities.

It's configured in `/etc/puppetlabs/orchestration-services/request-logging-api.xml`.

### /var/log/puppetlabs/orchestration-services/orchestration-services_gc.log.0.current

This log contains information about Garbage Collection on the JVM the PE orchestration service is running on. What has been written about the other gc logs applies also here.

## PostgreSQL: /var/log/puppetlabs/postgresql/

The directory `/var/log/puppetlabs/postgresql/` contains the logs of the PostgreSQL instance shipped with Puppet Enterprise.

These are standard PostgreSQL logs.

### /var/log/puppetlabs/postgresql/pgstartup.log

Generated at startup it just informs of the new log files locations.

### /var/log/puppetlabs/postgresql/postgresql-WEEKDAY.log

The actual PostgreSQL log files, rotated on a weekly base. They contain information about:

- Connections and disconnections to PostgreSQL
- Indexing operations    
- Checkpoint operations
- Eventual problems

Refer to this file if you have problems of access between PuppetDB and PostgreSQL.


## CLIENT LOGS

The following logs refer to all the Puppet agents, so they exist both on the Master and the clients.

### /var/log/messages 

/var/log/messages (or whatever log is used by syslog for normal system messages) contains the output of the Puppet runs. 

It's the same output seen when running `puppet agent -t` from the command line or what is visible on the reports on the PE console

### /var/log/puppetlabs/pxp-agent/pxp-agent.log

Is the log of the pxp-agent service with is running along with the puppet service on each node.

This service handles communication with the pxp-broker on the Puppet Master through which jobs and remote puppet runs are triggered.

In this log you can see information about:

- Tasks, remote puppet runs and plans triggerred as Jobs on the PER Console
- Maintenance notes about caches and temp dirs purging



That's enough about logs. Hope you survived.

So long and thanks for all the puppets.

Alessandro Franceschi