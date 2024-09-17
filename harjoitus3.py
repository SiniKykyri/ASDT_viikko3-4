import random
import pygame
import threading
from tkinter import Tk, Label, PhotoImage, Canvas, Button

# Alustetaan pygame
pygame.mixer.init()

#Ladataan äänet
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
# Määritellään ernestin ja kernestin osuma alueet
kernesti_osuma_alue = {
    "x_min": kernesti_x - 100,
    "x_max": kernesti_x + 100,
    "y_min": kernesti_y - 100,
    "y_max": kernesti_y + 100
}
ernestin_osuma_alue = {
    "x_min": ernesti_x - 100,
    "x_max": ernesti_x + 100,
    "y_min": ernesti_y - 100,
    "y_max": ernesti_y + 100
}

# Sanakirja osumille
osumat = {
    "Ernesti": 0,
    "Kernesti": 0
}
# Luodaan label johon voidaan tulostaa osumat
osumat_label = Label(root, text=f"Ernesti:{osumat['Ernesti']} Kernesti: {osumat['Kernesti']}")
osumat_label.pack()

# Luodaan kuvat
kernesti = canvas.create_image(kernesti_x, kernesti_y, image=kernesti_kuva)
maalitaulu = canvas.create_image(600, 350, image=maalitaulu_kuva)

#Piirretään apuviivat maalitaulu alueen helpottamiseksi
canvas.create_rectangle(
    maalitaulu_alue["x_min"],
    maalitaulu_alue["y_min"],
    maalitaulu_alue["x_max"],
    maalitaulu_alue["y_max"],
    outline="red",width=5
)
# Piirretään kernestille apuviivat
canvas.create_rectangle(
    kernesti_osuma_alue["x_min"],
    kernesti_osuma_alue["y_min"],
    kernesti_osuma_alue["x_max"],
    kernesti_osuma_alue["y_max"],
    outline="blue",width=5
)
# Luodaan funktio ernesti napille
def lisaa_ernesti():
    ernesti = canvas.create_image(ernesti_x, ernesti_y, image=ernesti_kuva)
    # Piirretään ernestille apuviivat
    canvas.create_rectangle(
    ernestin_osuma_alue["x_min"],
    ernestin_osuma_alue["y_min"],
    ernestin_osuma_alue["x_max"],
    ernestin_osuma_alue["y_max"],
    outline="green",width=5
)
# Luodaan funktio animaation suorittamiselle
def liikuta_tomaatti(tomaatti, dx, heittaja):
    def animoi():
        nonlocal tomaatti_x, tomaatti_y
        tomaatti_x, tomaatti_y = canvas.coords(tomaatti)
        if maalitaulu_alue["x_min"] <= tomaatti_x <= maalitaulu_alue["x_max"] and \
        maalitaulu_alue["y_min"] <= tomaatti_y <= maalitaulu_alue["y_max"]:
            osumat[heittaja] += 1
            print(f"Osuma! {heittaja} sai osuman!")
            play_sound(osuma_aani)
            osumat_label.config(text=f"Ernesti:{osumat['Ernesti']} Kernesti: {osumat['Kernesti']}")
            canvas.delete(tomaatti)
            canvas.create_image(tomaatti_x, tomaatti_y, image=splat_kuva)
        elif 0 <= tomaatti_x <= 1200:
            canvas.move(tomaatti, dx, 0)
            root.after(50, animoi)
    tomaatti_x, tomaatti_y = canvas.coords(tomaatti)
    animoi()

# Luodaan funktio tomaatin heittämiselle toista kohti
def heita_toista_kohti(tomaatti, dx, heittaja):
    def animoi():
        nonlocal tomaatti_x, tomaatti_y
        global splat
        if heittaja == "Ernesti":
            tomaatti_x, tomaatti_y = canvas.coords(tomaatti)
            if kernesti_osuma_alue["x_min"] <= tomaatti_x <= kernesti_osuma_alue["x_max"]  and \
            kernesti_osuma_alue["y_min"] <= tomaatti_y <= kernesti_osuma_alue["y_max"]:
                print("Ernesti osui kernestiin!")
                osumat_label.config(text= "Ernesti voitti kilpailun!")
                play_sound(osuma_aani)
                canvas.delete(tomaatti)
                canvas.create_image(tomaatti_x, tomaatti_y, image=splat_kuva)
            elif 0 <= tomaatti_x <= 1200:
                canvas.move(tomaatti, dx, 0)
                root.after(50, animoi)
        elif heittaja == "Kernesti":
            tomaatti_x, tomaatti_y = canvas.coords(tomaatti)
            if ernestin_osuma_alue["x_min"] <= tomaatti_x <= ernestin_osuma_alue["x_max"]  and \
            ernestin_osuma_alue["y_min"] <= tomaatti_y <= ernestin_osuma_alue["y_max"]:
                print("Kernesti osui ernestiin!")
                osumat_label.config(text= "Kernesti voitti kilpailun!")
                play_sound(osuma_aani)
                canvas.delete(tomaatti)
                canvas.create_image(tomaatti_x, tomaatti_y, image=splat_kuva)
            elif 0 <= tomaatti_x <= 1200:
                canvas.move(tomaatti, dx, 0)
                root.after(50, animoi)
    tomaatti_x, tomaatti_y = canvas.coords(tomaatti)
    animoi()
    
# Luodaan funktio ernesti heitolle
def ernesti_heitto():
    tomaatti = canvas.create_image(ernesti_x, ernesti_y, image=tomaatti_kuva)
    tulosero_ernesti = osumat["Ernesti"] - osumat["Kernesti"]
    print(tulosero_ernesti)
    if tulosero_ernesti > 1:
        print("ernesti heittää kohti kernestiä")
        heita_toista_kohti(tomaatti, -5, "Ernesti")
    else:
        liikuta_tomaatti(tomaatti, -5, "Ernesti")
    
# Luodaan funktio kernesti heitolle
def kernesti_heitto():
    tomaatti = canvas.create_image(kernesti_x, kernesti_y, image=tomaatti_kuva)
    tulosero_kernesti = osumat["Kernesti"] - osumat["Ernesti"]
    if tulosero_kernesti > 1:
        print("kernesti heittää kohti ernestiä")
        heita_toista_kohti(tomaatti, 5, "Kernesti")
    else:
        liikuta_tomaatti(tomaatti, 5, "Kernesti")

# Funktio jolla nollataan tulokset
def reset_tulokset():
    osumat["Ernesti"] = 0
    osumat["Kernesti"] = 0
    osumat_label.config(text=f"Ernesti:{osumat['Ernesti']} Kernesti: {osumat['Kernesti']}")
    
# Luodaan napit
ernesti_nappi= Button(root, text="Lisää ernesti", command=lisaa_ernesti)
ernesti_nappi.pack()
ernesti_heitto_nappi = Button(root, text="Ernesti heittää", command=lambda: threading.Thread(target=ernesti_heitto).start())
ernesti_heitto_nappi.pack()
kernesti_heitto_nappi = Button(root, text="Kernesti heittää", command=lambda: threading.Thread(target=kernesti_heitto).start())
kernesti_heitto_nappi.pack()
reset_tulokset_nappi = Button(root, text= "Nollaa tulokset", command=reset_tulokset)
reset_tulokset_nappi.pack()

#Käynnistä pääsilmukka
root.mainloop()

