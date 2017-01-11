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
    
def get_console_input():
    import libtcodpy as libtcod
    consoleInput = ""
    caps = False
    while (True):
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
        else:
            return consoleInput

class MessageLog:
    import libtcodpy as libtcod
    
    def __init__(self, size=50, xPos=0, yPos=0):
        self.messages = []
        self.size = size
        self.x = xPos
        self.y = yPos

    def display(self, inStr):  
        import libtcodpy as libtcod
        #from roguelite import con
        SCREEN_WIDTH = 80
        SCREEN_HEIGHT = 50
        textCon = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
            #prepare to render the GUI panel
        libtcod.console_set_default_background(textCon, libtcod.black)
        libtcod.console_set_default_foreground(textCon, libtcod.white)
        libtcod.console_clear(textCon)

        self.messages.append(inStr)
        if len(self.messages) > SCREEN_HEIGHT:
            self.messages = self.messages[1:]
        i=0
        for toDisplay in self.messages:
            libtcod.console_print(textCon, 0, (self.y + i), toDisplay)
            i += 1
                
        #blit the contents of "con" to the root console
        libtcod.console_blit(textCon, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        
        libtcod.console_flush()

    