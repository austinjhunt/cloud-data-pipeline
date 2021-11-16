## Energy Data
The provided [energy.csv](energy.csv) file for Assignment 4 is 1M lines, and was split into 4 smaller files of 250,000 lines using the split command as follows:
`split -l 250000 energy.csv`

These smaller files are used by the producers to feed energy data into the pipeline for Assignment 4 using the --read_data FILENAME option to the driver.py when running a producer.

The schema of the base stream is following:
- `id` – a unique identifier of the measurement [32 bit unsigned integer value]
- `timestamp` – timestamp of measurement (number of seconds since January 1, 1970, 00:00:00 GMT) [32 bit unsigned integer value]
- `value` – the measurement [32 bit floating point]
- `property` – type of the measurement: 0 for work or 1 for load [boolean]
- `plug_id` – a unique identifier (within a household) of the smart plug [32 bit unsigned integer value]
- `household_id` – a unique identifier of a household (within a house) where the plug is located [32 bit unsigned integer value]
- `house_id` – a unique identifier of a house where the household with the plug is located [32 bit unsigned integer value]