#!/usr/bin/env python3

from time import sleep
import argparse
import os
import sys
from selenium import webdriver
from scripts.generatereport import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

def capture_screenshot(driver, filename):
    screenshot_path = os.path.join(directory, filename)
    driver.save_full_page_screenshot(screenshot_path)

def whois(domain):
    try:
        driver.get('https://www.whoxy.com/whois-history/')
        print("Initiating whois module...")
        driver.find_element("id", 'bigSearchBox').clear()
        driver.find_element("id", 'bigSearchBox').send_keys(domain, Keys.ENTER)
        sleep(8)
        if "I'm not a Robot" in driver.find_element("xpath", "//button[@data-callback='verifyRecaptcha']").text:
            driver.find_element("xpath", "//button[@data-callback='verifyRecaptcha']").click()
            capture_screenshot(driver,f"whois-{str(domain)}.png")
            print("[+] Whois done\n")
    except Exception as e:
        capture_screenshot(driver,f"whois-{str(domain)}.png")
        print("[+] Whois done\n")
        return

def headers(domain):
    try:
        driver.get("https://securityheaders.com/")
        print("Initiating headers inspection module...")
        driver.find_element("id", 'q').clear()
        driver.find_element("id", 'q').send_keys(domain, Keys.ENTER)
        sleep(8)
        capture_screenshot(driver,f'proxy-technologies-{str(domain)}.png')
        print("[+] Headers inspection done\n")
    except Exception as e:
        print(f"[-] An error in headers module occurred: {str(e)}.")
        return

def certificate(domain):
    try:
        driver.get('https://crt.sh')
        print("Initiating certificate module...")
        sleep(1)
        driver.find_element("xpath", '//input[@class="input"]').clear()
        driver.find_element("xpath", '//input[@class="input"]').send_keys(domain)
        sleep(1)
        driver.find_element("xpath", '//input[@class="button"]').click()
        sleep(10)
        capture_screenshot(driver,f'certificates-{str(domain)}.png')
        print("[+] Certificate done\n")
    except Exception as e:
        print(f"[-] An error in certificate module occurred: {str(e)}.")
        return 

def technologies(domain):
    try:
        driver.get('https://w3techs.com/sites')
        print("Initiating technologies module...")
        sleep(1)
        driver.find_element("name", 'url').clear()
        driver.find_element("name", 'url').send_keys(domain)
        sleep(1)
        driver.find_element("xpath", '//input[@value="Site Info"]').click()
        sleep(10)
        capture_screenshot(driver,f'technologies-{str(domain)}.png')
        print("[+] Technologies done\n")
    except Exception as e:
        print(f"[-] An error in technologies module occurred: {str(e)}.")
        return 

def subdomains(domain):
    try:
        driver.get('https://dnsdumpster.com/')
        print("Initiating subdomains module...")
        driver.find_element("id", 'regularInput').clear()
        driver.find_element("id", 'regularInput').send_keys(domain)
        sleep(1)
        driver.find_element("xpath", '//button[@class="btn btn-default"]').click()
        sleep(12)
        capture_screenshot(driver,f"subdomains-{str(domain)}.png")
        print("[+] Subdomains done\n")
    except Exception as e:
        print(f"[-] An error in subdomains module occurred: {str(e)}.")
        return

def shodan(domain):
    try:
        driver.get('https://www.shodan.io/')
        print("Initiating shodan module...")
        sleep(2)
        driver.find_element("id", 'search-query').clear()
        driver.find_element("id", 'search-query').send_keys(domain)
        driver.find_element("xpath", '//button[@class="button-red"]').click()
        sleep(8)
        capture_screenshot(driver,f'shodan-{str(args.domain)}.png')
        if "No results found" in driver.find_element("xpath", "//div[@class='alert alert-notice']").text:
            print('[-] Shodan no results found\n')
            fofa(new_domain)
    except NoSuchElementException:
        print('[+] Shodan results found\n')
        fofa(new_domain)
        
def fofa(domain):
    try:
        driver.get('https://en.fofa.info/')
        print("Initiating fofa module...")
        sleep(2)
        driver.find_element("xpath", '//textarea[@type="search"]').clear()
        driver.find_element("xpath", '//textarea[@type="search"]').send_keys(domain, Keys.ENTER)
        sleep(15)
        capture_screenshot(driver,f'fofa-{str(args.domain)}.png')
        if '0 results' in driver.find_element("xpath", "//div[@class='hsxa-highlight-color']").text:
            print('[-] Fofa no results found\n')
            zoomeye(new_domain)
    except NoSuchElementException:
        print('[+] Fofa results found\n')
        zoomeye(new_domain)
        
