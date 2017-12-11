---
layout: blog
title: Tip of the Week 50 - Scheduling Puppet resources application
---

In our Puppet operations we may need to apply some resources only in given periods of time, such as maintenance windows, os specific days of the week of hour.

Puppet has a quite useful, and not too much known, resource for that: ```schedule```.

The schedule resource type can be used to define a time period. Once defined, by using the ```schedule``` metaparamter we can tell to Puppet to apply a given resource only when Puppet is running within the specified schedule.

For example, we can define a daily schedule from 2 AM to 4 AM, and also specify how many times a resource using such schedule should be applied via the ```repeat``` parameter, as follows:

    schedule { 'maintenance':
      range  => '2 - 4',
      period => daily,
      repeat => 1,
    }

and then apply to to any resource, via the schedule metaparameter:

    exec { '/usr/local/bin/daily_maintenance':
      schedule => 'maintenance',
    }

Note that such piece of code doesn't guarantee that the command is executed every day, and it doesn't ensure that this happens at a fixed time.

What will happen is that IF Puppet runs on a node, between 2 and 4 AM, THEN the maintenance exec is applied.

As every other resource type, we can declare as many instances of it as we want, they just need to have different titles.

The full list of attributes is:

    schedule { 'title':
      name        => # (namevar) The name of the schedule. The title is used if not set the name.
      period      => # The period of repetition for resources on this schedule, valid values:
                     # hourly, daily, weekly, monthly, never.
      periodmatch => # Whether periods should be matched by:
                     # - 'number' (IE: two times in an hour) or by
                     # - 'distance' (IE: two times which are 60 minutes apart)
      range       => # The hour (from 0 to 23) range when to apply a schedule.
                     # Midnight might be crossed with something like: 22:00 - 02:00
      repeat      => # How often a given resource may be applied in the schedule
      weekday     => # The days of the week in which the schedule occurs
    }

If we need to always run a specific command we probably better use ```cron``` on any similar system's scheduler, as in this case we have more control on when and if commands are executed.

There are still use cases for Puppet's resource type, for example we can use it to:

  - Manage different contents of configurations according to the hour or period
  - Trigger system reboots if conditions apply
  - Manage backups or other maintenance operations (given the described limitations)
  - Manage resources which take a long time to be applied and don't need be to continuously enforced
  - Do crazy things nobody has conceived before

Alessandro Franceschi
