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