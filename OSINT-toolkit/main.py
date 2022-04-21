import colorama, httpx, os, json, textwrap, time, ctypes #Importing the modules being used throughout the program. Must be installed prior to running the application
from getkey import getkey
from colorama import Fore as f

history = [] #Creating our list which is going to be responsible for storing our inputs
client = httpx.Client(timeout=None) #Client we are using to send requests

def clearConsole(): #Function determines whether the machine os is windows or linux
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    else:
        command = 'clear' #Could be linux therefore we use 'clear' to clear our terminal
    os.system(command)

def Ginput(str): #Function responsible for sending our strings then waiting for an input 
    print(str, end='') 
    while True:
        key = getkey() #Determining the key pressed
        return key

def Menu(): #Function respopnsible for entir program. Detecting inputs, sending requests, indexing data and so on...
    try:
      ctypes.windll.kernel32.SetConsoleTitleW('OSINT Network Toolbox') #this sets the terminals title if the machine is windows
    except: pass #if not, ignore and pass
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
""") #This is our main menu banner which could have been done more neatly for better appearance but this still manages

    choice = input(f"{f.LIGHTGREEN_EX}createTask@network-toolbox:~${f.RESET} Choice: ") #Waiting for an input preferably an int
    if choice == "1": #if "1" was inputted
        choice1 = input(f"{f.LIGHTGREEN_EX}createTask@whois-lookup:~${f.RESET} Enter an ip address or Hostname: ") #Once again waiting for an input as asked IF the choice was "1"
        url = f"https://api.apilayer.com/whois/query?domain=" + choice1 #The api we'll b e using to retrieve the data
        payload = {}
        headers= {
        "apikey": "tLrmkSKe4X8H0KHz4FqFKWFltJUsYBtO" #Our API key which is NEEDED to fetch/request data
        }
        response = client.request("GET", url, headers=headers, data = payload) #Here we send the request to the url using our API Key
        status_code = response.status_code 
        if status_code == 200: #Status code 200 basically means the request went through successfully
          pass #Went through well so we passed it as there is n othing to worry about
        else:
          Ginput(f"[{f.RED}Error{f.RESET}] Press any key to return to main screen. [{f.RED}Error{f.RESET}]") #Here we call our func Ginput which prints our str then waits for an input to continue
          clearConsole() #If we recieved the input lets call our func clearConsole, determine the OS, then clear the terminal
          Menu() #Back to the start
        res = response.text #The request went through! Lets start gathering our data
        data = json.loads(res) #We parse the JSON into a dict 

        #The next couple lines are us navigating through the JSON to collect specific data. The variable names are practically what we're looking for in the JSON dict
        domainName = data['result']['domain_name']; address = data['result']['address'];city = data['result']['city']
        country = data['result']['country']; creation = data['result']['creation_date']; dnssec = data['result']['dnssec']
        emails = data['result']['emails']; exp = data['result']['expiration_date']; name = data['result']['name']
        nameServs = data['result']['name_servers']; nameServers = ''; sep = ', ' #I noticed that usually several nameservers come up. So, for better format I created an empty string then added a for loop to collect the nameservers from the JSON dict (nameServs) and print them while using ',' as a seperator
        org = data['result']['org']; refferal = data['result']['referral_url']; registrar = data['result']['registrar']; state = data['result']['state']
        status = data['result']['status']; IndexedStatus = '';  update = data['result']['updated_date']; whois = data['result']['whois_server']; #Multiple domain status's usually are given so I once again, created an empty str, for loop, and added to the empty str
        zipcode = data['result']['zipcode']
        for i in status:
          IndexedStatus += i + sep.replace(sep, '\n') #For better format I replaced our var sep's str with '\n'
          #For loop for indexedStatus
        for i in nameServs: 
          nameServers += i + sep #For loop for nameServers 

        format = f"""
