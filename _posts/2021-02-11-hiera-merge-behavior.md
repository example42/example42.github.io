---
layout: blog
title: Puppet Tip 119 - Hiera merge behavior
---

Hiera v5 allows you to provide information regarding merge behavior in a couple of different ways.

Using different merge behaviors allows you to e.g. separate common (admin) users from application users by adding common users in common hiera layer and the application users into an application hiera layer.
This reduces duplicates in data and allow more simple data management.

Another example is installation of packages. You usually have a list of packages you need on all systems (admin packages) and some packages which are needed on special systems only.
Again you can mention all common packages in hiera common laxer and add node specific packages in node hiera layer.

In this posting we explain the different possible merge behaviors and their results.
Additionally we explain the options where you can set merge behavior.

* Table of content
{:toc}

# Hiera merge behavior options and the results

We will first have a look at all available merge options and explain the behavior and the result later in the explicit and automatic data explanations.

Hiera offers the following merge options:

* `first`
* `unique`
* `hash` and
* `deep`

All data examples assume that you have a hiera.yaml file using four hierarchies:

* node specific data
* application-stage specific data
* application specific data
* common data

Example for hiera config:

    version: 5
    defaults:
      datadir: data
      data_hash: yaml_data
    hierarchy:
      - name: "hiera hierarchies"
        paths: 
          - "nodes/%{trusted.certname}.yaml"
          - "application/%{::application}-%{::stage}.yaml"
          - "application/%{::application}.yaml"
          - "common.yaml"

## first

By default if no option is provided, hiera uses the `first` merge option.
Using `first` is not really a merge option as hiera will return the very first result of a key.

The data type of the result depends on the data type of hiera data.
e.g. if hiera finds a string, it will return a string, if it finds an array, it will return an array.

## unique

The `unique` merge option allows you to collect data from multiple hierarchies and returns the result as an array.
All elements in all matching hierarchies must be of data type array.

Now let's have a look at the hiera data:

In common you have a packages key:

    # data/common.yaml
    packages:
      - vim-enhanced
      - curl

In application level you also have a packages key:

    # data/application/mysql.yaml
    packages:
      - xtrabackup

The returned result for a packages key, using `unique` merge strategy will return the following values:

    packages:
      - vim-enhanced
      - curl
      - xtrabackup

Visualization:

| Result               | mysql              | common               |
|--------              |-------             |--------              |
| **packages:**        | **packages:**      | **packages:**        |
| ..**- vim-enhanced** |                    | ..**- vim-enhanced** |
| ..**- curl**         |                    | ..**- curl**         |
| ..**- xtrabackup**   | ..**- xtrabackup** |                      |

## hash

The `hash` merge option parses all matching hierarchies and returns a list of hashes.
All elements in all matching hierarchies must be of type hash.

Let's look at the data. In this case we manage users:

    # data/common.yaml
    users:
      martin:
        uid: 10012
        home: /mnt/home/martin
        shell: /bin/bash
      alessandro:
        uid: 10011
        home: /mnt/home/al
        shell: /bin/zsh

In application level, we also have users:

    # data/application/mysql.yaml
    users:
      simon:
        uid: 10013
        home: /home/simon
      martin: # mysql is different that common
        uid: 10012
        home: /home/martin

The hash key from highest hierarchy is taken first. other keys from lower hierarchies are just added.
If a hash key exists in several hierarchies, the one from the highest hierarchy is taken:

    # result
    users:
      simon:
        uid: 10013
        home: /home/simon
      martin: # mysql is different that common
        uid: 10012
        home: /home/martin
        shell: /bin/bash
      alessandro:
        uid: 10011
        home: /mnt/home/al
        shell: /bin/zsh

Visualization:

| Result                          | mysql                      | common                     |
|--------                         |-------                     |--------                            |
| **users:**                      | users:                     | users:                             |
| ..**simon:**                    | ..**simon:**               |                                    |
| ....**uid: 10013**              | ....**uid: 10013**         |                                    |
| ....**home: /home/simon**       | ....**home: /home/simon**  |                                    |
| ..**martin:**                   | ..**martin:**              | ..martin:                          |
| ....**uid: 10012**              | ....**uid: 10012**         | ....uid: 10012                     |
| ....**home: /home/martin**      | ....**home: /home/martin** | ....home: /mnt/home/martin         |
| ..**alessandro:**               |                            | ..**alessandro:**                  |
| ....**uid: 10011**              |                            | ....**uid: 10011**                 |
| ....**home: /home/alessandro**  |                            | ....**home: /mnt/home/alessandro** |

