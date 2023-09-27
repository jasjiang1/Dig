import dns
import time
import datetime

def mydig(domain,timeStart,ip = "198.41.0.4"): #ip is defaulted to a root server IP, can be changed if necessary
    timeNow = time.perf_counter() #return error if query has taken too long
    if timeNow-timeStart > 5:
        return "Timeout error, likely due to invalid domain"
    try:
        domainName = dns.name.from_text(domain) #takes the domain and queries it, if it fails return an error
        dnsRequest = dns.message.make_query(domainName, dns.rdatatype.A)
        nextServer = dns.query.udp(dnsRequest, ip)
    except:
        return "The DNS server could not be queried"
    add = nextServer.additional
    auth = nextServer.authority
    ans = nextServer.answer
    if (ans == []): 
        index = 0
        if not add == []:   #
            spl = str(add[0]).split()   #if first line is of type AAAA, uses the second line instead
            if spl[3] == "AAAA":
                index = 1
            for x in add[index]:        #recursive call with a new IP
                return mydig(domain, timeStart, str(x))
        elif not auth == []:
            spl = str(auth[0]).split()  #same as additional
            if spl[3] == "AAAA":
                index = 1
            for x in auth[index]:
                return mydig(str(x), timeStart) #recursive call with new domain and default IP
        else:
            print("No data could be found in the additional, authority and answer section") #if there is no additional, authority or answer section, return an error                  
    else:
        ansStr = str(ans[0])
        spl = ansStr.split()    #if answer contains CNAME, then recursively call with new domain and default IP
        if spl[3] == "CNAME":   
            for x in ans[0]:
                return mydig(str(x), timeStart)
        else:
            return ans[0]   
                   
if __name__ ==  "__main__":
    domain = input("Input a Domain: ")
    print("\nQUESTION SECTION:")
    print(domain + "            IN  A\n") #takes user input (domain)
    print("ANSWER SECTION:")
    start = time.perf_counter() #time before querying starts
    ansSection = mydig(domain, start)   #query
    end = time.perf_counter()   #end time of the query
    print(ansSection)
    print("\nQuery time: " + str((end-start)*1000) + " ms") #prints the time it took to query
    print("WHEN: " + str(datetime.datetime.now()))  #prints current time and day