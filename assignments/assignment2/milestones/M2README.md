# Milestone 2
## [Video Demonstration](https://youtu.be/XJ-yxZktSjk)
## Requirements
- Update your Vagrantfile so that it can execute a master Ansible playbook thru the vagrantfile and then invoke vagrant provision (not vagrant up)
  - Complete.
- This master Ansible playbook should be able to create VM2 and VM3 in the cloud (using a child playbook)
  - Complete.
- The master Ansible playbook should then invoke additional child playbooks to install Kafka and all the underlying needed packages, copy the consumer.py file to one of the cloud VMs, as well as set the server.properties file appropriately.
  - Complete
- Then, the master Ansible playbook via one of its child playbooks should be able to
  - Start ZooKeeper on VM2 (or VM3, your choice)
    - Complete
  - Start Apache Kafka brokers on both VM2 and VM3
    - Complete
  - Start Consumer on VM2 (or VM3, your choice)
    - Complete
- Team members should log into their respective laptop VMs (one of which is created by Vagrant) and run the producer code on each side, all of which should be able to stream their respective unique topic data with the realistic datasets that you used in Assignment 1 to Kafka exactly like we did for Assignment #1.
  - Complete.
- As before, Consumer should be able to receive all topic data from Kafka brokers.
  - Complete.
- Upload progress made via video and documentation till that point to Brightspace
  - Complete. [Video is here](https://youtu.be/XJ-yxZktSjk)
