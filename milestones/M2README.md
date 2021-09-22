# Milestone 2
1. Producer code should be installed on VM1.1, VM1.2... VM1.
   1. Complete.
2. Apache Kafka should be installed on VM2 and VM3 and brokers should be running on these VMs.
   1. Complete.
3. Zookeeper should run on VM2(or VM3)
   1. Complete. Zookeeper running on VM2, VM3 uses VM2 zookeeper service to allow for cluster.
4. Consumer should be installed on VM2(or VM3)
   1. Complete. VM3 running consumer.
5. Producers should be able to stream topic data to Kafka from both laptops.
   1. Complete. `python3 driver.py -v -p -t stock-market-data` can be run to drive a Producer process on N clients.
6. Consumer should be able to receive both topic data from Kafka.
   1. Complete.
7. Upload progress made and documentation till that point to Brightspace
8. Since we now have AWS classroom, attempt all the VM2-VM3 installations also on AWS instances.
9.  Currently, we do not yet have GCP approval and so we cannot use it as yet.
10. Demo the minimum expected capabilities to the TAs.


## Milestone 2 Steps Taken (due Week 5, 9/22/2021) - ([Video Demo](https://www.youtube.com/watch?v=TflXLZmG7cA))
### VirtualBox VM Prep
  - Project was already cloned to VirtualBox VM in Milestone 1 with: `git clone https://github.com/austinjhunt/cs5287progassign1.git`
  - Navigate into the project: `cd cs5287progassign1`
  - Create a virtual environment to isolate the Python package installations to this project: `python3 -m venv venv`
  - Activate the virtual environment: `source venv/bin/activate`
  - Install the Python requirements: `pip install -r requirements.txt`
### Chameleon Cloud VM Prep
   - SSH to **both** VMs using the key-based authentication enabled through the keypair selection previously. I like using [Iterm2](https://iterm2.com/downloads/stable/latest) for MacOS for this: `ssh cc@<public ip of VM>`
   - On **BOTH VM**s, do the following:
     - Install OpenJDK JRE with [these instructions](https://ubuntu.com/tutorials/install-jre#2-installing-openjdk-jre)
     - Install (but don't start yet) Apache Kafka using [these instructions](https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-20-04)
     - You need to modify the Kafka Config to allow the public IP of the Kafka server to be used. Add the following line to the end of the `/home/kafka/kafka/config/server.properties` file: `advertised.listeners=PLAINTEXT://<PUBLIC IP OF CURRENT VM>:9092`
     - Set up Python3 (already done in Milestone 1) using [these instructions](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server).
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
    - Zookeeper is now running on the first cloud VM. Second cloud VM is using the first VM's Zookeeper service for cluster functionality.
    - Your Apache Kafka cluster (2 brokers) is now successfully configured in Chameleon Cloud.

## Testing Producer / Consumer functionality
On Virtualbox VM, navigate into project, activate python virtual environment, and execute producer process:
```
cd <path to project>
source venv/bin/activate
cd src
python3 driver.py --cloud_platform chameleon -t stock-market-data -s 1 -v -p -pa "Producer 1" -n 50 -ss AMZN
```
On second cloud VM, navigate into project, activate python virtual environment, and execute consumer process:
```
cd <path to project>
source venv/bin/activate
cd src
python3 driver.py --cloud_platform chameleon -t stock-market-data -c -v
```

## Replicating CLoud Functionality to Other Platforms

Run all of the milestone 1 cloud commands and the milestone 2 cloud commands on a new pair of AWS EC2 instances, then run the tests again, passing in `--cloud_platform aws` to the driver instead of `--cloud_platform chameleon`
Store the aws addresses in the config.json file, under the `aws` key belonging to the `cloud_hosts` JSON dictionary.
## GCP
Optionally do the same for Google Cloud Platform, and execute driver instead with `--cloud_platform gcp`. Store the GCP addresses in the `config.json` file, under the `gcp` key belonging to the `cloud_hosts` JSON dictionary.