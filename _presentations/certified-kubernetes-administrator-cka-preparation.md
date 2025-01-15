---
number: '2'
layout: 'presentation'
title: 'Certified Kubernetes Administrator (CKA) Preparation Course'
description: 'A comprehensive guide to preparing for the Certified Kubernetes Administrator (CKA) exam, covering key concepts, workloads, networking, storage, security, and more.'
date: '20250111'
host: Alessandro Franceschi
source: 'cka.md'
tags:
  - Kubernetes
  - CKA
  - DevOps
  - Containers
  - Cloud Native
  - CNCF

---

class: center, middle

# Certified Kubernetes Administrator (CKA) Preparation Course  
### Preparing to Master Kubernetes Administration  

---

## Course Agenda  
1. **Introduction to Kubernetes**  
2. **Cluster Architecture, Installation, and Configuration**  
3. **Workloads and Scheduling**  
4. **Services and Networking**  
5. **Storage in Kubernetes**  
6. **Security Essentials**  
7. **Cluster Maintenance and Troubleshooting**  
8. **Practice Labs and Mock Exams**  

--- 


# What is Kubernetes?  
- Kubernetes, often abbreviated as **K8s**, is an open-source platform for **automating deployment**, **scaling**, and **management of containerized applications**.  
- Originally developed by Google and donated to the **Cloud Native Computing Foundation (CNCF)**.  

🔗 [Introduction to Kubernetes](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)  

---

# Why Kubernetes?  
- Simplifies managing containerized applications in distributed environments.  
- Key advantages:  
  - **Declarative Configuration**: Define desired state in YAML/JSON.  
  - **Automated Recovery**: Self-healing capabilities.  
  - **Horizontal Scaling**: Automatically adjust workloads based on demand.  

