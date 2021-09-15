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
6. Consumer should be able to receive both topic data from Kafka
7. Upload progress made and documentation till that point to Brightspace
8. Since we now have AWS classroom, attempt all the VM2-VM3 installations also on AWS instances.
9.  Currently, we do not yet have GCP approval and so we cannot use it as yet.
10. Demo the minimum expected capabilities to the TAs.