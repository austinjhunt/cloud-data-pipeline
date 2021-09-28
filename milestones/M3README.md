# Milestone 3 (due 9/29/21) - ([Video Demo](https://www.youtube.com/watch?v=crXXRN27cIg))
## Requirements
1. Apache CouchDB should be installed on VM3(or VM2)in single node configuration.
   1. Complete.
2. Consumer code should be able to dump the received contents into CouchDB.
   1. Complete.
3. Data should be viewable in CouchDB via web console.
   1. Complete.
4. All documentation needed for the assignment should be ready and submitted.
   1. Complete.
5. Demo the entire assignment to one of the TAs/2U.
   1. Complete (via YouTube video)
6. Should work with both Chameleon and AWS installations.
   1. Complete. (has been demoed with both Chameleon and AWS using `--cloud_platform` argument to `driver.py`)

## Steps Taken
1. On the second cloud VM (regardless of which platform is being used):
   - install CouchDB using [these instructions](https://docs.couchdb.org/en/main/install/unix.html#enabling-the-apache-couchdb-package-repository).
   - Use `0.0.0.0` as the CouchDB bind address during installation. This will allow the web GUI to be accessible to other hosts, not just localhost.
   - Make sure to save the password you use for the CouchDB `admin` user.
2. Implement and test a `-d [--dump]` flag to the `driver.py` to be used with `-c [--consumer]` that tells the consumer to dump to couchdb.
   - This requires adding [couchdb](https://couchdb-python.readthedocs.io/en/latest/) as a requirement in the Python [requirements.txt](../requirements.txt) file and learning to use it to save data.
   - Once familiar with couchdb package, save to database (optionally depending on `-d` argument) as part of consumption process.
3. Confirm that web console for Couchdb is accessible at the IP of the VM where couchdb is installed followed by port `5984` and the path `/_utils`, e.g. `1.2.3.4:5984/_utils`. Log in with admin username and password and choose the database used with the couchdb package.
4. Try this with both `--cloud_platform aws` and with `--cloud_platform chameleon`. We did, with successful results.