🔗 [Why Kubernetes](https://kubernetes.io/docs/concepts/overview/why-kubernetes/)  

---

# Kubernetes Use Cases  
- **Microservices Architecture**: Simplifies deployment and management.  
- **High-Availability Applications**: Ensures uptime through redundancy.  
- **CI/CD Pipelines**: Accelerates development and delivery cycles.  
- **Hybrid/Multicloud Deployments**: Unified control across environments.  

🔗 [Kubernetes Use Cases](https://kubernetes.io/docs/concepts/overview/use-cases/)  

---

# Kubernetes Key Terminology  
- **Container**: A lightweight, standalone executable (e.g., Docker).  
- **Pod**: The smallest deployable unit in Kubernetes.  
- **Cluster**: A set of nodes working together.  
- **Namespace**: Logical isolation of resources within a cluster.  

🔗 [Key Concepts](https://kubernetes.io/docs/concepts/)  

---

# Key Features of Kubernetes  
1. **Orchestration**: Automates container scheduling and lifecycle management.  
2. **Service Discovery and Load Balancing**: Automatically discovers services and balances traffic.  
3. **Self-Healing**: Replaces failed containers and restarts unhealthy pods.  
4. **Declarative Configuration**: Manage resources using YAML/JSON manifests.  
5. **Storage Orchestration**: Supports dynamic and persistent storage.  

🔗 [Kubernetes Features](https://kubernetes.io/docs/concepts/overview/components/)  

---

# Kubernetes vs. Traditional Systems  
| Feature                | Kubernetes                      | Traditional Systems            |  
|------------------------|--------------------------------|--------------------------------|  
| Deployment            | Declarative (YAML/JSON)       | Manual or Script-based         |  
| Scaling               | Automatic                     | Manual or Limited              |  
| Failover              | Self-healing                 | Requires Manual Intervention   |  
| Resource Utilization  | Optimized                     | Often Over-provisioned         |  

🔗 [Kubernetes Overview](https://kubernetes.io/docs/concepts/overview/)  

---

# Kubernetes Ecosystem  
- **Core Components**: Nodes, Control Plane, etc.  
- **Tools and Extensions**: Helm (Package Manager), Prometheus (Monitoring), Istio (Service Mesh).  
- **CNI Plugins**: Flannel, Calico, Weave for networking.  
- **Storage Options**: NFS, AWS EBS, GCP PD, Ceph.  

🔗 [Kubernetes Ecosystem](https://kubernetes.io/docs/home/)

---

# Cluster Architecture  

### Control Plane Components:  
1. **kube-apiserver**:  
   - Acts as the front end for the Kubernetes control plane.  
   - Handles all REST requests and validates configurations.  
   - 🔗 [kube-apiserver Documentation](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/)  

2. **etcd**:  
   - A distributed, reliable key-value store for all cluster data.  
   - Ensures consistency and stores the state of the cluster.  
   - 🔗 [etcd Documentation](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/)  

3. **kube-scheduler**:  
   - Assigns workloads (pods) to appropriate nodes.  
   - Bases decisions on resource availability, taints/tolerations, and affinity/anti-affinity rules.  
   - 🔗 [kube-scheduler Documentation](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/)  

4. **kube-controller-manager**:  
   - Runs controllers to ensure desired state:  
     - Node Controller  
     - Replication Controller  
     - Endpoints Controller  
     - Service Account Controller  
   - 🔗 [kube-controller-manager Documentation](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/)  

---

# Node Components  

1. **kubelet**:  
   - An agent that runs on each node.  
   - Ensures containers in pods are running as expected.  
   - Communicates with the control plane.  
   - 🔗 [kubelet Documentation](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)  

2. **kube-proxy**:  
   - Handles networking for Kubernetes Services.  
   - Maintains network rules and forwards requests to the appropriate pods.  
   - 🔗 [kube-proxy Documentation](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/)  

3. **Container Runtime**:  
   - Responsible for running containers (e.g., containerd, CRI-O, Docker).  
   - 🔗 [Container Runtimes Documentation](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)  

---

# Installation Tools  

### 1. kubeadm  
- A standard tool to set up Kubernetes clusters easily.  
- Automates installation of control plane and worker node components.  
- Ideal for production-grade clusters.  
- 🔗 [kubeadm Documentation](https://kubernetes.io/docs/reference/setup-tools/kubeadm/)  

---

### 2. Minikube  
- Lightweight Kubernetes for local testing.  
- Sets up a single-node cluster on a local machine.  
- Suitable for development and practice.  
- 🔗 [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)  

---

### 3. Managed Kubernetes Solutions  
- Cloud providers offer managed Kubernetes services:  
  - **Amazon EKS**: 🔗 [Amazon EKS Documentation](https://docs.aws.amazon.com/eks/)  
  - **Azure AKS**: 🔗 [Azure AKS Documentation](https://learn.microsoft.com/en-us/azure/aks/)  
  - **Google GKE**: 🔗 [Google GKE Documentation](https://cloud.google.com/kubernetes-engine)  

---

# Configuration Best Practices  

### Use ConfigMaps and Secrets  
- **ConfigMaps**: Store non-sensitive configuration data separately from application code.  
  - 🔗 [ConfigMaps Documentation](https://kubernetes.io/docs/concepts/configuration/configmap/)  
- **Secrets**: Store sensitive data securely.  
  - 🔗 [Secrets Documentation](https://kubernetes.io/docs/concepts/configuration/secret/)  

---

### Leverage Namespaces  
- **Namespaces**:  
  - Isolate resources within the same cluster.  
  - Ideal for multi-team or multi-environment use cases (e.g., dev, staging, production).  
  - 🔗 [Namespaces Documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)  

---

### Resource Management  
1. **Resource Quotas**:  
   - Limit resource consumption per namespace.  
   - 🔗 [Resource Quotas Documentation](https://kubernetes.io/docs/concepts/policy/resource-quotas/)  

2. **Limit Ranges**:  
   - Set default requests and limits for containers in a namespace.  
   - 🔗 [Limit Ranges Documentation](https://kubernetes.io/docs/tasks/administer-cluster/manage-resources/limit-range/)  

---

# Key Kubernetes Workloads  

### 1. **Pods**  
- Smallest deployable unit in Kubernetes.  
- Can run a single container or multiple tightly coupled containers.  
- Pods share:  
  - **Network namespace**: Same IP and ports.  
  - **Storage**: Shared volumes.  
- 🔗 [Pods Documentation](https://kubernetes.io/docs/concepts/workloads/pods/)  

---

## Example: Creating a Pod  

### Command Line  
```bash  
kubectl run my-pod --image=nginx --restart=Never  
```  

### YAML File  
```yaml  
apiVersion: v1  
kind: Pod  
metadata:  
  name: my-pod  
spec:  
  containers:  
    - name: nginx  
      image: nginx  
``` 

---

# Deployments  

### 2. **Deployments**  
- Manage **stateless applications** and ensure the desired number of pods are running.  
- Supports:  
  - Rolling updates.  
  - Rollbacks to previous versions.  
- Useful for web servers and API backends.  
- 🔗 [Deployments Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)  

---

## Example: Creating a Deployment  

### Command Line  
```bash  
kubectl create deployment my-deployment --image=nginx  
```  

### YAML File  
```yaml  
apiVersion: apps/v1  
kind: Deployment  
metadata:  
  name: my-deployment  
spec:  
  replicas: 3  
  selector:  
    matchLabels:  
      app: nginx  
  template:  
    metadata:  
      labels:  
        app: nginx  
    spec:  
      containers:  
        - name: nginx  
          image: nginx  
```

---

# StatefulSets  

### 3. **StatefulSets**  
- Manage **stateful applications** requiring stable, persistent identities.  
- Ensures:  
  - Stable network identities.  
  - Persistent storage across pod restarts.  
- Commonly used for databases like MySQL, MongoDB.  
- 🔗 [StatefulSets Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)  

---

## Example: Creating a StatefulSet  

### YAML File (Command line not recommended for StatefulSets)  
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

# DaemonSets  

### 4. **DaemonSets**  
- Ensure all (or some) nodes run a copy of a specific pod.  
- Common use cases:  
  - Log collectors (e.g., Fluentd).  
  - Monitoring agents (e.g., Prometheus Node Exporter).  
- 🔗 [DaemonSets Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)  

---

## Example: Creating a DaemonSet  

### YAML File (Command line not recommended for DaemonSets)  
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

# Jobs and CronJobs  

### 5. **Jobs and CronJobs**  
- **Jobs**: Run tasks to completion. Useful for batch processing.  
  🔗 [Jobs Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/job/)  
- **CronJobs**: Schedule tasks based on time intervals. Ideal for periodic backups or cleanups.  
  🔗 [CronJobs Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)  

---

## Example: Creating a Job  

### Command Line  
```bash  
kubectl create job my-job --image=busybox -- echo "Hello Kubernetes"  
```  

### YAML File  
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

## Example: Creating a CronJob  

### Command Line  
```bash  
kubectl create cronjob my-cronjob --image=busybox --schedule="*/1 * * * *" -- echo "Hello from CronJob"  
```  

### YAML File  
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

# Scheduling Basics  

### 1. Labels and Selectors  
- **Labels**: Key-value pairs attached to objects (e.g., pods, nodes).  
  - Examples: `app=frontend`, `tier=backend`.  
- **Selectors**: Match labels to identify objects for scheduling.  
- 🔗 [Labels and Selectors Documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)  

---

# Node Affinity and Anti-Affinity  

### 2. Node Affinity and Anti-Affinity  
- **Node Affinity**: Schedule pods on nodes based on labels.  
  - Example: "Only schedule on nodes with SSD storage."  
- **Anti-Affinity**: Prevent pods from being scheduled on the same node.  
  - Example: "Spread replicas across multiple nodes."  
- 🔗 [Affinity and Anti-Affinity Documentation](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity)  

---

## Example: Node Affinity  

### YAML File Example  
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

# Taints and Tolerations  

### 3. Taints and Tolerations  
- **Taints**: Applied to nodes to restrict pod scheduling.  
  - Example: `NoSchedule` taint prevents pods without tolerations from being scheduled.  
- **Tolerations**: Allow pods to bypass taints and be scheduled on specific nodes.  
- 🔗 [Taints and Tolerations Documentation](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)  

---

## Example: Taints and Tolerations  

### Add Taint to a Node  
```bash  
kubectl taint nodes node1 key=value:NoSchedule  
```  

### YAML File Example for Toleration  
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

# Resource Requests and Limits  

### 4. Resource Requests and Limits  
- **Resource Requests**: Minimum CPU/Memory a pod needs to run.  
- **Resource Limits**: Maximum CPU/Memory a pod can consume.  
- Prevents resource starvation and overcommitment.  
- 🔗 [Resource Management Documentation](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)  

---

## Example: Resource Requests and Limits  

### YAML File Example  
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

# Priority Classes  

### 5. Priority Classes  
- Define the importance of workloads during scheduling.  
- Higher-priority pods are scheduled first.  
- Lower-priority pods are evicted to make space during resource shortages.  
- 🔗 [Priority Classes Documentation](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/)  

---

## Example: Priority Classes  

### Create a Priority Class  
```bash  
kubectl create priorityclass high-priority --value=1000 --global-default=false --description="High-priority workload"  
```  

### YAML File Example for Priority Class  
```yaml  
apiVersion: scheduling.k8s.io/v1  
kind: PriorityClass  
metadata:  
  name: high-priority  
value: 1000  
globalDefault: false  
description: "High-priority workload"  
```  

### Pod Using Priority Class  
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

# Debugging Scheduling Issues  

### Debugging Commands  
- Use `kubectl describe pod <pod-name>` to review scheduling events.  
- Check events for detailed scheduling-related messages:  
  ```bash  
  kubectl get events --sort-by='.metadata.creationTimestamp'  
  ```  
- Use the **Kubernetes Scheduler Simulator** to test specific scenarios.  
- 🔗 [Debugging Pods Documentation](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pod-replication-controller/)  

---

# Kubernetes Networking Model  

### Networking in Kubernetes: Key Principles  
1. **Flat Network Space**: All pods can communicate with each other without NAT.  
2. **Service Discovery**: Built-in DNS to resolve service names.  
3. **Flexible Connectivity**: Supports ClusterIP, NodePort, LoadBalancer, and Ingress.  

🔗 [Kubernetes Networking Overview](https://kubernetes.io/docs/concepts/cluster-administration/networking/)  

---

# Services in Kubernetes  

### 1. ClusterIP (Default)  
- Exposes a service internally within the cluster.  
- Pods access the service via its DNS name or IP address.  
- 🔗 [ClusterIP Documentation](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services---service-types)  

---

## Example: ClusterIP  

### Command Line  
```bash  
kubectl expose deployment my-deployment --type=ClusterIP --port=80  
```  

### YAML File  
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

### 2. NodePort  
- Exposes a service on each node's IP and a static port (30000-32767).  
- Allows external access to the service.  
- 🔗 [NodePort Documentation](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport)  

---

## Example: NodePort  

### Command Line  
```bash  
kubectl expose deployment my-deployment --type=NodePort --port=80  
```  

### YAML File  
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

### 3. LoadBalancer  
- Exposes a service externally using a cloud provider's load balancer.  
- Requires integration with supported cloud providers (e.g., AWS, Azure, GCP).  
- 🔗 [LoadBalancer Documentation](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer)  

---

## Example: LoadBalancer  

### Command Line  
```bash  
kubectl expose deployment my-deployment --type=LoadBalancer --port=80  
```  

### YAML File  
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

# Ingress  

### 4. Ingress  
- Provides HTTP(S) routing to services within the cluster.  
- Supports advanced features like TLS termination and path-based routing.  
- Requires an **Ingress Controller** (e.g., NGINX, Traefik).  
- 🔗 [Ingress Documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/)  

---

## Example: Ingress  

### YAML File  
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

# Core Networking Concepts  

### 1. DNS in Kubernetes  
- Automatically creates DNS entries for services.  
- Pods can resolve services using their names:  
  ```plaintext  
  <service-name>.<namespace>.svc.cluster.local  
  ```  
- 🔗 [DNS Documentation](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)  

---

## Example: Verifying DNS  

### Command Line  
```bash  
kubectl exec -it <pod-name> -- nslookup my-service  
```  

---

### 2. Network Policies  
- Control traffic flow between pods or between pods and external resources.  
- Specify **allow/deny** rules for ingress/egress traffic.  
- 🔗 [Network Policies Documentation](https://kubernetes.io/docs/concepts/services-networking/network-policies/)  

---

## Example: Network Policy  

### YAML File  
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

# Debugging Networking Issues  

### Troubleshooting Steps  
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

# Storage in Kubernetes  

### Key Concepts  
1. **Volumes**: Attach storage to pods.  
2. **Persistent Volumes (PV)**: Cluster-wide storage resources.  
3. **Persistent Volume Claims (PVC)**: Requests for storage by pods.  
4. **Dynamic Provisioning**: Automatically provisions storage using a StorageClass.  

🔗 [Storage Concepts Documentation](https://kubernetes.io/docs/concepts/storage/)  

---

# Volumes  

### What are Volumes?  
- Allow pods to persist data beyond the lifecycle of a container.  
- Types of volumes:  
  - **emptyDir**: Temporary storage tied to the pod’s lifecycle.  
  - **hostPath**: Maps a host machine’s directory into the pod.  
  - **configMap**: Provide configurations as files.  
  - **secret**: Securely provide sensitive information.  

🔗 [Volumes Documentation](https://kubernetes.io/docs/concepts/storage/volumes/)  

---

## Example: Using a Volume  

### YAML File  
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

# Persistent Volumes (PV)  

### What are Persistent Volumes?  
- Abstracts storage from specific pods.  
- Supports multiple backends like NFS, AWS EBS, GCE PD.  
- Must be **manually created** or dynamically provisioned.  

🔗 [Persistent Volumes Documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)  

---

## Example: Creating a Persistent Volume  

### YAML File  
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

# Persistent Volume Claims (PVC)  

### What are Persistent Volume Claims?  
- A request for storage from a pod.  
- Links pods with available Persistent Volumes.  
- Defines:  
  - Requested size.  
  - Access modes (e.g., ReadWriteOnce).  

🔗 [Persistent Volume Claims Documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)  

---

## Example: Creating a PVC  

### YAML File  
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

# Dynamic Provisioning  

### What is Dynamic Provisioning?  
- Automatically provisions storage when PVCs are created.  
- Requires a **StorageClass** configured in the cluster.  

🔗 [Dynamic Provisioning Documentation](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/)  

---

## Example: Dynamic Provisioning with a StorageClass  

### StorageClass YAML  
```yaml  
apiVersion: storage.k8s.io/v1  
kind: StorageClass  
metadata:  
  name: my-storageclass  
provisioner: kubernetes.io/aws-ebs  
parameters:  
  type: gp2  
```  

### PVC Using the StorageClass  
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

# Storage for Configurations and Secrets  

### ConfigMaps  
- Use ConfigMaps to store configuration data as files or environment variables.  
🔗 [ConfigMaps Documentation](https://kubernetes.io/docs/concepts/configuration/configmap/)  

---

## Example: Using a ConfigMap  

### Create a ConfigMap from CLI  
```bash  
kubectl create configmap app-config --from-literal=key1=value1  
```  

### YAML File Example  
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

### Secrets  
- Use Secrets to store sensitive data securely (e.g., passwords, tokens).  
🔗 [Secrets Documentation](https://kubernetes.io/docs/concepts/configuration/secret/)  

---

## Example: Using a Secret  

### Create a Secret from CLI  
```bash  
kubectl create secret generic app-secret --from-literal=username=admin --from-literal=password=pass123  
```  

### YAML File Example  
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

# Debugging Storage Issues  

### Common Troubleshooting Commands  
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

# Authentication and Authorization  

### Authentication  
- Identifies **who** is making a request (e.g., users, service accounts).  
- Common authentication methods:  
  - Certificates  
  - Bearer Tokens  
  - External identity providers (e.g., OIDC).  

🔗 [Authentication Documentation](https://kubernetes.io/docs/reference/access-authn-authz/authentication/)  

---

### Authorization  
- Controls **what** a user or process can do.  
- Methods:  
  - **Role-Based Access Control (RBAC)**: Assign permissions to users or groups.  
  - Attribute-Based Access Control (ABAC) and Webhook Authorization (less common).  

🔗 [Authorization Documentation](https://kubernetes.io/docs/reference/access-authn-authz/authorization/)  

---

## Example: RBAC Role and RoleBinding  

### Role YAML File  
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

### RoleBinding YAML File  
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

# Pod Security  

### Pod Security Standards (PSS)  
- Ensure security at the pod level.  
- Three predefined standards:  
  1. **Privileged**: No restrictions.  
  2. **Baseline**: Minimum standards for common workloads.  
  3. **Restricted**: High-security standards.  

🔗 [Pod Security Standards Documentation](https://kubernetes.io/docs/concepts/security/pod-security-standards/)  

---

## Example: Enforcing Pod Security  

### Apply Pod Security Standards via Labels  
```bash  
kubectl label namespace my-namespace pod-security.kubernetes.io/enforce=baseline  
```  

---

### Securing Pods with SecurityContext  
- Set security options for pods or containers.  
- Examples: Run as non-root, drop capabilities, restrict privilege escalation.  

🔗 [Security Context Documentation](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)  

---

## Example: SecurityContext  

### YAML File  
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

# Networking Security  

### Network Policies  
- Control pod-to-pod and pod-to-external traffic.  
- Define **allow** or **deny** rules for ingress and egress.  

🔗 [Network Policies Documentation](https://kubernetes.io/docs/concepts/services-networking/network-policies/)  

---

## Example: Network Policy  

### YAML File  
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

# Image Security  

### Recommendations for Secure Container Images  
1. Use minimal base images.  
2. Regularly scan images for vulnerabilities.  
3. Avoid running containers as root.  

🔗 [Securing Images Documentation](https://kubernetes.io/docs/concepts/containers/images/#security)  

---

## Example: Using an ImagePullSecret  

### YAML File  
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

# Secrets Management  

### Use Kubernetes Secrets for Sensitive Data  
- Store sensitive information like passwords, tokens, and SSH keys.  
- Secrets are **base64-encoded**, not encrypted by default.  

🔗 [Secrets Documentation](https://kubernetes.io/docs/concepts/configuration/secret/)  

---

## Example: Secret for Environment Variables  

### YAML File  
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

# Debugging Security Issues  

### Common Troubleshooting Commands  
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

# Cluster Maintenance  

### 1. Regular Cluster Backups  
- Backup **etcd**, the key-value store holding the cluster state.  
- Use `etcdctl` or automation tools like Velero.  

🔗 [Backing up etcd Documentation](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-etcd)  

---

## Example: Backing up etcd  

### Command Line  
```bash  
ETCDCTL_API=3 etcdctl snapshot save snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key  
```  

---

### 2. Upgrading Kubernetes Clusters  
- Use `kubeadm upgrade` to safely update control plane and nodes.  
- Ensure you follow version skew policies between components.  

🔗 [Cluster Upgrades Documentation](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)  

---

## Example: Upgrading a Cluster  

### Upgrade Control Plane  
```bash  
kubeadm upgrade apply v1.26.0  
```  

### Upgrade kubelet and kubectl on Nodes  
```bash  
apt-get update && apt-get install -y kubelet=1.26.0-00 kubectl=1.26.0-00  
systemctl restart kubelet  
```  

---

# Monitoring and Logging  

### 1. Enable Metrics Server  
- Provides resource metrics for pods and nodes.  
- Required for `kubectl top` commands.  

🔗 [Metrics Server Documentation](https://github.com/kubernetes-sigs/metrics-server)  

---

## Example: Install Metrics Server  

### YAML File  
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

### 2. Logging with Fluentd and Elasticsearch  
- Aggregate logs for the cluster using tools like Fluentd or Loki.  
- Analyze logs via Kibana or Grafana.  

🔗 [Logging Documentation](https://kubernetes.io/docs/concepts/cluster-administration/logging/)  

---

# Troubleshooting Basics  

### 1. Inspect Pods and Nodes  
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

### 2. Debugging Pods  
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

# Troubleshooting Tools  

### 1. Use `kubectl` Debugging Features  
- Debug a pod with ephemeral containers:  
  ```bash  
  kubectl debug <pod-name> --image=busybox  
  ```  

🔗 [Debugging Ephemeral Containers Documentation](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#ephemeral-container)  

---

### 2. Network Troubleshooting  
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

### 3. Analyze Events  
- Check cluster events for errors or warnings:  
  ```bash  
  kubectl get events --sort-by='.metadata.creationTimestamp'  
  ```  

---

# Disaster Recovery  

### Key Steps for Recovery  
1. Restore **etcd** from a backup.  
2. Recreate control plane components with `kubeadm`.  
3. Validate cluster state and reconfigure workloads.  

🔗 [Disaster Recovery Documentation](https://kubernetes.io/docs/tasks/administer-cluster/disaster-recovery/)  

---

## Example: Restoring etcd  

### Command Line  
```bash  
ETCDCTL_API=3 etcdctl snapshot restore snapshot.db \
  --data-dir=/var/lib/etcd-from-backup  
```  

Update the `etcd` pod configuration to point to the restored data directory.  

---

# Best Practices  

### Maintenance Tips  
- Regularly back up **etcd** and validate snapshots.  
- Test upgrades in a staging environment before production.  
- Use tools like Prometheus and Grafana for proactive monitoring.  

### Troubleshooting Advice  
- Always start with `kubectl describe` for resource details.  
- Check cluster-wide events for anomalies.  
- Keep cluster logs centralized and searchable.  

🔗 [Cluster Administration Documentation](https://kubernetes.io/docs/tasks/administer-cluster/)  

---

# Practice Labs and Mock Exams  

### Goal of Hands-On Practice  
- Reinforce understanding of Kubernetes concepts.  
- Prepare for real-world cluster management tasks.  
- Build confidence for the CKA exam.

🔗 [CKA Exam Curriculum](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/)  

---

# Lab 1: Setting Up a Kubernetes Cluster  

### Tasks:  
1. Install Kubernetes using `kubeadm`.  
2. Configure networking with **Calico** or **Flannel**.  
3. Add worker nodes to the cluster.  

🔗 [Kubeadm Setup Documentation](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)  

---

## Example: Initializing the Cluster  

### Command Line  
```bash  
kubeadm init --pod-network-cidr=192.168.0.0/16  
```  

Apply a network plugin (e.g., Calico):  
```bash  
kubectl apply -f https://docs.projectcalico.org/v3.25/manifests/calico.yaml  
```  

---

# Lab 2: Managing Workloads  

### Tasks:  
1. Create a Deployment with 3 replicas of **nginx**.  
2. Scale the Deployment to 5 replicas.  
3. Update the Deployment to a new version of nginx.  

🔗 [Workloads Documentation](https://kubernetes.io/docs/concepts/workloads/)  

---

## Example: Scaling a Deployment  

### Command Line  
```bash  
kubectl scale deployment my-deployment --replicas=5  
```  

---

## Example: Updating a Deployment  

### Command Line  
```bash  
kubectl set image deployment/my-deployment nginx=nginx:1.21  
```  

---

# Lab 3: Configuring Services and Networking  

### Tasks:  
1. Create a **ClusterIP** service for a backend pod.  
2. Create an **Ingress** for HTTP traffic to a web application.  
3. Define a **NetworkPolicy** to allow traffic only from specific pods.  

🔗 [Networking Documentation](https://kubernetes.io/docs/concepts/services-networking/)  

---

## Example: ClusterIP Service YAML  
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

# Lab 4: Persistent Storage  

### Tasks:  
1. Create a Persistent Volume (PV) and Persistent Volume Claim (PVC).  
2. Mount the PVC to a pod.  
3. Dynamically provision storage using a **StorageClass**.  

🔗 [Storage Documentation](https://kubernetes.io/docs/concepts/storage/)  

---

## Example: Mounting a PVC in a Pod  

### YAML File  
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

# Lab 5: Securing the Cluster  

### Tasks:  
1. Create and apply a **NetworkPolicy** to secure traffic.  
2. Use **RBAC** to define granular permissions.  
3. Apply a **PodSecurityPolicy** to restrict privileged operations.  

🔗 [Security Documentation](https://kubernetes.io/docs/concepts/security/)  

---

## Example: RBAC Role for Pods  

### YAML File  
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

# Lab 6: Cluster Maintenance  

### Tasks:  
1. Backup and restore **etcd** data.  
2. Upgrade the cluster using `kubeadm`.  
3. Set up monitoring with **Metrics Server** and visualize metrics in Prometheus/Grafana.  

🔗 [Cluster Maintenance Documentation](https://kubernetes.io/docs/tasks/administer-cluster/)  

---

# Mock Exam: Sample Scenarios  

### Scenario 1: Troubleshooting  
- Pod stuck in **CrashLoopBackOff**.  
- Debug and resolve the issue using logs and events.  

### Scenario 2: Scaling and Updates  
- Scale a Deployment, then perform a rolling update.  

### Scenario 3: Networking  
- Secure communication between frontend and backend pods using **NetworkPolicy**.  

---

# Exam Preparation Tips  

### 1. Time Management  
- Practice solving tasks within time limits.  
- Prioritize tasks based on complexity.  

### 2. Focus Areas  
- Master `kubectl` commands.  
- Familiarize yourself with YAML file structures.  

### 3. Read Official Documentation  
- The exam environment provides access to Kubernetes documentation.  

🔗 [CKA Tips and Tricks](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/)  

---
