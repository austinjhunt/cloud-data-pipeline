# Milestone 1

## Requirements
- You will need to tear down at least one of the VMs prior to this assignment because we will need the master to be a m1.medium machine. On Chameleon, they allow you to resize it. I have tried this and it worked. So my suggestion is to resize say VM2 to m1.medium rather than having to terminate and recreate both VMs. If you prefer to terminate and recreate, then reuse your vagrantfile and Assignment 2 playbooks to create the two VMs (say VM2 is m1.medium and VM3 still is m1.small)
- Reuse and extend the playbooks to install all the necessary underlying packages you need to get Kubernetes work.
- Now do this manually for milestone 1
  - Log into VM2 (master) and run the kubeadm command on master to create a cluster
  - Add VM3 as a worker to this master
  - Taint the master so that the master can also become a worker
  - Run [this scaffolding code](https://github.com/asgokhale/CloudComputingCourse) (Deployment and Job demos) to show that you can deploy a deployment pod and worker pod on your k8s cluster