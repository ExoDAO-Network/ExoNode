import RPyC_client as RC
import RPyC_service as RS




IPlist = RC.importIP(ip.txt)
myServer = RS.StartServer(RS.SearchService)


