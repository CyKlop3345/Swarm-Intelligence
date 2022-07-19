from tkinter import *
import Logic

fontText='Times 15'
F1 = 4
F2 = 1
antPhero = 1000
vaporize = 64

def settings(canvas_0):
    global canvas
    canvas = canvas_0
    interface()

def start():
    F1 = int(entryF1.get())
    F2 = int(entryF2.get())
    antPhero = int(entryAntPhero.get())
    vaporize = int(entryVaporize.get())
    Logic.start(F1, F2, antPhero, vaporize/100)

def reset():
    Logic.reset()

def interface():
    global entryF1, entryF2, entryAntPhero, entryVaporize
    labelF1 = Label(canvas, text="Factor 1:", font=fontText)
    entryF1 = Entry(canvas, width = 15)
    labelF2 = Label(canvas, text="Factor 2:", font=fontText)
    entryF2 = Entry(canvas, width = 15)
    labelAntPhero = Label(canvas, text="Ant's Pheromons:", font=fontText)
    entryAntPhero = Entry(canvas, width = 15)
    labelVaporize = Label(canvas, text="Vaporize (%):", font=fontText)
    entryVaporize = Entry(canvas, width = 15)

    butStart = Button(canvas, width = 10, height = 1, command = start, text = "Start", font = fontText)
    butReset = Button(canvas, width = 10, height = 1, command = reset, text = "Reset", font = fontText)

    entryF1.insert(END, F1)
    entryF2.insert(END, F2)
    entryAntPhero.insert(END, antPhero)
    entryVaporize.insert(END, vaporize)

    i = 0
    labelF1.grid(column=0, row=i)
    entryF1.grid(column=1, row=i)
    labelF2.grid(column=2, row=i)
    entryF2.grid(column=3, row=i)
    i += 1
    labelAntPhero.grid(column=0, row=i)
    entryAntPhero.grid(column=1, row=i)
    i += 1
    labelVaporize.grid(column=0, row=i)
    entryVaporize.grid(column=1, row=i)
    i += 1
    butStart.grid(column=0, row=i)
    i += 1
    butReset.grid(column=0, row=i)
