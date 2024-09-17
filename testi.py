import random
import pygame
import threading
from tkinter import Tk, PhotoImage, Canvas, Button

# Alustetaan pygame
pygame.mixer.init()

# Ladataan äänet
osuma_aani = pygame.mixer.Sound("splat.wav")

# Luodaan funktio äänen soittamiselle
def play_sound(sound):
    sound.play()

# Alustetaan pääikkuna
root = Tk()
canvas = Canvas(root, width=1200, height=700)
canvas.pack()

# Tuodaan kuvat
ernesti_kuva = PhotoImage(file="erne.png")
kernesti_kuva = PhotoImage(file="kerne.png")
maalitaulu_kuva = PhotoImage(file="maalitaulu.png")
tomaatti_kuva = PhotoImage(file="tomaatti.png")
splat_kuva = PhotoImage(file="splat.png")

# Luodaan satunnaiset ernestin ja kernestin koordinaatit
kernesti_x = random.randint(50, 300)
kernesti_y = random.randint(50, 650)
ernesti_x = random.randint(900, 1150)
ernesti_y = random.randint(50, 650)

# Määritellään maalitaulun koordinaatit
maalitaulu_alue = {
    "x_min": 400,
    "x_max": 800,
    "y_min": 50,
    "y_max": 450
}

# Sanakirja osumille
osumat = {
    "Ernesti": 0,
    "Kernesti": 0
}

# Luodaan kuvat
kernesti = canvas.create_image(kernesti_x, kernesti_y, image=kernesti_kuva)
maalitaulu = canvas.create_image(600, 350, image=maalitaulu_kuva)

# Piirretään apuviivat maalitaulu alueen helpottamiseksi
canvas.create_rectangle(
    maalitaulu_alue["x_min"],
    maalitaulu_alue["y_min"],
    maalitaulu_alue["x_max"],
    maalitaulu_alue["y_max"],
    outline="red", width=5
)

# Luodaan funktio ernesti napille
def lisaa_ernesti():
    canvas.create_image(ernesti_x, ernesti_y, image=ernesti_kuva)

# Luodaan funktio osuman tarkastamiselle
def tarkista_osuma(tomaatti_x, tomaatti_y, heittaja):
    if maalitaulu_alue["x_min"] <= tomaatti_x <= maalitaulu_alue["x_max"] and \
        maalitaulu_alue["y_min"] <= tomaatti_y <= maalitaulu_alue["y_max"]:
        osumat[heittaja] += 1
        print(f"Osuma! {heittaja} sai osuman!")
        play_sound(osuma_aani)
    else:
        print(f"Ei osunut! {heittaja} ei saanut osumaa!")

# Luodaan funktio animaation suorittamiselle
def liikuta_tomaatti(tomaatti, dx, heittaja):
    def animoi():
        nonlocal tomaatti_x, tomaatti_y
        tomaatti_x, tomaatti_y = canvas.coords(tomaatti)
        if 0 <= tomaatti_x <= 1200:  # Tarkista, että tomaatti pysyy canvasin sisällä
            canvas.move(tomaatti, dx, 0)
            root.after(50, animoi)  # Päivitä tomaatin sijaintia
        else:
            # Haetaan tomaatin lopullinen sijainti
            tomaatti_coors = canvas.coords(tomaatti)
            tarkista_osuma(tomaatti_coors[0], tomaatti_coors[1], heittaja)
    tomaatti_x, tomaatti_y = canvas.coords(tomaatti)
    animoi()

# Luodaan funktio ernesti heitolle
def ernesti_heitto():
    tomaatti = canvas.create_image(ernesti_x, ernesti_y, image=tomaatti_kuva)
    liikuta_tomaatti(tomaatti, -5, "Ernesti")

# Luodaan funktio kernesti heitolle
def kernesti_heitto():
    tomaatti = canvas.create_image(kernesti_x, kernesti_y, image=tomaatti_kuva)
    liikuta_tomaatti(tomaatti, 5, "Kernesti")

# Luodaan napit
ernesti_nappi = Button(root, text="Lisää ernesti", command=lisaa_ernesti)
ernesti_nappi.pack()
ernesti_heitto_nappi = Button(root, text="Ernesti heittää", command=lambda: threading.Thread(target=ernesti_heitto).start())
ernesti_heitto_nappi.pack()
kernesti_heitto_nappi = Button(root, text="Kernesti heittää", command=lambda: threading.Thread(target=kernesti_heitto).start())
kernesti_heitto_nappi.pack()

# Käynnistä pääsilmukka
root.mainloop()