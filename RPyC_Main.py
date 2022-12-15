
import rpyc
import RPyC_client as RC
#import RPyC_Service as RS


IPset = RC.importIP("ip.txt")
pot_IPset =set([])

cList=[]
elist=[]

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
    print("Ready for search! To quit press ctrl+c")
    print("Enter Search query:")
    query = input()
    print("Enter search args (optional):")
    args = input()
    relevantIP=set([])
    print("Chcking neighbor Centroids...")
    for Cl in  cList:
        relevantIP = relevantIP.union(Cl.root.centroid_query(query, args)) #create the set of relevant IP to search 
    for ip in relevantIP:
        print(ip)

