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