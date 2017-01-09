---
layout: blog
title: Tip of the Week 3 - The optimal hiera.yaml
---

Yes, we are cheating. There's not a single optimal hiera.yaml file to configure [Hiera](https://docs.puppet.com/hiera/) in the perfect way for any infrastructure.

As usual different infrastructures may need different approaches and have different preferences on how and where to store data.

Here we are going a few suggestions on what could be common use cases.

## The backend

Hiera supports several [different backends](https://www.packtpub.com/mapt/book/networking-and-servers/9781783981441/2/ch02lvl1sec16/additional-hiera-backends) where to store data. Unless you don't have specific needs or preferences, you will generally use a file based backend, as yaml and json.

Also, you will probably need to encrypt some of your data so you'll likely move your eyes on the [hiera-eyaml](https://github.com/TomPoulton/hiera-eyaml) backend, which allows to easily encrypt some hiera keys in plain yaml files. In such a case, use ONLY the hiera-eyaml backend, there's really no sense in have both it and the normal yaml backend. So your hiera.yaml file would begin with:

    ---
    :backends:
      - eyaml

Then you have to configure hiera-eyaml. You have to provide the paths where keys used for encryption are stored. They are needed wherever a catalog, that uses encrypted data, is compiled, typically on the Puppet Server, but also in your development and testing stations (unless you take care to avoid to encrypt keys in such environments).

    :eyaml:
      :datadir: "/etc/puppetlabs/code/environments/%{environment}/hieradata"
      :pkcs7_private_key: '/etc/puppetlabs/keys/private_key.pkcs7.pem'
      :pkcs7_public_key: '/etc/puppetlabs/keys/public_key.pkcs7.pem'
      :extension: 'yaml'

Note that in the above configuration we place the keys in a dedicated directory outside the Puppet environment: we don't want to store in the same repo where we encrypt data the keys to decrypt it.

### The hierarchy

This is probably the part of your Hiera configuration where you will have to spend some time evaluating the best approach. You should not have too many levels in your hierarchy, definitively less than 10, they should start from the most specific one (where the same nodes' cert name is used) to the most generic.

The intermediary levels depend on your infrastructure and your decisions on them should be based on an evaluation of how values for the various configurations you manage may change in your setup according to different conditions.

Typically you'll have layers that represent the operational environment of your nodes (prod, qa, test, devel... here we call it $env as it does not match Puppet's environment for which there's the internal $environment variable), their role and the datacenter, network or zone where they are placed.

So a possible **sample** hierarchy may look like this:

    :hierarchy:
      - "hostname/%{::trusted.certname}"
      - "role/%{::role}-%{::env}"
      - "role/%{::role}"
      - "zone/%{::zone}"
      - common

Note that all the variables used in the hierarchy are top scope, and you need to define them in some way: either as facts or in an External Node Classifier (ENC) or in manifest/site.pp.

Note also that we haven't placed any reference to Operating System facts: even if (old) Hiera examples and online documentation used to have them in sample hierarchies, you generally should not need them: OS related settings should be managed directly in modules and classes, Hiera's hierarchy should reflect your own infrastructure logic, not the one of Operating Systems you use.

### Conclusions

Hiera has changed the way we work with Puppet. Since its introduction in Puppet 3 (before it was available as external add on) it has quickly become the standard tool to manage Puppet data and separate it from our code.

Should we use it? Yes definitively, that's currently the best and most versatile solution around.

Should we place ALL our data there? It depends.

I personally prefer to leave inside my profile and local classes the company defaults and the OS related infos to avoid too much data in Hiera yaml files.
Also, when a ENC is used, I avoid to use it to store data, so that infrastructure data is not present in multiple places.
The only exception is when the ENC is used to set global parameters in the hierarchy.

Still, your mileage may vary and you might find better or more fitting solutions for your use case. Maybe you want to check [VoxPupuli Website](https://voxpupuli.org/) for other [Hiera data backends](https://voxpupuli.org/plugins/#hiera).

Alessandro Franceschi
