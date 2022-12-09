import rpyc

class SearchService(rpyc.Service):
    exposed_IP_set = {"127.0.0.0", "0.0.0.0"} #exposed set of all ip in the network
    def on_connect(self, conn):
        # code that runs when a connection is created
        # Add IP of new connection. Sets do not allow duplicates, so the list will only add new IP
        exposed_IP_set.add(socket.getpeername(conn._channel.stream.sock))
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_search_query(query, args=""):
        results=42
        return results

    def exposed_centroid_query(query, args =""): # this method returns all nodes with relavant centroids
        #code that searches all centroids in the server file system
        IP_list = exposed_IP_set
        return IP_list

