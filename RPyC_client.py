import rpyc


def importIP(inputfile) #reads file and returns all ip from list
    # opening the file in read mode
    my_file = open(inputfile "r")
  
    # reading the file
    data = my_file.read()
      
    # replacing end of line('/n') with ' ' and
    # splitting the text it further when '.' is seen.
    data_into_list = data.replace('\n', ' ').split(".")
      
    # returning the data
        return(data_into_list)


class nodeClient:
    def __init__(address, port=18861):
        self.c = rpyc.connect("localhost", 18861)
        self.cmd = c.root


