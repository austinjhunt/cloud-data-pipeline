# Milestone 3
## [Video Demonstration](https://youtu.be/XJ-yxZktSjk)
## Requirements
- Design additional child Ansible playbooks to install CouchDB on VM2 (or VM3) using the same configuration as we did in Assignment #1
  - Complete
- Once again execute vagrant provision so that the updated ansible master playbook can install and configure the CouchDB. You do not want to recreate the earlier parts so Ansible playbook should treat the previous parts from Milestone 1 and 2 as idempotent because the previous parts will already be running on the cloud (at least on the chameleon cloud). If you do not want to do this step to show idempotent operations, then everything done in milestones 1 and 2 should be terminated and the entire process automated (which should not be a big deal as it was already shown to work before). For that, Ansible supports a way in which you can skip tasks and start at a desired task.
  - Complete.
- As before, Consumer code should be able to dump the received contents into CouchDB
  - Complete.
- Data should be viewable in CouchDB via web console.
  - Complete.
- Note: Keep a separate master playbook that is able to clean up everything after the demo is done.
  - Clean up is taken care of. Note: Cloud infrastructure cleanup is not included in a separate master playbook, but rather the same master playbook that creates it BECAUSE the cleanup process uses in-memory variables registered during the creation process (e.g. id attributes of EC2 objects).
- Demo the entire assignment to the TA including a final cleanup of everything.
  - Complete. (Video is here](https://www.youtube.com/watch?v=XJ-yxZktSjk)

