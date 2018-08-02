---
layout: blog
title: Tip of the Week 84 - Configuration Management and Containers
---

When we are at customers who start thinking about containers we usually get confronted with a combination of half knowledge and weird assumptions.
One of the most interesting topics usually deals with configuration management and the idea that this is no longer needed when switching to containers.

This posting will explain, how Puppet can help you managing your container infrastructure.

* Table of content
{:toc}

## Container host

To run containers you must have a system at hand. Usually people will just use a cloud provider, eliminating the need of local hardware.
But running on cloud needs detaiulled configuration like access control and authentication, besides the container host.

When running locally on your own hardware you want to configure the system to be capable of running container at all. Puppet Inc. has therefor published the [puppetlabs-docker](https://github.com/puppetlabs/puppetlabsdocker) module.

To make use of the puppetlabs docker module, you must use a supported operatingsystem like modern CentOS, Debian or SLES releases and have a Puppet Agent running locally.

The main docker class installs and configures your dockerd.

## Container runtime

With the docker module you can choose to either install Docker CE (Community Edition) or Docker EE (Enterprise Edition).
Please note that the puppetlabs-docker module does not install or configure the Docker Enterprise UCP (Universal Control Plane) nor the DTR (Docker Trusted Registry).

For installation and configuration of UCP and DTR you can use the [puppetlabs-ucp module](https://forge.puppetlabs.com/puppetlabs/docker_ucp)

Now let's get started installing docker:

    # Docker CE:
    class { 'docker': }
    
    # Docker EE:
    class { 'docker':
      docker_ee => true,
    }

This will give you a default docker installation from docker repositories and docker daemon is listening on socket only.

If you want to reach the docker daemon from remote and locally you must declare the docker class with several parameters:

    class { 'docker':
      tcp_bind        => ['tcp://127.0.0.1:4243','tcp://10.0.0.1:4243'],
      socket_bind     => 'unix:///var/run/docker.sock',
    }

Usually only root is allowed to access docker daemon. You can easily add other users to docker group:

    class { 'docker':
      docker_users => ['user1', 'user2'],
    }

Other useful parameters you want to set on your docker daemon might be `live-restore` or configuring the `storagedriver`.

    class { 'docker':
      stragedriver     => 'devicemapper',
      extra_parameters => ['--live-restore'],
    }

## Container network

If you need to use a specific bridge with individual network settings you can declare the docker class with core networking parameters.

    class { 'docker':
      ip_forward      => true,
      iptables        => true,
      ip_masq         => true,
      bridge          => br0,
      fixed_cidr      => '10.20.1.0/24',
      default_gateway => '10.20.0.1',
    }

Next to core networking you can add docker networks (which are supported since docker 1.9 and later):

    docker_network { 'my-network':
      ensure   => present,
      driver   => 'overlay',
      subnet   => '192.168.1.0/24',
      gateway  => '192.168.1.1',
      ip_range => '192.168.1.4/32',
    }

## Container volumes

Container should not have persitant data.
One option for persistant data (as long as you are on one host) is to make use of volumes:

    docker::volume { 'registry-volume':
      ensure => present,
    }

## Container images

We now can prepare the local docker daemon to have images available which can then be instantiated (`docker container run`).

As of now, we can only pull images from official Docker registry as we have no private registry yet available.
So let's pull the registry image via Puppet:

    docker::image { 'registry':
      image_tag => '2.6.2',
    }

You can also the `docker::image` defined resource type to build containers by yourself using a Dockerfile:

    docker::image { 'my_container':
      docker_file => '/home/docker/my_container/Dockerfile',
    }

## Running single containers

Now everything is prepared to spin up a container.
Let's start the registry container:

    docker::run { 'registry':
      image            => 'registry:2',
      ports            => ['5000:5000'],
      volumes          => ['registry-volume:/var/lib/registry'],
      extra_parameters => ['--restart=always'],
      privileged       => false,
      env              => [
        'REGISTRY_STORAGE_DELETE_ENABLED=true',
        'REGISTRY_LOG_LEVEL=warn',
      ],
    }

Especially for the registry container you want to also add the registry browser. We assume that both containers run on the same host:

    docker::run { 'registry-browser':
      image => 'klausmeyer/docker-registry-browser',
      ports => ['8888:8080'],
      env   => [
        "DOCKER_REGISTRY_URL=http://${::fqdn}:5000",
        'NO_SSL_VERIFICATION=true',
        'ENABLE_DELETE_IMAGES=true',
      ],
    }

## The container orchestration

Until now we created single instances of containers on single hosts.
This is not what you usally want, as this causes outage when the one hosts goes down or when docker needs maintenance (e.g. adding a configuration and restarting docker daemon).

The puppetlabs-docker module can also handle swarm and compose.

### Docker compose

Docker compose doues not give you high availability. It is useful when you want to run several containers which are functional **together** only.

e.g. you need a database and a webserver.

First you need to install the compose utility:

    class {'docker::compose':
      ensure => present,
      version => '1.9.0',
    }

Docker compose descriptions must be placed in a yam file, which can be easily deployed via Puppet:

    file { '/etc/docker-compose/teamA/web-db.yaml':
      ensure => file,
      source => 'puppet:///...',
    }

Now we can use the Docker compose resource type to deploy the application:

    docker_compose { '/etc/docker-compose/teamA/web-db.yaml':
      ensure => present,
      scale  => {
        'web_server' => '4',
      },
    }


### Docker swarm

When HA is required one should look into Swarm or Kubernetes. Both are capable of managing multiple containers on multiple hosts.

To activate docker swarm one first must run an initial command on the first swarm manager node.

    docker::swarm { 'cluster_manager':
      init           => true,
      advertise_addr => $fact['networking']['ip'],
      listen_addr    => $fact['networking']['ip'],
    }

The token can be found in the node log file.

Adding workers must use the token from forst master:

    docker::swarm { 'worker_1':
      join           => true,
      advertise_addr => $fact['networking']['ip'],
      listen_addr    => $fact['networking']['ip'],
      manager_ip     => '192.168.1.1',
      token          => '<your join token>'
    }

Having your Docker Swarm ready allos you to deploy docker services:

    docker::services { nginx':
      create    => true,
      service_name => 'nginx',
      image        => 'nginx:latest',
      publish      => '8443:80',
      replicas     => '5',
    }

### Kubernetes

Whereas Swarm integrates many configurations, Kubernetes allows you to choose the tools you need. This is done by separating APIs, Networks and Hosts into separate services (which are usually run in containers).

We will cover Kubernetes and Puppet in an upcoming Tip of the Week.

Martin Alfke
