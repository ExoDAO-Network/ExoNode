from SimpleXMLRPCServer import SimpleXMLRPCServer
import logging
import os

import socket
import sys
import re
import string

#from datetime import timezone
import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG)

server = SimpleXMLRPCServer(('localhost', 18861), logRequests=True)

# Expose a function
def     execute_query(query, args=""):
    # this method returns the results of this service
    results = []
    for i in range(0, 10):
        feed_title = "newspapertitle"+ str(i)
        title= "Title"+ str(i)
        link="http://duckduckgo.com/"+ str(i)
        area = "kjhdfldshf ___query___ dshdshd"+ str(i)
        published = datetime.datetime.now()
        result_dict = {
            "logic": "RSS",
            "feed_title": feed_title,
            "title": title,
            "link": link,
            "published": published,
            "match": area
        }
        results.append(result_dict)

    return results
server.register_function(execute_query)

name = sys.argv[1]
tags = sys.argv[2]
description = sys.argv[3]
# Getting the current date and time
onTime =  datetime.datetime.now()
IpSet = {"127.0.0.9", "100.100.0.0"}



def get_Node_details():
    details =  {"name": name, 
                "tags": tags,
                "description": description,
                "onlineTime": onTime,
                "storedIP": IpSet}
    return details

server.register_function(get_Node_details)

try:
    print 'Use Control-C to exit'
    server.serve_forever()
except KeyboardInterrupt:
    print 'Exiting'
