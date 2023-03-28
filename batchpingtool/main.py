#-*- coding:utf-8 -*-
from ping_test import ping_test
import threading
from Tkinter import *
import ttk

class BatchPingTkinter:
    def __init__(self):
        self.headers = ("","ip","address","status","max","min","avg","trans","recv","loss_rate")
        self.dic_colnames = {"ip":{"name":"ip","width":100}, "address":{"name":"地址","width":140},"status":{"name":"状态","width":60},
                             "max":{"name":"最大时延","width":80},"min":{"name":"最小时延","width":80},"avg":{"name":"平均时延","width":80},
                             "trans":{"name":"发包数","width":80},"recv":{"name":"收包数","width":80},"loss_rate":{"name":"丢包率","width":80}}

        self.ips = []
        self.threads = []

        self.root = Tk()
        self.root.title("dddd")

        self.frame_top = Frame(width=800,height=66)
        self.frame_center = Frame(width=800,height=500)

        self.top_frame_title = Label(self.frame_top, text="IPS")
        self.top_frame_entry = Entry(self.frame_top,width=90)
        self.top_frame_button = Button(self.frame_top, text="确定", command=self.start_task)
        self.top_frame_title.grid(row=0, column=0)
        self.top_frame_entry.grid(row=0, column=1)
        self.top_frame_button.grid(row=0, column=2, padx=20, pady=20)

        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.headers)
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vbar.set)
        for k,v in self.dic_colnames.items():
            width = v.get("width",60)
            text = v.get("name","null")
            self.tree.column(k, width=width, anchor="center")
            self.tree.heading(k, text=text)
        self.tree.column("",width=5)
        self.tree.heading("")
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        self.frame_top.grid(row=0, column=0, padx=10, pady=5)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.frame_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)

        self.root.mainloop()

    def start_task(self):
        map(self.tree.delete, self.tree.get_children(""))

        ip_text = self.top_frame_entry.get()
        self.ips = ip_text.split(",") if len(ip_text)>0 else []

        self.threads = []
        for index,ip in enumerate(self.ips):
            item = self.tree.insert("","end",values=(index+1,ip,'','start','','','','','',''))
            self.threads.append(threading.Thread(target=self.ping_task,args=(item,ip)))
        for thread in self.threads:
            thread.setDaemon(True)
            thread.start()

    def ping_task(self,item,ip):
        results = ping_test(ip)
        results["status"] = "end"
        results[""] = self.tree.item(item,"values")[0]
        values = [results.get(k,'N/A') for k in self.headers]
        self.tree.item(item,values=values)

if __name__ == '__main__':
    BatchPingTkinter()