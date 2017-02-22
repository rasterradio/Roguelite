import os
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

    def getChoice(self, messages):
        self.choice = messages.get_console_input()

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

    def run(self, messages):
        self.choice = "DEFAULT"
        while True:
            messages.display("")
            messages.display(self.data)
            messages.display("")

            #render the sceen
            self.event()
            if self.scripts:
                for scr in self.scripts.values():
                    messages.display(scr.name)

            self.getChoice(messages)

            if self.choice.lower() == "/":
                os.system('CLS')
                messages.display("------ROJO-------")
                messages.reset()
                break

            if self.scripts:
                for y in self.scripts.keys():
                    if self.choice.lower() == y.lower():
                        self = self.scripts.get(y)
