---
layout: blog
title: Test driven Puppet infrastructure deployment
created: 1298925679
---
<p>A server infrastructure can't be considered fully operative if it's not monitored in some way. <br />Various tools are available in the market and they cover different facets of the common monitoring needs (alerting, trending, performance, security...) but whatever&#160; is your choice you need to configure them in some way.</p><p>One of the nice side effects of having modules that include automatic monitoring functions, such as the Example42 ones, is that while deploying a Puppet infrastructure you add the relevant checks to your monitoring software so that you can quickly understand what is working out of the box and what has to be fixed.</p><p>All the Example42 Puppet modules provide built in monitoring features, you can activate them just by setting the <strong>$monitor</strong> variable to "<strong>yes</strong>" (whatever the method you use to define and classify nodes) and at least one <strong>$monitor_tool</strong>.</p><p>An unique feature of the Example42 modules is the <strong>abstraction</strong> that is embedded in all the modules, so that it's quite easy and quick to introduce new monitoring tools without having to modify anything in the modules.</p><p>Typically a module has 2 kind of checks enabled by default: its listening port, if it is a network service, and its process name, for example, in the samba module you have:</p><pre>    monitor::port { "samba_${samba::params::protocol}_${samba::params::port}": 
        protocol =&gt; "${samba::params::protocol}",
        port     =&gt; "${samba::params::port}",
        target   =&gt; "${samba::params::monitor_target_real}",
        enable   =&gt; "${samba::params::monitor_port_enable}",
        tool     =&gt; "${monitor_tool}",
    }
    
    monitor::process { "samba_process":
        process  =&gt; "${samba::params::processname}",
        service  =&gt; "${samba::params::servicename}",
        pidfile  =&gt; "${samba::params::pidfile}",
        enable   =&gt; "${samba::params::monitor_process_enable}",
        tool     =&gt; "${monitor_tool}",
    }</pre><p>Even if not excessively obvious, from the above lines we can deduce:<br />- Two custom defines are used to specify what to check (a port and a process)<br />- The arguments given to the defines are obtained via qualified variables set in the <strong>samba::params </strong>class<br />- The user variable <strong>$monitor_tool</strong> specifies the monitoring tool(s) to be used for the above resources.</p><p>Currently the Example42 Puppet modules support various tools (you can define them using an array): <strong>Nagios, Munin, Monit, Collectd </strong>and<strong> Puppi</strong>.</p><p>They are actually different by nature and scope but the most interesting ones to actually check if something is working as expected are Nagios and, in some way, Puppi.</p><p>Besides port and process checking, for these two tools is possible to define also URL tests based on pattern matching, so that you can actually check different functionalities of your web application checking if custom urls contain specific strings.</p><p>An example of Url check:</p><pre>&#160;&#160;&#160; monitor::url { "Url-Example42_TestDatabase":
