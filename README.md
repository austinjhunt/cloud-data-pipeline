# CS 5287: Principles of Cloud Computing
## Programming Assignment 1
Programming assignment 1 for Vanderbilt University's CS 5287: Principles of Cloud Computing

This project uses [kafka-python](https://pypi.org/project/kafka-python/), a Python client for the [Apache Kafka](https://kafka.apache.org/), "an open-source distributed event streaming platform used by thousands of companies for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications"


# Steps Taken to Build Project
## Milestone 1 Steps (due Week 4, 9/15/2021)

### Setting Up A Local Ubuntu 20.04 VM with VirtualBox (each team member must do this)
- If not installed, [install VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- Install Ubuntu 20.04 LTS on VirtualBox using [these instructions](https://fossbytes.com/how-to-install-ubuntu-20-04-lts-virtualbox-windows-mac-linux/)
- Rather than creating a shared folder between the host and guest OS, we'll use git to keep the code synchronized between the guest and host. You can develop locally on your host OS using an IDE and whatever changes you commit can be pulled into the guest.
  - Log into your Ubuntu 20.04 VM once you've created it.
  - Open a Terminal window.
  - Set up Python 3 on your VM using [these instructions](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server).
  - Clone the project repository: `git clone https://github.com/austinjhunt/cs5287progassign1.git`
  - Navigate into the project: `cd cs5287progassign1`
  - Create a virtual environment to isolate the Python package installations to this project: `python3 -m venv venv`
  - Activate the virtual environment: `source venv/bin/activate`
  - Install the Python requirements: `pip install -r requirements.txt`
### Creating [Chameleon Cloud](https://chameleoncloud.org) VMs with KVM
   - Sign into [Chameleon Cloud](https://chameleoncloud.org). Navigate to the project for this class.
   - Choose the **Experiment** tab at the top, and choose the **KVM** option from the dropdown menu.
   - From within the KVM view, choose **Compute** on the left navigation menu, then choose the **Instances** option to open the list of currently running instances.
   - Select the **Launch Instance** button.
     - Details:
       - Instance Name: **team10-vm** since we are team 10.
       - Description: **Team 10 VM**
       - Count: **2**
     - Source:
       - Boot Source: **Image**
       - Choose **CC-Ubuntu20.04**
     - Flavor: **m1.medium**
     - Networks: **CH-822922-net**
     - Network Ports: skip
     - Security Groups: **SHARED-CLOUDCOMPUTING**; this security group contains all of the necessary firewall rules for CouchDB, Kafka, and SSH.
     - Keypair: create a new one, give it a name, choose SSH key as the type, and download it. Then, open a terminal window, and execute the following command to change the file permissions and add the private key identity to your SSH authentication agent: ``` chmod 600 <file>.pem && ssh-add <file>.pem ```
     - Configuration: skip
     - Server Groups: skip
     - Scheduler Hints: skip
     - Metadata: skip
     - Submit by clicking the **Launch Instance** button. This will create two VMs, **team10-vm-1** and **team10-vm-2**
   - Once created, allocate a **floating IP** for each one. For each VM:
     - On the far right of the VM row in the Instances table, choose the dropdown, then choose **Associate Floating IP**.
     - Select any of the available IPs, and submit by clicking the **Associate** button.
   - Once allocated, take note of the private and public IP addresses of both VMs and add an entry to the cloud-hosts value in [config.json](config.json) in this project for each VM, as follows:
    ```
    "team10-vm-1": {
            "private": "1.2.3.4",
            "public": "5.6.7.8"
        },
    ```
   - SSH to both VMs using the key-based authentication enabled through the keypair selection previously. I like using [Iterm2](https://iterm2.com/downloads/stable/latest) for MacOS for this: `ssh cc@<public ip of VM>`
   - On each VM, do the following:
     - Install Apache Kafka using [these instructions](https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-20-04)
     - Set up Python3 using [these instructions](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server)

### The Data Source
We are using the [Yahoo Finance API](https://finance.yahoo.com/quotes/API,Documentation/view/v1/) as a data source for our pipeline. Specifically, we use the [yfinance](https://pypi.org/project/yfinance/) Python package for downloading and sending Stock Market data into the Kafka pipeline.
## Milestone 2 Steps (due Week 5, 9/22/2021)

## Milestone 3 Steps (due Week 6, 9/29/2021)