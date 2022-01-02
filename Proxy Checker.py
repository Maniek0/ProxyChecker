from tkinter import *
from tkinter import filedialog,messagebox
from tkinter.ttk import Separator
import requests
import threading
import time
class Interface(threading.Thread):
    def __init__(self,threadID,name,counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        ws = Tk()
        ws.title('Proxy checker')
        ws.resizable(0,0)
        
        proxyList = Listbox(ws,height=15,width=30,state=DISABLED)
        proxyList.pack(side=LEFT,pady=10,padx=10)
        sep = Separator(ws,orient='vertical')
        sep.pack(fill=Y,side=LEFT)
        rightFrame = Frame(ws)
        rightFrame.pack(expand=True,fill=Y,side=LEFT)
        buttons = Frame(rightFrame,padx=10,pady=20)
        buttons.pack(side=TOP)
        def openProxy():
            Proxies().openProxy()
            if len(proxy) >=1:
                proxyList.config(state=NORMAL)
                proxyList.delete(0,END)
                for line in proxy:
                    proxyList.insert(END,str(line))
                proxyList.config(state=DISABLED)
        proxyOpenButton = Button(buttons,width=15,height=2,text='Wczytaj proxy',command=openProxy)
        proxyOpenButton.pack()
        def startCheck():
            global checking
            if checking == False:
                messagebox.showinfo('Proxy checker', 'Sprawdzanie jeszcze trwa.')
            elif proxy != []:
                checking = False
                check = Check(1,"CheckTread",1)
                check.setDaemon(gui)
                check.start()
            else: messagebox.showerror('Proxy checker', 'Proszę wczytać proxy.')
        proxyCheckButton = Button(buttons,width=15,height=2,text='Sprawdź proxy',command=startCheck)
        proxyCheckButton.pack(pady=10)
        proxySaveButton = Button(buttons,width=15,height=2,text='Save',command=Proxies().saveProxy)
        proxySaveButton.pack()

        labels = Frame(rightFrame)
        labels.pack(side=BOTTOM,pady=20)
        global l2,l4
        l1 = Label(labels,text='Działające: ')
        l1.grid(row=0,column=0)
        l2 = Label(labels, text='0')
        l2.grid(row=0,column=1)
        l3 = Label(labels, text='Nie działające: ')
        l3.grid(row=1, column=0)
        l4 = Label(labels,text='0')
        l4. grid(row=1, column=1)
        ws.mainloop()
class Proxies:
    def openProxy(self):
        global proxy
        filename = filedialog.askopenfilename(title="Wybierz proxy",filetypes=(("Pliki tekstowe","*.txt"),("Wszystkie pliki","*.*")) )
        if filename != "":
            file = open(filename,encoding='utf-8')
            data = file.read()
            file.close()
            proxy = data.split('\n')
    def saveProxy(self):
        if goodProxy != []:
            proxyFile = goodProxy
            filename = filedialog.asksaveasfilename(title="Zapisz proxy", defaultextension=".txt", filetypes=(("Pliki tekstowe","*.txt"),("Wszystkie pliki","*.*")))
            if filename != "":
                good = ""
                for line in proxyFile:
                    good += str(line) +'\n'
                goods = good[0:-1]
                data = open(filename, 'w')
                dataWrite = data.write(goods)
                data.close()
        else:
            messagebox.showerror('Proxy checker', 'Nie ma nic do zapiszania')
class Check(threading.Thread):
    def __init__(self,threadID,name,counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        goods = []
        proxy_ = proxy
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pl',
            'accept-charset': 'utf-8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
        }
        i = x = 0
        l2.config(text=i)
        l4.config(text=x)
        for line in proxy_:
            try:
                proxies = {
                    'http': 'http://'+line,
                    'https': 'http://'+line,
                }
                s = requests.get(url='https://onet.pl',timeout=5,proxies=proxies,headers=headers)
                print(s.status_code)
                i+=1
                l2.config(text=i)
                goods.append(line)
            except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.SSLError,requests.exceptions.ReadTimeout,requests.exceptions.ConnectionError,requests.exceptions.InvalidProxyURL):
                x+=1
                l4.config(text=x)
            time.sleep(1)
        if goods != []:
            global goodProxy
            goodProxy = goods
        messagebox.showinfo('Proxy checker','Sprawdzanie skończone')
        global checking
        checking = True
if __name__ == '__main__':
    gui = Interface(1,"Main",1)
    gui.start()
    proxy = goodProxy = []
    checking = True