def zoomeye(domain):
    try:
        driver.get('https://www.zoomeye.org/')
        print("Initiating zoomeye module...")
        sleep(2)
        driver.find_element("xpath", '//input[@class="ant-input ant-select-search__field" and @type="text"]').clear()
        driver.find_element("xpath", '//input[@class="ant-input ant-select-search__field" and @type="text"]').send_keys(domain, Keys.ENTER)
        sleep(10)
        capture_screenshot(driver,f'zoomeye-{str(args.domain)}.png')
        if 'About 0 results' in driver.find_element("xpath", "//p[@class='search-result-summary']").text:
            print('[-] Zoomeye no results found\n')
            print('[+] Shodan, Fofa and Zoomeye done\n')
            return
        else:
            print('[+] Zoomeye results found\n')
            print('[+] Shodan, Fofa and Zoomeye done\n')
    except NoSuchElementException:
        return

def crawling(domain):
    try:
        driver.get('https://www.xml-sitemaps.com/')
        print("Initiating crawling module...")
        driver.find_element("xpath", '//input[@class="form-control "]').clear()
        driver.find_element("xpath", '//input[@class="form-control "]').send_keys(domain)
        sleep(3)
        driver.find_element("xpath", '//button[@class="btn btn-primary btn-block"]').click()
        sleep(5)
        results_list = []
        unique_results_set = set()
        print('Sometimes it takes 5 to 15 minutes, please be patient :)')
        while int(driver.find_element("xpath", '//div[@class="icon s-p3"]').text) != 0:
            results_list.append(driver.find_element("xpath", '//span[@class="s-pc"]').text)

        for riga in results_list :
            unique_results_set.add(riga)

        with open(f'Output/crawling-{str(domain)}.txt', 'w') as file:
            file.write("Crawling results:\n\n")
            for row in unique_results_set:
                file.write(f"{domain}/" + row + '\n')
        print("[+] Crawling done\n")
    except Exception as e:
        print(f"[-] An error in crawling module occurred: {str(e)}.")
        return 

def email(domain):
    try:
        driver.get("https://www.skymem.info/")
        print("Initiating email module...")  
        driver.find_element("xpath", '//input[@ng-model="Doc.SearchRequest"]').clear()
        driver.find_element("xpath", '//input[@ng-model="Doc.SearchRequest"]').send_keys(domain, Keys.ENTER)
        sleep(5)   
        emails = []
        for row in driver.find_elements("xpath","//table[@class='table table-striped  table-sm table-hover table-bordered text-muted']/tbody/tr"):
            email_element = row.find_element("xpath",".//td[2]/a").text
            emails.append(email_element)

        with open(f'Output/email-{str(new_domain)}.txt', 'w') as file:
            file.write("Email results:\n\n")
            for row in emails:
                file.write(f"{new_domain}" + row + '\n\n')
        print("[+] Email done\n")
        return emails
    except Exception as e:
        print(f"[-] An error in email module occurred: {str(e)}.")
        return 

def geotraceroute(domain):
    try:
        driver.get('https://gsuite.tools/traceroute')
        print("Initiating geotraceroute module...")
        sleep(2)
        driver.find_element("xpath", '//input[@name="host" and @id="host"]').clear()
        driver.find_element("xpath", '//input[@name="host" and @id="host"]').send_keys(domain)
        sleep(1)
        driver.find_element("xpath", '//button[@id="traceroute_button"]').click()
        sleep(1)
        screenshot_path = os.path.join(directory, f'geotraceroute-{str(args.domain)}.png')
        sleep(20)
        capture_screenshot(driver,f'geotraceroute-{str(args.domain)}.png')
        text = driver.find_element("id", 'traceroute_results_table_container').text
        with open(f'Output/geo-{str(domain)}.txt', 'w') as file:
            file.write("Traceroute results:\n\n")
            file.write(f"{text}\n" + "\n")
        print("[+] Geotraceroute done\n")
    except Exception as e:
        print(f"[-] An error in geotraceroute module occurred: {str(e)}.")
        return 

def proxy(domain, mode):
    try:
        if args.subdomains == True:
            driver.get('https://www.proxysite.com/')
            print("Initiating proxy subdomains module...")
            driver.find_element("xpath", '//input[@name="d"]').clear()
            driver.find_element("xpath", '//input[@name="d"]').send_keys("https://dnsdumpster.com/")
            sleep(2)
            driver.find_element("xpath", '//button[@type="submit"]').click()
            sleep(15)
            driver.find_element("id", 'regularInput').clear()
            driver.find_element("id", 'regularInput').send_keys(domain)
            sleep(1)
            driver.find_element("xpath", '//button[@class="btn btn-default"]').click()
            sleep(20)
            capture_screenshot(driver,f'proxy-subdomains-{str(domain)}.png')
            print("[+] Proxy subdomains done\n")
            return
            
        if args.technologies == True:
            driver.get('https://www.proxysite.com/')
            print("Initiating proxy technologies module...")
            driver.find_element("xpath", '//input[@name="d"]').clear()
            driver.find_element("xpath", '//input[@name="d"]').send_keys("https://w3techs.com/sites")
            sleep(2)
            driver.find_element("xpath", '//button[@type="submit"]').click()
            sleep(15)
            driver.find_element("name", 'url').clear()
            driver.find_element("name", 'url').send_keys(domain)
            sleep(1)
            driver.find_element("xpath", '//input[@value="Site Info"]').click()
            sleep(20)
            capture_screenshot(driver,f'proxy-technologies-{str(domain)}.png')
            print("[+] Proxy technologies done\n")
            return
    except Exception as e:
        print(f"[-] An error in proxy module occurred: {str(e)}.")
        return

