import requests
import time
import sys
import re
from bs4 import BeautifulSoup

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
banner = f'''
{bblue}██████╗ ██╗   ██╗██████╗  ██████╗ ██████╗ ██╗  ██╗    
{bblue}██╔══██╗╚██╗ ██╔╝██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝    
{yellow}██████╔╝ ╚████╔╝ ██║  ██║██║   ██║██████╔╝█████╔╝     
{green}██╔═══╝   ╚██╔╝  ██║  ██║██║   ██║██╔══██╗██╔═██╗     
{red}██║        ██║   ██████╔╝╚██████╔╝██║  ██║██║  ██╗    
{red}╚═╝        ╚═╝   ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    
{purple}                                by [KalelS] v1.1{nc}
'''

print(banner)


if len(sys.argv) != 2:
    print(f'''{red}[!] Usage: python google_dork.py <domain>''')
    sys.exit(1)

# Diccionario de dorks más comunes
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
    ##
    "site:{} inurl:admin intext:password".format(sys.argv[1]),
    "site:{} intitle:index of".format(sys.argv[1]),
    #"site:{} ext:doc | ext:pdf | ext:docx | ext:txt | ext:xlsx | ext:xls".format(sys.argv[1]),
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
    "related:{} ext:doc".format(sys.argv[1]),
    "related:{} ext:docx".format(sys.argv[1]),
    "related:{} ext:xls".format(sys.argv[1]),
    "related:{} ext:xlsx".format(sys.argv[1]),
    "related:{} ext:ppt".format(sys.argv[1]),
    "related:{} ext:pptx".format(sys.argv[1]),
    "related:{} ext:pdf".format(sys.argv[1]),
    ##
    "inurl:{} filetype:doc".format(sys.argv[1]),
    "inurl:{} filetype:docx".format(sys.argv[1]),
    "inurl:{} filetype:xls".format(sys.argv[1]),
    "inurl:{} filetype:xlsx".format(sys.argv[1]),
    "inurl:{} filetype:ppt".format(sys.argv[1]),
    "inurl:{} filetype:pptx".format(sys.argv[1]),
    "inurl:{} filetype:pdf".format(sys.argv[1]),
    "related:{} filetype:doc".format(sys.argv[1]),
    "related:{} filetype:docx".format(sys.argv[1]),
    "related:{} filetype:xls".format(sys.argv[1]),
    "related:{} filetype:xlsx".format(sys.argv[1]),
    "related:{} filetype:ppt".format(sys.argv[1]),
    "related:{} filetype:pptx".format(sys.argv[1]),
    "related:{} filetype:pdf".format(sys.argv[1]),
]

# Delay apra evitar los bloqueos
delay = 10

# Se recorre el diccionario de dorks
for dork in dorks:
    # Se establece la query
    query = f"https://www.google.com/search?q={dork}"


    response = requests.get(query)

    #print(response.text)

    if response.status_code == 200:
        print(f'''{blue}[+] Resultados para: '{dork}':\n''')
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
            # else:
            #     print(f"[!!] Resultado encontrado sin enlace:")
            #     #print(f"Title: {title}\n")
            #     #print(f"Link: {url}\n")       
    else:
        print(f'''{pink}\n [-] Error al econtrar resultados para: '{dork}''')
    time.sleep(delay)