&#160;&#160;&#160;&#160;&#160;&#160;&#160; url&#160;&#160;&#160;&#160;&#160; =&gt; "http://www.example42.com/testdb.php",
&#160;&#160;&#160;&#160;&#160;&#160;&#160; port&#160;&#160;&#160;&#160; =&gt; '80',
&#160;&#160;&#160;&#160;&#160;&#160;&#160; target&#160;&#160; =&gt; "${fqdn}",
&#160;&#160;&#160;&#160;&#160;&#160;&#160; pattern&#160; =&gt; 'Database OK',
&#160;&#160;&#160;&#160;&#160;&#160;&#160; enable&#160;&#160; =&gt; "true",
&#160;&#160;&#160;&#160;&#160;&#160;&#160; tool&#160;&#160;&#160;&#160; =&gt; "${monitor_tool}",
&#160;&#160;&#160; }</pre><p>If the http://www.example42.com/testdb.php page contains the string "Database OK" the check is positive. Note that the host on which is run the check is defined with the target argument. Note also that if you set enable to false, the check is removed/disabled.</p><p>Another available check is for mount points. With a define like:</p><pre>&#160;&#160;&#160; monitor::mount { "/var/www/repo":
&#160;&#160;&#160;&#160;&#160;&#160;&#160; name&#160;&#160;&#160; =&gt; "/var/www/repo",
&#160;&#160;&#160;&#160;&#160;&#160;&#160; fstype&#160; =&gt; "nfs",
&#160;&#160;&#160;&#160;&#160;&#160;&#160; ensure&#160; =&gt; mounted,
&#160;&#160;&#160;&#160;&#160;&#160;&#160; options =&gt; "defaults",
&#160;&#160;&#160;&#160;&#160;&#160;&#160; device&#160; =&gt; "nfs.example42.com:/data/repo",
&#160;&#160;&#160;&#160;&#160;&#160;&#160; atboot&#160; =&gt; true,
&#160;&#160;&#160; }</pre><p>you both mount and monitor the specified resource.</p><p>A proper test driven infrastructure does not only checks if the services delivered by Puppet are running or the mount points are mounted, it verifies also HOW they work.<br />You can have Apache running but the web application failing in one or more elements. While the basic service/port checks are automatically added when is included the relevant module, for more accurate tests you need to write some (Puppet) code.<br />For this the monitor::url define is useful for web applications but we haven't still identified a good method to abstract application specific tests (for example: is ldap/mysql/activemq responding correctly?), performance and security checks, proactive failure detection and other generally needed features.<br />Probably there's not a real way to abstract certain specificities and some custom approach, strictly related to the software used and the contingency, is required.</p><p>One possible approach to manage arbitrary checks could be to consider Nagios plugins as de facto standard and refer to them to handle custom checks, considering that they are used by different tools, besides Nagios, and are easily extendable.<br />Currently, in the Example42 module there's a monitor::plugin define, but its usage is not yet standardized and is more oriented to be used to manage plugins for software like Collectd or Munin rather than to refer to Nagios plugins, practice and operational needs will drive our choice for this point.</p><h2>Understanding the monitor module</h2><p>All the above references to the monitor classes or defines imply the usage of the Example42 monitor module.<br />This is an implementation entirely based on Puppet's DSL of a (strongly needed) monitor abstraction type. <br />Different approaches and implementations would be welcomed, as we think that for the Puppet ecosystem it would be advisable to define at least standard naming&#160; and syntax for the monitoring elements to be included in every module.</p><p>The Example42 monitor implementation prefers linearity and extendability over performance and optimization of resources.<br />The generic monitor defines are placed in files like:<br /><strong>monitor/manifests/process.pp</strong>, <strong>monitor/manifests/port.pp</strong>, <strong>monitor/manifests/url.pp</strong>.<br />Let's see for example <strong>monitor/manifests/port.pp:</strong></p><pre>define monitor::port (
    $port,
    $protocol,
    $target,
    $tool,
    $checksource='remote',
    $enable='true'
    ) {

[...]

    if ($tool =~ /nagios/) {
        monitor::port::nagios { "$name":
            target      =&gt; $target,
            protocol    =&gt; $protocol,
            port        =&gt; $port,
            checksource =&gt; $checksource,
            enable      =&gt; $enable,
        }
    }

    if ($tool =~ /puppi/) {
        monitor::port::puppi { "$name":
            target      =&gt; $target,
            protocol    =&gt; $protocol,
            port        =&gt; $port,
            checksource =&gt; $checksource,
            enable      =&gt; $enable,
        }
    }

}</pre><p>note that here according to the tool requested are called some specific functions that are configured in places like:</p><p><strong>monitor/manifests/port/nagios.pp</strong>, <strong>monitor/manifests/process/port.pp</strong> where are called the actual defines that "do" the checks.</p><p>Let's see for example <strong>monitor/manifests/port/nagios.pp:</strong></p><pre>define monitor::port::nagios (
    $target,
    $port,
    $protocol,
    $checksource,
    $enable
    ) {

    $ensure = $enable ? {
        "false" =&gt; "absent",
        "no"    =&gt; "absent",
        "true"  =&gt; "present",
        "yes"   =&gt; "present",
    }

    # Use for Example42 nagios/nrpe modules
    nagios::service { "$name":
        ensure      =&gt; $ensure,
        check_command =&gt; $protocol ? {
            tcp =&gt; $checksource ? {
                local   =&gt; "check_nrpe!check_port_tcp!localhost!${port}",
                default =&gt; "check_tcp!${port}",
            },
            udp =&gt; $checksource ? {
                local   =&gt; "check_nrpe!check_port_udp!localhost!${port}",
                default =&gt; "check_udp!${port}",
            },
        }
    }

    # Use for Camptocamp Nagios Module
    # nagios::service::distributed { "$name":
    #    ensure      =&gt; $ensure,
    #    check_command =&gt; $protocol ? {
    #        tcp =&gt; "check_tcp!${port}",
    #        udp =&gt; "check_udp!${port}",
    #        }
    # }

}</pre><p>Note that here you can choose different implementations of the specific module, so you are free to change the whole module to be used for a specific monitoring tool editing just these few files, for example if you don't like the Example42 Nagios module you can use the Camptocamp one just by changing the references in this file.<br />Note, incidentally, that the port check can be triggered either from the Nagios server or from the same monitored host via nrpe, according to the value of the <strong>checksource</strong> parameter.</p><p>In order to manage per site, per module and per role or host exceptions, the Example42 modules provide a fat but functional approach, generally managed in the params.pp class of each module.<br />You can basically manage if to enable or not monitoring for all the modules or also module by module by setting the value of some variables:</p><p>There are some "node-wide" variables you can set, their defaults are set in params.pp of each module:<br /><strong>$monitor_port</strong> (true|false) : Set if you want to enable port monitoring for the host.<br /><strong>$monitor_process</strong> (true|false) : Set if you want to enable process checking.<br /><strong>$monitor_target</strong> : Set the ip/hostname you want to use on an external monitoring server to monitor the host<br />These variables can be overriden on a per-module basis (needed, for example if you want to enable process monitoring for some service but not all):<br /><strong>$foo_monitor_port</strong> (true|false) : Set if you want to monitor foo's port(s). If any. Default: As defined in $monitor_port<br /><strong>$foo_monitor_process</strong> (true|false) : Set if you want to monitor foo's process. If any. Default: As defined in $monitor_process<br /><strong>$foo_monitor_target</strong> : Define how to reach (Ip, fqdn...) the host to monitor foo from an external server. Default: As defined in $monitor_target</p><p>Note that generally you really have not to care about them, as sensible defaults are set. But this it's important to note that with <strong>$monitor_target</strong> variable you can set HOW to reach the host to be monitored, by default is its <strong>$fqdn</strong>, but on multihomed nodes you might want to reach it via and alternative IP or name (possible defined or based on a fact value in order to avoid manual settings).</p>
<p>Finally note that for tools that imply a central monitoring node and a variety of nodes to check, we have introduced the possibility to define a "<em>grouplogic</em>" variable to automatically manage different monitoring servers according to custom groups of nodes.</p><p>Let's see how it works, for example for the Nagios module. <br />You just have to define a variable,<strong> $nagios_grouplogic, </strong>and set as value the name of another variable you use to group your nodes.&#160; For example you may want to have different Nagios servers according custom variables as zones, environments, datacenters etc (ie: $nagios_grouplogic = "env" ).<br />By default all the checks go to the same server (managed by the same PuppetMaster) if you define in $nagios_grouplogic the name of the variable you want to use as discrimitator, you will have different Nagios servers monitoring the group of nodes having the same value for that variable.<br /> Note that you need to add in the list below your own variable name, if is not already provided.</p><p> In <strong>nagios/manifests/params.pp</strong> you have:</p><pre>    # Define according to what criteria you want to organize
    # what nodes your Nagios servers monitor
         <strong>$grouptag</strong> = <strong>$nagios_grouplogic</strong> ? {
         ''            =&gt; "",
         'type'        =&gt; $type,
         'env'         =&gt; $env,
         'environment' =&gt; $environment,
         'zone'        =&gt; $zone,
         'site'        =&gt; $site,
         'role'        =&gt; $role,
    }</pre><p>In <strong>nagios/manifests/service.pp</strong> the define nagios::service used to specify every Nagios service check (as we've seen before) is:</p>
<pre>define nagios::service (
    $host_name = $fqdn,
    $check_command  = '',
    $service_description = '',
    $use = 'generic-service',
    $ensure = 'present' ) {

    require nagios::params

    # Autoinclude the target host class 
    include nagios::target

    # Set defaults based on the same define $name
    $real_check_command = $check_command ? {
        '' =&gt; $name,
        default =&gt; $check_command
    }

    $real_service_description = $service_description ? {
        '' =&gt; $name,
        default =&gt; $service_description
    }

    @@file { "${nagios::params::customconfigdir}/services/${host_name}-${name}.cfg":
        mode    =&gt; "${nagios::params::configfile_mode}",
        owner   =&gt; "${nagios::params::configfile_owner}",
        group   =&gt; "${nagios::params::configfile_group}",
        ensure  =&gt; "${ensure}",
        require =&gt; Class["nagios::extra"],
        notify  =&gt; Service["nagios"],
        content =&gt; template( "nagios/service.erb" ),
<strong>        tag     =&gt; "${nagios::params::grouptag}" ? {
            ''       =&gt; "nagios_service",
            default  =&gt; "nagios_service_$nagios::params::grouptag",
        },</strong>
    }

}</pre><p>In <strong>nagios/manifests/init.pp</strong>&#160; (used only on the Nagios servers) you collect exported resources with:</p><pre>    case $nagios::params::grouptag {
        "": {
        File &lt;&lt;| tag == "nagios_host" |&gt;&gt;
        File &lt;&lt;| tag == "nagios_service" |&gt;&gt;
        }
        default: {
<strong>        File &lt;&lt;| tag == "nagios_host_$nagios::params::grouptag" |&gt;&gt;
        File &lt;&lt;| tag == "nagios_service_$nagios::params::grouptag" |&gt;&gt;</strong>
        }
    }</pre><p>This lets you automatically deploy different Nagios servers monitoring different groups of nodes according to custom variables.<br />If you need to use a variable different from the ones already defined (type, env, environment, zone, site, role) just add a line in the selector shown in nagios/manifests/params.pp.Neat, isn't it?</p><p>In this article we have seen how to use Example42 modules to automatically monitor the resources included in Puppet managed nodes, how to add checks based on string patterns in Urls or mount points, how all this is done using a layer of abstraction that makes it possible to introduce a new monitoring tool that uses all the already present checks and how, de facto, systematic automatic monitoring implies a test driven deployment, since you find yourself checking what you want on your servers and you can quickly see, for example on your Nagios server, what is up and running and what needs to be fixed.</p><p>Further work in Example42 modules will be done in the development of support for other monitoring tools, in the definition of other abstract enough monitor defines and generally in exploring the possibilities to automate more specific and complete checks.</p>