if __name__ == "__main__":
    try:
        os.makedirs("./Output/", exist_ok=True)
        os.makedirs("./Reports/", exist_ok=True)
        directory = 'Output'
        parser = argparse.ArgumentParser(description='Python script for passive and non-intrusive reconnaissance. The goal is to minimize active interactions with the target and eventually generate a report.')
        parser.add_argument('-d', '--domain', type=str, help='Domain name')
        parser.add_argument('--clear', action='store_true', help='Clear the Reports and Output folder')
        parser.add_argument('-P', '--profile', type=str, default="./firefox_custom_settings/6rmhsi0z.Custom-Profile", help='Specify a custom Firefox profile to import by providing the path. Example: --profile <path>')
        parser.add_argument('-a', '--all', action='store_true', help='Run all modules')
        parser.add_argument('-w', '--whois', action='store_true', help='Check whois and its historical records')
        parser.add_argument('-head', '--headers', action='store_true', help='Examine the HTTP response headers')
        parser.add_argument('-cert', '--certificate', action='store_true', help='Inspect SSL/TLS certificate')
        parser.add_argument('-t', '--technologies', action='store_true', help='Discover the technologies behind a domain')
        parser.add_argument('-subd', '--subdomains', action='store_true', help='Retrieve subdomains')
        parser.add_argument('-sfz', '--shofozom', action='store_true', help='Use Shodan, Fofa and ZoomEye to retrieve information on the target domain')
        parser.add_argument('-craw', '--crawling', action='store_true', help='Crawl the target domain')
        parser.add_argument('-e', '--email', action='store_true', help='Recover emails')
        parser.add_argument('-g', '--geotraceroute', action='store_true', help='Traceroute with a world map')
        parser.add_argument('-p', '--proxy', action='store_true', help='Enable website proxy to handle a few captcha checks; this feature is available only for the subdomains and technologies modules, it may be slow')
        parser.epilog = ('This script uses the free plan on several sites, so it is not possible to collect all the data. We recommend further manual research.')
        args = parser.parse_args()

        if len(sys.argv) == 1:
            parser.print_help()
            driver.quit()
            exit(0)
        
        service = Service('./firefox_custom_settings/firefox_driver/geckodriver')
        options = webdriver.FirefoxOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(f"--profile")
        options.add_argument(f"./firefox_custom_settings/6rmhsi0z.Custom-Profile")
        driver = webdriver.Firefox(options=options, service=service)
        driver.maximize_window()
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        if args.clear:
            delete_old_elements()
            delete_reports()
        
        if not args.domain:
            print('Insert the domain name.')
            driver.quit()
            exit(1)
        else:
            new_domain = args.domain.replace("www.","")
        
        if not (args.all or args.headers or args.whois or args.subdomains or args.certificate or args.technologies or args.crawling or args.shofozom or args.email or args.geotraceroute or args.proxy):
            print('Choose a module to run.')
            driver.quit()
            exit(1)
        
        if args.all:
            if  any([args.whois, args.headers, args.subdomains, args.certificate, args.technologies, args.crawling, args.shofozom, args.email, args.geotraceroute, args.proxy]):
                print('Cannot enter other parameters if -a is active.')
                driver.quit()
                exit(1)
            else:
                whois(new_domain)
                headers(new_domain)
                certificate(new_domain)
                technologies(new_domain)
                subdomains(new_domain)
                shodan(new_domain)
                crawling(new_domain)
                email(new_domain)
                geotraceroute(new_domain)

        if args.proxy:
            if  not (args.subdomains or args.technologies):
                print('Insert the -subd (subdomain module) or -t (technologies module).')
                driver.quit()
                exit(1)

            if args.subdomains:
                proxy(new_domain, args.subdomains)
                args.subdomains = False

            if args.technologies:
                proxy(new_domain, args.technologies)
                args.technologies = False

        if args.whois:
            whois(new_domain)

        if args.headers:
            headers(new_domain)

        if args.certificate:
            certificate(new_domain)

        if args.technologies:
            technologies(new_domain)

        if args.subdomains:
            subdomains(new_domain)

        if args.shofozom:
            shodan(new_domain)

        if args.crawling:
            crawling(new_domain)

        if args.email:
            email(new_domain)
        
        if args.geotraceroute:
            geotraceroute(new_domain) 

        report(new_domain)
        driver.quit()
        
    except KeyboardInterrupt:
        print(f"[-] Script terminated by user.")
    except IOError as e:
        print(f"[-] I/O error: {str(e)}.")
    except Exception as e:
        print(f"[-] An unexpected error occurred: {str(e)}.")
