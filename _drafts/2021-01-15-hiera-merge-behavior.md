---
layout: blog
title: Hiera merge behavior
---

Hiera v5 allows you to provide information regarding merge behavior from data.

Using this functionality allows you to e.g. separate common (admin) users from application users by adding common users in common hiera layer and the application users into an application hiera layer.
This reduces duplicates in data and allow more simple data management.

Another example is installation of packages,´. You usually have a list of packages you need on all systems (admin packages) and some packages which are needed on special systems only.
Again you can mention all common packages in hiera common laxer and add node specific packages in node hiera layer.

* Table of content
{:toc}

# Hiera merge behavior options and the results

We will first have a look at all available merge options and explain the behavior and the result later in the explizit and automatic data explanations.

Hiera offers the following merge options:
- `first`
- `unique`
- `hash` and
- `deep`

# first
 
By default if no option is provided, hiera uses the `first` merge option.
Using `first` is not really a merge option as hiera will return the very first result of a key.

The data type of the result depends on the data type of hiera data.
e.g. if hiera finds a string, it will return a string, if it finds an array, it will return an array.

# unique

Unique r


# Merge behavior on explizit lookup

# Merge behavior on autoamtic data binding

Happy puppetizing,

Martin Alfke

