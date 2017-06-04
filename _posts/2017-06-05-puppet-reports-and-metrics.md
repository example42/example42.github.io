---
layout: blog
title: Tip of the Week 23 - Puppet reports and metrics
---

Any Puppet infrastructure must be monitored and needs log checking.  
For monitoring we can re-use existing solutions like cacti, checkmk, icinga, monit, munin, nagios, sensu, zabbix (see also Wikipedia)[https://en.wikipedia.org/wiki/Comparison_of_network_monitoring_systems].

Every puppet agent has locally stored important information for your puppet infrastructure. Most of these informations are stored inside the ```statedir```.

    puppet agent --configprint statedir
    /opt/puppetlabs/puppet/cache/state

    tree /opt/puppetlabs/puppet/cache/state
    /opt/puppetlabs/puppet/cache/state
    |- classes.txt
    |- graphs
    |- last_run_report.yaml
    |- last_run_summary.yaml
    |- resources.txt
    |- state.yaml
    \- transactionstore.yaml

One wants to check not only for running puppet agent, but also for proper catalog retrieval. This can be achieved by analyzing the ````last_run_summary.yaml``` file.

For logchecking it is possible to re-use your exiting log infrastructure like syslog-ng, elasticsearch or splunk. Within a basic puppet installation logfiles are written to the ```logdir``` setting.

    puppet master --configprint logdir
    /var/log/puppetlabs/puppetserver

    tree /var/log/puppetlabs/puppetserver
    /var/log/puppetlabs/puppetserver
    |- masterhttp.log
    |- puppetserver-access.log
    \- puppetserver.log

Most important is the ```puppetserver.log``` files **deprecation messages**. These messages inform you of upcoming incompatibilities with your puppet code.

    grep deprecated /var/log/puppetlabs/puppetserver/puppetserver.log
    2017-05-28 13:29:30,563 WARN  [clojure-agent-send-pool-0] [puppetserver] Puppet Support for ruby version 1.9.3 is deprecated and will be removed in a future release. See https://docs.puppet.com/puppet/latest/system_requirements.html#ruby for a list of supported ruby versions.
    2017-05-28 13:31:05,084 WARN  [qtp1631527616-56] [puppetserver] Puppet /etc/puppetlabs/puppet/hiera.yaml: Use of 'hiera.yaml' version 3 is deprecated. It should be converted to version 5
    2017-05-28 13:31:05,105 WARN  [qtp1631527616-56] [puppetserver] Puppet Defining environment_data_provider='hiera' in environment.conf is deprecated
    2017-05-28 13:31:05,698 WARN  [qtp1631527616-56] [puppetserver] Puppet Defining "data_provider": "hiera" in metadata.json is deprecated
    2017-05-28 13:31:06,377 WARN  [qtp1631527616-56] [puppetserver] Puppet Defining "data_provider": "hiera" in metadata.json is deprecated. It is ignored since a 'hiera.yaml' with version >= 5 is present
    2017-05-28 13:31:07,767 WARN  [qtp1631527616-56] [puppetserver] Puppet The function 'hiera_hash' is deprecated in favor of using 'lookup'. See https://docs.puppet.com/puppet/5.0/reference/deprecated_language.html


Still most of these tools don't give you an insight on Puppet internal status or provide information about all changes of your infrastructure. This is where the Puppet reporting frontends come into place.

There are several possible solutions available:

As Puppet Enterprise user you will get the Puppet Enterprise Console installed automatically. On Puppet Open Source no webinterface will get installed automatically.

For both platforms it is possible to make use of other open source developments:

  - (Puppet Board)[https://github.com/voxpupuli/puppetboard]
  - (Puppet Explorer)[https://github.com/dalen/puppet-explorer]

Both webinterfaces require PuppetDB configured as reporting backend. This is easily possible by setting the reports setting in puppet.conf for the puppet server to 'puppetdb'

    [server]
    reports = puppetdb

There is one major difference between PuppetBoard/PuppetExplorer and the Puppet Entrprise Console: PuppetBoard/PuppetExplorer only have read access to PuppetDB. They are not designed to be able to work as External Nodes Classifier.

With Puppet 5 there is another possible source of information where you can receive insights of your Puppet server status: the Puppet server **metrics backend**.

This backend was originally available on Puppet Enterprise only and has been ported to Puppet Open Source.

The following settings must be activated:

    #/etc/puppetlabs/puppetserver/conf.d/puppetserver.conf
    # enable metrics in http-client
    http-client: {
      metrics-enabled: true
    }

    #/etc/puppetlabs/puppetserver/confd/metrics.conf
    metrics: {
    # a server id that will be used as part of the namespace for metrics produced
    # by this server
    server-id: localhost
    registries: {
        puppetserver: {
            # specify metrics to allow in addition to those in the default list
            #metrics-allowed: ["compiler.compile.production"]

            reporters: {
                # enable or disable JMX metrics reporter
                jmx: {
                    enabled: true
                }
                # enable or disable Graphite metrics reporter
                graphite: {
                    enabled: true
                }
            }

        }
    }
    # this section is used to configure settings for reporters that will send
    # the metrics to various destinations for external viewing
    reporters: {
        graphite: {
            # graphite host
            host: "127.0.0.1"
            # graphite metrics port
            port: 2003
            # how often to send metrics to graphite
            update-interval-seconds: 5
        }
    }

Now you can follow the description from PE site regarding (installation of grafana dashbord)[https://docs.puppet.com/pe/latest/puppet_server_metrics.html].

Martin Alfke
