# Milestone 1
## [Video Demonstration 1](https://youtu.be/xMSoP5IG0pU)
## [Video Demonstration 2](https://youtu.be/mAWtgLduiPc)
## Requirements
- VM1.1 (or any one of the local Virtualbox VMs designated to run a producer) should be created via Vagrant and the others will still be manual from previous assignment.
  - Complete.
- Do not teardown your VM2 and VM3 from assignment 1 (on Chameleon; for AWS/GCP you will probably have to in order to avoid credits getting deducted)
  - Complete. Chameleon Cloud experiencing issues so two new VMs created in AWS.
- All necessary packages including private key to access Cloud, Ansible installation, producer.py file, etc should all be available on Vagrant-created VM so that they are accessible to both vagrant and ansible master playbook
  - Complete. We share this entire project repository with the Vagrant-created VM using: `config.vm.synced_folder "../../", "/vagrant"` in the Vagrantfile.
  - We also run all necessary installation in the provisioning process using a [local-vm-provision.sh](../../automation/../../automation/local-vm/local-vm-provision.sh) provisioning script.
- Use the different playbooks from our Scaffolding code AnsibleOnly_Local_and_Cloud and demo that you can run these scripts manually from the generated VM.
  - Complete. Demonstrated use of scaffolding playbook from inside Vagrant VM to install Ansible on two remote AWS EC2 instances using the apt module.
- Upload progress made as video and documentation till that point to Brightspacemilestone 1
  - Complete. [Video is here](https://youtu.be/xMSoP5IG0pU)