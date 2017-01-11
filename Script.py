import os
from HelperFunctions import get_console_input
from HelperFunctions import MessageLog

class Script:
    def __init__(self, name=None, data=None, event=lambda:None, scripts=None):
        self.name = name
        self.data = data
        self.scripts = scripts
        self.event = event
        self.choice = "DEFAULT"

    def __str__(self):
        return str(self.name)        

    def getChoice(self):
        self.choice = get_console_input()
        #self.choice = raw_input("=>")
        if not self.scripts:
            return False
        if not self.scripts.keys():
            return False
        for x in self.scripts.keys():
            if self.choice.lower() == x.lower():
                return True
        return False

    def connect(self, toConnect):
        if isinstance(toConnect, Script):
            if self.scripts:
                self.scripts[toConnect.name] = toConnect
            else:
                self.scripts = {toConnect.name:toConnect}
        else:
            if self.scripts:
                for script in toConnect:
                    self.scripts[script.name] = script
            else:
                self.scripts = toConnect

    def run(self):
        messages = MessageLog()
        self.choice = "DEFAULT"
        while True:
            messages.display("")
            messages.display(self.data)
            messages.display("")

            #render the screen
            VIEWSTATE = 'text'
            self.event()
            if self.scripts:
                for scr in self.scripts.values():
                    messages.display(scr.name)
            if self.choice.lower() == "/":
                os.system('CLS')
                messages.display("------ROJO-------")
                break
            if self.getChoice() and self.scripts:
                for y in self.scripts.keys():
                    if self.choice.lower() == y.lower():
                        self = self.scripts.get(y)
