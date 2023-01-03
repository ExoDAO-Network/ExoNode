import rpyc
import RPyC_client as RC
#import RPyC_Service as RS


IPset = RC.importIP("ip.txt")
pot_IPset =set([])

cList=[]
elist=[]
results=[]
port=18861
for ip in IPset:
    serviceX=RC.ClientService(ip)
    print("will connect to", ip)
    try:
        c = rpyc.connect(ip, port, service= serviceX, config={'allow_public_attrs': True}) #create clients in all neighboring services
        print("connected to service\n")
        cList.append(c)
    except:
        print("Could not connect to ", ip, "! Will remove IP from List!\n")
        elist.append(ip)

for err_ip in elist:
    IPset.discard(err_ip)

for Cl in  cList:
    thisSet= Cl.root.difference_IPset(frozenset(IPset))
    pot_IPset= pot_IPset.union(thisSet)
    #potential IP,
    #that are stored on neighbor nodes
print(pot_IPset)
while True:
    results = []
    print("Ready for search! To quit press ctrl+c")
    relevantIP=set([])
    print("Enter Search query:")
    query = input()
    relevantIP=set([])
    print("Checking neighbor Indices...")
    for Cl in  cList:
        results.append(Cl.root.search_query(query)) #create the set of relevant IP to search
    tmp = 1
    for resultz in results:
        print("\n")
        print("*"*80)
        print("Printing Results for Node "+ str(tmp))
        print("*"*80)
        print("\n")
        
        tmp += 1
        index = 1
        for result in resultz:
            print("\n")
            print("="*80)
            print("Result: %s" % index)
            print("="*80)
            print("Area: %s" % result["area"])
            print("Date: %s" % result["datum"])
            print("Score: %s" % result["score"])
            print("Hits: %s" % result["hits"])
            print("="*80)
            print("\n")
            index += 1
