import rpyc
import socket
import sys

class SearchService(rpyc.Service):
    ALIASES = ["SearchNode"]
    
    def __init__(self):
        self.IP_set = {"127.0.0.9", "100.100.0.0"} #exposed set of all ip in the network
        self.potential_IP_set=set([])
        
    def on_connect(self, conn):
        # code that runs when a connection is created
        # Add IP of new connection. Sets do not allow duplicates, so the list will only add new IP
        self.IP_set.add(conn.root.showIP())
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # The service only stores the nodes that are connected
        self.IP_set.remove(conn.root.showIP())
        pass

    def renameService(self,newName):
        self.ALIASES = [newName]
        pass

    def addAlias(self,newAlias):
        self.ALIASES.add(newAlias)
        pass

    def exposed_difference_IPset(self, clientSet): #Return a set that contains the items that only exist on the server and not in client:
        diff_server = self.IP_set.difference(clientSet)
        print(diff_server)
        diff_client = clientSet.copy()
        self.potential_IP_set.add(diff_client.difference(self.IP_set)) #store the IP that need to be checked
        return diff_server

    # def unite_IPset(clientSet) #unite one set with the other, not safe, could have IP which are unwanted
    #     combined = IP_set.union(clientSet)
    #     exposed_IP_set = combined
    #     return combined

    #------- Search Related Stuff ----------
    def exposed_search_query(self,query, args=""):
        results=42
        return results

    def exposed_centroid_query(self,query, args =""): # this method returns all nodes with relavant centroids
        #code that searches all centroids in the server file system
        IP_list = self.IP_set
        return IP_list
######### CLASS DEFINITION OVER #################

from rpyc.utils.server import ThreadedServer
def StartServer(port=18861):
    t = ThreadedServer(SearchService(), port, protocol_config={'allow_public_attrs': True,})
    t.start()
    return t


print("Server started with hostname= ", sys.argv[1])
t = ThreadedServer(SearchService(),hostname=sys.argv[1], port=18861, protocol_config={'allow_public_attrs': True,})
t.start()
