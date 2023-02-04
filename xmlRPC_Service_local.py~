from SimpleXMLRPCServer import SimpleXMLRPCServer
import logging
import os

import socket
import sys
import re
import string
from IB import *

# Set up logging
logging.basicConfig(level=logging.DEBUG)

server = SimpleXMLRPCServer(('localhost', 18861), logRequests=True)

# Expose a function
def execute_query(query, args=""):
    # this method returns the results of this service
        junk="/tmp/JUNK"
        pdb = IDB(junk)
        squery = SQUERY(query)
        query = QUERY()
        query.SetSQUERY(squery)
        elements = pdb.GetTotalRecords()
        if elements > 0:
            rset = pdb.VSearchSmart(query)
            if not (rset == None):
                total = rset.GetTotalEntries()
            else:
                total = 0
            print "Searching for: ", query;
            print "Got = ", total, " Records";
            results = []
            for i in range(1,total+1):
                result = rset.GetEntry(i);
                hits   = result.GetHitTable();
                feed_title = pdb.Present(result, "feed\\title")
                feed_title = re.sub(' +', ' ', feed_title)
                title_prev = ""
                n = 1
                for hit in hits:
                    offset = result.GetRecordStart()
                    fc = FC(hit[0]+offset, hit[1]+offset)
                    lfc = pdb.GetAncestorFc (fc, "entry")
                    area = pdb.NthContext(n, result, "___", "___")
                    n += 1
                    if (lfc.GetLength() > 0):
                        fct = pdb.GetDescendentsFCT (lfc, "title")
                        if len(fct) > 0:
                            title =  pdb.GetPeerContent(FC(fct[0][0], fct[0][1]))
                            title = re.sub(' +', ' ', title)
                            if title_prev != title:
                                link = None
                                fct = pdb.GetDescendentsFCT (lfc, "link")
                                if len(fct) > 0:
                                    link = pdb.GetPeerContent(FC(fct[0][0], fct[0][1]))
                                published = None
                                fct = pdb.GetDescendentsFCT (lfc, "published")
                                if len(fct) > 0:
                                    published = pdb.GetPeerContent(FC(fct[0][0], fct[0][1]))
                                title_prev = title
                                result_dict = {
                                    "logic": "RSS",
                                    "feed_title": feed_title,
                                    "title": title,
                                    "link": link,
                                    "published": published,
                                    "match": area
                                }
                                results.append(result_dict)
        else:
            print 'Empty Index!';

        pdb = None
        return results
server.register_function(execute_query)

name = sys.argv[1]
tags = sys.argv[2]
description = sys.argv[3]
from datetime import timezone
import datetime
# Getting the current date and time
onTime =  datetime.datetime.now(timezone.utc)
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
