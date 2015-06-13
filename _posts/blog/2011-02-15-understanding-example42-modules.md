---
layout: blog
title: Understanding Example42 modules 
created: 1297777255
---
<p>Example42 modules are based on a module template called "<strong>foo</strong>". They share a common structure that might seem too complex at first glance but once grasped few basic elements it results coherent, easy to manage and solid (so we like to think).<br />The main features of Example42 modules are:<br />- Support for <strong>different Operating Systems</strong>,<br />- <strong>Separation of custom code</strong> and logic from the module core,<br />- Extendible <strong>automatic monitoring</strong> for the resources provided by the module,<br />- <strong>Coherent structure</strong> with standard naming,<br />- <strong>Debugging </strong>functionalities,<br />- <strong>Plug &amp; Play</strong> approach with User variables that can change the module's behaviour.</p><p>The usage of a common foo template makes it possible to create a new full featured module very quickly, using the script<strong> 00_example42scripts/module_clone.sh </strong>.</p><p>The foo module template is an evolving skeleton for modules, new features are introduced with new versions and the approach is done in order ot make the "upgrade" of a module generated from an earlier foo version relatively easy. Currently the Puppet code is compatible both for version 0.25 and version 2.6, this is done for backward compatibility (the default Puppet version on many distros is still 0.2x) at the price of renouncing some of the new interesting features of Puppet 2.6. </p><h2>The foo module template structure</h2><p>Let's examine the <strong>foo module</strong>, once you understand it, you can grasp the logic behind all the other modules and cope with their apparently complex manifests.</p><p>The module's layout follows Puppet official <strong>standards</strong> and some community <strong>best practices</strong>.<br />At its root you can see the following elements:</p><pre>manifests/    # The directory with all the module's classes and defines
templates/    # The directory for the templates 
tests/        # The directory containing quick tests
Modulefile    # Metadata for the Module Forge
README        # General module's documentation</pre><p>Let's begin from the quick things.<br />The tests directory actually is not widely used at the moment, but is intended, in the future, to provide unit tests for the module's classes and defines. Currently in each test, there's just an "include classname". Nothing particularly relevant or exciting.</p><p>The templates directory contains a file called:</p><pre>templates/variables_foo.erb</pre><p>This is a template that shows all the variables used in the module and is placed on<strong> /var/lib/puppet/debug/variables/foo</strong> if you have the <strong>$debug</strong> variable set to <strong>yes</strong> (reccomended if you use Example42 modules, it helps a lot in troubleshooting variables scoping).</p><p>Then there's the manifests directory, which contains all the modules's classes and defines:</p><pre>init.pp              # Contains the main "foo" class
params.pp            # foo::params contains ALL the module's variables 
absent.pp            # foo::absent removes the foo package
disable.pp           # foo::disable stops the foo service
                     #   (both runtime and at boot)
disableboot.pp       # foo::disableboot removes foo service from boot
                     #   but doesn't check if is running
debug.pp             # foo::debug provides the debugging template 
monitor.pp           # foo::monitor describes what has to be monitored
                     #   for the foo application
monitor/absent.pp    # foo::monitor::absent decommits also monitoring
                     #   elements when you include foo::absent
backup.pp            # foo::backup describes what to backup of foo
backup/absent.pp     # foo::backup::absent decommits backup elements
firewall.pp          # foo::firewall describes what has to be firewalled
firewall/absent.pp   # foo::firewall::absent
conf.pp              # Generic foo::conf define for infile line
                     #   modifications of foo's main configuration file
example42.pp         # foo::example42 is the custom class where to place
                     #   all the customizations. This is renamed to your
                     #   $my_project by the project_rename.sh script