Domain Name: {domainName}\nAddress: {address}\nCity: {city}
Country: {country}\nCreation Date: {creation}\nDnssec: {dnssec}
Name Servers: {nameServers}\nEmails: {emails}\nExpiration : {exp}\nName: {name}
Org: {org}\nReferral_url: {refferal}\nRegistrar: {registrar}\nState: {state}
Domain Status: \n{textwrap.indent(IndexedStatus, '    ')}Updated Date: {update}
Whois_Server: {whois}\nZipcode: {zipcode}
        """ #Here I created a pretty nefty format which will be returned to the user with the data found. We call in all our JSON Dict variables which were responsible for fetching the information specified

        try:
            history.append(choice1) #Here I append our input to the empty list history
            Ginput(f"\n{format}\n\n {f.LIGHTGREEN_EX}createTask@reverse-dns:~${f.RESET} Press any key to return to main screen.")
            clearConsole()
            Menu()
        except Exception as e: #If somethign went wrong, the error will be returned to the client
            print(f'[{f.RED}{e}{f.RESET}]')
    if choice == "2":
      choice2 = input(f"{f.LIGHTGREEN_EX}createTask@reverse-dns:~${f.RESET} Enter an IP Address/IP Range/Domain Name: ")
      url = "https://api.hackertarget.com/reversedns/?q=" + choice2 #Different API this time as our previous one does not support reverse dns lookups
      try:
        req = client.get(url) #Fetching url
        status_code = req.status_code
        if status_code == 200: #Success
          pass
        else:
          Ginput(f"[{f.RED}Error{f.RESET}] Press any key to return to main screen. [{f.RED}Error{f.RESET}]") #We did not recieve status code 200 therefore, error
          clearConsole() #Clear func
          Menu()# Back to the start
        history.append(choice2) #Once again appending our input to the history list
        Ginput(f"\n{req.text}\n\n {f.LIGHTGREEN_EX}createTask@reverse-dns:~${f.RESET} Press any key to return to main screen.")
        clearConsole()
        Menu()
      except Exception as e: #If error, we return the error str
        print(e)

#The following code was used to determine the hops that will follow across the Ip/Domain BUT the api became paid leaving us to pay for a key. In which I did not pay for


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
      url = "https://api.hackertarget.com/geoip/?q=" + choice3 #Same API this time just different tool
      try:
        req = client.get(url) #Fetching 
        status_code = req.status_code
        if status_code == 200:
          pass
        else:
          Ginput(f"[{f.RED}Error{f.RESET}] Press any key to return to main screen. [{f.RED}Error{f.RESET}]") #Returns data then waits for input
          clearConsole() #Clearing
          Menu() #Back to start
        history.append(choice3) #Appending the input to our list
        Ginput(f"\n{req.text}\n\n {f.LIGHTGREEN_EX}createTask@geoip-lookup:~${f.RESET} Press any key to return to main screen.")
        clearConsole()
        Menu()
      except Exception as e:
        print(e) #If error, return it
    if choice == "4":
      choice4 = input(f"{f.LIGHTGREEN_EX}createTask@reverseip-lookup:~${f.RESET} Enter an IP Address or Hostname: ")#Waiting input
      url = "https://api.hackertarget.com/reverseiplookup/?q=" + choice4 #Same API once again, different tool
      try:
        req = client.get(url)#Fetching
        status_code = req.status_code
        if status_code == 200: #Success
          pass
        else:
          Ginput(f"[{f.RED}Error{f.RESET}] Press any key to return to main screen. [{f.RED}Error{f.RESET}]") #Code was not 200 so raising error
          clearConsole()#Clearing func
          Menu()#Restarting func
        history.append(choice4)#Appending to our list
        Ginput(f"\n{req.text}\n\n {f.LIGHTGREEN_EX}createTask@geoip-lookup:~${f.RESET} Press any key to return to main screen.")#Returns our str then waits for input
        clearConsole()#Clearing
        Menu()
      except Exception as e:
        print(e) #Notifying client that an error was encountered
    if choice == "5":
      choice5 = input(f"{f.LIGHTGREEN_EX}createTask@subnet-lookup:~${f.RESET} Enter cidr or ip with netmask: ") #Waiting for input
      url = "https://api.hackertarget.com/subnetcalc/?q=" + choice5 #Same API, different tool
      try:
        req = client.get(url) #Fetching 
        status_code = req.status_code
        if status_code == 200: #Sucess
          pass
        else: #Error
          Ginput(f"[{f.RED}Error{f.RESET}] Press any key to return to main screen. [{f.RED}Error{f.RESET}]") #Code 200 was not recieved
          clearConsole()#Clearing
          Menu()#Back to the start
        history.append(choice5) #Appending to list
        Ginput(f"\n{req.text}\n\n {f.LIGHTGREEN_EX}createTask@subnet-lookup:~${f.RESET} Press any key to return to main screen.")
        clearConsole()
        Menu()
      except Exception as e:
        print(e)
    if choice == "6": 
      try:
        if history: #Here we call in our list to make sure it isn't empty
          for x in history: #Creating a for loop to iterate over all the inputs we've appended
            Ginput(f"\n{f.BLUE}Latest searches:{f.RESET} "+ x+', '+'\nPress any key to return to main menu.') #Returning the inputs (x), and using ',' as a seperator. Then waits for input to continue
            clearConsole() #Clearing func after input
            Menu() #Restarting func
        else: #list came back as empty
          Ginput(f"\n{f.RED}createTask@searches${f.RESET} No recent searches have been searched in the program's runtime\nPress any key to return.") #No data to show so we wait for input to move on
          clearConsole()
          Menu()
      except Exception as e: #Error, returning
        print(e)
    else: #If any of the inputs we not inputs we checked for ('1', '2', '3' and so on..) we clear the console and restart the func below
      clearConsole()
      Menu()
 
Menu()#How we start our program. We call in the main func which is menu 

