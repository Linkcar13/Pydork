import argparse
import requests
import time
import sys
import re
from bs4 import BeautifulSoup
import json
import markdown ## For reporting
from prettytable import PrettyTable

# Definición de Colores

black="\033[0;30m"
red="\033[0;31m"
bred="\033[1;31m"
green="\033[0;32m"
bgreen="\033[1;32m"
yellow="\033[0;33m"
byellow="\033[1;33m"
blue="\033[0;34m"
bblue="\033[1;34m"
purple="\033[0;35m"
bpurple="\033[1;35m"
cyan="\033[0;36m"
bcyan="\033[1;36m"
white="\033[0;37m"
nc="\033[00m"

# Banner
def print_banner():
    banner = f'''
    {bblue}██████╗ ██╗   ██╗██████╗  ██████╗ ██████╗ ██╗  ██╗    
    {bblue}██╔══██╗╚██╗ ██╔╝██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝    
    {yellow}██████╔╝ ╚████╔╝ ██║  ██║██║   ██║██████╔╝█████╔╝     
    {green}██╔═══╝   ╚██╔╝  ██║  ██║██║   ██║██╔══██╗██╔═██╗     
    {red}██║        ██║   ██████╔╝╚██████╔╝██║  ██║██║  ██╗    
    {red}╚═╝        ╚═╝   ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    
    {purple}                                by [KalelS] v1.2{nc}
    '''

    print(banner)


""" if len(sys.argv) != 2:
    print(f'''{red}[!] Usage: python google_dork.py <domain>''')
    sys.exit(1) """

""" # Diccionario de dorks más comunes
dorks = [
    ##
    "site:{} ext:doc".format(sys.argv[1]),
    "site:{} ext:docx".format(sys.argv[1]),
    "site:{} ext:xls".format(sys.argv[1]),
    "site:{} ext:xlsx".format(sys.argv[1]),
    "site:{} ext:ppt".format(sys.argv[1]),
    "site:{} ext:pptx".format(sys.argv[1]),
    "site:{} ext:log".format(sys.argv[1]),
    "site:{} ext:sql".format(sys.argv[1]),
    "site:{} ext:pdf".format(sys.argv[1]),
     "site:{} ext:txt".format(sys.argv[1]),
    ##
    "site:{} filetype:doc".format(sys.argv[1]),
    "site:{} filetype:docx".format(sys.argv[1]),
    "site:{} filetype:xls".format(sys.argv[1]),
    "site:{} filetype:xlsx".format(sys.argv[1]),
    "site:{} filetype:ppt".format(sys.argv[1]),
    "site:{} filetype:pptx".format(sys.argv[1]),
    "site:{} filetype:log".format(sys.argv[1]),
    "site:{} filetype:sql".format(sys.argv[1]),
    "site:{} filetype:pdf".format(sys.argv[1]),
    "site:{} filetype:txt".format(sys.argv[1]),
    ##
    "site:{} inurl:admin intext:password".format(sys.argv[1]),
    "site:{} intitle:index of".format(sys.argv[1]),
    "site:{} ext:doc | ext:pdf | ext:docx | ext:txt | ext:xlsx | ext:xls".format(sys.argv[1]),
    "site:{} inurl:config intext:password".format(sys.argv[1]),
    "site:{} ext:log".format(sys.argv[1]),
    "site:{} ext:sql".format(sys.argv[1]),
    "intitle:password site:{}".format(sys.argv[1]),
    "intitle:login site:{}".format(sys.argv[1]),
    "intitle:Index of site:{}".format(sys.argv[1]),
    "inurl:password site:{}".format(sys.argv[1]),
    "inurl:login site:{}".format(sys.argv[1]),
    ##
    "inurl:{} ext:doc".format(sys.argv[1]),
    "inurl:{} ext:docx".format(sys.argv[1]),
    "inurl:{} ext:xls".format(sys.argv[1]),
    "inurl:{} ext:xlsx".format(sys.argv[1]),
    "inurl:{} ext:ppt".format(sys.argv[1]),
    "inurl:{} ext:pptx".format(sys.argv[1]),
    "inurl:{} ext:pdf".format(sys.argv[1]),
    "inurl:{} ext:txt".format(sys.argv[1]),
    "inurl:{} ext:sql".format(sys.argv[1]),
    "inurl:{} ext:log".format(sys.argv[1]),
    "related:{} ext:doc".format(sys.argv[1]),
    "related:{} ext:docx".format(sys.argv[1]),
    "related:{} ext:xls".format(sys.argv[1]),
    "related:{} ext:xlsx".format(sys.argv[1]),
    "related:{} ext:ppt".format(sys.argv[1]),
    "related:{} ext:pptx".format(sys.argv[1]),
    "related:{} ext:pdf".format(sys.argv[1]),
    "related:{} ext:txt".format(sys.argv[1]),
    "related:{} ext:sql".format(sys.argv[1]),
    "related:{} ext:log".format(sys.argv[1]),
    ##
    "inurl:{} filetype:doc".format(sys.argv[1]),
    "inurl:{} filetype:docx".format(sys.argv[1]),
    "inurl:{} filetype:xls".format(sys.argv[1]),
    "inurl:{} filetype:xlsx".format(sys.argv[1]),
    "inurl:{} filetype:ppt".format(sys.argv[1]),
    "inurl:{} filetype:pptx".format(sys.argv[1]),
    "inurl:{} filetype:pdf".format(sys.argv[1]),
    "inurl:{} filetype:txt".format(sys.argv[1]),
    "inurl:{} filetype:log".format(sys.argv[1]),
    "inurl:{} .env".format(sys.argv[1]),
    "inurl:{} filetype:sql".format(sys.argv[1]),
    "inurl:{} config".format(sys.argv[1]),
    "inurl:{} user".format(sys.argv[1]),
    "inurl:{} usuario".format(sys.argv[1]),
    "inurl:{} contraseña".format(sys.argv[1]),
    "inurl:{} password".format(sys.argv[1]),
    "related:{} filetype:doc".format(sys.argv[1]),
    "related:{} filetype:docx".format(sys.argv[1]),
    "related:{} filetype:xls".format(sys.argv[1]),
    "related:{} filetype:xlsx".format(sys.argv[1]),
    "related:{} filetype:ppt".format(sys.argv[1]),
    "related:{} filetype:pptx".format(sys.argv[1]),
    "related:{} filetype:pdf".format(sys.argv[1]),
    "related:{} filetype:txt".format(sys.argv[1]),
    "related:{} filetype:sql".format(sys.argv[1]),
    "related:{} filetype:log".format(sys.argv[1]),
    "related:{} .env".format(sys.argv[1]),
    "related:{} config".format(sys.argv[1]),
    "related:{} username".format(sys.argv[1]),
    "related:{} contraseña".format(sys.argv[1]),
    "related:{} user".format(sys.argv[1]),
    "related:{} password".format(sys.argv[1]),
] """


    ## Define domain for search
    #domain = sys.argv[1]
