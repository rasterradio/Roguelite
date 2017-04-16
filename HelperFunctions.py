def read_grid_text(file, xRange, yRange):
    text_file = open(file, 'r')
    text_data = [["" for a in range(yRange)] for b in range(xRange)]
    x = 0
    y = 0
    for line in text_file:
        for word in line.split(';'):
            if x < xRange and y < yRange:
                text_data[x][y] = word.replace("^", "\n")

                #print file + " " + str(x) + " " + str(y) + " " + text_data[x][y]
            x += 1
        x = 0
        y += 1
    return text_data

class Message:
    def __init__(self, arr):
        self.lines = []
        self.y = 0
        self.margin = 10
        for i in range(len(arr)):
            currentLine = arr[i]

            diff = len(currentLine) - (MessageLog.SCREEN_WIDTH + self.margin)
            newLines = []
            while (True):
                if (diff <= 0):
                    newLines.append(currentLine)
                    break

    #What Happens here??? Should we add a null term char? or a newline char?
                newLines.append(currentLine[:MessageLog.SCREEN_WIDTH])
                currentLine = currentLine[-diff:]
                diff = len(currentLine) - MessageLog.SCREEN_WIDTH
            self.lines += newLines

    def getHeight(self):
        return len(self.lines)

    def rmLine(self):
        self.lines = self.lines[:-1]

class MessageLog:
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    def __init__(self, size=50, xPos=0, yPos=0):
        import libtcodpy as libtcod
        self.messages = []
        self.size = size
        self.x = xPos
        self.y = yPos
        self.cursor = yPos

        self.textCon = libtcod.console_new(MessageLog.SCREEN_WIDTH, MessageLog.SCREEN_HEIGHT)

    def reset(self):
        self.cursor = self.y
        self.messages = []

    def get_console_input(self):
        import libtcodpy as libtcod
        key = libtcod.Key()
        mouse = libtcod.Mouse()
        consoleInput = ""
        textCon = self.textCon
        caps = False

        libtcod.mouse_show_cursor(True)
        while (True):
            libtcod.sys_check_for_event(libtcod.EVENT_MOUSE,None,mouse)
            mouseStat = mouse

            if(mouseStat.lbutton_pressed):
                for element in self.messages:
                    for i in range(element.getHeight()):
                        if  (element.y + i == mouseStat.cy):
                            return element.lines[i]

            instr = key
            if instr.vk == libtcod.KEY_NONE:
                continue

            for i in range(MessageLog.SCREEN_WIDTH):
                libtcod.console_put_char_ex(textCon, i, (self.y + self.cursor), " ", libtcod.white, libtcod.black)

            if instr.c != 13:
                if instr.c == 0:
                    caps = True
                elif instr.c == 8:
                    consoleInput = consoleInput[0:-1]
                else:
                    if instr.c < 123:
                        if caps:
                            consoleInput += chr(instr.c).capitalize()
                        else:
                            consoleInput += chr(instr.c)

                libtcod.console_print(textCon, 0, (self.y + self.cursor), consoleInput)
                libtcod.console_blit(textCon, 0, 0, MessageLog.SCREEN_WIDTH, MessageLog.SCREEN_HEIGHT, 0, 0, 0)

                libtcod.console_flush()
            else:
                libtcod.mouse_show_cursor(False)
                return consoleInput

            caps = False

    def display(self, inStr):
        import libtcodpy as libtcod
        textCon = self.textCon

        #prepare to render the GUI panel
        libtcod.console_set_default_background(textCon, libtcod.black)
        libtcod.console_set_default_foreground(textCon, libtcod.white)
        libtcod.console_clear(textCon)

        newMessage = Message(inStr.splitlines())

        newY = 0
        for elem in self.messages:
            newY += elem.getHeight()
        newMessage.y = newY
        self.messages.append(newMessage)
        #everytime you delete a message i could be deleting multiple lines,
        #you want to delete the log line by line
        #messages should store an individual message, and a message should store lines
        while self.cursor > MessageLog.SCREEN_HEIGHT:
                for each in self.messages:
                    each.y -= self.messages[0].getHeight()
                self.cursor -= self.messages[0].getHeight()
                self.messages = self.messages[1:]
        i=0
        for toDisplay in self.messages:
            for strin in toDisplay.lines:
                libtcod.console_print(textCon, toDisplay.margin/2, (self.y + i), strin)
                i += 1
        self.cursor = i+1
        #blit the contents of "con" to the root console
        libtcod.console_blit(textCon, 0, 0, MessageLog.SCREEN_WIDTH, MessageLog.SCREEN_HEIGHT, 0, 0, 0)

        libtcod.console_flush()
