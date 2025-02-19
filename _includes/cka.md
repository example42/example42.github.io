## Certified Kubernetes Administrator (CKA) Preparation

#### A slides deck with the topics to learn for the CKA certification exam.

### Agenda  
1. Introduction to Kubernetes and its ecosystem
2. Cluster Architecture, Installation, and Configuration  
3. Workloads and Scheduling  
4. Services and Networking  
5. Storage in Kubernetes  
6. Security Essentials  
7. Cluster Maintenance and Troubleshooting  
8. Practice Labs and Mock Exams  

First chapter provides an overview of Kubernetes, its key features, ecosystem, and core components. For the exam preparation, you don't need to know most of the mentioned tools and resources.

---

## Chapter 1: Introduction to Kubernetes  

### Learn the Basics  
- What is Kubernetes, and why is it important?  
- Key features that make Kubernetes the leading container orchestration platform.  
- Core components and architecture of a Kubernetes cluster.  
- Terminology and concepts essential for working with Kubernetes.  
- The Kubernetes ecosystem: Tools, extensions, and the CNCF landscape.

---

## What is Kubernetes?  
- Kubernetes (commonly called **K8s**) is an open-source platform for **automating deployment**, **scaling**, and **management** of containerized applications.  
- Originally developed by **Google**; donated to the **Cloud Native Computing Foundation (CNCF)** in 2015.  
- Provides an abstraction layer for managing workloads in distributed systems.
- **Kubernetes** is derived from the Greek word for **helmsman** or **pilot**.
- **Kubernetes** is often abbreviated with **K8s** which stands for **K**-**8** letters between **K** and **s**.

🔗 [Introduction to Kubernetes](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)  

---

## 🔗 [Why Kubernetes](https://cloud.google.com/learn/what-is-kubernetes) ?

### Solves Key Challenges of Containerized Workloads  
1. **Resource Efficiency**: Optimizes utilization of compute, storage, and network resources.  
2. **Portability**: Runs seamlessly across on-premises, public cloud, or hybrid environments.  
3. **Resilience**: High availability through redundancy and self-healing.  
4. **Flexibility**: Handles stateless, stateful, and batch workloads.
5. **Scalability**: Scales applications horizontally or vertically based on demand.
6. **Automation**: Simplifies deployment, scaling, and management of applications.

### Kubernetes in Numbers  
- Thousands of contributors globally.  
- Backed by major organizations (Google, Red Hat, Amazon, Microsoft, etc.).
- Widely adopted by enterprises for cloud-native applications.
- **CNCF Survey 2021**: 91% of respondents use Kubernetes in production.

---

## Key features of Kubernetes

### Orchestration 
- Automates the deployment, scaling, and management of containerized applications.  

### Service Discovery and Load Balancing 
- Built-in DNS and network load balancers ensure reliable communication.

### Self-Healing
- Automatically restarts failed containers, reschedules workloads, and kills non-responsive applications.

### Declarative Configuration
- Define desired state in YAML/JSON files for version-controlled, reproducible infrastructure.  

### Scalability
- Dynamically scale up/down workloads based on demand or predefined rules.  

