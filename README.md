# Host Unit Hour Consumption Finder

    usage: huh_overages.py [-h] -hu HOSTUNITS <raw-data-file>

Find when host units hours were consumed

positional arguments:

    <raw-data-file>       Include a .csv of a folder containing .csv

optional arguments:

    -h, --help            show this help message and exit
    -hu HOSTUNITS, --hostunits HOSTUNITS
                            The account host unit limit
                            
## Features

- Process a large volume of `raw-data` files in a short amount of time. Tested wih 100MB of .csvs and processes within a few seconds. 

## Limitations

- Curerntly only works with the data provided by SaaS tenants
- Assumes that the .csv files are the correct files. Strange things will happen if invalid .csv files are used. 
