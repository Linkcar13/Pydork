#Libraries Definition
import argparse
import requests
import time
import sys
import re
from bs4 import BeautifulSoup
import json
from tabulate import tabulate 
import pandas as pd

# Color Definition

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
    {purple}██████╔╝ ╚████╔╝ ██║  ██║██║   ██║██████╔╝█████╔╝     
    {green}██╔═══╝   ╚██╔╝  ██║  ██║██║   ██║██╔══██╗██╔═██╗     
    {red}██║        ██║   ██████╔╝╚██████╔╝██║  ██║██║  ██╗    
    {purple}╚═╝        ╚═╝   ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    
    {purple}                                by [KalelS] v1.2{nc}
    '''

    print(banner)

def read_file(file):
    #Custom file of dorks or filters
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
    # avoid google ban
    delay = 10
    columns1 = ["dork","Title","Link"]
    columns2 = ["Title","Link"]
    relevant_results = pd.DataFrame(columns=columns2)
    results = pd.DataFrame(columns=columns1)
    dorks = read_file(file_dorks)
    filters = read_file(file_filters)
    # read dictionary of dorks
    for dork in dorks:
        # set query
        query = f"https://www.google.com/search?q={dork.format(domain)}"
        response = requests.get(query)

        if response.status_code == 200:
            print(f'''{blue}[+] Resultados para: '{dork.format(domain)}':\n''')
            soup = BeautifulSoup(response.text, "html.parser")

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
                    new_result = pd.DataFrame([{
                        "dork": dork,
                        "Title": title,
                        "Link": url
                    }])
                    results = pd.concat([results, new_result], ignore_index=True)

                    for interesting in filters:
                        if str(interesting) in title or str(interesting) in link:
                            new_result_r = pd.DataFrame([{
                                "Title": title,
                                "Link": url}])
                            relevant_results = pd.concat([relevant_results, new_result_r], ignore_index=True)     
        else:
            print(f'''{red}\n [-] Error al econtrar resultados para: '{dork}''')
        time.sleep(delay)
    gen_report(len(dorks),len(results["dork"]),relevant_results,results,output,domain)

def adjust_width(df, widths):
    df = df.copy()  # Create a copy of original df
    for col, width in widths.items():
        df[col] = df[col].astype(str).apply(lambda x: x.ljust(width)[:width])
    return df    

def gen_report(num_dorks, num_results, relevant_results, total_results,output,domain):
    print_banner()

    widths1 = {
    "Title": 50,
    "Link": 160,
    }

    print(f'''{red}
  ___     _                  _   _                             _ _      
 |_ _|_ _| |_ ___ _ _ ___ __| |_(_)_ _  __ _   _ _ ___ ____  _| | |_ ___
  | || ' \  _/ -_) '_/ -_|_-<  _| | ' \/ _` | | '_/ -_|_-< || | |  _(_-<
 |___|_||_\__\___|_| \___/__/\__|_|_||_\__, | |_| \___/__/\_,_|_|\__/__/
                                       |___/                            {nc}''')
    print(tabulate(adjust_width(relevant_results,widths1), headers = 'keys', tablefmt = 'fancy_grid',showindex=False))

    widths2 = {
    "dork": 20,
    "Title": 40,
    "Link": 130
    }

    print(f'''{green}
  ___             _ _      
 | _ \___ ____  _| | |_ ___
 |   / -_|_-< || | |  _(_-<
 |_|_\___/__/\_,_|_|\__/__/
                           
:{nc}''')
    print(tabulate(adjust_width(total_results,widths2), headers = 'keys', tablefmt = 'fancy_grid',showindex=False))

    # print total operations
    print(f'''{cyan}dorks executed: {num_dorks}''')
    print(f'''{purple}total of results: {num_results} {nc}''')

    reporte_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Report for the site {domain} </title>
          <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js" integrity="sha384-BBtl+eGJRgqQAUMxJ7pMwbEyER4l1g+O15P+16Ep7Q9Q+zqX6gSbd85u4mG4QzX+" crossorigin="anonymous"></script>
    </head>
    <body>
        <h1 style="text-align:center;">Report for the site {domain}</h1>
        <h2 style="text-align:center;">Interesting Results</h2>
        {relevant_results.to_html(index=False,border=0, classes="table table-hover")}
        <h2 style="text-align:center;">Results</h2>
        {total_results.to_html(index=False,border=0,classes="table table-hover")}
    </body>
    </html>
    """
     

    with open(output, "w") as file:
        file.write(reporte_html)

    print(f"Report Generated on {output}")


if __name__ == "__main__":
    print_banner()

    parser = argparse.ArgumentParser(description="Automated Google Doorking Tool")
    parser.add_argument("--domain", required=True, help="Domain for Google Dorking")
    parser.add_argument("--file_dorks", default="dorks.json", help="Path to custom dorks dictionary")
    parser.add_argument("--file_filters", default="filters.json", help="Path to custom filters for results dictionary")
    parser.add_argument("--output", default="report.html", help="Path to save md report")

    args = parser.parse_args()

    search(args.domain, args.file_dorks, args.file_filters, args.output)