example42/monitor.pp # foo::example42::monitor for monitoring customizations
example42/backup.pp  # foo::example42::backup for backup customizations</pre><p>As you see there are quite a lot of classes but generally you have to touch just few of them, when you create a module from scratch, based on the foo template, and ideally you should not modify anything else than the example42 classes (renamed to your $my_project) when you have to use existing modules.</p><h2>It all starts from init.pp</h2><p>If you look inside a class you will see Puppet code that at first sight might look not clear. In all the classes in fact there's wide usage of <strong>qualified variables</strong> ( things like $foo::params::packagename ) that refer to the ones defined in the params class.<br />Let's see, for example how the main <strong>foo class</strong> present in <strong>init.pp </strong>is done, and how this class may actually include many of the other classes defined before if the right variables are set:</p><div class="highlight"><pre>#
# Class: foo
#
# Manages foo.
# Include it to install and run foo
# It defines package, service, main configuration file.
#
# Usage:
# include foo
#
class foo {

    # Load the variables used in this module. Check the params.pp file
    require foo::params

    # Basic Package - Service - Configuration file management
    package { "foo":
        name   =&gt; "${foo::params::packagename}",
        ensure =&gt; present,
    }

    service { "foo":
        name       =&gt; "${foo::params::servicename}",
        ensure     =&gt; running,
        enable     =&gt; true,
        hasrestart =&gt; true,
        hasstatus  =&gt; "${foo::params::hasstatus}",
        pattern    =&gt; "${foo::params::processname}",
        require    =&gt; Package["foo"],
        subscribe  =&gt; File["foo.conf"],
    }

    file { "foo.conf":
        path    =&gt; "${foo::params::configfile}",
        mode    =&gt; "${foo::params::configfile_mode}",
        owner   =&gt; "${foo::params::configfile_owner}",
        group   =&gt; "${foo::params::configfile_group}",
        ensure  =&gt; present,
        require =&gt; Package["foo"],
        notify  =&gt; Service["foo"],
        # content =&gt; template("foo/foo.conf.erb"),
    }

    # Include OS specific subclasses, if necessary
    case $operatingsystem {
        default: { }
    }

    # Include extended classes, if relevant variables are defined
    if $backup == "yes" { include foo::backup }
    if $monitor == "yes" { include foo::monitor }
    if $firewall == "yes" { include foo::firewall }

    # Include project specific class if $my_project is set
    # The extra project class is by default looked in foo module
    # If $my_project_onmodule == yes it's looked in your project module
    if $my_project {
        case $my_project_onmodule {
            yes,true: { include "${my_project}::foo" }
            default: { include "foo::${my_project}" }
        }
    }

