import os
from HelperFunctions import MessageLog

class Condition:
    def __init__(self, name, state, failResponse):
        self.name = name
        self.state = state
        self.failResponse = failResponse

    def __str__(self):
        return str(self.failResponse)

class Script:

    conditions = {}

    def __init__(self, name=None, data=None, event=lambda:None, scripts=None, breakable=True, requirements = None):
        self.name = name
        self.data = data
        self.scripts = scripts
        self.event = event
        self.choice = "DEFAULT"
        self.breakable = breakable
        self.requirements = requirements
        for r in requirements:
            conditions[r.name] = r.state

    def __str__(self):
        return str(self.name)

    def getChoice(self, messages):
        self.choice = messages.get_console_input()
        print(self.choice)
        if not self.scripts:
            return False
        if not self.scripts.keys():
            return False
        for x in self.scripts.keys():
            if self.choice.lower() == x.lower():
                return True
        return False

    def checkAllRequirements(self, giveReason = False):
        meetAll = True

        for r in self.requirements:
            meetAll = meetAll and conditions[r.name]
            if giveReason and not conditions[r.name]:
                messages.display(r.failResponse)
                messages.display("")
        return meetAll

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
                messages.display("\n")
                for scr in self.scripts.values():
                    messages.display(scr.name)

            if self.breakable :
                messages.display("\nLeave")

            messages.display("\n")

            self.getChoice(messages)

            if self.choice.lower() == "leave" and self.breakable:
                os.system('CLS')
                messages.display("------ROJO-------")
                messages.reset()
                break

            if self.scripts:
                for y in self.scripts.keys():
                    if self.choice.lower() == y.lower() and self.scripts.get(y).checkAllRequirements():
                        self = self.scripts.get(y)
                    else:
                        messages.display("Unavailable Choice")
