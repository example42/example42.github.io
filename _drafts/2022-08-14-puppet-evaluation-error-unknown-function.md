---
layout: blog
title: Puppet Evaluation Error - Unknown function
---

We have seen in the [previous post](2022-08-07-puppet-evaluation-error-unknown-resource-type.md) reasons and solutions for errors related to not found resources like:

    Error: Could not retrieve catalog from remote server: Error 500 on SERVER: Server Error: Evaluation Error: Error while evaluating a Resource Statement, Unknown resource type: 'concat' ...

A very similar Puppet error is one is:

Error: Could not retrieve catalog from remote server: Error 500 on SERVER: Server Error: Evaluation Error: Unknown function: 'str2bool'. (file: xxx.pp, line: x, column: x) on node xxx



## TL;DR

Functions provide additional functionality to Puppet language. As resource types, there are native functions, shipped with Puppet and additional ones, available through modules.

An **Unknown function** error refers to a function which is not native and is not present in the available modules.

Fix either by checking the function name for typos or by adding the module that provides it.



### Decomposing the "Unknown resource type" Puppet error message  [JUNIOR]