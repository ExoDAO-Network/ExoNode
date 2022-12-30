from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
import rpyc
import RPyC_client as RC


    




class SwarmSearchApp(App):
    def build(self):
    
        ##start RPyC infrastrcture
        IPset = RC.importIP("ip.txt")
        pot_IPset =set([])
        cList=[]
        elist=[]
        results=[]
        port=18861
        root_widget = BoxLayout(orientation='vertical')
            
        output_label = Label(size_hint_y=1)
        def print_out(input_text):
            output_label.text+=input_text+"\n"
            
        def reset_result(instance):
            output_label.text=""
            results = []
        btn_reset = Button(text='Clear outputs!', size_hint_y=None,
                              width=100, height=30)
                              
        btn_reset.bind(on_press=reset_result)
        MainGrid = GridLayout(rows=3, size_hint_y=2)
        
        ServerGrid = GridLayout(rows=2, cols =2, size_hint_y=2)
        
        MainGrid.add_widget(ServerGrid)
        
        querybar=TextInput(text='your search query',
              font_size=12  ,
              size_hint_y=None,
              height=30)
        searchgrid  = GridLayout(cols =2, size_hint_y=2)    
              
        searchgrid.add_widget(querybar)
        

        
            
        btn_search = Button(text='Search!', size_hint_y=None,
                              width=100, height=30)
        
        searchgrid.add_widget(btn_search)
        MainGrid.add_widget(searchgrid)
        resultGrid = GridLayout(rows=3, cols =2, size_hint_y=2)
        
        MainGrid.add_widget(resultGrid)

        root_widget.add_widget(btn_reset)
        root_widget.add_widget(output_label)
        root_widget.add_widget(MainGrid)
        print("starting RPyC")
        for ip in IPset:
            serviceX=RC.ClientService(ip)
            print_out("will connect to"+str(ip))
            try:
                c = rpyc.connect(ip, port, service= serviceX, config={'allow_public_attrs': True}) #create clients in all neighboring services
                print_out("connected to service")
                ip_switch = Switch(active=True)
                ip_label = Label()
                ip_label.text = str(ip)
                ServerGrid.add_widget(ip_label)
                ServerGrid.add_widget(ip_switch)
                cList.append(c)
            except:
                print_out("Could not connect to "+str(ip)+ "! Will remove IP from List!\n")
                elist.append(ip)
        
        print("added servers")
        for err_ip in elist:
            IPset.discard(err_ip)
            
        for Cl in  cList:
            thisSet= Cl.root.difference_IPset(frozenset(IPset))
            pot_IPset= pot_IPset.union(thisSet)
            #potential IP,
            #that are stored on neighbor nodes
        
        btn1 = ToggleButton(text='Centroid', group='search', state='down', 
              size_hint_y=None, height = 30)
        btn2 = ToggleButton(text='Full', group='search',
              size_hint_y=None,height = 30)
        searchgrid.add_widget(btn1)
        searchgrid.add_widget(btn2)
        
        
        print("added toggle")
        
        def execute(instance):
            output_label.text += querybar.text+"\n"
            if btn1.state == 'down':
                print_out("Enter Search query:")
                query = querybar.text
                print_out("Enter search args (optional):")
                args = "input()"
                relevantIP=set([])
                print_out("Chcking neighbor Centroids...")
                for Cl in  cList:
                    relevantIP = relevantIP.union(Cl.root.centroid_query(query, args)) #create the set of relevant IP to search 
                for ip in relevantIP:
                    print_out(ip)
            elif btn2.state == 'down':
                print_out("Enter Search query:")
                query = querybar.text
                print_out("Enter search args (optional):")
                args =" input()"
                relevantIP=set([])
                print_out("Chcking neighbor Indices...")
                for Cl in  cList:
                    results.append(Cl.root.search_query(query, args)) #create the set of relevant IP to search 
                print_out("The results are: "+ str(results))
            querybar.test= 'your search query'

        btn_search.bind(on_press=execute)

        print("done")
        return root_widget


SwarmSearchApp().run()