def read_file(file):
    #Custom file of dorks
    try:
        with open(file,'r') as json_file:
            decoded_file = json.load(json_file)
    except FileNotFoundError:
        print(f"File {file} not found!!")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"decode of JSON file {file} failed")
        sys.exit(1)
    return decoded_file

def search(domain, file_dorks, file_filters,output):        
    # Delay para evitar los bloqueos
    delay = 10
    relevant_results = dict()
    results = dict()
    dorks = read_file(file_dorks)
    filters = read_file(file_filters)
    # Se recorre el diccionario de dorks
    for dork in dorks:
        # Se establece la query
        query = f"https://www.google.com/search?q={dork.format(domain)}"
        response = requests.get(query)
        #print(response.text)
        if response.status_code == 200:
            print(f'''{blue}[+] Resultados para: '{dork.format(domain)}':\n''')
            soup = BeautifulSoup(response.text, "html.parser")

            #results = soup.find_all("div")
            #for result in results:
            urls = soup.find_all("div")
            for result in soup.find_all("div"):
                link = result.find("a")
                title = result.find("h3")
                if link and title:
                    title = result.find("h3").get_text()
                    url = link.get("href")
                    urlf = re.search(r'/url\?q=(.*?)&', url)
                    if urlf:
                        url = urlf.group(1)
                    print(f'''{bgreen}[!!] Resultado encontrado:\n''')
                    print(f'''{nc}Title: {title}''')
                    print(f'''{nc}Link: {url}\n''')
                    results["dork"] = dork
                    results["Title"] = title
                    results["Link"] = url

                    for interesting in filters:
                        if str(interesting) in title or str(interesting) in link:
                            relevant_results["Title"] = title
                            relevant_results["Link"] = url
                    
                # else:
                #     print(f"[!!] Resultado encontrado sin enlace:")
                #     #print(f"Title: {title}\n")
                #     #print(f"Link: {url}\n")       
        else:
            print(f'''{red}\n [-] Error al econtrar resultados para: '{dork}''')
        time.sleep(delay)
    gen_report(len(dorks),len(results["dork"]),relevant_results,results)

def gen_report(num_dorks,num_results,relevant_results,total_results):
    
    print_banner()
    relevant = PrettyTable()
    max_length = max(len(column) for column in relevant.values())

    
    for key in relevant:
        if len(relevant[key]) < max_length:
            relevant[key] += [''] * (max_length - len(relevant[key]))

    for key, value in relevant_results.items():
        relevant.add_column(key, value)
    print("Interesting Results:")
    print("------------------------------------------------------")
    print(relevant)


    results = PrettyTable()

    max_length2 = max(len(column) for column in results.values())

    
    for key in results:
        if len(results[key]) < max_length2:
            results[key] += [''] * (max_length2 - len(results[key]))


    for key, value in total_results.items():
        results.add_column(key, value)
    print("Results:")
    print("------------------------------------------------------")
    print(results)

    print(f"dorks executed: {num_dorks}")
    print(f"total of results: {num_dorks}")

    print("ReportGenrated")


if __name__ == "__main__":
    print_banner()

    parser = argparse.ArgumentParser(description="Automated Google Doorking Tool")
    parser.add_argument("--domain", required=True, help="Domain for Google Dorking")
    parser.add_argument("--file_dorks", default="dorks.json", help="Path to custom dorks dictionary")
    parser.add_argument("--file_filters", default="filters.json", help="Path to custom filters for results dictionary")
    parser.add_argument("--output", default="report.md", help="Path to save md report")

    args = parser.parse_args()

    search(args.domain, args.file_dorks, args.file_filters, args.output)
