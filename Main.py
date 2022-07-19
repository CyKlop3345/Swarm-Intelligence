from tkinter import *
import pygame
import Logic, UI

bgColor = "gray60"

def main():
    root = Tk()

    root.title("Ку!")
    root.configure(bg=bgColor)
    root.resizable(width=False, height=False)
    canvasUI = Canvas(root, height=500, width=400, highlightthickness=0, bg=bgColor)
    canvasUI.grid(sticky=N+E+S+W, column=0, row=0)

    labelBy = Label(root, text="By: CyKlop3345", font="Times 15", bg="#EC5700", fg="White", width=15, height=1)
    labelBy.grid(sticky=E+S+W, column=0, row=1)

    screen = pygame.display.set_mode((1000,600))
    pygame.display.set_caption("Swarm intelligence")
    clock = pygame.time.Clock()
    fps = 60

    UI.settings(canvasUI)
    Logic.settings(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return()
            if Logic.mode == "setPoints" and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Logic.createPoint(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if Logic.mode != "setPoints":
                        Logic.logic()

        if Logic.mode != "setPoints":
            Logic.logic()

        try:
            root.update()
        except:
            tkon = False
        pygame.display.update()

        # clock.tick(fps)

if __name__ == "__main__":
    main()
