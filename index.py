import sys
import string
from IB import *

#Filepath of index
junk="/tmp/JUNK";
pdb = IDB(junk);
print "This is PyIB version %s/%s" % (string.split(sys.version)[0], pdb.GetVersionID());
if not pdb.IsDbCompatible():
  raise ValueError, "The specified database '%s' is not compatible with this version. Re-index!" % `junk`

#Specify file to be indexed
pdb.AddRecord ("articles.xml");

pdb.SetMergeStatus(iMerge);

pdb.BeforeIndexing();

if not pdb.Index() :
  print "Indexing error encountered";

pdb.AfterIndexing();
