---
layout: blog
title: Tip of the Week 78 - What you need to know about Puppet facts. Part 5 - facter.conf
---

We end our series of blog posts about what is essential to know about Facter with some notes about the often forgotten Facter's configuration file  ```/etc/puppetlabs/facter/facter.conf``` (on Windows systems: ```C:\ProgramData\PuppetLabs\facter\etc\facter.conf```).

If you missed the previous posts, you can read them here:
- [Part 1 - Facter and core facts](https://www.example42.com/2018/05/28/what-you-need-to-know-about-puppet-facts-part-1-core_facts/)
- [Part 2 - Custom facts](https://www.example42.com/2018/06/04/what-you-need-to-know-about-puppet-facts-part-2-custom_facts/)
- [Part 3 - External facts](https://www.example42.com/2018/06/11/what-you-need-to-know-about-puppet-facts-part-3-external_facts/)
- [Part 4 - Trusted facts](https://www.example42.com/2018/06/18/what-you-need-to-know-about-puppet-facts-part-4-trusted_facts/)


### The forgotten (and useful) configuration file

Do not worry if you didn't even know that Facter has a configuration file which permits the configuration of rather interesting and useful features.

It has been introduced from Version 3, and by default it's not even created when  Facter is installed, so it's up to us to create and configure it (typically via Puppet).

```facter.conf``` is written in [Hocon](https://en.wikipedia.org/wiki/HOCON) format, and has 3 main sections:

- **facts** where we configure facts groups and policies on how to cache or distribute them
- **global** where we defines the paths where facter looks for  and if to include some kind of core_facts
- **cli** where are managed facter cli command outputs

A sample output may look as follows:

    facts : {
        blocklist : [ "file system", "EC2" ],
        ttls : [
            { "operating system" : 2 days },
        ]
    }

    global : {
        external-dir     : [ "path1", "path2" ],
        custom-dir       : [ "custom/path" ],
        no-exernal-facts : false,
        no-custom-facts  : false,
        no-ruby          : false
    }

    cli : {
        debug     : false,
        trace     : true,
        verbose   : false,
        log-level : "warn"
    }


### Configuring caching and exclusions

The most useful and interesting settings can be set under the **facts** section, here we can configure, with the ```ttls``` key, a caching Time To Live for each listed fact group, so that Facter doesn't have to resolve all the facts of that group every time is executed (that is, at least at every Puppet run).

Here we can also completely exclude from execution, with the ```blocklist``` key, whole groups of facts.

We can see the list of all the cacheable groups, with the ```ttls``` key, (with the relevant facts) with:

    facter --list-block-groups

    EC2
      - ec2_metadata
      - ec2_userdata
    GCE
      - gce
    Xen
      - xen
      - xendomains
    augeas
      - augeas
      - augeasversion
    desktop management interface
      - dmi
      - bios_vendor
      - bios_version
      - bios_release_date
      - boardassettag
      - boardmanufacturer
      - boardproductname
      - boardserialnumber
      - chassisassettag
      - manufacturer
      - productname
      - serialnumber
      - uuid
      - chassistype
    disk
      - blockdevices
      - disks
    file system
      - mountpoints
      - filesystems
      - partitions
    fips
      - fips_enabled
    hypervisors
      - hypervisors
    id
      - id
      - gid
      - identity
    kernel
      - kernel
      - kernelversion
      - kernelrelease
      - kernelmajversion
    load_average
      - load_averages
    memory
      - memory
      - memoryfree
      - memoryfree_mb
      - memorysize
      - memorysize_mb
      - swapfree
      - swapfree_mb
      - swapsize
      - swapsize_mb
      - swapencrypted
    networking
      - networking
      - hostname
      - ipaddress
      - ipaddress6
      - netmask
      - netmask6
      - network
      - network6
      - macaddress
      - interfaces
      - domain
      - fqdn
      - dhcp_servers
    operating system
      - os
      - operatingsystem
      - osfamily
      - operatingsystemrelease
      - operatingsystemmajrelease
      - hardwaremodel
      - architecture
      - lsbdistid
      - lsbdistrelease
      - lsbdistcodename
      - lsbdistdescription
      - lsbmajdistrelease
      - lsbminordistrelease
      - lsbrelease
      - macosx_buildversion
      - macosx_productname
      - macosx_productversion
      - macosx_productversion_major
      - macosx_productversion_minor
      - system32
      - selinux
      - selinux_enforced
      - selinux_policyversion
      - selinux_current_mode
      - selinux_config_mode
      - selinux_config_policy
    path
      - path
    processor
      - processors
      - processorcount
      - physicalprocessorcount
      - hardwareisa
    ssh
      - ssh
      - sshdsakey
      - sshrsakey
      - sshecdsakey
      - sshed25519key
      - sshfp_dsa
      - sshfp_rsa
      - sshfp_ecdsa
      - sshfp_ed25519
    timezone
      - timezone
    uptime
      - system_uptime
      - uptime
      - uptime_days
      - uptime_hours
      - uptime_seconds
    virtualization
      - virtual
      - is_virtual
      - cloud

The list of the blockable groups, via the ```blocklist``` key is shorter:

    facter --list-block-groups

    EC2
      - ec2_metadata
      - ec2_userdata
    file system
      - mountpoints
      - filesystems
      - partitions
    hypervisors
      - hypervisors

The configuration of caching or blocking of groups of facts can save a lot of time during Facter execution but we can still disable caching or blocking with, respectively, the following command line arguments:

    facter --no-cache
    facter --no-block

### Global and cli settings

The other keys we can configure on ```facter.conf``` can be used to manage the general behaviour of the ```facter command```, all of them can be set or overridden via arguments specified in the command line.

The **global** settings are the following:

- ```external-dir``` A list of directories to search for external facts (equivalent to the cli argument ```--external-dir```)
- ```custom-dir``` A list of directories to search for custom facts (equivalent to ```--custom-dir```)	 
- ```no-external-facts``` If true, prevents Facter from searching for external facts. (Default false, when set to ```true``` is equivalent to argument ```--no-external-facts```)
- ```no-custom-facts``` If true, prevents Facter from searching for custom facts. (Default false, when set to ```true``` is equivalent to argument ```--no-custom-facts```)
- ```no-ruby``` If true, prevents Facter from loading facts written in Ruby.  (Default false, when set to ```true``` is equivalent to argument ```--no-ruby```)

The **cli** settings are the following:

- ```debug``` If true, Facter outputs debug messages. (Default false, when set to ```true``` is equivalent to cli argument ```--debug```)
- ```trace``` If true, Facter prints stack traces from errors arising in your custom facts. (Default false, when set to ```true``` is equivalent to cli argument ```--trace```)
- ```verbose``` If true, Facter outputs its most detailed messages. (Default false, when set to ```true``` is equivalent to cli argument ```--verbose```)
- ```log-level``` Sets the minimum level of message severity that gets logged. Valid options: “none”, “fatal”, “error”, “warn”, “info”, “debug”, “trace”. Equivalent to cli argument ```--log-level```

### Conclusions

We have reached the last post of our series about "What you need to know about Facter".

We have reviewed the most important things to know about Facter and also some more or less known features or capabilities.

Facter has seen continuous improvements in the last years, both in terms of performance (facts written in C++ and caching/blocking from version 3) and flexibility (structured and external facts from version 2) and we hope to have helped you in understanding how to make the best use out of them.

Alessandro Franceschi
