# Milestone 1
## Requirements
1. VMs on teammember laptops should be running with needed packages (Python3, producer code, etc). These are VMs VM1.1, VM1.2... VM1.n as shown in the figure.
   1. Complete.
2. VM2 and VM3 in Chameleon (and eventually on AWS for milestone 2) should be up with Python3. They should be reachable from outside via ssh.
   1. Complete. Private key is shared by both team members for key based authentication. Project is cloned to both cloud VMs. Python3 is installed on both cloud VMs. Python3 requirements are installed on both cloud VMs.
3. The “top” command output dumped by my scaffolding code is just a toy example; you should try to find existing data streams on the web to collect and stream data information to Kafka brokers. This could be as simple as some traffic data or weather data, etc. For example, OpenWeatherMap or AccuWeather could be one source for weather data. You could make weather for different cities as individual topics and stream it to Kafka brokers from your producer code. It is up to you as to what data source you choose, but please document this.Accordingly your producer code will be slightly modified from the toy example.
   1. Complete. Producer code has been updated to produce Yahoo Finance data for a given stock, namely the current share price.
4. Upload progress made and documentation till that point to Brightspace/2U.
5. Demo the minimum expected capabilities to one of the TAs/grading team.
   1. DEMO VIDEO IS HERE: [https://youtu.be/TflXLZmG7cA](https://youtu.be/TflXLZmG7cA).
   2. This video demonstrates that:
      - Chameleon Cloud VM 1 has Python3 installed and Python3 requirements installed, Zookeeper installed and running, Kafka installed and running (Kafka Broker 1), and the Github project cloned to /home/kafka
      - Chameleon Cloud VM 2  has Python3 installed and Python3 requirements installed, Kafka installed and running, and the Github project cloned to /home/kafka (Kafka Consumer code is installed). This Kafka Broker (Kafka Broker 2) uses the Zookeeper service on the first Cloud VM, which allows for a cluster functionality.
      - Local Virtualbox VM has Python3 and Python3 requirements installed, has the Github repo cloned (Producer code is installed).
      - We are using stock market-related data for our project, sourced from Yahoo Finance.

      - Chameleon Cloud VM 2 can run a Kafka Consumer to consume messages produced by multiple distributed clients (Kafka Producers), and each producer can give itself a unique alias to make distinguishing them easier.


## Steps Taken (due Week 4, 9/15/2021) - ([Video Demo](https://www.youtube.com/watch?v=TflXLZmG7cA))
### Setting Up A Local Ubuntu 20.04 VM with VirtualBox (each team member must do this)
- If not installed, [install VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- Install Ubuntu 20.04 LTS on VirtualBox using [these instructions](https://fossbytes.com/how-to-install-ubuntu-20-04-lts-virtualbox-windows-mac-linux/)
- Rather than creating a shared folder between the host and guest OS, we'll use git to keep the code synchronized between the guest and host. You can develop locally on your host OS using an IDE and whatever changes you commit can be pulled into the guest.
  - Log into your Ubuntu 20.04 VM once you've created it.
  - Open a Terminal window.
  - Set up Python 3 on your VM using [these instructions](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server).
  - Clone the project repository: `git clone https://github.com/austinjhunt/cs5287datapipeline.git`
  - Navigate into the project: `cd cs5287datapipeline`
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
   - Once allocated, take note of the private and public IP addresses of both VMs and add an entry to the `"cloud_hosts":{"chameleon": [] }` array in [config.json](src/config.json) in this project for each VM, as follows:
    ```
    {
      "private": "1.2.3.4",
      "public": "5.6.7.8"
    },
    ```
    We'll later store similar arrays for AWS and GCP cloud hosts.
   - SSH to both VMs using the key-based authentication enabled through the keypair selection previously. I like using [Iterm2](https://iterm2.com/downloads/stable/latest) for MacOS for this: `ssh cc@<public ip of VM>`
   - On **BOTH VM**s, do the following:
     - Set up Python3 using [these instructions](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server)
     - Also be sure to install the venv module with `sudo apt install python3-venv`