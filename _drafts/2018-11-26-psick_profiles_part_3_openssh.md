---
layout: blog
title: Tip of the Week 98 - Psick profiles. Part 2 - Managing OpenSSH
---

On the [first post](){:target="_blank"} of our series on Psick profiles we introduced the psick module and had an overview of its reusable profiles.

In this post we are going to review the resources that psick module provides to manage OpenSSH.

The main psick::openssh profile

class psick::openssh (
  Enum['present','absent'] $ensure        = 'present',
  Hash                     $configs_hash  = {},
  Hash                     $keygens_hash  = {},
  Hash                     $keypairs_hash = {},
  String                   $module        = 'psick',
  Boolean                  $use_tp        = true,



  define psick::openssh::config (
    Enum['present','absent'] $ensure         = present,
    Variant[Undef,String]    $content        = undef,
    Variant[Undef,String]    $template       = 'psick/generic/spaced_with_stanzas.erb',
    Variant[Undef,String]    $source         = undef,
    Optional[String]         $user           = undef,
    Optional[String]         $path           = undef,
    Hash                     $options_hash   = {},
    Boolean                  $create_ssh_dir = false,

    define psick::openssh::keygen (
      Optional[String] $user     = undef,
      Optional[String] $type     = undef,
      Optional[Integer] $bits    = undef,
      Optional[String] $home     = undef,
      Optional[String] $filename = undef,
      Optional[String] $comment  = undef,
      Optional[String] $options  = undef,

      define psick::openssh::keyscan (
        String                         $user             = 'root',
        String                         $host             = $title,
        Optional[Stdlib::AbsolutePath] $known_hosts_path = undef,

        define psick::openssh::keypair (

          Variant[Boolean,String]    $ensure        = 'present',
          Optional[String] $user                    = $title,

          Optional[String] $private_key_content     = undef,
          Optional[String] $private_key_source      = undef,
          Optional[String] $private_key_owner       = undef,
          Optional[String] $private_key_group       = undef,
          Optional[String] $private_key_mode        = '0600',

          Optional[String] $public_key_content      = undef,
          Optional[String] $public_key_source       = undef,
          Optional[String] $public_key_owner        = undef,
          Optional[String] $public_key_group        = undef,
          Optional[String] $public_key_mode         = '0644',

          Optional[String] $dir_path                = undef,
          Optional[String] $dir_owner               = undef,
          Optional[String] $dir_group               = undef,
          Optional[String] $dir_mode                = '0700',

          String $key_name                          = 'id_rsa',
          Boolean $create_ssh_dir                   = true,

Alessandro Franceschi
