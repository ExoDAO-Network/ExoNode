import rpyc


def importIP(inputfile): #reads file and returns all ip from list
    # opening the file in read mode
    my_file = open(inputfile, "r")
  
    # reading the file
    data = my_file.read()
      
    # 
    data_into_list = data.split("\n")
    for data in data_into_list:
        data.replace("\n", "")
        if(data == ""):
            data_into_list.remove(data)
      
    # returning the data
    return(set(data_into_list))

class ClientService(rpyc.Service):
    def __init__(self, address):
        self.ip = address
    def exposed_showIP(self):
        return self.ip


