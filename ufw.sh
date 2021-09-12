#!/bin/bash

# Execute this script using 'sudo' on the Chameleon Cloud VMs once they are created.
for port in 2181 4369 5984 9092; do
    ufw allow $port
done