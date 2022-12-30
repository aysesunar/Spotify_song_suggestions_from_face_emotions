from tkinter import *
import spotify
from PIL import ImageTk, Image

def on_enter(e):
    button['background'] = 'green'

def on_leave(e):
    button['background'] = 'SystemButtonFace'

def center(toplevel):
    toplevel.update_idletasks()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

    toplevel.geometry("+%d+%d" % (x, y))
    toplevel.title("")

window = Tk()
window.title('Spotify Song Suggestions From Face Emotions')
window.geometry('350x400')
window.configure(background='white')
window.maxsize(350, 400)
window.minsize(350, 400)

# Add image to background:
background_image = Image.open("UI_background_image/3.jpg")
img2 = background_image.resize((350,400))
img = ImageTk.PhotoImage(img2)
label = Label(window,image=img)
label.pack(side='top',fill=Y,expand=True)


label = Label(text="Press the button below to listen the suggested playlist", padx=20, pady=20, fg="black", bg="white")
label.config(font=("Roboto", 14, 'bold'))
label.pack()


button = Button(window, text="Start", compound="center", height= 110, borderwidth=0, width=180, command=spotify.run)
button.pack()
button.config(font=('Roboto', 20, 'bold'))
button.config(background='white')
button.config(fg='white')
button.place(relx=0.5, rely=0.5, anchor='center')

original = Image.open('UI_background_image/button1.jpg')
original = original.resize((180,110), Image.ANTIALIAS)
ph_im = ImageTk.PhotoImage(original) # <----------
button.config(image=ph_im)
button.config(text="Play!")

button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)

# arka plan resim
# button resim
# button size

center(window)
#window.overrideredirect(True)
window.mainloop()

# Image by <a href="https://www.freepik.com/free-vector/white-abstract-background_12066098.htm#query=minimalist%20background&position=2&from_view=keyword">Freepik</a>
# Image by <a href="https://www.freepik.com/free-vector/hand-drawn-psychedelic-colorful-background_17807024.htm#query=colorful&position=0&from_view=keyword">Freepik</a>