    # Include debug class is debugging is enabled ($debug=yes)
    if ( $debug == "yes" ) or ( $debug == true ) { include foo::debug }

}</pre></div><p>Let's analyze what this class does:<br />- At the beginning it has a <strong>brief description</strong>, in <strong>Puppetdoc</strong> compliant standard.<br />- Then the first thing is the <strong>inclusion of foo::params</strong> where all the variables used later are defined. Foo::params is included in all the classes and represents the only point where modules variables are defined: both "internal variables" such as the <em>packagename</em> and "user variables" that are somehow "filtered" in foo::params which sets default values if these variables are not actually provided by users. This choice is done because we want "<strong>include and play</strong>" modules that work, with default settings, out of the box.<br />- Then there are the definitions of the main resources of the foo application: the <strong>package</strong>, the <strong>service </strong>and the <strong>main configuration file</strong>. Of course these may change from case to case if more resources have to be defined for a certain application (for example more packages or more configuration files). Just notice the wide usage of qualified variables and that the configuration file name (foo.conf) is just the name of the resource and not the pathname of the file, so that, for example, we will have a File resource called "samba.conf" in the Samba module, even if the actual filename is smb.conf (as defined by the samba::params::configfile variable).<br />- Then <strong>OS specific subclasses </strong>are included if necessary. This is done in modules where the difference between different distros or OS in managing an application are more radical than just names changes and require additional resources. Eventual OS specific classes are placed in different files with the fact name of the Operating system (ie: class foo::ubuntu placed in foo/manifests/ubuntu.pp).<br />- After there's the automatic inclusion of the so-called <strong>Example42 extended classes </strong>for <strong>monitoring</strong>, <strong>backup </strong>and <strong>firewalling</strong>. These classes are included if the relevant user variables are set to "yes", so you can also ignore them if you don't intend to use these extensions.<br />- Then there's the code that manages the autoloading of <strong>custom $my_project classes</strong>. The if and case constructs are just needed to load the $my_project class from a file present in the same module or from a dedicated "project related" module. By default the custom classes are placed in the application module (as seen before with the example42.pp file) but you can have them completely separated in a module called $my_project setting <strong>$my_project_onmodule</strong> to <strong>"yes</strong>".<br />- Finally there's the inclusion of the <strong>debug class </strong>if the <strong>$debug</strong> user variable is set to "<strong>yes</strong>".</p><p>In various cases (when to manage an application you just have to install a package, manage a service and deploy a configuration file) there's actually no need to touch the init.pp file at all, since all the OS relevant modifications are defined in the <strong>params.pp</strong> class. In other cases, further resources might be added or sub classes included, according to the module's logic and complexity.</p><h2>The relative beauty and absolute power of params.pp</h2><p>The params class might be considered the cornerstone of all the other classes, has a standard structure, whose content, obviously, changes according to the managed application. Let's see a default params class (the parts with [...] indicate omissis for uninteresting or reduntand parts):</p><div class="highlight"><pre>class foo::params  {

## DEFAULTS FOR VARIABLES USERS CAN SET
# (Here are set the defaults, provide your custom variables externally)
# (The default used is in the line with '')

## Example: Full hostname of foo server
    $server = $foo_server ? {
        ''      =&gt; "foo",
        default =&gt; "${foo_server}",
    }


## EXTRA MODULE INTERNAL VARIABLES
#(add here module specific internal variables)



## MODULE INTERNAL VARIABLES
# (Modify to adapt to unsupported OSes)

    $packagename = $operatingsystem ? {
        solaris =&gt; "CSWfoo",
        debian  =&gt; "foo",
        ubuntu  =&gt; "foo",
        default =&gt; "foo",
    }

    $servicename = $operatingsystem ? {
        debian  =&gt; "foo",
        ubuntu  =&gt; "foo",
        default =&gt; "foo",
    }

    $configfile = $operatingsystem ? {
        freebsd =&gt; "/usr/local/etc/foo/foo.conf",
        default =&gt; "/etc/foo/foo.conf",
    }

[...]

    $protocol = "tcp"
    $port = "80"
    

## DEFAULTS FOR MONITOR CLASS
# These are settings that influence the (optional) foo::monitor class
# You can define these variables or leave the defaults
# The apparently complex variables assignements below follow this logic:
# - If no user variable is set, a reasonable default is used
# - If the user has set a host-wide variable (ex: $monitor_target ) that one is set
# - The host-wide variable can be overriden by a module specific one (ex: $foo_monitor_target)

    # How the monitor server refers to the monitor target 
    $monitor_target_real = $foo_monitor_target ? {
        ''      =&gt; $monitor_target ? {
           ''      =&gt; "${fqdn}",
           default =&gt; $monitor_target,
        },
        default =&gt; "$foo_monitor_target",
    }

    # If foo port monitoring is enabled 
    $monitor_port_enable = $foo_monitor_port ? {
        ''      =&gt; $monitor_port ? {
           ''      =&gt; true,
           default =&gt; $monitor_port,
        },
        default =&gt; $foo_monitor_port,
    }

[...]

## FILE SERVING SOURCE
# Sets the correct source for static files
# In order to provide files from different sources without modifying the module
# you can override the default source path setting the variable $base_source
# Ex: $base_source="puppet://ip.of.fileserver" or $base_source="puppet://$servername/myprojectmodule"
# What follows automatically manages the new source standard (with /modules/) from 0.25 

    case $base_source {
        '': {
            $general_base_source = $puppetversion ? {
                /(^0.25)/ =&gt; "puppet:///modules",
                /(^0.)/   =&gt; "puppet://$servername",
                default   =&gt; "puppet:///modules",
            }
        }
        default: { $general_base_source=$base_source }
    }

}</pre></div><p>This class is divided in various parts:</p><p>DEFAULTS FOR VARIABLES USERS CAN SET<br />Here are enforced the default values for all the <strong>module specific </strong>variables users can set.<br />The syntax might look a bit verbose but that's what is currently needed to manage variables' value assignement (at least with a standard Puppet 0.2x).<br />Note that you set the value of the variable $server (that is <strong>$foo::params::server</strong>) according to the value of the user's variable <strong>$foo_server</strong>. The convention is to have all the users' variables prepended by the relevant module name (as foo_) and reassigned, in params.pp, with an omonimous variable without the foo_ prefix.<br />Note also how the  $foo::params::server value is defined: if $foo_server is null (that is if the user has not defined it) it has the default value "foo", otherwise it gets the value of $foo_server.<br />You might define many other module specific user variables that might be used in templates of in the module logic to autoload specific classes.</p><p>EXTRA MODULE INTERNAL VARIABLES<br />Here you might find other variables that are used internally in the module (the user has not to define them). They are placed here, before other more relevant parameters, because all the other following variables in the module are the same (with different values) in different modules.</p><p>MODULE INTERNAL VARIABLES<br />In this section you find all the variables that are used in the module's classes. As you can see different values can be given to valiables like <strong>$foo::params::packagename</strong>,&#160;  <strong>$foo::params::configfile</strong> etc. according to the underlining operating system.<br />On a simple module, just by changing these variables you can manage basic support for different operating systems.<br />This set of variables is the same on all the modules derived from the foo template and makes it quick and easy to clone new modules based on it.</p><p>DEFAULTS FOR MONITOR/BACKUP/FIREWALL CLASS<br />These 3 groups of variables manage the behaviour of the omonimous extended classes. You can ignore them if you don't use these features (shame! :-) . The horrendously verbous syntax used to assign their values is needed to set defaults if the user doesn't define neither a global variable (such as <strong>$monitor_target</strong> to define how to reach the node for monitoring purposes) nor a module specific variable (such as <strong>$foo_monitor_target</strong> to define the monitoring target to use only for the foo application). The default value of the variable that is actually used (<strong>$foo::params::monitor_target_real</strong>) in this example is <strong>${fqdn}</strong>.<br />The existing Example42 modules have a reasonable default for all these settings.</p><p>FILE SERVING SOURCE<br />Finally is defined the <strong>$general_base_source</strong> variable, which is the same in every module (it's repeated in order to make single modules reusable out of the whole Example42 set). This variable should be used whenever there's a "source" parameter to provide a location for file serving.<br />Note that by default this variable just set the correct naming for the current Puppet version, but you can define a site wide <strong>$base_source </strong>to provide static files from a different server.</p><h2>Disabling and removing modules</h2><p>Init.pp and params.pp are the most relevant manifests in the module, but there are various other manifest files that provide omonimous classes to manage common features. So of them have to inherit the main class in order to override specific resources, such as the service to manage in <strong>disable.pp</strong>:</p><pre>class foo::disable inherits foo {

    require foo::params

    Service["foo"] {
        ensure =&gt; "stopped" ,
        enable =&gt; "false",
    }

    # Remove relevant monitor entries
    if $monitor == "yes" { include foo::monitor::absent }

}</pre><p>Note that this class automatically includes the foo::monitor::absent class to decomission monitoring resources for the disabled service.<br />In all the modules based on the foo template there is also a <strong>foo::disableboot</strong> class that is identical to the above foo::disable but it hasn't the "ensure =&gt; stopped" argument.<br />You can use this class in all the cases where the specific service is not directly managed by Puppet, for example in clusters where there's the cluster software that starts services at boot and assures they are running on the desired node. Kris Buytaert has suggested to rename this class to a more elegant and meaningfull <strong>foo:unmanaged</strong>, maybe this will be done in future versions of the foo template (but we fear it might be too late).<br />In other cases, such as <strong>absent.pp</strong> we don't want (and need) to inherit the main class:</p><pre>class foo::absent {

    require foo::params

    package { "foo":
        name   =&gt; "${foo::params::packagename}",
        ensure =&gt; absent,
    }

    # Remove relevant monitor, backup, firewall entries
    if $monitor == "yes" { include foo::monitor::absent }
    if $backup == "yes" { include foo::backup::absent }
    if $firewall == "yes" { include foo::firewall::absent  }

    # Include debug class is debugging is enabled ($debug=yes)
    if ( $debug == "yes" ) or ( $debug == true ) { include foo::debug }

}</pre><p>Note that here we remove all the monitoring/backup/firewall resources but still include the debug class.</p><h2>Example42 extended classes</h2><p>Finally let's give a glimpse to the so-called <em>extended</em> (and embraced?) Example42 classes.<br />These are powerful meta-classes that let you automatically manage monitoring, firewalling and backup of the resources provided by the module, at the cost of some overhead in terms of number of resources applied to the node and the need, in most cases, of store configs support.<br />Let's see the most interesting manifest of the bunch, monitor.pp, we leave the original comments because they explain how to use the module's variables:</p><pre># Class: foo::monitor
#
# Monitors foo process/ports/service using Example42 monitor meta module (to be adapted to custom monitor solutions)
# It's automatically included and used if $monitor=yes and is defined at least one monitoring software in $monitor_tool
# This class permits to abstract what you want to monitor from the actual tool and modules you'll use for monitoring
# and can be used to quickly deploy a new monitoring solution that instantly notifies what's working and what's needs
# to be fixed (call it Test Driven Puppet Deployment, if you like ;-)
#
# Variables:
# The behaviour of this class has some defaults that can be overriden by user's variables:
# $foo_monitor_port (true|false) : Set if you want to monitor foo's port(s). If any. Default: As defined in $monitor_port
# $foo_monitor_url (true|false) : Set if you want to monitor foo's url(s). If any. Default: As defined in $monitor_url
# $foo_monitor_process (true|false) : Set if you want to monitor foo's process. If any. Default: As defined in $monitor_process
# $foo_monitor_plugin (true|false) : Set if you want to monitor foo using specific monitor tool's plugin  is. If any. Default: As defined in $monitor_plugin
# $foo_monitor_target : Define how to reach (Ip, fqdn...) the host to monitor foo from an external server. Default: As defined in $monitor_target
# $foo_monitor_url : Define the baseurl (http://$fqdn/...) to use for eventual foo URL checks. Default: As defined in $monitor_url
# 
# You can therefore set site wide variables that can be overriden by the above module specific ones:
# $monitor_port (true|false) : Set if you want to enable port monitoring site-wide.
# $monitor_url (true|false) : Set if you want to enable url checking site-wide.
# $monitor_process (true|false) : Set if you want to enable process monitoring site-wide.
# $monitor_plugin (true|false) : Set if you want to try to use specific plugins of your monitoring tools 
# $monitor_target : Set the ip/hostname you want to use on an external monitoring server to monitor this host
# $monitor_baseurl : Set baseurl to use for eventual URL checks of services provided by this host
# For the defaults of the above variables check foo::params
#
# Usage:
# Automatically included if $monitor=yes
# Use the variable $monitor_tool (can be an array) to define the monitoring software you want to use.
# To customize specific and more granular behaviours use the above variables and eventually your custom modulename::monitor::$my_project class
#
class foo::monitor {

