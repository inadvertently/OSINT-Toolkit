
import colorama, httpx, os, json, textwrap, time, ctypes
from getkey import getkey
from colorama import Fore as f

history = []
client = httpx.Client(timeout=None)

def clearConsole():
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    else:
        command = 'clear'
    os.system(command)

def Ginput(str):
    print(str, end='')
    while True:
        key = getkey()
        return key

def Menu():
    start = time.time()
    try:
      ctypes.windll.kernel32.SetConsoleTitleW('OSINT Network Toolbox')
    except: pass
    print(f"""
 {f.LIGHTRED_EX}           ┌┐┌┌─┐┌┬┐┬ ┬┌─┐┬─┐┬┌─  ╔╦╗┌─┐┌─┐┬  ┌┐ ┌─┐─┐ ┬{f.RESET}
  {f.RED}          │││├┤  │ ││││ │├┬┘├┴┐   ║ │ ││ ││  ├┴┐│ │┌┴┬┘{f.RESET}
            ┘└┘└─┘ ┴ └┴┘└─┘┴└─┴ ┴   ╩ └─┘└─┘┴─┘└─┘└─┘┴ └─ 
                                                         
{f.LIGHTRED_EX}    ╔═══════════════════════╦═══════════════╦═══════════════════════╗{f.RESET}
{f.LIGHTRED_EX}    ║   {f.RESET}  1. Whois Lookup      2. Reverse DNS    3. GeoIP Lookup  {f.LIGHTRED_EX}  ║{f.RESET}
    ║                                                               ║
    ║                                                               ║
    ║     4. Reverse IP      5. Subnet Lookup  6. Recent Searches   ║
  {f.RED}  ║                                                               ║{f.RESET}
  {f.RED}  ╚═══════════════════════╩════════════════╩══════════════════════╝{f.RESET}
""")
    choice = input(f"{f.LIGHTGREEN_EX}createTask@network-toolbox:~${f.RESET} Choice: ")
    if choice == "1":
        choice1 = input(f"{f.LIGHTGREEN_EX}createTask@whois-lookup:~${f.RESET} Enter an ip address: ")
        url = f"https://api.apilayer.com/whois/query?domain=" + choice1
        payload = {}
        headers= {
        "apikey": "tLrmkSKe4X8H0KHz4FqFKWFltJUsYBtO"
        }
        response = client.request("GET", url, headers=headers, data = payload)
        status_code = response.status_code
        if status_code == 200:
          pass
        else:
          Ginput(f"[{f.RED}Error{f.RESET}] Press any key to return to main screen. [{f.RED}Error{f.RESET}]")
          clearConsole()
          Menu()
        res = response.text
        data = json.loads(res)
        domainName = data['result']['domain_name']; address = data['result']['address'];city = data['result']['city']
        country = data['result']['country']; creation = data['result']['creation_date']; dnssec = data['result']['dnssec']
        emails = data['result']['emails']; exp = data['result']['expiration_date']; name = data['result']['name']
        nameServs = data['result']['name_servers']; nameServers = ''; sep = ', '
        org = data['result']['org']; refferal = data['result']['referral_url']; registrar = data['result']['registrar']; state = data['result']['state']
        status = data['result']['status']; IndexedStatus = '';  update = data['result']['updated_date']; whois = data['result']['whois_server'];
        zipcode = data['result']['zipcode']
        for i in status:
          IndexedStatus += i + sep.replace(sep, '\n')
        for i in nameServs: 
          nameServers += i + sep
        format = f"""
Domain Name: {domainName}\nAddress: {address}\nCity: {city}
Country: {country}\nCreation Date: {creation}\nDnssec: {dnssec}
Name Servers: {nameServers}\nEmails: {emails}\nExpiration : {exp}\nName: {name}
Org: {org}\nReferral_url: {refferal}\nRegistrar: {registrar}\nState: {state}
Domain Status: \n{textwrap.indent(IndexedStatus, '    ')}Updated Date: {update}
Whois_Server: {whois}\nZipcode: {zipcode}
        """
        try:
            history.append(choice1)
            Ginput(f"\n{format}\n\n {f.LIGHTGREEN_EX}createTask@whois-lookup:~${f.RESET} Press any key to return to main screen.")
            clearConsole()
            Menu()
        except Exception as e:
            print(f'[{f.RED}{e}{f.RESET}]')
    if choice == "2":
      choice2 = input(f"{f.LIGHTGREEN_EX}createTask@reverse-dns:~${f.RESET} Enter an IP Address/IP Range/Domain Name: ")
      url = "https://api.hackertarget.com/reversedns/?q=" + choice2
      try:
        req = client.get(url)
        status_code = req.status_code
        if status_code == 200:
          pass
        else:
          Ginput(f"[{f.RED}Error{f.RESET}] Press any key to return to main screen. [{f.RED}Error{f.RESET}]")
          clearConsole()
          Menu()
        history.append(choice2)
        Ginput(f"\n{req.text}\n\n {f.LIGHTGREEN_EX}createTask@reverse-dns:~${f.RESET} Press any key to return to main screen.")
        clearConsole()
        Menu()
      except Exception as e:
        print(e)
    #if choice == "3":
      #choice3 = input(f"{f.LIGHTGREEN_EX}createTask@traceroute:~${f.RESET} Enter an IP Address or Domain Name: ")
      #API_KEY = "772636357d0a8f3768b9c17cdc4223980b32e7ad"
      #url = f"https://api.hackertarget.com/mtr/?q={choice3}&apikey={API_KEY}"
      #try:
        #req = client.get(url)
        #history.append(choice3)
        #print(history)
        #Ginput(f"\n{req.text}\n\n {f.LIGHTGREEN_EX}createTask@traceroute:~${f.RESET} Press any key to return to main screen.")
        #clearConsole()
        #Menu()
      #except Exception as e:
        #print(e)
    if choice == "3":
      choice3 = input(f"{f.LIGHTGREEN_EX}createTask@geoip-lookup:~${f.RESET} Enter an IP Address or Hostname: ")
      url = "https://api.hackertarget.com/geoip/?q=" + choice3
      try:
        req = client.get(url)
        status_code = req.status_code
        if status_code == 200:
          pass
        else:
          Ginput(f"[{f.RED}Error{f.RESET}] Press any key to return to main screen. [{f.RED}Error{f.RESET}]")
          clearConsole()
          Menu()
        history.append(choice3)
        Ginput(f"\n{req.text}\n\n {f.LIGHTGREEN_EX}createTask@geoip-lookup:~${f.RESET} Press any key to return to main screen.")
        clearConsole()
        Menu()
      except Exception as e:
        print(e)
    if choice == "4":
      choice4 = input(f"{f.LIGHTGREEN_EX}createTask@reverseip-lookup:~${f.RESET} Enter an IP Address: ")
      url = "https://api.hackertarget.com/reverseiplookup/?q=" + choice4
      try:
        req = client.get(url)
        status_code = req.status_code
        if status_code == 200:
          pass
        else:
          Ginput(f"[{f.RED}Error{f.RESET}] Press any key to return to main screen. [{f.RED}Error{f.RESET}]")
          clearConsole()
          Menu()
        history.append(choice4)
        Ginput(f"\n{req.text}\n\n {f.LIGHTGREEN_EX}createTask@geoip-lookup:~${f.RESET} Press any key to return to main screen.")
        clearConsole()
        Menu()
      except Exception as e:
        print(e)
    if choice == "5":
      choice5 = input(f"{f.LIGHTGREEN_EX}createTask@subnet-lookup:~${f.RESET} Enter cidr or ip with netmask: ")
      url = "https://api.hackertarget.com/subnetcalc/?q=" + choice5
      try:
        req = client.get(url)
        status_code = req.status_code
        if status_code == 200:
          pass
        else:
          Ginput(f"[{f.RED}Error{f.RESET}] Press any key to return to main screen. [{f.RED}Error{f.RESET}]")
          clearConsole()
          Menu()
        history.append(choice5)
        Ginput(f"\n{req.text}\n\n {f.LIGHTGREEN_EX}createTask@subnet-lookup:~${f.RESET} Press any key to return to main screen.")
        clearConsole()
        Menu()
      except Exception as e:
        print(e)
    if choice == "6":
      try:
        if history:
          for x in history:
            Ginput(f"\n{f.BLUE}Latest searches:{f.RESET} "+ x+', '+'\nPress any key to return to main menu')
            clearConsole()
            Menu()
        else:
          Ginput(f"\n{f.RED}createTask@searches${f.RESET} No recent searches have been searched in the program's runtime\nPress any key to return.")
          clearConsole()
          Menu()
      except Exception as e:
        print(e)
    else:
      clearConsole()
      Menu()

Menu()