## deep

The `deep` merge option is a special behavior of the `hash` merge option.
Hash uses the first hash ke from highest hierarchy.

Using `deep` allows you to merge data from hashes with the same key.
All elements in all matching hierarchies must be of type hash.

Let's look at the data. In this case we manage users:

    # data/common.yaml
    users:
      martin:
        uid: 10012
        home: /mnt/home/martin
        shell: /bin/bash
      alessandro:
        uid: 10011
        home: /mnt/home/al
        shell: /bin/zsh

In application level, we also have users:

    # data/application/mysql.yaml
    users:
      simon:
        uid: 10013
        home: /home/simon
      martin: # mysql and shell is different that common
        home: /home/martin
        shell: /bin/zsh

The hash key from highest hierarchy is taken first. other keys from lower hierarchies are just added.
If a hash key exists in several hierarchies, the one from the highest hierarchy is taken:

    # result
    users:
      simon:
        uid: 10013
        home: /home/simon
      martin: # mysql is different that common
        uid: 10012
        home: /home/martin
        shell: /bin/zsh
      alessandro:
        uid: 10011
        home: /mnt/home/al
        shell: /bin/zsh

Visualization:

| Result                          | mysql                      | common                     |
|--------                         |-------                     |--------                            |
| **users:**                      | users:                     | users:                             |
| ..**simon:**                    | ..**simon:**               |                                    |
| ....**uid: 10013**              | ....**uid: 10013**         |                                    |
| ....**home: /home/simon**       | ....**home: /home/simon**  |                                    |
| ..**martin:**                   | ..**martin:**              | ..**martin:**                      |
| ....**uid: 10012**              |                            | ....**uid: 10012**                 |
| ....**home: /home/martin**      | ....**home: /home/martin** | ....home: /mnt/home/martin         |
| ....**shell: /bin/zsh**         | ....**shell: /bin/zsh**    | ....shell: /bin/bash               |
| ..**alessandro:**               |                            | ..**alessandro:**                  |
| ....**uid: 10011**              |                            | ....**uid: 10011**                 |
| ....**home: /home/alessandro**  |                            | ....**home: /mnt/home/alessandro** |
| ....**shell: /bin/zsh**         |                            | ....**shell: /bin/zsh**            |

## Merge behavior on explizit lookup

Note: This is not my preferred option! I prefer automatic data binding!

When using the `lookup` function one can specify the merge behavior in 2 different ways:

1. merge parameter

When using the merge parameter you must also provide the data type parameter:

    lookup( <NAME>, [<VALUE TYPE>], [<MERGE BEHAVIOR>], [<DEFAULT VALUE>] )

    lookup('users', Hash, 'deep')

1. parameter hash

When using the parameter hash, you can skip the data type:

    lookup( [<NAME>], <OPTIONS HASH> )

    lookup('users', { 'merge' => { 'strategy' => 'deep', }, 'value_type' => Hash})

## Merge behavior configuration within hiera data

When using automatic data binding (naming hiera keys according to t eh class/parameter names) one can not directly specify the merge behavior as the lookup is done automatically.
But hiera offers an option to use a special key called `lookup_options`.

Within the lookup_options key one specifies a Hash. The key of the hash is the hiera key to look for. For each key you can then specify e.g. the merge strategy and the return value data type conversion.

Let's have a look at the users with deep merge example from above. Let's assume we have a class class users with a parameter called users. To allow automatic data fetching the key in hiera must have the name `users::users`:

    # data/common.yaml
    users::users:
      martin:
        uid: 10012
        home: /mnt/home/martin
        shell: /bin/bash
      alessandro:
        uid: 10011
        home: /mnt/home/al
        shell: /bin/zsh

In application level, we also have users:

    # data/application/mysql.yaml
    users::users:
      simon:
        uid: 10013
        home: /home/simon
      martin: # mysql and shell is different that common
        home: /home/martin
        shell: /bin/zsh

Additionally we add the lookup_options key to common.yaml:

    lookup_options:
      users::users:
        merge: 'deep'

It is up to you and your use case if you place the lookup_option into the common layer or if you even overwrite lookup_options on a higher level.

Happy puppetizing and data merging,

Martin Alfke