    include foo::params

    # Port monitoring
    monitor::port { "foo_${foo::params::protocol}_${foo::params::port}": 
        protocol =&gt; "${foo::params::protocol}",
        port     =&gt; "${foo::params::port}",
        target   =&gt; "${foo::params::monitor_target_real}",
        enable   =&gt; "${foo::params::monitor_port_enable}",
        tool     =&gt; "${monitor_tool}",
    }
    
    # URL monitoring 
    monitor::url { "foo_url":
        url      =&gt; "${foo::params::monitor_baseurl_real}/index.php",
        pattern  =&gt; "${foo::params::monitor_url_pattern}",
        enable   =&gt; "${foo::params::monitor_url_enable}",
        tool     =&gt; "${monitor_tool}",
    }

    # Process monitoring 
    monitor::process { "foo_process":
        process  =&gt; "${foo::params::processname}",
        service  =&gt; "${foo::params::servicename}",
        pidfile  =&gt; "${foo::params::pidfile}",
        enable   =&gt; "${foo::params::monitor_process_enable}",
        tool     =&gt; "${monitor_tool}",
    }

    # Use a specific plugin (according to the monitor tool used)
    monitor::plugin { "foo_plugin":
        plugin   =&gt; "foo",
        enable   =&gt; "${foo::params::monitor_plugin_enable}",
        tool     =&gt; "${monitor_tool}",
    }

