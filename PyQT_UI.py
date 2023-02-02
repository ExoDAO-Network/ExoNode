
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
import rpyc
import RPyC_client as RC
import webbrowser
from functools import partial


class SwarmSearchApp(App):
        
    def build(self):
    
        
        root_widget = BoxLayout(orientation='vertical')
            
        MainGrid = GridLayout(cols =1)
        
        ShellViewer = ScrollView(size_hint=(1, 0.5), size=(Window.width, 100))
        output_label = Label(size_hint_y=3, height = 100)
        def print_out(input_text):
            output_label.text+=input_text+"\n"
            
        btn_reset = Button(text='Clear outputs!', size_hint_y=None,
                              width=100, height=10)
        btn_refresh = Button(text='refresh_server', size_hint_y=None,
                              width=100, height=10)
        MainGrid.add_widget(btn_reset)
        ShellViewer.add_widget(output_label)
        MainGrid.add_widget(ShellViewer)
        MainGrid.add_widget(btn_refresh)
        
        ServerGrid = GridLayout(cols =2, height=20, size_hint_y=1)
        ServerViewer = ScrollView(size_hint=(1, 0.5), size=(Window.width, 200))
        ServerViewer.add_widget(ServerGrid)   
        MainGrid.add_widget(ServerViewer)           
        
        
        querybar=TextInput(text='your search query',
              font_size=12  ,
              size_hint_y=None,
              height=30)
        searchgrid  = GridLayout(rows=10, cols =2, size_hint_y=None)    
              
        searchgrid.add_widget(querybar)
        btn_search = Button(text='Search!', size_hint_y=None,
                              width=100, height=30)
        
        searchgrid.add_widget(btn_search)
        MainGrid.add_widget(searchgrid)
        resultGrid = GridLayout(cols =3, size_hint_y=2)
        
        resultViewer = ScrollView(size_hint=(1, 2), size=(Window.width, 400))
        resultViewer.add_widget(resultGrid)
        MainGrid.add_widget(resultViewer)

        def reset_result(instance):
            output_label.text=""
            results = [] 
            while len(resultGrid.children)>0: 
                resultGrid.remove_widget(resultGrid.children[len(resultGrid.children)-1])
                
                
        def ip_toggler(ip,cList, cipList, sList, sipList, instance, value):
            if(value == True):
                index = cipList.index(ip)
                sList.append(cList[index])
                sipList.append(ip)
            else:
                index = sipList.index(ip)
                sList.pop(index)
                sipList.pop(index)
            
        def scan_and_connect(IPset, cList, cipList, sList, sipList, elist):
            for ip in IPset:
                serviceX=RC.ClientService(ip)
                try:
                    c = rpyc.connect(ip, port, service= serviceX, config={'allow_public_attrs': True}) #create clients in all neighboring services
                    print(c)
                    
                    ip_switch = Switch(active=False)
                    ip_switch.bind(active=partial(ip_toggler, str(ip), cList, cipList, sList, sipList))
                    ip_label = Label(size=(30,100))
                    ip_label.text = str(ip)
                    ServerGrid.add_widget(ip_label)
                    ServerGrid.add_widget(ip_switch)
                    cList.append(c)
                    
                    cipList.append(ip)
                    print_out("Connected to"+str(ip))
                except:
                    print_out("Could not connect to "+str(ip)+ "! Try to refresh later!\n")
                    elist.append(ip)
        
            print("added servers")
            for err_ip in elist:
                IPset.discard(err_ip)
                
            print("removed inactive servers")


        
        btn_reset.bind(on_press=reset_result)
        
        root_widget.add_widget(MainGrid)
        
        ##start RPyC infrastrcture
        IPset = RC.importIP("ip.txt")
        pot_IPset =set([])
        cList=[]
        cipList=[]
        sList =[]
        sipList=[]
        elist=[]
        results=[]
        port=18861
        print("starting RPyC")
        scan_and_connect(IPset,cList, cipList, sList, sipList, elist)
        
        def refresh_IP(instance):
            for ip in elist:
                serviceX=RC.ClientService(ip)
                try:
                    c = rpyc.connect(ip, port, service= serviceX, config={'allow_public_attrs': True}) #create clients in all neighboring services
                    ip_switch = Switch(active=False)
                    ip_switch.bind(active=partial(ip_toggler, str(ip), cList, cipList, sList, sipList))
                    ip_label = Label()
                    ip_label.text = str(ip)
                    ServerGrid.add_widget(ip_label)
                    #ip_switch.bind(active =)
                    ServerGrid.add_widget(ip_switch)
                    cList.append(c)
                    cipList.append(ip)
                    IPset.add(ip)
                    elist.remove(ip)
                    print_out("Connected to"+str(ip))
                except:
                    print_out("Could not connect to "+str(ip)+ "! Try to refresh later!\n")
            print("refreshed servers")
        btn_refresh.bind(on_press=refresh_IP)
            
        #for Cl in  cList:
            #thisSet= Cl.root.difference_IPset(frozenset(IPset))
            #print(thisSet)
            #pot_IPset= pot_IPset.union(thisSet)
            #potential IP,
            #that are stored on neighbor nodes
        btn1 = ToggleButton(text='Centroid - not working :(', group='search', 
              size_hint_y=None, height = 30)
        btn2 = ToggleButton(text='Full search', group='search', state='down',
              size_hint_y=None,height = 30)
        searchgrid.add_widget(btn1)
        searchgrid.add_widget(btn2)
        
        
        print("added toggle")

        def follow_link(url, instance):
            webbrowser.open_new_tab(url)
            
        def execute(instance):
            output_label.text += querybar.text+"\n"
            if btn1.state == 'down':
                query = querybar.text
                args = "input()"
                relevantIP=set([])
                for Cl in  sList:
                    relevantIP = relevantIP.union(Cl.root.centroid_query(query, args)) #create the set of relevant IP to search 
                for ip in relevantIP:
                    print_out(ip)	
            elif btn2.state == 'down':
                query = str(querybar.text) 
                args =""
                relevantIP=set([])
                findsmth=False
                print(type(query))
                for Cl in  sList:
                    query_result = Cl.root.search_query(query)
                    for qresult in query_result:
                        qresult = {key: qresult[key] for key in qresult}
                        print(str(qresult["title"]))
                        #query_result = {key: query_result[key] for key in query_result}
                        #if(shortres != ""):
                        result= Button(text=str(qresult["feed_title"]),size_hint_y=None, width=50, height=30,on_press=partial(follow_link, str(qresult["link"])))
                        reslabel = Label(text=str(qresult["title"]), text_size= (500,100), halign= 'right',   valign= 'middle')
                        res2label = Label(text=str(qresult["match"]), text_size= (500,100), halign= 'right',   valign= 'middle')
                        resultGrid.add_widget(reslabel)
                        resultGrid.add_widget(res2label)
                        resultGrid.add_widget(result)
                    findsmth =  True
                if(not findsmth):
                    print_out("NO RESULTS!")
                else:
                    resultGrid.add_widget(Label(text=''))
                    #results.append(Cl.root.search_query(query, args)) #create the set of relevant IP to search 
                
            querybar.test= 'your search query'

        btn_search.bind(on_press=execute)

        print("done")
        return root_widget


SwarmSearchApp().run()

