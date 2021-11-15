## Energy Data
The provided [energy.csv](energy.csv) file for Assignment 4 is 1M lines, and was split into 4 smaller files of 250,000 lines using the split command as follows:
`split -l 250000 energy.csv`

These smaller files are used by the producers to feed energy data into the pipeline for Assignment 4 using the --read_data FILENAME option to the driver.py when running a producer.