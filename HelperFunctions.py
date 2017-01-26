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

    def get_console_input(self):
        import libtcodpy as libtcod
        consoleInput = ""
        textCon = self.textCon
        caps = False
        while (True):
            for i in range(MessageLog.SCREEN_WIDTH):
                libtcod.console_put_char_ex(textCon, i, (self.y + self.cursor), " ", libtcod.white, libtcod.black)
                
            instr = libtcod.console_wait_for_keypress(True)
            if instr.c != 13:
                if instr.c == 0:
                    caps = True
                elif instr.c == 8:
                    consoleInput = consoleInput[0:-1]
                else:
                    if caps:
                        consoleInput += chr(instr.c).capitalize()
                    else:
                        consoleInput += chr(instr.c)
                    caps = False
                libtcod.console_print(textCon, 0, (self.y + self.cursor), consoleInput)
                libtcod.console_blit(textCon, 0, 0, MessageLog.SCREEN_WIDTH, MessageLog.SCREEN_HEIGHT, 0, 0, 0)
        
                libtcod.console_flush()
            else:
                return consoleInput

    def display(self, inStr):  
        import libtcodpy as libtcod
        textCon = self.textCon
        #from roguelite import con
        #prepare to render the GUI panel
        libtcod.console_set_default_background(textCon, libtcod.black)
        libtcod.console_set_default_foreground(textCon, libtcod.white)
        libtcod.console_clear(textCon)

        self.messages.append(inStr)
        #everytime you delete a message i could be deleting multiple lines,
        #you want to delete the log line by line
        #messages should store an individual message, and a message should store lines
        while self.cursor > MessageLog.SCREEN_HEIGHT:
                self.cursor -= len(self.messages[0])/MessageLog.SCREEN_WIDTH
                self.messages = self.messages[1:]
        i=0  
        for toDisplay in self.messages:
            libtcod.console_print(textCon, 0, (self.y + i), toDisplay)
            if (len(toDisplay)) > MessageLog.SCREEN_WIDTH:
                i += (len(toDisplay) / MessageLog.SCREEN_WIDTH)
            i += 1
        self.cursor = i+1
        #blit the contents of "con" to the root console
        libtcod.console_blit(textCon, 0, 0, MessageLog.SCREEN_WIDTH, MessageLog.SCREEN_HEIGHT, 0, 0, 0)
        
        libtcod.console_flush()

    