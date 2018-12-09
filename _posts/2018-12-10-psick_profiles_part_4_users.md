---
layout: blog
title: Tip of the Week 102 - Psick profiles. Part 4 - Managing users
---

We continue our review of psick profiles describing how `psick::users` can help in configuring users, root password, sudo and ssh keys.

This comes after:

- [Part 1 - Overview](https://www.example42.com/2018/11/12/psick_profiles_part_1_overview/){:target="_blank"} of the psick module and its reusable profiles.

- [Part 2 - Proxy and Hostname](https://www.example42.com/2018/11/19/psick_profiles_part_2_proxy_and_hostname_settings/){:target="_blank"} settings with psick profiles.

- [Part 3 - OpenSSH](https://www.example42.com/2018/12/03/psick_profiles_part_3_openssh/){:target="_blank"} settings, keys, configs management.

For the following configuation we just need to classify for `psick::users` class:

    include psick::users

As usual the following hiera sample parameters are expressed in yaml format.

## Managing root user

We can set password of root user with:

    psick::users::root_pw: '$6$OkmG4mu/$RbyL'

The value is passed as password argument for the user root, in whatever encrypted format the local system requires.

It's possible to configure any other argumente of the root user with the parameter root_params:

    psick::users::root_params:
      comment: 'Root user'
      shell: '/bin/bash'

## Managing all users

For all the other users there's the `users_hash` parameter, looked up in deep merge mode (as any parameter of psick classes whose name ends with _hash), which allows to define one or more users with the relevant set or arguments.

This is not just a wrapper around the user resource type, as we can use component modules as "backends".

This is managed via the `psick::users::module` parameter which define which module to use to manage users:
- 'user' to use Puppet native type `user`
- 'psick' to use the define [`psick::users::managed`](https://github.com/example42/puppet-psick/blob/master/manifests/users/managed.pp)
- 'accounts' to use [`accounts::user`](https://github.com/puppetlabs/puppetlabs-accounts/blob/master/manifests/user.pp) from puppetlabs-accounts module

So for example we can manage our users, using Puppet native type user, with:

    psick::users::module: 'user'
    psick::users::users_hash:
      al:
        ensure: present
        comment: 'Al'
        groups:
          - users
      ma:
        ensure: present
        comment: 'Ma'
        groups:
          - users

In the above example the users "al" and "ma" are created, the parameters specified in the hash must be compatible with resource provided by the selected module, otherwise you get an Unknown Argument error.

### Managing extra users resources

In the users hash, besides the arguments acceptable by the selected module define, we can set other special parameters to manage resources for users:

- ssh_authorized_keys: An array of keys to add to the user' authorized keys
- openssh_keygen: A boolean, if true a ssh key pair is automatically generated for the user using the `psick::openssh::keygen` define [check here the available parameters](https://github.com/example42/puppet-psick/blob/master/manifests/openssh/keygen.pp)
- sudo_template: The path as used by the template() function of an erb template to use to manage the user's sudo file. Nothing is created if not defined.


    psick::users::users_hash:
      al:
        ensure: present
        ssh_authorized_keys:
          - 'ssh-rsa AAAAB3BAQC93uOkdIr...'
        sudo_template: 'profile/users/sudo/admins'
      jenkins:
        openssh_keygen: true

### Purge unmanaged users

By default Puppet only manages the resources we instruct it to manage, and the same is done with users here. Still there are cases where we want full control on the interactive users managed on a server, this can be accomplished with the (quite dangerous) parameter:

    psick::users::delete_unmanaged: true

The default is false, but is this is the to true all non system users not managed by Puppet are automatically deleted.


## Managing /etc/skel

The /etc/skel directory on a Linux systems contains files that are added to the homes of all the users created on the system. We can manage its content with:

    psick::users::source: 'puppet:///modules/profile/users/skel'

The contents of the directory specified as source (used as in the file resource type so, in the above sample, on a local profile module, under the `files/users/skel` directory) are copied to the system's /etc/skel directory.

Note that files from here are copied to only to newly created users, so changes here don't affect the home of existing users.

## Alternative way to define users

If a single hash becomes hard to manage via hiera, due to different users to be applied to different kind of servers, we can have an alternative way to define the users we want to configure on a system.

Alternatively (or complementarily) to `users_hash` we have the key `available_users_hash` which acts exactly in the same way, but rather than actually creating the users, it can serve as key to define all the possible users we want to manage. The actual users to create are then defined by the `available_users_to_add` array.

    psick::users::available_users_hash:
      al:
        ensure: present [...]
      ma:
        ensure: present [...]
      jenkins:
        ensure: present [...]
    psick::users::available_users_to_add:
      - al
      - ma

In this way we can define all our users in a single Hiera layer, and then use the  `available_users_to_add` parameter on the different Hiera hierarchies, to actually manage which users are created where.

This is what can be done for users with `psick::users` profile.

Have fun with Puppet, Life, Universe and Everything.

Alessandro Franceschi