🔗 [Kubernetes Use Cases](https://www.ibm.com/think/topics/kubernetes-use-cases)  

---

## Kubernetes Terminology  

### Core Objects  
- **Pod**: Smallest deployable unit, encapsulates one or more containers.  
- **Service**: Exposes applications running in pods to internal or external traffic.  
- **ConfigMap**: Manages configuration data decoupled from application code.  
- **Secret**: Stores sensitive information securely.  
- **Volume**: Provides persistent storage for pods.

### Namespaces  
- Logical isolation for resources in a cluster.  
- Use cases: Separate environments for dev/stage/prod.

🔗 [Key Concepts](https://kubernetes.io/docs/concepts/)  

---

## Kubernetes vs. Traditional Systems

| Feature                | Kubernetes                      | Traditional Systems            |  
|------------------------|--------------------------------|--------------------------------|  
| Deployment            | Declarative (YAML/JSON)       | Manual or Script-based         |  
| Scaling               | Automatic                     | Manual or Limited              |  
| Failover              | Self-healing                 | Requires Manual Intervention   |  
| Resource Utilization  | Optimized                     | Often Over-provisioned         |  
| Networking            | Service Discovery Built-in    | Requires Manual Configuration   |
| Configuration         | Declarative (YAML/JSON)       | Manual or Script-based         |
| Portability           | Runs on Any Cloud Platform    | Vendor-specific                |
| Monitoring            | Integrated Metrics and Logs   | Requires Third-party Tools     |
| Security              | Role-Based Access Control     | Limited Access Control         |
| Cost                  | Efficient Resource Utilization | Often Over-provisioned         |

🔗 [Kubernetes Overview](https://kubernetes.io/docs/concepts/overview/)  

---

## Kubernetes Ecosystem - Core Components  

#### Package Management
- **Helm**: Kubernetes package manager for deploying pre-configured application templates. 🔗 [Helm Documentation](https://helm.sh/docs/)

#### Monitoring and Observability
- **Prometheus**: Metric collection, monitoring, and alerting system.  🔗 [Prometheus Kubernetes Integration](https://prometheus.io/docs/prometheus/latest/installation/)
- **Grafana**: Visualization tool for monitoring data.  🔗 [Grafana Kubernetes Integration](https://grafana.com/docs/grafana/latest/installation/kubernetes/)

#### Networking Plugins 🔗 [CNI Plugins Documentation](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)
- **Flannel**: Simple and easy-to-use networking solution. 🔗 [Flannel](https://github.com/flannel-io/flannel)
- **Calico**: Provides network policy enforcement. 🔗 [Calico Documentation](https://docs.projectcalico.org/)
- **WeaveNet**: Network plugin with built-in encryption and observability. 🔗 [WeaveNet Documentation](https://www.weave.works/docs/net/latest/)
- **Cilium**: Provides networking, security, and observability.  🔗 [Cilium Documentation](https://cilium.io/)

#### Service Mesh
- **Istio**: Service mesh with traffic management, security, and observability features. 🔗 [Istio Documentation](https://istio.io/latest/docs/)
- **Linkerd**: Lightweight service mesh for cloud-native applications. 🔗 [Linkerd Documentation](https://linkerd.io/)
- **Consul**: Service mesh with service discovery and configuration management. 🔗 [Consul Documentation](https://www.consul.io/)

---

## Kubernetes Operators  

### What Are Operators?  
- Extend Kubernetes functionality by automating domain-specific tasks.  
- Encapsulate application lifecycle management logic (e.g., provisioning, scaling, and failover).
- Use Custom Resource Definitions (CRDs) to define new resources.
- **Operator SDK**: Framework for building Kubernetes Operators.  🔗 [Operator SDK Documentation](https://sdk.operatorframework.io/)

### Popular Operators:  
- **PostgreSQL Operator**: Automates database management.  
- **Prometheus Operator**: Simplifies Prometheus deployment and configuration.  
- **ElasticSearch Operator**: Manages ElasticSearch clusters.

🔗 [Kubernetes Operators Documentation](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)  

---

## Kubernetes Distributions  

### Open-Source Distributions

- **k3s**: Lightweight Kubernetes, ideal for edge or IoT use cases. 🔗 [k3s Documentation](https://k3s.io/)  
- **MicroK8s**: Canonical’s lightweight Kubernetes distribution. 🔗 [MicroK8s Documentation](https://microk8s.io/)
- **k0s**: Zero-friction Kubernetes distribution. 🔗 [k0s Documentation](https://k0sproject.io/)
- **Kind**: Kubernetes in Docker for local development. 🔗 [Kind Documentation](https://kind.sigs.k8s.io/)


### Enterprise Distributions
- **Red Hat OpenShift**: Enterprise-grade Kubernetes with built-in CI/CD and security features.  🔗 [OpenShift Documentation](https://www.openshift.com/)  
- **Rancher**: Kubernetes management platform for multi-cluster operations. 🔗 [Rancher Documentation](https://rancher.com/)
- **VMware Tanzu**: Kubernetes platform for building, running, and managing applications. 🔗 [VMware Tanzu Documentation](https://tanzu.vmware.com/)
- **D2iQ Konvoy**: Kubernetes distribution with built-in monitoring and logging. 🔗 [D2iQ Konvoy Documentation](https://d2iq.com/)
- **Mirantis Kubernetes Engine (formerly Docker Enterprise)**: Kubernetes platform with integrated container runtime. 🔗 [Mirantis Kubernetes Engine Documentation](https://www.mirantis.com/software/kubernetes-engine/)

---

## Managed Cloud Solutions

- **Amazon Elastic Kubernetes Service (EKS)**: Kubernetes on AWS. 🔗 [EKS Documentation](https://aws.amazon.com/eks/)  
- **Google Kubernetes Engine (GKE)**: Fully managed Kubernetes from Google. 🔗 [GKE Documentation](https://cloud.google.com/kubernetes-engine)  
- **Azure Kubernetes Service (AKS)**: Kubernetes on Microsoft Azure. 🔗 [AKS Documentation](https://learn.microsoft.com/en-us/azure/aks/)
- **IBM Cloud Kubernetes Service**: Managed Kubernetes on IBM Cloud. 🔗 [IBM Cloud Kubernetes Service Documentation](https://www.ibm.com/cloud/kubernetes)
- **DigitalOcean Kubernetes**: Managed Kubernetes on DigitalOcean. 🔗 [DigitalOcean Kubernetes Documentation](https://www.digitalocean.com/products/kubernetes/)
- **Alibaba Cloud Container Service for Kubernetes**: Managed Kubernetes on Alibaba Cloud. 🔗 [Alibaba Cloud Kubernetes Service Documentation](https://www.alibabacloud.com/product/kubernetes)

---

## CNCF Landscape  

### What is CNCF?  
- **Cloud Native Computing Foundation (CNCF)**: Governing body supporting open-source, cloud-native projects.  
- Manages the Kubernetes project and fosters a thriving ecosystem.  

### CNCF Landscape Highlights:  
- Kubernetes is part of a broader cloud-native ecosystem, including:  
  1. **Container Runtimes**: containerd, CRI-O, Docker.  
  2. **Storage Solutions**: Rook, OpenEBS, Ceph.  
  3. **CI/CD Tools**: Tekton, ArgoCD, Flux.  
  4. **Security**: Falco, OPA, Kyverno.  

🔗 [CNCF Interactive Landscape](https://landscape.cncf.io/)  

---

## Chapter 1: Introduction to Kubernetes | Wrap-Up 

### Key Takeaways:  
- Kubernetes (K8s) automates deployment, scaling, and management of containerized applications.  
- Features: Service discovery, load balancing, self-healing, declarative configuration, scalability.  
- Use cases: Microservices, high-availability applications, CI/CD pipelines, hybrid/multi-cloud.  
- Ecosystem: Helm (packages), Prometheus (monitoring), Istio (service mesh), CNCF projects.  
- Managed solutions: EKS, GKE, AKS, OpenShift, Tanzu, DigitalOcean Kubernetes.

---

## Chapter 2: Cluster Architecture, Installation, and Configuration  

### Understand How Clusters Work  
- Explore the architecture of a Kubernetes cluster.  
- Learn about the Control Plane and Node components.  
- Install Kubernetes using tools like kubeadm and Minikube.  
- Configure clusters for security, scalability, and performance.  

---

## Cluster Architecture - Control Plane Components

**kube-apiserver** 🔗 [Documentation](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/)  
- Acts as the front end for the Kubernetes control plane.  
- Handles all REST requests and validates configurations.  

**etcd** 🔗 [Documentation](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/)
- A distributed, reliable key-value store for all cluster data.  
- Ensures consistency and stores the state of the cluster.  

**kube-scheduler** 🔗 [Documentation](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/)  
- Assigns workloads (pods) to appropriate nodes.  
- Bases decisions on resource availability, taints/tolerations, and affinity/anti-affinity rules.  

**kube-controller-manager** 🔗 [Documentation](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/)  
- Runs controllers to ensure desired state of the cluster
- Node Controller, Replication Controller, Endpoints Controller, Service Account Controller

---

## Cluster Architecture - Node Components  

**kubelet** 🔗 [Documentation](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)
  - An agent that runs on each node.  
  - Ensures containers in pods are running as expected.  
  - Communicates with the control plane.  
 
**kube-proxy** 🔗 [Documentation](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/)
  - Handles networking for Kubernetes Services.  
  - Maintains network rules and forwards requests to the appropriate pods.  

**Container Runtime** 🔗 [Documentation](https://kubernetes.io/docs/setup/production-environment/container-runtimes/) 
  - Responsible for running containers (e.g., containerd, CRI-O, Docker).  
  - Communicates with the kubelet to manage container lifecycle.

---

## Cluster Architecture - Topologies

### Single-Node Cluster
- All components run on a single node (control plane and worker node).
- Ideal for development and testing.
- Can be scaled to a multi-node cluster if needed.

### Multi-Node Cluster
- Control Plane: Manages the cluster state and API requests.
- Worker Nodes: Run workloads (pods) and communicate with the control plane.
- Scalable and fault-tolerant.
- For HA, run multiple instances (at least 3) of control plane components
- Worker Nodes can be added or removed dynamically.

---

## Installation Tools  

**  🔗 [kubeadm](https://kubernetes.io/docs/reference/setup-tools/kubeadm/) **
  - A standard tool to set up Kubernetes clusters easily.  
  - Automates installation of control plane and worker node components.  
  - Ideal for production-grade clusters.

** 🔗 [kind](https://kind.sigs.k8s.io/docs/user/quick-start/) **
  - Kubernetes in Docker for local development.  
  - Creates a multi-node cluster using Docker containers.  
  - Suitable for testing and development.

** 🔗 [Minikube](https://minikube.sigs.k8s.io/docs/) **
  - Lightweight Kubernetes for local testing.  
  - Sets up a single-node cluster on a local machine.  
  - Suitable for development and practice.  

---

## Installation prerequisites

On a node where you want to install Kubernetes, ensure the following prerequisites are met:
- A **Linux** host with at least 2 CPUs and 2GB of RAM.
- **Container Runtime**: Install a container runtime like containerd, CRI-O, or Docker.
- **kubeadm, kubectl, kubelet**: Install the Kubernetes binaries.
- **Disable swap**: Disable swap to ensure Kubernetes runs smoothly.
- **Firewall Rules on control plane**
  Open required ports for inbound traffic (defaults, can be customized):
  - API Server: **6443** (used by All)
  - etcd Server client API: **2379-2380** (used by etcd and kube-apiserver)
  - Kubelet API: **10250** (used by kubelet and control plane)
  - Controller Manager: **10257** (used by kube-controller-manager)
  - Scheduler: **10259** (used by kube-scheduler)
- **Firewall Rules on worker nodes**
  - Kubelet API: **10250** (used by kubelet and control plane)
  - Kube-proxy: **10256** (used by kube-proxy and load balancers)
  - NodePort Services: **30000-32767** (used by external clients)
  
---
## Installing Kubernetes with kubeadm 1/2

**Initialize the Cluster**:
On the master node, run a command as follows:
  ```bash  
  kubeadm init --pod-network-cidr 192.168.0.0/16
  ```
Some common options:
  - **--pod-network-cidr**: Specify the pod network CIDR. Can be different based on the network plugin used.
  - **--apiserver-advertise-address**: Specify the API server address, as used by worker nodes.
  - **--control-plane-endpoint**: Specify the control plane endpoint (IP or DNS name), useful if you plan to use external load balancers.

**Configure client tools**:
After initializing the cluster, you'll be shown commands to run in order configure kubectl to access the cluster.
```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

---

## Installing Kubernetes with kubeadm 2/2

**Set Up Networking**:
By default Kubernetes doesn't provide any networking. You need to install a CNI plugin to enable pod-to-pod communication.
Common choices are Flannel, Calico, or WeaveNet. Example with Calico (which uses, by default, the network CIDR 192.168.0.0/16 specified during initialization):
  ```bash
    kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
  ```
**Join Worker Nodes**:
On Worker nodes, use the join command provided after initializing the master node.
You can get the join command running:
  ```bash
  kubeadm token create --print-join-command
  ```
The join command looks like:
  ```bash
  kubeadm join <master-node-ip>:<master-node-port> --token <token> --discovery-token-ca-cert-hash <hash>
  ```

---

## kubeadm commands

Common kubeadm commands
- **kubeadm init**: Initialize a Kubernetes cluster.
- **kubeadm join**: Join a node to the cluster.
- **kubeadm token**: Manage tokens for joining nodes.
- **kubeadm config**: Manage configuration files.
- **kubeadm upgrade**: Upgrade a Kubernetes cluster.
- **kubeadm reset**: Reset a node to its initial state.

---

## Kubernetes Configuration

#### kubectl Configuration
The tool **kubectl** uses **kubeconfig** files where are stored cluster information, authentication details, and context.
The default kubeconfig path is **~/.kube/config**.

Inside a kubeconfig file you can have different contexts, each pointing to a different cluster.

With the command `kubectl config get-contexts` you can see the available contexts.

With the command `kubectl config use-context <context-name>` you can switch between contexts.

With the command `kubectl config view` you can see the merged kubeconfig settings.

---

## Kubernetes [ Namespaces 🔗 ](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) 

Namespaces are a way to divide cluster resources between multiple users or teams, they isolate resources within the same cluster and are ideal for multi-team or multi-environment use cases.
Common namespaces are:
- **default**: The default namespace for objects with no other namespace.
- **kube-system**: Namespace for objects created by Kubernetes system.
- **kube-public**: Namespace for objects that need to be accessible by all users.

When working with kubectl you always need to be aware that your commands are run within a specific namespace, you can change the namespace with the `--namespace` flag or by running:

```bash
kubectl config set-context --current --namespace=<namespace-name>
```

If you need to create new namespaces, run:

```bash
kubectl create namespace <namespace-name>
``` 

---

## Chapter 2: Cluster Architecture, Installation, and Configuration | Wrap-Up 

### Key Takeaways:  
- **Cluster Architecture**:
  - Control Plane manages cluster state; nodes run workloads. 
  - Control Plane components: API server, etcd, scheduler and controllers
  - Nodes components: kubelet, kube-proxy and the container runtime (Docker, containerd, CRI-O...).
- **Installation Tools**:  
  - kubeadm: Standard tool for production clusters.  
  - Minikube: Lightweight tool for local testing. 
  - kind: Kubernetes in Docker for development. 
- **Configuration**:  
  - Kubeconfigs are the configuration files for kubectl.
  - Organize resources with namespaces.  

---

## Chapter 3: Workloads and Scheduling  

### Resources and objects in Kubernetes
- Difference between resources and objects.
- Common commands to interact with resources.

### Manage Workloads Effectively  
- Discover Kubernetes workloads: Pods, Deployments, StatefulSets, and Jobs.  
- Learn about DaemonSets for node-specific tasks.  
- Master scheduling concepts like node affinity, taints/tolerations, and resource allocation.  
- Practice debugging and resolving workload issues.

---

## Kubernetes [objects and resources](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/)  🔗

Kubernetes **objects** are persistent entities in the Kubernetes system.

Kubernetes uses these entities to represent the state of your cluster.

Each object has a **spec** field that describes the desired state, and a **status** field that describes the current state of the object.

Kubernetes provides several built-in objects, like pods, services, and deployments and additionally allows you to define custom objects.

**Resources** are the endpoints in the Kubernetes API that store a collection of objects of a certain kind.

The difference between a resource and an object is that the resource is a "noun", while the object is a "instance" of a resource.

If you are familiar with OOP, the resource is the class, and the object is the instance of the class.

Or, to put it in a simpler way, the resource is the menu item and the object is the dish.

---

## Kubernetes [Resources](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/) 🔗

Kubernetes provides several built-in resources to manage the cluster:
- **Nodes**: Worker machines in the cluster.
- **Namespaces**: Organize resources within a cluster.
- **Pods**: Running instances of a container.
- **Deployments**: Manage replica sets and pods.
- **Services**: Expose applications running in pods.
- **ConfigMaps**: Store configuration data.
- **Secrets**: Store sensitive information securely.

For the complete list of the available resources run:
```bash
kubectl api-resources
```

---

## kubectl commands

These are common and useful kubectl commands to use with resources:
- **kubectl get**: Display info a resource.
- **kubectl describe**: Show detailed information about a resource.
- **kubectl create**: Create a new resource from a file or stdin.
- **kubectl apply**: Apply a configuration to a resource by file name or stdin.
- **kubectl delete**: Delete a resource.
- **kubectl edit**: Edit a resource.
- **kubectl explain**: Show documentation of a resource.

---

## Pods

**   [Pods](https://kubernetes.io/docs/concepts/workloads/pods/) 🔗 **
- Smallest deployable unit in Kubernetes.  
- Can run a single container or multiple tightly coupled containers.  
- Pods share:  
  - **Network namespace**: Same IP and ports.  
  - **Storage**: Shared volumes.  
  - **Lifecycle**: Start and stop together.
- **PodSpec**: Defines the pod's configuration (containers, volumes, etc.).

---

### Example: Creating a Pod  

#### Command Line  
```bash  
kubectl run my-pod --image=nginx --restart=Never  
```  

#### YAML File (output redacted)
```yaml  
apiVersion: v1  
kind: Pod  
metadata:  
  name: my-pod  
spec:  
  containers:  
    - name: my-pod  
      image: nginx
  restartPolicy: Never
``` 

---

### Example: Showing Pod Information (output redacted)

```bash
$ kubectl get pods my-pod
NAME                      READY   STATUS    RESTARTS   AGE
my-pod                    1/1     Running   0          3m39s
```

```bash
$ kubectl get pods my-pod -o yaml
kind: Pod
metadata:
  labels:
    run: my-pod
  name: my-pod
  namespace: default
spec:
  containers:
  - image: nginx
    imagePullPolicy: Always
    name: my-pod
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-cmz5n
      readOnly: true
  nodeName: minikube
  volumes:
  - name: kube-api-access-cmz5n
    projected:
      defaultMode: 420
      sources:
      - serviceAccountToken:
          expirationSeconds: 3607
          path: token
      - configMap:
          items:
          - key: ca.crt
            path: ca.crt
          name: kube-root-ca.crt
status:
  conditions:
  - lastProbeTime: null
    lastTransitionTime: "2025-01-24T14:40:19Z"
    status: "True"
    type: PodReadyToStartContainers
  containerStatuses:
  - containerID: docker://edb170adedefdf9655ec2dfd296411c796ba28e2ee03c85e683ec5e8e1a1307e
    image: nginx:latest
    name: my-pod
    ready: true
    restartCount: 0
    started: true
    state:
      running:
        startedAt: "2025-01-24T14:40:18Z"
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-cmz5n
      readOnly: true
  hostIP: 192.168.49.2
  podIP: 10.244.0.12
```

---

### Example: Describing a Pod (output redacted)

```bash
$ kubectl describe pod my-pod
Name:             my-pod
Namespace:        default
Service Account:  default
Node:             minikube/192.168.49.2
Labels:           run=my-pod
Status:           Running
IP:               10.244.0.12
Containers:
  my-pod:
    Image:          nginx
    State:          Running
    Ready:          True
    Restart Count:  0
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-cmz5n (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True 
  Initialized                 True 
  Ready                       True 
  ContainersReady             True 
  PodScheduled                True 
Volumes:
  kube-api-access-cmz5n:
    ConfigMapName:           kube-root-ca.crt
Events:
  Type    Reason     Age    From               Message
  ----    ------     ----   ----               -------
  Normal  Scheduled  2m30s  default-scheduler  Successfully assigned default/my-pod to minikube
  Normal  Pulling    2m30s  kubelet            Pulling image "nginx"
  Normal  Pulled     2m25s  kubelet            Successfully pulled image "nginx" in 4.887s (4.887s including waiting). Image size: 197009709 bytes.
  Normal  Created    2m25s  kubelet            Created container: my-pod
  Normal  Started    2m25s  kubelet            Started container my-pod

---

## Deployments  

#### 2. **Deployments**  
- Manage **stateless applications** and ensure the desired number of pods are running.  
- Supports:  
  - Rolling updates.  
  - Rollbacks to previous versions.  
- Useful for web servers and API backends.  
- 🔗 [Deployments Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)  

---

### Example: Creating a Deployment  

#### Command Line  
```bash  
kubectl create deployment my-deployment --image=nginx  
```  

#### YAML File  
```yaml  
apiVersion: apps/v1  
kind: Deployment  
metadata:  
  name: my-deployment  
spec:  
  replicas: 1
  selector:  
    matchLabels:  
      app: my-deployment  
  template:  
    metadata:  
      labels:  
        app: my-deployment  
    spec:  
      containers:  
        - name: nginx  
          image: nginx  
```

---

## StatefulSets  

#### 3. **StatefulSets**  
- Manage **stateful applications** requiring stable, persistent identities.  
- Ensures:  
  - Stable network identities.  
  - Persistent storage across pod restarts.  
- Commonly used for databases like MySQL, MongoDB.  
- 🔗 [StatefulSets Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)  

---

### Example: Creating a StatefulSet  

#### YAML File (Command line not recommended for StatefulSets)  
```yaml  
apiVersion: apps/v1  
kind: StatefulSet  
metadata:  
  name: my-statefulset  
spec:  
  serviceName: "my-service"  
  replicas: 3  
  selector:  
    matchLabels:  
      app: my-app  
  template:  
    metadata:  
      labels:  
        app: my-app  
    spec:  
      containers:  
        - name: nginx  
          image: nginx  
```  

---

## DaemonSets  

#### 4. **DaemonSets**  
- Ensure all (or some) nodes run a copy of a specific pod.  
- Common use cases:  
  - Log collectors (e.g., Fluentd).  
  - Monitoring agents (e.g., Prometheus Node Exporter).  
- 🔗 [DaemonSets Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)  

---

### Example: Creating a DaemonSet  

#### YAML File (Command line not recommended for DaemonSets)  
```yaml  
apiVersion: apps/v1  
kind: DaemonSet  
metadata:  
  name: my-daemonset  
spec:  
  selector:  
    matchLabels:  
      name: my-daemonset  
  template:  
    metadata:  
      labels:  
        name: my-daemonset  
    spec:  
      containers:  
        - name: nginx  
          image: nginx  
```

---

## Jobs and CronJobs  

#### 5. **Jobs and CronJobs**  
- **Jobs**: Run tasks to completion. Useful for batch processing.  
  🔗 [Jobs Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/job/)  
- **CronJobs**: Schedule tasks based on time intervals. Ideal for periodic backups or cleanups.  
  🔗 [CronJobs Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)  

---

### Example: Creating a Job  

#### Command Line  
```bash  
kubectl create job my-job --image=busybox -- echo "Hello Kubernetes"  
```  

#### YAML File  
```yaml  
apiVersion: batch/v1  
kind: Job  
metadata:  
  name: my-job  
spec:  
  template:  
    spec:  
      containers:  
        - name: my-container  
          image: busybox  
          command: ["echo", "Hello Kubernetes"]  
      restartPolicy: Never  
```  

---

### Example: Creating a CronJob  

#### Command Line  
```bash  
kubectl create cronjob my-cronjob --image=busybox --schedule="*/1 * * * *" -- echo "Hello from CronJob"  
```  

#### YAML File  
```yaml  
apiVersion: batch/v1  
kind: CronJob  
metadata:  
  name: my-cronjob  
spec:  
  schedule: "*/1 * * * *"  
  jobTemplate:  
    spec:  
      template:  
        spec:  
          containers:  
            - name: my-container  
              image: busybox  
              command: ["echo", "Hello from CronJob"]  
          restartPolicy: Never  
```  

---

## Scheduling Basics  

#### 1. Labels and Selectors  
- **Labels**: Key-value pairs attached to objects (e.g., pods, nodes).  
  - Examples: `app=frontend`, `tier=backend`.  
- **Selectors**: Match labels to identify objects for scheduling.  
- 🔗 [Labels and Selectors Documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)  

---

## Node Affinity and Anti-Affinity  

#### 2. Node Affinity and Anti-Affinity  
- **Node Affinity**: Schedule pods on nodes based on labels.  
  - Example: "Only schedule on nodes with SSD storage."  
- **Anti-Affinity**: Prevent pods from being scheduled on the same node.  
  - Example: "Spread replicas across multiple nodes."  
- 🔗 [Affinity and Anti-Affinity Documentation](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity)  

---

### Example: Node Affinity  

#### YAML File Example  
```yaml  
apiVersion: v1  
kind: Pod  
metadata:  
  name: affinity-pod  
spec:  
  affinity:  
    nodeAffinity:  
      requiredDuringSchedulingIgnoredDuringExecution:  
        nodeSelectorTerms:  
          - matchExpressions:  
              - key: kubernetes.io/hostname  
                operator: In  
                values:  
                  - node1  
  containers:  
    - name: nginx  
      image: nginx  
```

---

## Taints and Tolerations  

#### 3. Taints and Tolerations  
- **Taints**: Applied to nodes to restrict pod scheduling.  
  - Example: `NoSchedule` taint prevents pods without tolerations from being scheduled.  
- **Tolerations**: Allow pods to bypass taints and be scheduled on specific nodes.  
- 🔗 [Taints and Tolerations Documentation](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)  

---

### Example: Taints and Tolerations  

#### Add Taint to a Node  
```bash  
kubectl taint nodes node1 key=value:NoSchedule  
```  

#### YAML File Example for Toleration  
```yaml  
apiVersion: v1  
kind: Pod  
metadata:  
  name: toleration-pod  
spec:  
  tolerations:  
    - key: "key"  
      operator: "Equal"  
      value: "value"  
      effect: "NoSchedule"  
  containers:  
    - name: nginx  
      image: nginx  
```

---

## Resource Requests and Limits  

#### 4. Resource Requests and Limits  
- **Resource Requests**: Minimum CPU/Memory a pod needs to run.  
- **Resource Limits**: Maximum CPU/Memory a pod can consume.  
- Prevents resource starvation and overcommitment.  
- 🔗 [Resource Management Documentation](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)  

---

### Example: Resource Requests and Limits  

#### YAML File Example  
```yaml  
apiVersion: v1  
kind: Pod  
metadata:  
  name: resource-pod  
spec:  
  containers:  
    - name: nginx  
      image: nginx  
      resources:  
        requests:  
          memory: "64Mi"  
          cpu: "250m"  
        limits:  
          memory: "128Mi"  
          cpu: "500m"  
```   

---

## Priority Classes  

#### 5. Priority Classes  
- Define the importance of workloads during scheduling.  
- Higher-priority pods are scheduled first.  
- Lower-priority pods are evicted to make space during resource shortages.  
- 🔗 [Priority Classes Documentation](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/)  

---

### Example: Priority Classes  

#### Create a Priority Class  
```bash  
kubectl create priorityclass high-priority --value=1000 --global-default=false --description="High-priority workload"  
```  

#### YAML File Example for Priority Class  
```yaml  
apiVersion: scheduling.k8s.io/v1  
kind: PriorityClass  
metadata:  
  name: high-priority  
value: 1000  
globalDefault: false  
description: "High-priority workload"  
```  

#### Pod Using Priority Class  
```yaml  
apiVersion: v1  
kind: Pod  
metadata:  
  name: priority-pod  
spec:  
  priorityClassName: high-priority  
  containers:  
    - name: nginx  
      image: nginx  
```    

---

## Debugging Scheduling Issues  

#### Debugging Commands  
- Use `kubectl describe pod <pod-name>` to review scheduling events.  
- Check events for detailed scheduling-related messages:  
  ```bash  
  kubectl get events --sort-by='.metadata.creationTimestamp'  
  ```  
- Use the **Kubernetes Scheduler Simulator** to test specific scenarios.  
- 🔗 [Debugging Pods Documentation](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pod-replication-controller/)  

---

## Chapter 3: Resources, Workloads and Scheduling | Wrap-Up

### Key Takeaways:
- **Resources**: Nodes, Namespaces, Pods, Deployments, StatefulSets, DaemonSets, Jobs/CronJobs.
- **Workloads**: Pods (smallest deployable unit), Deployments (stateless apps), StatefulSets (stateful apps), Jobs/CronJobs (batch/scheduled tasks), DaemonSets (node-specific tasks).  
- **Scheduling**:  
  - Node affinity, taints/tolerations, and priority classes control pod placement.  
  - Resource requests/limits manage CPU and memory allocation.  
  - Network policies secure pod communication.
- **Debugging**: Use `kubectl describe`, `kubectl logs`, and ephemeral containers for troubleshooting.  

---

## Chapter 4: Services and Networking  

### Enable Connectivity and Communication  
- Learn how Kubernetes handles networking between pods and services.  
- Explore service types: ClusterIP, NodePort, LoadBalancer, and Ingress.  
- Use DNS for service discovery and networking plugins for pod communication.  
- Implement Network Policies to secure traffic within your cluster.  

---

## Kubernetes Networking Model  

#### Networking in Kubernetes: Key Principles  
1. **Flat Network Space**: All pods can communicate with each other without NAT.  
2. **Service Discovery**: Built-in DNS to resolve service names.  
3. **Flexible Connectivity**: Supports ClusterIP, NodePort, LoadBalancer, and Ingress.  

🔗 [Kubernetes Networking Overview](https://kubernetes.io/docs/concepts/cluster-administration/networking/)  

---

## Services in Kubernetes  

#### 1. ClusterIP (Default)  
- Exposes a service internally within the cluster.  
- Pods access the service via its DNS name or IP address.  
- 🔗 [ClusterIP Documentation](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services---service-types)  

---

### Example: ClusterIP  

#### Command Line  
```bash  
kubectl expose deployment my-deployment --type=ClusterIP --port=80  
```  

#### YAML File  
```yaml  
apiVersion: v1  
kind: Service  
metadata:  
  name: my-service  
spec:  
  selector:  
    app: my-deployment  
  ports:  
    - protocol: TCP  
      port: 80  
      targetPort: 80  
  type: ClusterIP  
```  

---

#### 2. NodePort  
- Exposes a service on each node's IP and a static port (30000-32767).  
- Allows external access to the service.  
- 🔗 [NodePort Documentation](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport)  

---

### Example: NodePort  

#### Command Line  
```bash  
kubectl expose deployment my-deployment --type=NodePort --port=80  
```  

#### YAML File  
```yaml  
apiVersion: v1  
kind: Service  
metadata:  
  name: my-service  
spec:  
  selector:  
    app: my-deployment  
  ports:  
    - protocol: TCP  
      port: 80  
      targetPort: 80  
      nodePort: 30007  
  type: NodePort  
```  

---

#### 3. LoadBalancer  
- Exposes a service externally using a cloud provider's load balancer.  
- Requires integration with supported cloud providers (e.g., AWS, Azure, GCP).  
- 🔗 [LoadBalancer Documentation](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer)  

---

### Example: LoadBalancer  

#### Command Line  
```bash  
kubectl expose deployment my-deployment --type=LoadBalancer --port=80  
```  

#### YAML File  
```yaml  
apiVersion: v1  
kind: Service  
metadata:  
  name: my-service  
spec:  
  selector:  
    app: my-deployment  
  ports:  
    - protocol: TCP  
      port: 80  
      targetPort: 80  
  type: LoadBalancer  
```  

---

## Ingress  

#### 4. Ingress  
- Provides HTTP(S) routing to services within the cluster.  
- Supports advanced features like TLS termination and path-based routing.  
- Requires an **Ingress Controller** (e.g., NGINX, Traefik).  
- 🔗 [Ingress Documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/)  

---

### Example: Ingress  

#### YAML File  
```yaml  
apiVersion: networking.k8s.io/v1  
kind: Ingress  
metadata:  
  name: my-ingress  
spec:  
  rules:  
    - host: my-app.example.com  
      http:  
        paths:  
          - path: /  
            pathType: Prefix  
            backend:  
              service:  
                name: my-service  
                port:  
                  number: 80  
```  

---

## Core Networking Concepts  

#### 1. DNS in Kubernetes  
- Automatically creates DNS entries for services.  
- Pods can resolve services using their names:  
  ```plaintext  
  <service-name>.<namespace>.svc.cluster.local  
  ```  
- 🔗 [DNS Documentation](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)  

---

### Example: Verifying DNS  

#### Command Line  
```bash  
kubectl exec -it <pod-name> -- nslookup my-service  
```  

---

#### 2. Network Policies  
- Control traffic flow between pods or between pods and external resources.  
- Specify **allow/deny** rules for ingress/egress traffic.  
- 🔗 [Network Policies Documentation](https://kubernetes.io/docs/concepts/services-networking/network-policies/)  

---

### Example: Network Policy  

#### YAML File  
```yaml  
apiVersion: networking.k8s.io/v1  
kind: NetworkPolicy  
metadata:  
  name: allow-frontend  
spec:  
  podSelector:  
    matchLabels:  
      app: frontend  
  ingress:  
    - from:  
        - podSelector:  
            matchLabels:  
              app: backend  
      ports:  
        - protocol: TCP  
          port: 80  
```  

---

## Debugging Networking Issues  

#### Troubleshooting Steps  
1. **Check Service and Pod Connectivity**:  
   ```bash  
   kubectl exec -it <pod-name> -- curl <service-name>:<port>  
   ```  

2. **Inspect Network Policies**:  
   ```bash  
   kubectl describe networkpolicy <policy-name>  
   ```  

3. **Test DNS Resolution**:  
   ```bash  
   kubectl exec -it <pod-name> -- nslookup <service-name>  
   ```  

4. **Verify Pod-to-Pod Communication**: Use `ping` or `curl`.  

🔗 [Debugging Services Documentation](https://kubernetes.io/docs/tasks/debug-application-cluster/debug-service/)  

---

## Chapter 4: Services and Networking | Wrap-Up   

### Key Takeaways:  
- **Networking Models**: All pods in a cluster can communicate without NAT.  
- **Services**: Expose applications via ClusterIP (internal), NodePort, LoadBalancer, or Ingress.  
- **Core Networking Concepts**:  
  - DNS for service discovery.  
  - CNI plugins (Calico, Flannel) handle pod networking.  
  - Network policies restrict traffic flow between pods.  
- Debugging: Test connectivity with `curl`, verify DNS resolution, and review events for issues.

---

## Chapter 5: Storage in Kubernetes  

### Persist and Manage Data  
- Understand how Kubernetes manages storage for containerized applications.  
- Use Persistent Volumes (PV) and Persistent Volume Claims (PVC).  
- Configure dynamic storage provisioning with StorageClasses.  
- Work with ConfigMaps and Secrets to manage configurations and sensitive data securely.  

---

## Storage in Kubernetes  

#### Key Concepts  
1. **Volumes**: Attach storage to pods.  
2. **Persistent Volumes (PV)**: Cluster-wide storage resources.  
3. **Persistent Volume Claims (PVC)**: Requests for storage by pods.  
4. **Dynamic Provisioning**: Automatically provisions storage using a StorageClass.  

🔗 [Storage Concepts Documentation](https://kubernetes.io/docs/concepts/storage/)  

---

## Volumes  

#### What are Volumes?  
- Allow pods to persist data beyond the lifecycle of a container.  
- Types of volumes:  
  - **emptyDir**: Temporary storage tied to the pod’s lifecycle.  
  - **hostPath**: Maps a host machine’s directory into the pod.  
  - **configMap**: Provide configurations as files.  
  - **secret**: Securely provide sensitive information.  

🔗 [Volumes Documentation](https://kubernetes.io/docs/concepts/storage/volumes/)  

---

### Example: Using a Volume  

#### YAML File  
```yaml  
apiVersion: v1  
kind: Pod  
metadata:  
  name: volume-pod  
spec:  
  containers:  
    - name: nginx  
      image: nginx  
      volumeMounts:  
        - mountPath: "/data"  
          name: my-volume  
  volumes:  
    - name: my-volume  
      emptyDir: {}  
```  

---

## Persistent Volumes (PV)  

#### What are Persistent Volumes?  
- Abstracts storage from specific pods.  
- Supports multiple backends like NFS, AWS EBS, GCE PD.  
- Must be **manually created** or dynamically provisioned.  

🔗 [Persistent Volumes Documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)  

---

### Example: Creating a Persistent Volume  

#### YAML File  
```yaml  
apiVersion: v1  
kind: PersistentVolume  
metadata:  
  name: my-pv  
spec:  
  capacity:  
    storage: 1Gi  
  accessModes:  
    - ReadWriteOnce  
  persistentVolumeReclaimPolicy: Retain  
  hostPath:  
    path: "/mnt/data"  
```  

---

## Persistent Volume Claims (PVC)  

#### What are Persistent Volume Claims?  
- A request for storage from a pod.  
- Links pods with available Persistent Volumes.  
- Defines:  
  - Requested size.  
  - Access modes (e.g., ReadWriteOnce).  

🔗 [Persistent Volume Claims Documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)  

---

### Example: Creating a PVC  

#### YAML File  
```yaml  
apiVersion: v1  
kind: PersistentVolumeClaim  
metadata:  
  name: my-pvc  
spec:  
  accessModes:  
    - ReadWriteOnce  
  resources:  
    requests:  
      storage: 500Mi  
```  

---

## Dynamic Provisioning  

#### What is Dynamic Provisioning?  
- Automatically provisions storage when PVCs are created.  
- Requires a **StorageClass** configured in the cluster.  

🔗 [Dynamic Provisioning Documentation](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/)  

---

### Example: Dynamic Provisioning with a StorageClass  

#### StorageClass YAML  
```yaml  
apiVersion: storage.k8s.io/v1  
kind: StorageClass  
metadata:  
  name: my-storageclass  
provisioner: kubernetes.io/aws-ebs  
parameters:  
  type: gp2  
```  

#### PVC Using the StorageClass  
```yaml  
apiVersion: v1  
kind: PersistentVolumeClaim  
metadata:  
  name: dynamic-pvc  
spec:  
  accessModes:  
    - ReadWriteOnce  
  resources:  
    requests:  
      storage: 1Gi  
  storageClassName: my-storageclass  
```  

---

## Storage for Configurations and Secrets  

#### ConfigMaps  
- Use ConfigMaps to store configuration data as files or environment variables.  
🔗 [ConfigMaps Documentation](https://kubernetes.io/docs/concepts/configuration/configmap/)  

---

### Example: Using a ConfigMap  

#### Create a ConfigMap from CLI  
```bash  
kubectl create configmap app-config --from-literal=key1=value1  
```  

#### YAML File Example  
```yaml  
apiVersion: v1  
kind: ConfigMap  
metadata:  
  name: app-config  
data:  
  key1: value1  
  key2: value2  
```  

---

#### Secrets  
- Use Secrets to store sensitive data securely (e.g., passwords, tokens).  
🔗 [Secrets Documentation](https://kubernetes.io/docs/concepts/configuration/secret/)  

---

### Example: Using a Secret  

#### Create a Secret from CLI  
```bash  
kubectl create secret generic app-secret --from-literal=username=admin --from-literal=password=pass123  
```  

#### YAML File Example  
```yaml  
apiVersion: v1  
kind: Secret  
metadata:  
  name: app-secret  
type: Opaque  
data:  
  username: YWRtaW4=  
  password: cGFzczEyMw==  
```  

---

## Debugging Storage Issues  

#### Common Troubleshooting Commands  
1. **Verify Persistent Volumes and Claims**:  
   ```bash  
   kubectl get pv,pvc  
   ```  

2. **Inspect Events for Failures**:  
   ```bash  
   kubectl describe pvc <pvc-name>  
   ```  

3. **Check Pod Logs for Mount Errors**:  
   ```bash  
   kubectl logs <pod-name>  
   ```  

🔗 [Debugging PV and PVC Documentation](https://kubernetes.io/docs/tasks/debug-application-cluster/debug-persistent-volumes/)  

---

## Chapter 5: Storage in Kubernetes | Wrap-Up   

### Key Takeaways:  
- **Storage Concepts**:  
  - Volumes (temporary storage), Persistent Volumes (PV), Persistent Volume Claims (PVC).  
  - Dynamic provisioning simplifies storage management using StorageClasses.  
- **ConfigMaps and Secrets**:  
  - ConfigMaps manage non-sensitive configuration data.  
  - Secrets securely store sensitive information like passwords or keys.  
- Debugging: Use `kubectl describe pv/pvc` for storage issues and check pod logs for mount errors.  

---

## Chapter 6: Security Essentials  

### Secure Your Cluster and Applications  
- Learn Kubernetes authentication and authorization mechanisms.  
- Use Role-Based Access Control (RBAC) for fine-grained permissions.  
- Apply Pod Security Standards and define security contexts for pods.  
- Secure communication and traffic with Network Policies.  

---

## Authentication and Authorization  

#### Authentication  
- Identifies **who** is making a request (e.g., users, service accounts).  
- Common authentication methods:  
  - Certificates  
  - Bearer Tokens  
  - External identity providers (e.g., OIDC).  

🔗 [Authentication Documentation](https://kubernetes.io/docs/reference/access-authn-authz/authentication/)  

---

#### Authorization  
- Controls **what** a user or process can do.  
- Methods:  
  - **Role-Based Access Control (RBAC)**: Assign permissions to users or groups.  
  - Attribute-Based Access Control (ABAC) and Webhook Authorization (less common).  

🔗 [Authorization Documentation](https://kubernetes.io/docs/reference/access-authn-authz/authorization/)  

---

### Example: RBAC Role and RoleBinding  

#### Role YAML File  
```yaml  
apiVersion: rbac.authorization.k8s.io/v1  
kind: Role  
metadata:  
  namespace: default  
  name: pod-reader  
rules:  
  - apiGroups: [""]  
    resources: ["pods"]  
    verbs: ["get", "list", "watch"]  
```  

#### RoleBinding YAML File  
```yaml  
apiVersion: rbac.authorization.k8s.io/v1  
kind: RoleBinding  
metadata:  
  name: read-pods  
  namespace: default  
subjects:  
  - kind: User  
    name: jane  
    apiGroup: rbac.authorization.k8s.io  
roleRef:  
  kind: Role  
  name: pod-reader  
  apiGroup: rbac.authorization.k8s.io  
```  

---

## Pod Security  

#### Pod Security Standards (PSS)  
- Ensure security at the pod level.  
- Three predefined standards:  
  1. **Privileged**: No restrictions.  
  2. **Baseline**: Minimum standards for common workloads.  
  3. **Restricted**: High-security standards.  

🔗 [Pod Security Standards Documentation](https://kubernetes.io/docs/concepts/security/pod-security-standards/)  

---

### Example: Enforcing Pod Security  

#### Apply Pod Security Standards via Labels  
```bash  
kubectl label namespace my-namespace pod-security.kubernetes.io/enforce=baseline  
```  

---

#### Securing Pods with SecurityContext  
- Set security options for pods or containers.  
- Examples: Run as non-root, drop capabilities, restrict privilege escalation.  

🔗 [Security Context Documentation](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)  

---

### Example: SecurityContext  

#### YAML File  
```yaml  
apiVersion: v1  
kind: Pod  
metadata:  
  name: secure-pod  
spec:  
  securityContext:  
    runAsUser: 1000  
    runAsGroup: 3000  
    fsGroup: 2000  
  containers:  
    - name: nginx  
      image: nginx  
      securityContext:  
        allowPrivilegeEscalation: false  
        capabilities:  
          drop: ["ALL"]  
```  

---

## Networking Security  

#### Network Policies  
- Control pod-to-pod and pod-to-external traffic.  
- Define **allow** or **deny** rules for ingress and egress.  

🔗 [Network Policies Documentation](https://kubernetes.io/docs/concepts/services-networking/network-policies/)  

---

### Example: Network Policy  

#### YAML File  
```yaml  
apiVersion: networking.k8s.io/v1  
kind: NetworkPolicy  
metadata:  
  name: allow-from-frontend  
  namespace: default  
spec:  
  podSelector:  
    matchLabels:  
      app: backend  
  ingress:  
    - from:  
        - podSelector:  
            matchLabels:  
              app: frontend  
      ports:  
        - protocol: TCP  
          port: 80  
```  

---

## Image Security  

#### Recommendations for Secure Container Images  
1. Use minimal base images.  
2. Regularly scan images for vulnerabilities.  
3. Avoid running containers as root.  

🔗 [Securing Images Documentation](https://kubernetes.io/docs/concepts/containers/images/#security)  

---

### Example: Using an ImagePullSecret  

#### YAML File  
```yaml  
apiVersion: v1  
kind: Secret  
metadata:  
  name: my-registry-secret  
data:  
  .dockerconfigjson: <base64-encoded-auth>  
type: kubernetes.io/dockerconfigjson  
```  

Associate the secret with a pod:  
```yaml  
apiVersion: v1  
kind: Pod  
metadata:  
  name: secure-pod  
spec:  
  imagePullSecrets:  
    - name: my-registry-secret  
  containers:  
    - name: nginx  
      image: my-private-registry/nginx:1.21  
```  

---

## Secrets Management  

#### Use Kubernetes Secrets for Sensitive Data  
- Store sensitive information like passwords, tokens, and SSH keys.  
- Secrets are **base64-encoded**, not encrypted by default.  

🔗 [Secrets Documentation](https://kubernetes.io/docs/concepts/configuration/secret/)  

---

### Example: Secret for Environment Variables  

#### YAML File  
```yaml  
apiVersion: v1  
kind: Secret  
metadata:  
  name: db-secret  
type: Opaque  
data:  
  username: YWRtaW4=  
  password: cGFzczEyMw==  
```  

Use the secret in a pod:  
```yaml  
apiVersion: v1  
kind: Pod  
metadata:  
  name: db-pod  
spec:  
  containers:  
    - name: app  
      image: my-app  
      env:  
        - name: DB_USER  
          valueFrom:  
            secretKeyRef:  
              name: db-secret  
              key: username  
        - name: DB_PASS  
          valueFrom:  
            secretKeyRef:  
              name: db-secret  
              key: password  
```  

---

## Debugging Security Issues  

#### Common Troubleshooting Commands  
1. **Inspect RoleBindings and ClusterRoleBindings**:  
   ```bash  
   kubectl get rolebinding,clusterrolebinding -A  
   ```  

2. **Check Pod SecurityContext**:  
   ```bash  
   kubectl describe pod <pod-name>  
   ```  

3. **Inspect Network Policies**:  
   ```bash  
   kubectl describe networkpolicy <policy-name>  
   ```  

4. **Audit Logs**: Enable and inspect logs to identify unauthorized access.  

🔗 [Debugging Access Issues Documentation](https://kubernetes.io/docs/tasks/debug/debug-cluster/access/)  

---

## Chapter 6: Security Essentials | Wrap-Up   

### Key Takeaways:  
- **Authentication and Authorization**:  
  - Authentication via certificates, tokens, or external providers.  
  - RBAC controls access to resources.  
- **Pod Security**:  
  - Use Pod Security Standards (Baseline, Restricted).  
  - Define security context to enforce non-root execution and drop privileges.  
- **Networking Security**:  
  - Network policies control ingress/egress traffic between pods.  
- Best Practices: Regularly scan images, use Secrets for sensitive data, and audit logs for potential breaches.  

---

## Chapter 7: Cluster Maintenance and Troubleshooting  

### Keep Your Cluster Healthy  
- Perform routine cluster maintenance tasks like upgrades and backups.  
- Monitor cluster performance with Metrics Server, Prometheus, and Grafana.  
- Debug and troubleshoot issues with logs, events, and ephemeral containers.  
- Prepare for disaster recovery by restoring etcd and validating cluster state.  
- Magage cluster resources with best practices for limits, requests, and priority classes.

---

## Cluster Maintenance  

#### 1. Regular Cluster Backups  
- Backup **etcd**, the key-value store holding the cluster state.  
- Use `etcdctl` or automation tools like Velero.  

🔗 [Backing up etcd Documentation](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-etcd)  

---

### Example: Backing up etcd  

#### Command Line  
```bash  
ETCDCTL_API=3 etcdctl snapshot save snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key  
```  

---

#### 2. Upgrading Kubernetes Clusters  
- Use `kubeadm upgrade` to safely update control plane and nodes.  
- Ensure you follow version skew policies between components.  

🔗 [Cluster Upgrades Documentation](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)  

---

### Example: Upgrading a Cluster  

#### Upgrade Control Plane  
```bash  
kubeadm upgrade apply v1.26.0  
```  

#### Upgrade kubelet and kubectl on Nodes  
```bash  
apt-get update && apt-get install -y kubelet=1.26.0-00 kubectl=1.26.0-00  
systemctl restart kubelet  
```  

---

## Monitoring and Logging  

#### 1. Enable Metrics Server  
- Provides resource metrics for pods and nodes.  
- Required for `kubectl top` commands.  

🔗 [Metrics Server Documentation](https://github.com/kubernetes-sigs/metrics-server)  

---

### Example: Install Metrics Server  

#### YAML File  
```yaml  
apiVersion: apps/v1  
kind: Deployment  
metadata:  
  name: metrics-server  
  namespace: kube-system  
spec:  
  replicas: 1  
  selector:  
    matchLabels:  
      k8s-app: metrics-server  
  template:  
    metadata:  
      labels:  
        k8s-app: metrics-server  
    spec:  
      containers:  
        - name: metrics-server  
          image: k8s.gcr.io/metrics-server/metrics-server:v0.5.0  
          args:  
            - --kubelet-insecure-tls  
```  

---

#### 2. Logging with Fluentd and Elasticsearch  
- Aggregate logs for the cluster using tools like Fluentd or Loki.  
- Analyze logs via Kibana or Grafana.  

🔗 [Logging Documentation](https://kubernetes.io/docs/concepts/cluster-administration/logging/)  

---

## Troubleshooting Basics  

#### 1. Inspect Pods and Nodes  
- View pod details:  
  ```bash  
  kubectl describe pod <pod-name>  
  ```  

- Check node status:  
  ```bash  
  kubectl get nodes  
  kubectl describe node <node-name>  
  ```  

---

#### 2. Debugging Pods  
- Check pod logs:  
  ```bash  
  kubectl logs <pod-name>  
  ```  

- Execute commands in a running pod:  
  ```bash  
  kubectl exec -it <pod-name> -- /bin/bash  
  ```  

🔗 [Debugging Pods Documentation](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pod/)  

---

## Troubleshooting Tools  

#### 1. Use `kubectl` Debugging Features  
- Debug a pod with ephemeral containers:  
  ```bash  
  kubectl debug <pod-name> --image=busybox  
  ```  

🔗 [Debugging Ephemeral Containers Documentation](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#ephemeral-container)  

---

#### 2. Network Troubleshooting  
- Test service connectivity:  
  ```bash  
  kubectl exec -it <pod-name> -- curl <service-name>:<port>  
  ```  

- Verify DNS resolution:  
  ```bash  
  kubectl exec -it <pod-name> -- nslookup <service-name>  
  ```  

🔗 [Debugging Network Issues Documentation](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/)  

---

#### 3. Analyze Events  
- Check cluster events for errors or warnings:  
  ```bash  
  kubectl get events --sort-by='.metadata.creationTimestamp'  
  ```  

---

## Disaster Recovery  

#### Key Steps for Recovery  
1. Restore **etcd** from a backup.  
2. Recreate control plane components with `kubeadm`.  
3. Validate cluster state and reconfigure workloads.  

🔗 [Disaster Recovery Documentation](https://kubernetes.io/docs/tasks/administer-cluster/disaster-recovery/)  

---

### Example: Restoring etcd  

#### Command Line  
```bash  
ETCDCTL_API=3 etcdctl snapshot restore snapshot.db \
  --data-dir=/var/lib/etcd-from-backup  
```  

Update the `etcd` pod configuration to point to the restored data directory.  

---

## Best Practices  

#### Maintenance Tips  
- Regularly back up **etcd** and validate snapshots.  
- Test upgrades in a staging environment before production.  
- Use tools like Prometheus and Grafana for proactive monitoring.  

#### Troubleshooting Advice  
- Always start with `kubectl describe` for resource details.  
- Check cluster-wide events for anomalies.  
- Keep cluster logs centralized and searchable.  

🔗 [Cluster Administration Documentation](https://kubernetes.io/docs/tasks/administer-cluster/)  


---

#### Resource Management

**Resource Requests and Limits**:
- **Resource Requests**: Minimum CPU/Memory a pod needs to run.
- **Resource Limits**: Maximum CPU/Memory a pod can consume.
- Prevents resource starvation and overcommitment.
- 🔗 [Resource Management Documentation](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

**Resource Quotas**:  
  - Limit resource consumption per namespace.  
  - 🔗 [Resource Quotas Documentation](https://kubernetes.io/docs/concepts/policy/resource-quotas/)  

**Limit Ranges**:  
  - Set default requests and limits for containers in a namespace.
  - 🔗 [Limit Ranges Documentation](https://kubernetes.io/docs/tasks/administer-cluster/manage-resources/limit-range/)  

---

## Chapter 7: Cluster Maintenance and Troubleshooting | Wrap-Up   

### Key Takeaways:  
- **Maintenance**:  
  - Regularly back up etcd using `etcdctl snapshot save`.  
  - Upgrade clusters with `kubeadm upgrade`.  
- **Monitoring**:  
  - Use Metrics Server for resource metrics (`kubectl top`).  
  - Visualize metrics and logs with Prometheus and Grafana.  
- **Troubleshooting**:  
  - Debug pods using logs (`kubectl logs`) and ephemeral containers.  
  - Analyze events (`kubectl get events`) and validate DNS/network configurations.  
- **Disaster Recovery**:
  - Restore etcd from backups and validate control plane.  
- **Resource Management**:  
  - Set resource requests and limits to prevent overcommitment.  
  - Use Resource Quotas and Limit Ranges to manage resource consumption.

---

## Chapter 8: Practice Labs and Mock Exams  

### Prepare for Real-World Scenarios  
- Gain hands-on experience with Kubernetes through structured labs.  
- Set up clusters, deploy workloads, and configure networking and storage.  
- Secure your cluster and troubleshoot common issues.  
- Test your knowledge with mock exam scenarios and practical exercises.

---

## Practice Labs and Mock Exams  

#### Goal of Hands-On Practice  
- Reinforce understanding of Kubernetes concepts.  
- Prepare for real-world cluster management tasks.  
- Build confidence for the CKA exam.

🔗 [CKA Exam Curriculum](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/)  

---

## Lab 1: Setting Up a Kubernetes Cluster  

#### Tasks:  
1. Install Kubernetes using `kubeadm`.  
2. Configure networking with **Calico** or **Flannel**.  
3. Add worker nodes to the cluster.  

🔗 [Kubeadm Setup Documentation](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)  

---

### Example: Initializing the Cluster  

#### Command Line  
```bash  
kubeadm init --pod-network-cidr=192.168.0.0/16  
```  

Apply a network plugin (e.g., Calico):  
```bash  
kubectl apply -f https://docs.projectcalico.org/v3.25/manifests/calico.yaml  
```  

---

## Lab 2: Managing Workloads  

#### Tasks:  
1. Create a Deployment with 3 replicas of **nginx**.  
2. Scale the Deployment to 5 replicas.  
3. Update the Deployment to a new version of nginx.  

🔗 [Workloads Documentation](https://kubernetes.io/docs/concepts/workloads/)  

---

### Example: Scaling a Deployment  

#### Command Line  
```bash  
kubectl scale deployment my-deployment --replicas=5  
```  

---

### Example: Updating a Deployment  

#### Command Line  
```bash  
kubectl set image deployment/my-deployment nginx=nginx:1.21  
```  

---

## Lab 3: Configuring Services and Networking  

#### Tasks:  
1. Create a **ClusterIP** service for a backend pod.  
2. Create an **Ingress** for HTTP traffic to a web application.  
3. Define a **NetworkPolicy** to allow traffic only from specific pods.  

🔗 [Networking Documentation](https://kubernetes.io/docs/concepts/services-networking/)  

---

### Example: ClusterIP Service YAML  
```yaml  
apiVersion: v1  
kind: Service  
metadata:  
  name: backend-service  
spec:  
  selector:  
    app: backend  
  ports:  
    - protocol: TCP  
      port: 80  
      targetPort: 8080  
  type: ClusterIP  
```  

---

## Lab 4: Persistent Storage  

#### Tasks:  
1. Create a Persistent Volume (PV) and Persistent Volume Claim (PVC).  
2. Mount the PVC to a pod.  
3. Dynamically provision storage using a **StorageClass**.  

🔗 [Storage Documentation](https://kubernetes.io/docs/concepts/storage/)  

---

### Example: Mounting a PVC in a Pod  

#### YAML File  
```yaml  
apiVersion: v1  
kind: Pod  
metadata:  
  name: storage-pod  
spec:  
  volumes:  
    - name: my-pvc-volume  
      persistentVolumeClaim:  
        claimName: my-pvc  
  containers:  
    - name: nginx  
      image: nginx  
      volumeMounts:  
        - mountPath: "/data"  
          name: my-pvc-volume  
```  

---

## Lab 5: Securing the Cluster  

#### Tasks:  
1. Create and apply a **NetworkPolicy** to secure traffic.  
2. Use **RBAC** to define granular permissions.  
3. Apply a **PodSecurityPolicy** to restrict privileged operations.  

🔗 [Security Documentation](https://kubernetes.io/docs/concepts/security/)  

---

### Example: RBAC Role for Pods  

#### YAML File  
```yaml  
apiVersion: rbac.authorization.k8s.io/v1  
kind: Role  
metadata:  
  namespace: default  
  name: pod-manager  
rules:  
  - apiGroups: [""]  
    resources: ["pods"]  
    verbs: ["create", "delete"]  
```  

---

## Lab 6: Cluster Maintenance  

#### Tasks:  
1. Backup and restore **etcd** data.  
2. Upgrade the cluster using `kubeadm`.  
3. Set up monitoring with **Metrics Server** and visualize metrics in Prometheus/Grafana.  

🔗 [Cluster Maintenance Documentation](https://kubernetes.io/docs/tasks/administer-cluster/)  

---

## Mock Exam: Sample Scenarios  

#### Scenario 1: Troubleshooting  
- Pod stuck in **CrashLoopBackOff**.  
- Debug and resolve the issue using logs and events.  

#### Scenario 2: Scaling and Updates  
- Scale a Deployment, then perform a rolling update.  

#### Scenario 3: Networking  
- Secure communication between frontend and backend pods using **NetworkPolicy**.  

---

## Exam Preparation Tips  

#### 1. Time Management  
- Practice solving tasks within time limits.  
- Prioritize tasks based on complexity.  

#### 2. Focus Areas  
- Master `kubectl` commands.  
- Familiarize yourself with YAML file structures.  

#### 3. Read Official Documentation  
- The exam environment provides access to Kubernetes documentation.  

🔗 [CKA Tips and Tricks](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/)  

---

## Useful shortcuts

During th exam you'll find yourself running the same commands over and over again.
To save time, you can create shortcuts for these commands. Here are some examples:

```bash

# Options to generate yaml output based on a command
export dryrun='--dry-run=client -o yaml'
# kubectl run nginx --image=nginx $dryrun

# Quickly Show the Example section of the help
alias example='grep Examples -A15'
# kubectl create role -h | example

# Quickly switch namespace
alias kn='kubectl config set-context --namespace'
# kn mynamespace
```
---

# Chapter 8: Practice Labs and Mock Exams | Wrap-Up   

### Key Takeaways:  
- Hands-on labs include:  
  - Cluster setup (kubeadm, Minikube).  
  - Deploying workloads (Deployments, StatefulSets, Jobs).  
  - Configuring networking (Services, Ingress, Network Policies).  
  - Managing storage (PV, PVC, StorageClasses).  
- Mock exam scenarios cover troubleshooting, scaling, and securing clusters.  
- Exam preparation tips:  
  - Master `kubectl` commands and YAML manifests.  
  - Prioritize tasks and practice within time limits.  
  - Leverage official Kubernetes documentation during the exam.  

