
import rpyc
import RPyC_client as RC
#import RPyC_Service as RS


IPset = RC.importIP("ip.txt")
pot_IPset =set([])

cList=[]

port=18861
for ip in IPset:
    serviceX=RC.ClientService(ip)
    print("will connect to", ip)
    c = rpyc.connect(ip, port, service= serviceX, config={'allow_public_attrs': True}) #create clients in all neighboring services
    print("connected to service")
    cList.append(c)

for Cl in  cList:
    pot_IPset.union(Cl.root.difference_IPset(frozenset(IPset)))
    #potential IP,
    #that are stored on neighbor nodes

while True:
    print("Ready for search! To quit press ctrl+c")
    print("Enter Search query:")
    query = input()
    print("Enter search args (optional):")
    args = input()
    relevantIP=set([])
    print("Chcking neighbor Centroids...")
    for Cl in  cList:
        relevantIP.union(Cl.root.centroid_query(query, args)) #create the set of relevant IP to search 
    print(relevantIP)

