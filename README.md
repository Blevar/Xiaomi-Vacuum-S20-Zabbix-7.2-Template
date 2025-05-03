Place xiaomi_vacuum_s20plus.py in /lib/zabbix/externalscripts on your Zabbix server (or proxy - depending on the layout) machine.
Install required dependencies: pip install miio-cloud or pip install git+https://github.com/nicjo814/miio-cloud.git or pip install python-miot

After importing the template you will need to edit macros of the host to add ip and the token.
Token can be obtained by running: pip install xiaomi-cloud-tokens-extractor and then python token_extractor.py - login to the Xiaomi cloud.
