
import requests
from urllib.request import urlopen

my_file = open("subscriptions_tech.txt", "r")
  
# reading the file
data = my_file.read()
  
# 
data_into_list = data.split("\n")
for data in data_into_list:
    print(data)
    data.replace("\n", "")
    if(data == ""):
        data_into_list.remove(data)
i=0 
for url in data_into_list:
    print(url)
    resp = requests.get(url)
    try:
        with urlopen(url) as r:
            s = r.read()
        with open('rss_feeds/feed'+str(i)+'.xml', 'wb') as foutput:
            foutput.write(s) 
    except:
        print("no description")
    
    i=i+1
    

