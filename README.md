#wol-server
A simple web server written in python and powered by flask to send wake on lan packages to the server's network.

Possible applications:

- Use on you NAS to remotely wake your pc
- Use an automation tool on your smartphone to automatically make an api call when you connect to your home wifi

#Usage
Tested with Python 3.4.1, but should work on 2.6, 2.7, 3.3 and 3.4.

0. Install pip: `easy_install pip`
1. Install requirements: `pip install -r requirements.txt`
2. Run `python WolServer.py`

## How to wake a computer
- Browse to [http://localhost:5000](http://localhost:5000) and enter the mac address
- Use the api like `http://localhost:5000/api/wake/<mac>`

##Favicon
Favicon by [IconShock](http://www.iconshock.com/)
