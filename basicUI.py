from tkinter import *
import spotify

window = Tk()
window.title('Spotify Song Suggestions From Face Emotions')
window.geometry('500x250')
window.configure(background='white')
window.maxsize(500, 250)
window.minsize(500, 250)

label = Label(text="Press the button below to listen the suggested playlist", padx=20, pady=20, fg="black", bg="white")
label.config(font=("Roboto", 14, 'bold'))
label.pack()

button = Button(window, text="Start", command=spotify.run)
button.pack()
button.config(font=('Roboto', 20, 'bold'))
button.config(background='red')
button.config(fg='white')
button.place(x=200, y=100)

window.mainloop()
