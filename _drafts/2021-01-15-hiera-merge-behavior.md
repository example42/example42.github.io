---
layout: blog
title: Hiera merge behavior
---

Hiera v5 allows you to provide information regarding merge behavior in a couple of different ways.

Using different merge behaviors allows you to e.g. separate common (admin) users from application users by adding common users in common hiera layer and the application users into an application hiera layer.
This reduces duplicates in data and allow more simple data management.

Another example is installation of packages. You usually have a list of packages you need on all systems (admin packages) and some packages which are needed on special systems only.
Again you can mention all common packages in hiera common laxer and add node specific packages in node hiera layer.

In this posting we explain the different possible merge behaviors and their results.
Aditionally we explain the options where you can set merge behavior.

* Table of content
{:toc}

# Hiera merge behavior options and the results

We will first have a look at all available merge options and explain the behavior and the result later in the explizit and automatic data explanations.

Hiera offers the following merge options:
- `first`
- `unique`
- `hash` and
- `deep`

All data examples assume that you have a hiera.yaml file using four hierarchies:
- node specific data
- application-stage specific data
- application specific data
- common data

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

The returned result for a packages keky, using `unique` merge strategy will return the following values:

    packages:
      - vim-enhanced
      - curl
      - xtrabackup

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
      alessandro:
        uid: 10011
        home: /mnt/home/al
        shell: /bin/zsh

## deep

The `deep` merge option is a specila behavior of the `hash` merge option.
Hash uses the first hash ke from highest hierarchy.

Using `deep` allows you to merge data from hashes with the same key.
All elemts in all matching hierarchie smust be of type hash.

# Merge behavior on explizit lookup

# Merge behavior configuration within hiera data

Happy puppetizing and data merging,

Martin Alfke

