---
layout: blog
title: Tip of the Week 22 - Hiera 5 globs and mapped paths
---

The release of Hiera 5, shipped with Puppet 4.9, has introduced several new features.

We have already talked about it in a previous [blog post](2017-04-17-hiera-5.md) and now we are going to explore new features which may be quite interesting and useful in some use cases: **mapped paths** and **globs**.

We already know that in ```hiera.yaml```, wen using file based backends, we can define hierarchies using 2 similar keywords: **path** and **paths**. They are similar as they allow us to specify a path, or an array of paths, where to look for in Hiera's endless seek for data.

Use for them is something like:

    hierarchy:
      - name: "Per-node data"
        path: "nodes/%{trusted.certname}.yaml"

      - name: "Common data"
        path: "common.yaml"

which, when using the **paths**, is equivalent to :

    hierarchy:
      - name: "Hiera data"
        paths:
          - "nodes/%{trusted.certname}.yaml"
          - "common.yaml"

This is common and known stuff, more or less we have always used this path based approach to define our hierarchies.

Now we have some more options, more dynamic and evoluted ways to define hierarchies and where to look for data files.

One of them is the usage of the **glob** and **globs** keywords:

    hierarchy:
      - name: "Hiera data"
        glob: "groups/*.yaml"

In this case the Hiera lookup is done for *each* yaml file present in the groups directory, parsed in alphanumerical order. Note that in the above example no variable interpolation is used, but that's still possible any fact or variable in the scope can be used in the glob definition.

The Ruby glob method is used to map file paths, so the following rules may apply:

  - With one asterisk (*) we match any character for a single file.
  - With two asterisks (**) any depth of nested directories is matched.
  - A question mark (?) matches one character.
  - Comma-separated lists in curly braces ({admins,dba}) match any option in the list.
  - Sets of characters in square brackets ([abcd]) match any character in the set.
  - A backslash (\) escapes special characters.

Using ```globs``` instead of ```glob``` allows us to specify an array of glob patterns, the same lofic of ```paths``` and ```path```.

I'm still trying to figure out a useful use case for glob, considering that I don't personally like long or complex hierarchies.

Maybe this could be useful for cases where we want to have different users to edit indipendently different files, or when we want to define the parameters for our classes in different places, for sake of order or semplicity.

Another interesting way to define hierarchies is by using **mapped paths**.


... TODO

