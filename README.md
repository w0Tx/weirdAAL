# WeirdAAL (AWS Attack Library)
WeirdAAL (AWS Attack Library)

Install instructions :
```
git clone https://github.com/carnal0wnage/weirdAAL.git
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

All credits to [carnal0wnage](https://github.com/carnal0wnage)
Documentation available on the [wiki](https://github.com/carnal0wnage/weirdAAL/wiki).