    # Include project specific monitor class if $my_project is set
    if $my_project { 
        case $my_project_onmodule {
            yes,true: { include "${my_project}::foo::monitor" }
            default: { include "foo::${my_project}::monitor" }
        }
    }

}</pre><p>Just notice how nothing in this class has application specific information: replace foo with apache and you have the monitoring class for apache based on settings defined in params.pp.<br />Consider that generally are activated (via the <strong>$monitor_*_enable</strong> variables set in params.pp) only the process and port checks. Url checks are quite useful to check web applications funnctionality but are seldom related to a module application and plugins are special cases used to monitoring tools that provide application oriented plugins.</p><p>Currently there are 5 monitor tools (with different scopes and usage fields) supported: <strong>Nagios</strong>, <strong>Munin</strong>, <strong>Collectd, Monit</strong> and <strong>Puppi</strong> (an Example42 module for applications deployments and local checks of services) but the nice side effect of this monitoring abstraction (note that in the above class we have defined WHAT to monitor, not HOW to monitor it) is that you just have to write the plugin for a new tool in the <strong>monitor module</strong> (more about it in another post) and you'll find yourself with all the monitoring elements already configured for it. <br />Note also that you can use different modules for the supported monitoring tools, for example you might use Immerda, DavidS or Camptocamp Nagios modules instead of the native Example42 one for Nagios monitoring.</p><h2>Isolation of customizations</h2><p>Among the various classes present in the foo template there are the ones called example42. Here we provide the possibility to customize the module behaviour without modifying other parts. The path to complete module's customization and resuability is far from being fulfilled, using custom "project" classes we have considered various issues.<br />The logic on how to provide configuration files and their content should not be enforced by a module. It varies too much according to specific environments, operating systems and needs. That's why the Example42 modules often don't provide by default the content of a configuration file, but just its general properties, such as path and&#160; permissions. HOW you want to provide that file should be defined in a custom class.<br />As we have seen custom classes are autoloaded if you define the variable <strong>$my_project</strong> (in this case its value is "example42"), these classes should inherit the main one only when they set some parameters for an already defined resources. If you just add new resources just don't have to inherit anything.<br />For example you might want to provide a static file according to a custom order:</p><pre>class foo::example42 inherits foo {
     File["foo.conf"] {
         source =&gt; [ "puppet:///foo/foo.conf-$hostname" ,
                     "puppet:///foo/foo.conf-$role" ,
                     "puppet:///foo/foo.conf" ],
     }
}</pre><p>or use a template:</p><pre>class foo::example42 inherits foo {
     File["foo.conf"] {
         content =&gt; template("foo/foo.conf.erb"),
     }
}</pre>
<p>Having a dedicated $my_project class to manage customizations permits better delegation of the management of Puppet code when different teams work on indipendent infrastructures that might share some common Puppet modules.<br />In this case each infrastructure is to be considered a different project.<br />To ease this kind of delegation the custom classes can be searched in a dedicated module, just set <strong>$my_project_onmodule</strong> to "yes" for this.</p><p>The use of custom classes faces one of the problems of modules' reasability and customization. Another one is how to provide data that is used by a module (variables values, source file paths and so on). Puppet 2.6 already natively provides the <strong>extlookup</strong> function that lets you dynamically define data sources (note that you can introduce and use extlookup in these custom classes, even if it's not used in the core classes) and some discussion is <a title="Data/Model Separation - Data in (and out of) Modules" href="https://projects.puppetlabs.com/issues/6079">ongoing</a> on how to separate the module data.</p><p>What is still unclear, at least to me, is how much people really need or want full module's reusability, and if they are likely to accept the extra complexity that this probably leads to. When using the Example42 modules in real scenarios I've seen that there's always the temptation of following the quick approach of placing custom assumptions in the core classes: it's easier and after all it doesn't prevent reusability (just copy, paste and modify where needed) but ... well, it's simply not the right way, at least concerning Example42 modules reusability ambition. More details on how to customize modules are <a title="Customize Example42 modules" href="http://www.example42.com/?q=node/5">here</a>.</p><h2>Who fears variables scoping issues?</h2><p>As you should have realized by now Example42 modules rely heavily on variables, both internal and user provided ones.<br />This somehow conflicts with some philosophical approaches emerging in the Puppet community such as facts-driven configuration or the endless fear of variables scoping issues.<br />Well let's underline some points:<br />- I don't think there's the <strong>right</strong> way to do things with Puppet. There are probably many <strong>wrong</strong> ways and there's the <strong>one</strong> you find comfortable with, that fits your infrastructure, needs and mindset.<br />- I'm conscious of some of Example42 modules <strong>limitations</strong>, for example the fact that they are not optimized for performance, their verbosity or some very inelegant constructs (see default enforcings in params.pp). Still there are design choices behind them: compatibility with Puppet 0.2x versions, quick cloning with just a find and replace script, abstraction, reusability and include&amp;play. These concepts have been expressed also in presentation at <a title="Puppet Modules Standards and Interoperability" href="http://lab42.it/presentations/puppetmodules/puppetmodules.html">PuppetCamp 2010 Europe</a> and <a title="Reuse Your Modules!" href="http://www.slideshare.net/Alvagante/reuse-your-puppet-modules-5403529">PuppetCamp 2010 SF</a>.<br />- <strong>Variables scoping issues</strong> are not generally due to modules organization but to how and where you define your variables and when you include your classes: under this point of view the use of qualified variables and the params class inside the module helps in having, at least in the module itself, a rigorous scoping coherency.<br />- There are <strong>various ways</strong> to "<em>define variables and include classes</em>", you can do that with external node classifiers, dedicated classes or whatever method I won't debate here. I've found reliable, scalable and well manageable an approach based on <strong>nodes inheritances</strong>, where you define and override variables at different levels of the inheritance tree, and <strong>ONLY AT THE END</strong> you include classes (typically a general class that include common classes and a role class that includes role specific classes).<br />You might also define role specific variables inside a role class, but always before including the classes that use them. Trust me, it's ages I don't face scoping problems with this appoach.<br />- If you use Example42 modules, turn on debugging (set <strong>$debug to "yes"</strong>). You will find in /var/lib/puppet/debug/variables/modulename all the variables used in your module and this lets you spot immediately during a Puppet run if some variable is not set as you want.</p><p>Any comment on this post and the solutions used in Example42 modules is very welcomed, more than once, in the past I've modified my "template module" and the approach used in designing modules. The same foo template is to be considered an evolving work in progress, that is going to follow Puppet evolution and new features. <br />Always open to redefine my Puppet beliefs, given the right motivations.</p>
