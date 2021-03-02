# Table of Contents

- [Introudction](#Introduction)
- [Prerequisites](#Prerequisites)
- [Installation](#Installation)
- [How it works](<#How\ it\ works>)
- [Uninstallation](#Uninstallation)

# Introduction

A simple REST API that saves its visitors' IPs. The api is deployed to a kubernetes cluster baked by a PostgreSQL
database deployment in the same cluster.

# Prerequisites

- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Helm](https://helm.sh/docs/intro/install/)
- [k3d](https://rancher.com/docs/k3s/latest/en/installation/)

# Installation

1. To get the cluster up and running locally, simply run

```bash
$ ./deploy/kube/bootstrap
```

2. Check pods status

```bash
$ kubectl get pods
NAME                      READY   STATUS    RESTARTS   AGE
pg-release-postgresql-0   1/1     Running   0          73m
halan-6d7f45d547-m5lkx    1/1     Running   2          73m

```

3. Once the pods get scheduled, test the api

```bash
$ curl localhost
"Halan ROCKS"

$ curl localhost/ip
{"ip":"10.42.2.7"}

$ curl localthost/allips
{"ips":[{"id":1,"ip_str":"10.42.2.7"},{"id":2,"ip_str":"10.42.2.5"}]}
```

# How it works

Let's walk through some of the keystone commands in the bootstrap script and see how we got the cluster up and running.

1.

```bash
$ k3d cluster create \
    -p "${INGRESS_HTTP_PORT}:80@loadbalancer"
    --agents 2 \
    "${CLUSTER_NAME}"
```

The command creates a k8s cluster using rancher k8s with two agents and port-forwards traffic from the host port, in this case, INGRESS_HTTP_PORT to port 80 inside the cluster's load balancer. An [ingress resouce definition](https://github.com/A-Fayez/halan/blob/6f5ab53b79e619fd21f8caa4fd7e29f5a62a34d4/deploy/kube/api.yml#L2) is used to route requests to the [api service](https://github.com/A-Fayez/halan/blob/6f5ab53b79e619fd21f8caa4fd7e29f5a62a34d4/deploy/kube/api.yml#L19).

2.

```bash
$ helm repo add bitnami https://charts.bitnami.com/bitnami
$ helm install "${HELM_RELEASE_NAME}" bitnami/postgresql
```

The command deploys a production-grade PostgreSQL on the Kubernetes cluster using [Bitnami's helm chart](https://github.com/bitnami/charts/tree/master/bitnami/postgresql/#installing-the-chart).

3.

```bash
$ kubectl apply -f "${SCRIPT_DIR}"/api.yml
```

This deploys the api deployment and service to the cluster using necessary environment configurations.

# Uninstallation

```bash
$ ./deploy/kube/teardown
```
