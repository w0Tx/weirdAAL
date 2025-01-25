# WeirdAAL (AWS Attack Library)

Install instructions :
```
git clone https://github.com/w0Tx/weirdAAL.git
cd weirdAAL
python3 -m venv weirdAAL
source weirdAAL/bin/activate
pip3 install -r requirements.txt
python3 create_dbs.py
```

Usage instructions :
```
# Recon all services
python3 weirdAAL.py -m recon_all -t name-of-my-recon

# List services that have been found
python3 weirdAAL.py -m list_services_by_key -t name-of-my-recon
```

Some changes over carnal0wnage version :
- Updated versions (requirements.txt)
- Fixed ImportError 'Iterable' : [Github Issue](https://github.com/carnal0wnage/weirdAAL/pull/81)
- Added feature to timeout for services that aren't answering
- Removed GCP stuff since it isn't implemented
- Updated the logic to check AWS credentials validity
- Added feature to support `--profile` logic available with boto3

It's still possible to use the original way for providing your `.env` other than `~/.aws/credentials`. You must set the following ENV variable with the path of your file containing the credentials.

```
export AWS_SHARED_CREDENTIALS_FILE="env.sample"
```

All credits to [carnal0wnage](https://github.com/carnal0wnage)
Documentation available on the [wiki](https://github.com/carnal0wnage/weirdAAL/wiki).

