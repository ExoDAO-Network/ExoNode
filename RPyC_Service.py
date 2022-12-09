import rpyc

class SearchService(rpyc.Service):
    ALIASES = ["SearchNode"]
    
    def __init__()
        self.IP_set = {"127.0.0.0", "0.0.0.0"} #exposed set of all ip in the network
        self.potential_IP_set={}
        
    def on_connect(self, conn):
        # code that runs when a connection is created
        # Add IP of new connection. Sets do not allow duplicates, so the list will only add new IP
        self.IP_set.add(socket.getpeername(conn._channel.stream.sock))
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # The service only stores the nodes that are connected
        self.IP_set.remove(socket.getpeername(conn._channel.stream.sock))
        pass

    def renameService(newName)
        self.ALIASES = [newName]
        pass

    def addAlias(newAlias)
        self.ALIASES.add(newAlias)
        pass

    def exposed_difference_IPset(self, clientSet) #Return a set that contains the items that only exist on the server and not in client:
        diff_server = self.IP_set.difference(clientSet)
        diff_client = clientSet.difference(self.IP_set)
        self.potential_IP_set.add(diff_client) #store the IP that need to be checked
        return diff_server

    # def unite_IPset(clientSet) #unite one set with the other, not safe, could have IP which are unwanted
    #     combined = IP_set.union(clientSet)
    #     exposed_IP_set = combined
    #     return combined

    #------- Search Related Stuff ----------
    def exposed_search_query(query, args=""):
        results=42
        return results

    def exposed_centroid_query(query, args =""): # this method returns all nodes with relavant centroids
        #code that searches all centroids in the server file system
        IP_list = exposed_IP_set
        return IP_list
######### CLASS DEFINITION OVER #################


from rpyc.utils.server import ThreadedServer
def StartServer(service, port=18861)
    t = ThreadedServer(service(), port)
    t.start()
    return t
