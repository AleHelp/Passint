# Passint:

## Description:
_Passint is a simple Python script that extensively employs the Selenium library to automate passive OSINT searches. The primary objective is to minimize active interactions with the target and eventually generate a comprehensive reports. The script is capable of performing the following tasks: Whois lookup, Examine HTTP headers, SSL/TLS certificate inspection, Technology discovery, Subdomain enumeration, Shodan, Fofa, Zoomeye searches, crawling, Email retrieval, and Traceroute._

## Organization:
`passint.py` _Main script_

`Scripts` _Folder for other scripts such as generatereport.py and cleaner.py_

`firefox_custom_settings` _Folder with geckodriver (Firefox driver) and a predefined custom Firefox profile with some add-ons (AdBlock and Random User-Agent)_

`requirements.txt` _File .txt with all necessary dependencies_

## Setup:

Commands to install it:
```bash
git clone https://github.com/AleHelp/Passint.git
cd Passint
pip3 install -r requirements.txt
```
_You can also use it with ven to avoid problems with dependencies:_
```bash
python3 -m venv <virtual environment name>
source <virtual environment name>/bin/activate 
git clone https://github.com/AleHelp/Passint.git
cd Passint
pip3 install -r requirements.txt
```
_When you're done, to turn off the virtual environment, just type the command `deactivate`_

## Usage:
```bash
-h, --help            show this help message and exit
-d DOMAIN, --domain DOMAIN
                      Domain name
--clear               Clear the Reports folder
--headless            Active the headless mode does not display Firefox GUI
-P PROFILE, --profile PROFILE
                      Specify a custom Firefox profile to import by providing the path. Example: --profile <path>
-a, --all             Run all modules
-w, --whois           Check whois and its historical records
-head, --headers      Examine the HTTP response headers
-cert, --certificate  Inspect SSL/TLS certificate
-t, --technologies    Discover the technologies behind a domain
-subd, --subdomains   Retrieve subdomains
-sfz, --shofozom      Use Shodan, Fofa and ZoomEye to retrieve information on the target domain
-craw, --crawling     Crawl the target domain
-e, --email           Recover emails
-g, --geotraceroute   Traceroute with a world map
-p, --proxy           Enable website proxy to handle a few captcha checks; this feature is available only for the subdomains and technologies modules, it may be slow
```
Command to run all modules:
```bash
python3 passint.py -d <domain name> -a
```
Command to run one module:
```bash
python3 passint.py -d <domain name> -g
```
Command to run the proxy module:
```bash
python3 passint.py -d <domain name> -p -subd
```
_At the end, two folders will be generated: __"Output"__ containing all the generated photos and .txt files, and __"Reports"__ containing:_

1) _Image-only reports if the modules returns .png files_

2) _Text-only reports if the modules returns .txt files_

3) _Full reports if the modules returns both_

Command to read the reports:
```bash
cat ./Reports/report-images-<domain name written>.pdf
```
```bash
cat ./Reports/report-text-<domain name written>.pdf
```
```bash
cat ./Reports/report-<domain name written>.pdf
```

## Tips:
I. _After repeated usage, the Captcha control may appear. I recommend using a service like [ProtonVPN](https://protonvpn.com/support/linux-vpn-tool/#debian) to handle it._

II. _There is an option to import your own Firefox profile. Here are the steps:_
```bash
firefox -ProfileManager
```
_Click on "Create Profile" -> Next -> "Enter a name" -> Next -> "Start Firefox". Once it is set up, you can find it in `/home/<username>/.mozilla/firefox/<random number and letters>.<chosen name>`. To simplify the importing process, you can use the `cp` command in the `Passint folder`:_
```bash
cp /home/<username>/.mozilla/firefox/<random number and letters>.<name choosen> ./Passint
```
_Finally, you can add it with the following command:_
```bash
python3 passint.py -d <domain name> -craw -P
```
III. _The script whether with gui or without (headless mode) quietly allows you to be able to do other things_
## Disclaimer:
__The script utilizes Selenium with extensive interaction with the HTML code of the target websites. However, it is important to note that changes in the HTML structure of these websites may occur.__

__The script is still under development may have errors.__
