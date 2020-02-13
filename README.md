# routerquery

This is a python script designed to query the Hitron CGNM 2250 router for the list of connected devices. This ay work with other routers on the market but I make no gurantees. The goal is to make both a CLI and GUI version that can be used.


# nicknames.config

this file contains a json object that contains nicknames of connected devices. The key for the nickname is the mac address as that should be unique to each device. 

# routerinfo.config

File containing JSON list of router information so that I can query different routers

# wql.py

This is the Wifi Query Library and will contain all the code required to do the http queries so that both the CLI and GUI versions can just import this file and get the same functionality.


# routerquery.py

This will be the name of the CLI version (at the given moment).

```
Usage: python3 routerquery.py [options]

Options:    -h -H                 print help window
            -v -V                 be verbose
            --Version             print version info            
            -l  [data]            set location            
            -n  [mac, data]       set nickname for given mac address            
            -iL [value]           requery the router every given number of seconds            
            --config [loc, data]  edit config file for a given location
```

# xrouterquery.py

This will be the name of the GUI version (at the given moment). I plan on using tkinter to produce the gui as it doesn't need to be complex. 
