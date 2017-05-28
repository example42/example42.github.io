---
layout: blog
title: Tip of the Week 22 - Hiera 5 globs and mapped paths
---

The release of Hiera 5, shipped with Puppet 4.9, has introduced several new features.

We have already talked about it in a previous [blog post](2017-04-17-hiera-5.md) and now we are going to explore new elements which may be quite interesting and useful in some use cases:  **globs** and **mapped paths**.

We already know that in ```hiera.yaml```, when using file based backends, we can define hierarchies using 2 similar keys: **path** and **paths**. They are similar as they allow us to specify a path, or an array of paths, where to look for in Hiera's endless seek for data.

Use for them is something like:

    hierarchy:
      - name: "Per-node data"
        path: "nodes/%{trusted.certname}.yaml"

      - name: "Common data"
        path: "common.yaml"

which, when using the **paths** key, is equivalent to :

    hierarchy:
      - name: "Hiera data"
        paths:
          - "nodes/%{trusted.certname}.yaml"
          - "common.yaml"

This is common and known stuff, more or less we have always used this path based approach to define our hierarchies.

Now we have some more options, more dynamic and evolved ways to define hierarchies and where to look for data files.

One of them is the usage of the **glob** and **globs** keys:

    hierarchy:
      - name: "Hiera data"
        glob: "groups/*.yaml"

In this case the Hiera lookup is done for *each* yaml file present in the groups directory, parsed in alphanumerical order. Note that in the above example no variable interpolation is used, but that's still possible any fact or variable in the scope can be used in the glob definition.

The Ruby glob method is used to map file paths, so the following rules apply:

  - With one asterisk (*) we match any character for a single file.
  - With two asterisks (**) any depth of nested directories is matched.
  - A question mark (?) matches one character.
  - Comma-separated lists in curly braces ({admins,dba}) match any option in the list.
  - Sets of characters in square brackets ([abcd]) match any character in the set.
  - A backslash (\) escapes special characters.

Using ```globs``` instead of ```glob``` allows us to specify an array of glob patterns, the same logic of ```paths``` and ```path```.

I'm still trying to figure out good use cases for glob, considering that I don't personally like long or complex hierarchies.

Maybe this could be useful for cases where we want to have different users to edit independently different files, or when we want to define the parameters for our classes in different places, for sake of order or simplicity.

For example it could be useful to split a file like [this](https://github.com/example42/psick/site/data/common.yaml) in different files, eventually one of each class / profile.

Another interesting way to define hierarchies is by using **mapped paths** key.

An example:

    - name: Applications
      mapped_paths: [apps, app, "apps/%{app}.yaml"]

The mapped_paths key must contain three string elements, in the following order:
  - A variable whose value is an array or hash (```apps``` in the example)
  - A temporary variable name to represent each element of the array or hash. This variable name, (```app``` in the example), is used only in the path in this key.
  - A path where that temporary variable can be used in interpolation expressions.

With the above example if we had a $apps variable containing an array like ['fe','be','db'] Hiera would lookup for data in the following files (relative to the defined ```datadir```):

    apps/fe.yaml
    apps/be.yaml
    apps/db.yaml

What's the use case for mapped paths?

One typical (?) case is when we want to assign to a node one or more *roles*.  Usual practice is to have a role and only a role for each node, but in some cases the concept of role has slightly different nuances and we may want to be able to have more than one role (or equivalent concept) in a node.

With the good old ```path``` key we imply that for each variable used in the hierarchy there can be only one possible value at a time, and that's the value used to identify the path of the file with our data.

Both globs and mapped_paths allow far more flexible hierarchies, with data which may be looked, in the same hierarchy, in different files according to values of variables (with ```mapped_paths```) or more general wild card or regexp based matches (with ```globs``` and ```glob```).

Having more options is hardly a negative thing, with Hiera 5 a remarkable new spectrum of alternatives is available for more complex, dynamic or flexible data storing and handling.  It's up to us to understand if we actually need them, but it's definitively useful to know the possible alternatives, as in some cases they can make our Puppet life better.

Alessandro Franceschi
