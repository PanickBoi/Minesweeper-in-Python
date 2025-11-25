import tkinter as tk
import random
cellSize = 20  # px
map_sizes = {  # X | Y
    "S": (16, 16),
    "M": (24, 24),
    "L": (32, 32),
    "XL": (64, 32),
}

difficulty = {
    "E": 20 / 100,
    "M": 40 / 100,
    "H": 55 / 100,
}
directions={ # x | Y
    "N" : [0,1],
    "NE" : [1,1],
    "E" : [1,0],
    "SE" : [1,-1],
    "S" : [0,-1],
    "SW" : [-1,-1],
    "W" : [-1,0],
    "NW" : [-1,1],
    }


class Game:
    def __init__(self, ms=map_sizes["S"], diff=difficulty["E"]):
        self.dimensions = ms
        self.difficulty = diff
        self.Map = []
        self.mineCount = 0
    def startGame(self,parent,mainframe,cords):
        x,y = self.dimensions[0],self.dimensions[1]
        self.mineCount = int((x*y)*self.difficulty)
        print("Num of mines:",self.mineCount)
        while self.mineCount > 0:
            for X in range(x):
                for Y in range(y):
                    cell = self.Map[X][Y]
                    if cell[0] != 0:
                        chance = random.random()
                        if chance <= self.difficulty:
                            cell[0] = 10
                            self.mineCount -=1
                        else:
                            minesNear = 0
                            if 0 < X < x-1 and 0 < Y < y-1:
                               for direction,cords in directions.items():
                                   dirX = cords[0]
                                   dirY = cords[1]
                                   checkCord = self.Map[X+dirX][Y+dirY]
                                   if checkCord[0]== 10:
                                       minesNear+=1
                            if minesNear > 0:
                                cell[0] = minesNear
                            else:
                                cell[1].destroy()
                            cell[1].config(text=str(minesNear))
    def createMap(self, parent,mainframe):
        cols, rows = self.dimensions
        for x in range(cols):
            self.Map.append([])
            for y in range(rows):
                # default state
                state = -1

                # pixel position of each cell
                px = x * cellSize
                py = y * cellSize
            
                # create cell button
                cell = CellButton(parent, state, px, py, cellSize)
                mainframe.game.Map[x].append([state,cell])

class CellButton(tk.Button):
    def __init__(self, parent, state, x, y, size):
        super().__init__(parent)

        self.state = state
        self.parent = parent
        # Use ONLY PLACE → pixel exact
        self.place(x=x, y=y, width=size, height=size)

        # Mouse bindings
        self.bind("<Button>",self.click)

    def click(self,event):
        pos = self.get_position()
        print(pos)
        game = self.parent.mainframe.game
        cellData = game.Map[pos[0]][pos[1]]
        if event.num == 1:
            print("LEFT CLICK")
            if self.parent.mainframe.game.mineCount == 0:
               cellData[0] = 0
               cellData[1].destroy()
               game.startGame(self.parent,self.parent.mainframe,pos)
        elif event.num==2:
            print("MIDDLE CLICK")
        else:
            print("RIGHT CLICK")
        
        print(cellData)

    def get_position(self):
        """Get pixel coordinates relative to main window."""
        x = int(self.winfo_x()/cellSize)
        y = int(self.winfo_y()/cellSize)
        return (x, y)


class MainFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        S = input("Map Size (S/M/L/XL): ")
        D = input("Difficulty (E/M/H): ")

        self.game = Game(map_sizes[S], difficulty[D])
        cols, rows = self.game.dimensions

        # Calculate exact pixel window size
        width = cols * cellSize
        height = rows * cellSize

        # Apply exact window size
        parent.geometry(f"{width}x{height}")
        parent.resizable(False, False)

        # Create cells AFTER resizing
        self.game.createMap(parent,self)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minesweeper")
        self.mainframe = MainFrame(self)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
