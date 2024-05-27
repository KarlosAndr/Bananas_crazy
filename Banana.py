import tkinter as tk
from tkinter import PhotoImage, Canvas
import ctypes,pyautogui,random

class Banana:
    def __init__(self, scene, x=0, y=0):
        self.scene = scene
        self.image = PhotoImage(file="banana.png")
        self.image = self.image.subsample(65)
        self.imagRef = scene.canvas.create_image(x, y, image=self.image)
        self.image_Bomb = PhotoImage(file="banana2.png")
        self.image_Bomb = self.image_Bomb.subsample(65)
        self.bomb_status= False

    def update(self):
        x,y = pyautogui.position()
        ban_x,ban_y = self.scene.canvas.coords(self.imagRef)
        dist = (abs(x-ban_x)+abs(y-ban_y))

        if self.bomb_status:
            self.scene.canvas.move(
                self.imagRef,
                random.choice((-30,30)),
                random.choice((-30,30))
            )
            
            self.scene.canvas.itemconfig(self.imagRef, image=self.image)

            for _ in range(10):
                self.scene.new_bananas(
                    random.randint(0,self.scene.screen_width),
                    random.randint(0,self.scene.screen_height)
                )

            self.bomb_status=False

        elif dist < 5:
            self.scene.canvas.itemconfig(self.imagRef, image=self.image_Bomb)
            self.bomb_status=True

        else:
            move_pos_ = random.randint(1,5)
            move_neg_ = random.randint(-5,-1)#fff

            self.scene.canvas.move(
                self.imagRef,
                move_pos_ if x > ban_x else move_neg_, 
                move_pos_ if y > ban_y else move_neg_
            )



class Scene:
    def __init__(self, window: tk.Tk):
        self.screen_width = window.winfo_screenwidth()
        self.screen_height = window.winfo_screenheight()
        self.canvas = Canvas(
            window,
            width=self.screen_width,
            height=self.screen_height,
            highlightthickness=0,
            bg="red"
        )
        self.canvas.pack()
        self.bananas = list()

    def update(self):
        for i in self.bananas:
            i.update()



    def new_bananas(self, x=0, y=0):
        banana = Banana(self, x, y)
        self.canvas.move(banana.imagRef, x, y)
        self.bananas.append(banana)

class Game:
    def __init__(self):
        self.window = self.create_window()
        self.scene = Scene(self.window)
        self.apply_click_through(self.window)

    def update(self):
        self.scene.update()
        self.window.after(5,self.update)#Refrezcar la scena cada 20 milisec


    def create_window(self):
        window = tk.Tk()
        window.wm_attributes("-topmost", True)
        window.wm_attributes("-fullscreen", True)
        window.overrideredirect(True)
        window.attributes("-transparentcolor", "red")
        window.config(bg="white")
        return window

    def apply_click_through(self, window):
        WS_EX_TRANSPARENT = 0x00000020
        WS_EX_LAYERED = 0x00080000
        GWL_EXSTYLE = -20

        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)

        style = style | WS_EX_TRANSPARENT | WS_EX_LAYERED
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

    def start(self):
        self.update()
        self.window.mainloop()

juego = Game()
juego.scene.new_bananas()
juego.start()
