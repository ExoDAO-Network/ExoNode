from SimpleXMLRPCServer import SimpleXMLRPCServer
import logging
import os
import base64
import socket
import sys
import re
import string


sys.path.append('/root/re-Isearch/swig')
sys.path.append('/root/re-Isearch/lib')

from IB import *

# Set up logging
logging.basicConfig(level=logging.DEBUG)

server = SimpleXMLRPCServer(("0", 18861), logRequests=True)

#Make sure it's a string that is input
#other types don't get encoded!

reload(sys).setdefaultencoding("ISO-8859-1")
def stringtobase64(stringinput):
    if (type(stringinput) == str):
        sample_string = stringinput
        sample_string_bytes = sample_string.encode("ISO-8859-1")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ISO-8859-1", errors='ignore')
        return base64_string
    else:
        return stringinput

def getnormalization(arg):
        if arg == "Unnormalized":
            return 0
        if arg == "NoNormalization":
            return 1
        if arg == "CosineNormalization":
            return 2
        if arg == "MaxNormalization":
            return 3
        if arg == "LogNormalization":
            return 4
        if arg == "BytesNormalization":
            return 5
        if arg == "preCosineMetricNormalization":
            return 6
        if arg == "CosineMetricNormalization":
            return 7
        if arg == "UndefinedNormalization":
            return 8
        return 2


def getsorting(arg):
    if arg == "Unsorted":
        return 0
    if arg == "ByDate":
        return 1
    if arg == "ByReverseDate":
        return 2
    if arg == "ByScore":
        return 3
    if arg == "ByAdjScore":
        return 4
    if arg == "ByAuxCount":
        return 5
    if arg == "ByHits":
        return 6
    if arg == "ByReverseHits":
        return 7
    if arg == "ByKey":
        return 8
    if arg == "ByIndex":
        return 9
    if arg == "ByCategory":
        return 10
    if arg == "ByNewsrank":
        return 11
    return 0

# Expose a function
#arg1 is normalization, arg2 is ranking
def execute_query(query, arg1 = "", arg2 = ""):
# this method returns the results of this service
        junk="/tmp/JUNK7"
        print(query)
        pdb = IDB(junk)
        squery = SQUERY(query)
        query = QUERY()
        query.SetSQUERY(squery)
        query.SetNormalizationMethod(getnormalization(arg1))
        query.SetSortBy(getsorting(arg2))
        query.SetMaximumResults(100)
        elements = pdb.GetTotalRecords()
        if elements > 0:
            rset = pdb.VSearchSmart(query)
            if not (rset == None):
                total = rset.GetTotalEntries()
            else:
                total = 0
            print ("Searching for: ", query)
            print ("Got = ", total, " Records")
            results = []
            for i in range(1,total+1):
                result = rset.GetEntry(i)
                hits   = result.GetHitTable()
                feed_title = pdb.Present(result, "feed\\title")
                feed_title = re.sub(' +', ' ', feed_title)
                title_prev = ""
                n = 1
                for hit in hits:
                    offset = result.GetRecordStart()
                    fc = FC(hit[0] + offset, hit[1] + offset)
                    lfc = pdb.GetAncestorFc(fc, "entry")
                    area = pdb.NthContext(n, result, "___", "___")
                    n += 1
                    if (lfc.GetLength() > 0):
                        fct = pdb.GetDescendentsFCT(lfc, "title")
                        if len(fct) > 0:
                            title = pdb.GetPeerContent(FC(fct[0][0], fct[0][1]))
                            title = re.sub(' +', ' ', title)
                            if title_prev != title:
                                link = None
                                fct = pdb.GetDescendentsFCT(lfc, "link")
                                if len(fct) > 0:
                                    link = pdb.GetPeerContent(FC(fct[0][0], fct[0][1]))
                                published = None
                                fct = pdb.GetDescendentsFCT(lfc, "published")
                                if len(fct) > 0:
                                    published = pdb.GetPeerContent(FC(fct[0][0], fct[0][1]))
                                    date = SRCH_DATE(published)
                                    if date.Ok():
                                        published = date.ISOdate()
                                title_prev = title
                                result_dict = {
                                    "logic": stringtobase64("RSS"),
                                    "feed_title": stringtobase64(feed_title),
                                    "title": stringtobase64(title),
                                    "link": stringtobase64(link),
                                    "published": stringtobase64(published),
                                    "match": stringtobase64(area)
                                }
                                results.append(result_dict)
        else:
            print('Empty Index!')

        pdb = None
        return results

server.register_function(execute_query)

#Change this
name = "Name"
tags = "Tags"
description = "Description"

import datetime
# Getting the current date and time
onTime =  datetime.datetime.now()
IpSet = {"127.0.0.9", "100.100.0.0"}

def get_Node_details(newIPlist):
    details =  {"name": name,
                "tags": tags,
                "description": description,
                "onlineTime": onTime,
                "storedIP": list(IpSet)}
    newset=set(newIPlist)
    IpSet.update(newset)
    return details

server.register_function(get_Node_details)

def con_test():
    return True
server.register_function(con_test)

try:
    print ('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print ('Exiting')
