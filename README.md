# CS 5287: Principles of Cloud Computing
## Programming Assignment 1
Programming assignment 1 for Vanderbilt University's CS 5287: Principles of Cloud Computing

This project uses [kafka-python](https://pypi.org/project/kafka-python/), a Python client for the [Apache Kafka](https://kafka.apache.org/), "an open-source distributed event streaming platform used by thousands of companies for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications".

The goal of the project is to gain experience implementing a data pipeline using clustered cloud architecture. We aim to implement a pipeline with the architecture shown in the image below:
![Architectural Diagram of Data Pipeline](img/pipeline.png)

Each team member will be able to run their own **Kafka Producer** on their own local VM (Ubuntu 20.04) within VirtualBox. Each producer will send stock market-related data (namely a stream of the current price) into the 2-node Kafka cluster in the cloud in which two brokers will run, each on their own Cloud VM. **One** of the cloud VMs will run a **Kafka Consumer** process which will consume, or receive, the produced messages from the Kafka Brokers. While consuming, the Consumer will further pipe the data into a **data sink**, which will just be a [CouchDB](https://couchdb.apache.org/) database. In a later stage, an intermediary step of processing will be added between the consumer and the data sink using Apache Spark. Here is another high level architectural diagram that shows which services/processes we intend to run on which host:

![Process Map Architecture](img/processmap.png)

We intend to run one producer on each team member's local VirtualBox VM, and we intend to lay out the processes for the Cloud VMs as follows:

- VM1
  - Kafka Broker id=0
  - Zookeeper (i.e. cluster bootstrap server)
  - Consumer (Python process )
- VM2
  - Kafka Broker id=1
  - CouchDB
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
   - Once allocated, take note of the private and public IP addresses of both VMs and add an entry to the cloud_hosts list in [config.json](src/config.json) in this project for each VM, as follows:
    ```
    {
      "private": "1.2.3.4",
      "public": "5.6.7.8"
    },
    ```
   - SSH to both VMs using the key-based authentication enabled through the keypair selection previously. I like using [Iterm2](https://iterm2.com/downloads/stable/latest) for MacOS for this: `ssh cc@<public ip of VM>`
   - On **BOTH VM**s, do the following:
     - Install OpenJDK JRE with [these instructions](https://ubuntu.com/tutorials/install-jre#2-installing-openjdk-jre)
     - Install (but don't start yet) Apache Kafka using [these instructions](https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-20-04)
     - You need to modify the Kafka Config to allow the public IP of the Kafka server to be used. Add the following line to the end of the `/home/kafka/kafka/config/server.properties` file: `advertised.listeners=PLAINTEXT://<PUBLIC IP OF CURRENT VM>:9092`
     - Set up Python3 using [these instructions](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server)
     - Clone this repo: `git clone https://github.com/austinjhunt/cs5287progassign1.git`
     - Navigate into the repo: `cd cs5287progassign1`
     - Execute `ufw.sh` with `sudo` to set up local firewall rules: `sudo ./ufw.sh`
     - Create and activate a Python3 virtual environment: `python3 -m venv venv && source venv/bin/activate`
     - Run `pip install wheel` then install the Python requirements for the project: `pip install -r requirements.txt`
   - On the **SECOND VM ONLY**, do the following (to enable the two-broker cluster):
     - set `zookeeper.connect=<PUBLIC IP OF FIRST VM>:2181` in `/home/kafka/config/server.properties`
     - set `broker.id = 1` in the same file
     - install CouchDB using [these instructions](https://docs.couchdb.org/en/main/install/unix.html#enabling-the-apache-couchdb-package-repository). Use `0.0.0.0` as the CouchDB bind address during installation. Make sure to save the password you use for the CouchDB `admin` user.
   - On **BOTH VM**s, do the following:
     - Start Kafka service: `sudo systemctl start kafka`
     - Verify it is running: `sudo systemctl status kafka`
   - On the **SECOND VM**, you can check to see the cluster is set up properly with:
     - ```cd /home/kafka/kafka && ./bin/zookeeper-shell.sh <PUBLIC IP OF FIRST VM>:2181 ls /brokers/ids```
       - You should see an array containing both 0 and 1 (the ids of the two brokers)
  - Your Apache Kafka cluster (2 brokers) is now successfully configured in Chameleon Cloud.
### The Data Source
We are using the [Yahoo Finance API](https://finance.yahoo.com/quotes/API,Documentation/view/v1/) as a data source for our pipeline. Specifically, we use the [yfinance](https://pypi.org/project/yfinance/) Python package for downloading and sending Stock Market data into the Kafka pipeline.

### Testing
- On your VirtualBox VM:
  - Navigate into the project: `cd cs5287progassign1`
  - Pull the project from GitHub to ensure you have the latest changes: `git pull origin main`
  - Navigate into `src`: `cd src`
  - Create a Kafka Producer process to produce 100 messages: `python3 driver.py -v -p -t stock-market-data -n 100 `
- On the FIRST VM (while the above is running):
  - Navigate into the project root: `cd cs5287progassign1`
  - Activate virtual environment if not activated: `source venv/bin/activate`
  - Navigate into `src`: `cd src`
  - Create a Kafka Consumer Process: `python3 driver.py -v -c -t stock-market-data`
- You should see the consumer receiving and logging the messages generated by the producer.
## Milestone 2 Steps (due Week 5, 9/22/2021)

## Milestone 3 Steps (due Week 6, 9/29/2021)