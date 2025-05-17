import pyxel, random

class Jeu():
    def __init__(self) :

        pyxel.init(256,192, fps= 60, title= "SpaceRun")

        pyxel.load("niveau0.pyxres")

        #menu du jeux
        self.niveau = 0
        self.entre = 0
        self.sortie = 0

        #règle du jeux
        self.pv = 100
        self.pvvaisseau = 100
        self.rev = 180
        self.batt = 100
        self.point = 0
        self.anim = 0
        self.temps = 0

        #vaisseau
        self.vaisseau_x = 124
        self.vaisseau_y = 200
        self.changement = False

        #temps de recharge des att
        self.tdr = [600, 300, 420]

        #tirs
        self.ltir = []
        self.acttir2 = 0
        self.ttir2 = []

        #laser
        self.llaser = [False, 0, 0, []]
        self.animlaser = 0
        self.artlaser = 0

        #bouclier
        self.lbouclier = False
        self.animbouclier = 0
        self.artbouclier = 0

        #ennemis
        self.lennemi = []
        self.appennemi1 = [60, 0]
        self.appennemi2 = [60, 0]
        self.appennemi3 = [60, 0]

        #chasseurs
        self.tirchasseur = [0,0]
        self.lchasseur = []
        self.appchasseur1 = [60, 0]

        #rayon
        self.rayon1 = [False, 0, 360, 0, 180, 112, 0, 0]
        self.rayon2 = [False, 0, 360, 0, 180, 80, 0, 0]

        #bonus
        self.lbonus = []
        self.attbonus1 = 0
        self.appbonus1 = 0
        self.appbonus = [[0, 240], [0, 600]]

        pyxel.run(self.update, self.draw)

    def demarage(self):
        if pyxel.mouse_x > 103 and pyxel.mouse_x < 152 and pyxel.mouse_y > 79  and pyxel.mouse_y < 112:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.niveau += 1
                if self.niveau == 1:
                    pyxel.load("niveau1.pyxres")
                if self.niveau == 2:
                    pyxel.load("niveau2.pyxres")
                self.entre = 0
                self.sortie = 0
                self.vaisseau_y = 200
                self.pv = 100
                self.pvvaisseau = 100
                self.point = 0
                if self.temps >= 63:
                    self.temps = 0

    #début et fin du jeux
    def debut(self):
        if self.entre <120:
            self.entre += 1
            self.vaisseau_y -= 0.5

    def fin(self):
        if self.temps >=63:
            self.lennemi = []
            self.lchasseur = []
            self.lbonus = []
            self.rayon1[0] = False
            self.rayon2[0] = False
            self.rayon1[1] = 0
            self.rayon2[1] = 0
            self.lbouclier = False
            self.llaser[0] = False
            if self.sortie < 210:
                self.sortie += 1
                self.vaisseau_y -= 1
            if self.sortie >= 210:
                self.demarage()

    #mouvement du vaisseau
    def deplacement(self):
        if pyxel.btnp(pyxel.KEY_A):
            if self.changement == False:
                self.changement = True
            else:
                self.changement = False
        if self.pvvaisseau > 0:
            if self.changement == False:
                if pyxel.btn(pyxel.KEY_SHIFT):
                    s = 3
                else:
                    s = 0
                if pyxel.btn(pyxel.KEY_LEFT) and self.vaisseau_x > 0:
                    self.vaisseau_x -= 1 + s
                if pyxel.btn(pyxel.KEY_RIGHT) and self.vaisseau_x < 232:
                    self.vaisseau_x += 1 + s
                if pyxel.btn(pyxel.KEY_UP) and self.vaisseau_y > 0:
                    self.vaisseau_y -= 1 + s
                if pyxel.btn(pyxel.KEY_DOWN) and self.vaisseau_y < 168:
                    self.vaisseau_y += 1 + s
            if self.changement == True:
                self.vaisseau_x = pyxel.mouse_x
                self.vaisseau_y = pyxel.mouse_y

        if self.pvvaisseau <= 0:
            if pyxel.frame_count % 1 == 0:
                self.rev -= 1
            if self.rev <= 0:
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.rev = 180
                    self.pvvaisseau = 100
                    self.batt = 30
                    self.vaisseau_x = 124
                    self.vaisseau_y = 140

    #batterie et attaque
    def energie(self):
        if self.batt <= 98:
            if pyxel.frame_count % 105 == 0:
                self.batt += 5
        for t in range(len(self.tdr)):
            if pyxel.frame_count % 1 == 0:
                self.tdr[t] -= 1

    #attaque de tir
    def tir(self):
        if self.pvvaisseau > 0:

            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if self.batt >= 5:
                    self.ltir.append([self.vaisseau_x + random.randint(11,12), self.vaisseau_y, random.randint(0,2), 1])
                    self.batt -= 5

            if self.batt >= 50:
                if pyxel.btnp(pyxel.KEY_Q):
                    if self.tdr[1] <= 0:
                        self.acttir2 = True
                        self.batt -= 50
                        self.ttir2.append([0])
                        self.tdr[1] = 300
            if self.acttir2 == True:
                for tir in self.ttir2:
                    if pyxel.frame_count % 1 == 0:
                        tir[0] += 1
                    if tir[0] == 1:
                        self.ltir.append([self.vaisseau_x + 4, self.vaisseau_y + 7, random.randint(3, 3), 2])
                        self.ltir.append([self.vaisseau_x + 19, self.vaisseau_y + 7, random.randint(3, 3), 2])
                    if tir[0] == 11:
                        self.ltir.append([self.vaisseau_x + 4, self.vaisseau_y + 7, random.randint(3, 3), 2])
                        self.ltir.append([self.vaisseau_x + 19, self.vaisseau_y + 7, random.randint(3, 3), 2])
                    if tir[0] == 21:
                        self.ltir.append([self.vaisseau_x + 4, self.vaisseau_y + 7, random.randint(3, 3), 2])
                        self.ltir.append([self.vaisseau_x + 19, self.vaisseau_y + 7, random.randint(3, 3), 2])
                        self.ttir2.remove(tir)
                if self.ttir2 == []:
                    self.acttir2 = False


        for tir in self.ltir :
            if tir[3] ==1:
                tir[1] -= 2
                if tir[1] < 0 :
                    self.ltir.remove(tir)

            if tir[3] ==2:
                tir[1] -= 1
                tir[1] -= 1
                tir[1] -= 1
                tir[1] -= 1
                tir[1] -= 1
                if tir[1] < 0 :
                    self.ltir.remove(tir)

            if tir[3] ==3:
                tir[1] += 1
                if self.vaisseau_x+24 >= tir[0] and self.vaisseau_x <= tir[0]+1 and self.vaisseau_y+24 >= tir[1] and self.vaisseau_y <= tir[1]+3:
                    self.ltir.remove(tir)
                    if self.lbouclier == False:
                        self.pvvaisseau -= 10
                if tir[1] < 0 :
                    self.ltir.remove(tir)

            if tir[3] ==4:
                tir[1] += 0.5
                if self.vaisseau_y+10 <= tir[1]:
                    self.ltir.append([tir[0]-21, tir[1]-21, 12, 5, [0, 0], 0])
                    self.ltir.remove(tir)

            if tir[3] ==5:
                if pyxel.frame_count % 1 == 0:
                    tir[4][0] += 1
                    tir[5] += 3
                if tir[4][0] == 150:
                    self.ltir.remove(tir)
                if tir[5] == 360:
                    tir[5] = 0
                if self.vaisseau_x + 24 >= tir[0] and self.vaisseau_x <= tir[0]+49 and self.vaisseau_y + 24 >= tir[1] and self.vaisseau_y <= tir[1] + 49:
                    if self.lbouclier == False:
                        tir[4][1] += 1
                        if tir[4][1] >= 10:
                            tir[4][1] = 0
                            self.pvvaisseau -= 5
    #attaque laser
    def laser(self):
        if self.pvvaisseau > 0:
            if pyxel.btnp(pyxel.KEY_Z):
                if self.tdr[0] <= 0:
                    if self.llaser[0] == True:
                        self.artlaser = 0
                    if self.batt >= 30:
                        self.llaser[0] = True
                        self.batt -= 30
                    self.tdr[0] = 600
            if self.llaser[0] == True :
                self.animlaser += 1
                if self.animlaser >= 10:
                    self.animlaser = 0
                    self.artlaser += 1
                if self.artlaser >= 12:
                    self.llaser[0] = False
                    self.llaser[2] = 0
                    self.llaser[3] = []
                    self.artlaser = 0

    #attaque bouclier
    def bouclier(self):
        if self.pvvaisseau > 0:
            if pyxel.btnp(pyxel.KEY_S):
                if self.tdr[2] <= 0:
                    if self.lbouclier == True:
                        self.artbouclier = 0
                    if self.batt >= 40:
                        self.lbouclier = True
                        self.batt -= 40
                    self.tdr[2] = 420
            if self.lbouclier == True :
                self.animbouclier += 1
                if self.animbouclier >= 20:
                    self.animbouclier = 0
                    self.artbouclier += 1
                if self.artbouclier >= 9:
                    self.lbouclier = False
                    self.artbouclier = 0

    #si l'ennemi est touché par une attaque ou le vaisseau
    def elimination(self, ennemis: list, tirs: list):
        for ennemi in ennemis :
            for tir in tirs :
                if tir[0] >= ennemi[0] and tir[0] <= ennemi[0]+ennemi[8] and tir[1] >= ennemi[1] and tir[1] <= ennemi[1]+ennemi[8]/2 :
                    if tir[3] == 1:
                        tirs.remove(tir)
                        ennemi[2] -= 100
                    if tir[3] == 2:
                        ennemi[2] -= 100

            if self.llaser[0] == True:
                if self.vaisseau_x + 10 < ennemi[0] + ennemi[8]-1 and self.vaisseau_x + 13 > ennemi[0] and self.vaisseau_y > ennemi[1]:
                    if ennemi not in self.llaser[3]:
                        self.llaser[3].append(ennemi)
                if self.vaisseau_x + 10 >= ennemi[0] + ennemi[8]-1 or self.vaisseau_x + 13 <= ennemi[0]:
                    if ennemi in self.llaser[3]:
                        self.llaser[3].remove(ennemi)
                        self.llaser[2] = 0
                for enn in self.llaser[3]:
                    if self.llaser[2] < enn[8] / 2 + enn[1]:
                        self.llaser[2] = enn[8] / 2 + enn[1]
                    if self.llaser[2] <= enn[8] / 2 + enn[1] + 1:
                        if pyxel.frame_count % 1 == 0:
                            self.llaser[1] += 1
                        if self.llaser[1] >= 6:
                            enn[2] -= 25
                            self.llaser[1] = 0
                    if enn[2] <= 0 or self.vaisseau_y <= enn[1]:
                        self.llaser[3].remove(enn)
                        self.llaser[2] = 0
                if self.llaser[3] == []:
                    self.llaser[2] = 0

            if self.pvvaisseau > 0:
                if self.vaisseau_x+24 >= ennemi[0] and self.vaisseau_x <= ennemi[0]+ennemi[8] and self.vaisseau_y+24 >= ennemi[1] and self.vaisseau_y <= ennemi[1]+ennemi[8]:
                    if self.lbouclier == True:
                        ennemi[2] -= 10000
                    else:
                        if ennemis == self.lbonus:
                            if ennemi[9] == 2 :
                                ennemi[2] -= 10000
                            else:
                                if ennemi in ennemis:
                                    ennemis.remove(ennemi)
                        else:
                            if ennemi in ennemis:
                                ennemis.remove(ennemi)
                            self.pvvaisseau -= ennemi[3]
                            self.point += ennemi[4]


    #apparition d'ennemi
    def appennemi(self, app, liste, x, y, pv, deg, point, t1, t2, v, taille, n):
        if pyxel.frame_count % 1 == 0:
            app[1] += 1
        if app[1] >= app[0]:
            liste.append([x, y, pv, deg, point, t1, t2, v, taille, n, 0])
            app[1] = 0
            app[0] = random.randint(t1, t2)

    def ennemi(self, liste):
        for ennemi in liste :
            #vaisseau ennemi
            ennemi[1] += ennemi[7]
            self.elimination(liste, self.ltir)
            if ennemi[9] == 3:
                if ennemi[2] <= 0:
                    if ennemi in liste:
                        liste.remove(ennemi)
                    self.point += ennemi[4]

                if ennemi[1] > 192 :
                    liste.remove(ennemi)

                if ennemi[0] <= self.vaisseau_x:
                    ennemi[0] += 1
                if ennemi[0] >= self.vaisseau_x+15:
                    ennemi[0] -= 1
                if ennemi[1] >= self.vaisseau_y+24:
                    ennemi[1] -= 0.5
            else:
                if ennemi[2] <= 0:
                    if ennemi in liste:
                        liste.remove(ennemi)
                    self.point += ennemi[4]
                    if ennemi[9] == 1:
                        self.appennemi1[1] += ennemi[6] - ennemi[5]

                if ennemi[1] > 192 :
                    self.pv -= ennemi[3]
                    liste.remove(ennemi)

    def chasseur(self, liste):
        for ennemi in liste :
            #chasseur
            self.elimination(liste, self.ltir)
            if ennemi[1] < 12:
                ennemi[1] += ennemi[7]
            if ennemi[1] >= 12:
                if ennemi[9] == 1:
                    if pyxel.frame_count % 1 == 0:
                        self.tirchasseur[0] += 1
                    if self.tirchasseur[0] >= 60:
                        self.ltir.append([ennemi[8] / 2 + ennemi[0] -1, ennemi[1] + ennemi[8] - 2, 8, 3])
                        self.tirchasseur[0] = 0
                    if pyxel.frame_count % 2 == 0:
                        if self.vaisseau_x > ennemi[0]:
                            ennemi[0] += 1
                        if self.vaisseau_x < ennemi[0]:
                            ennemi[0] -= 1

                if ennemi[9] == 2:
                    if pyxel.frame_count % 1 == 0:
                        self.tirchasseur[1] += 1
                    if self.tirchasseur[1] >= 180 and self.vaisseau_x == ennemi[0]:
                        self.ltir.append([ennemi[8] / 2 + ennemi[0] -1, ennemi[1] + ennemi[8] - 4, 8, 4])
                        self.tirchasseur[1] = 0
                    if ennemi[10] == 0:
                        ennemi[0] += 1
                    if ennemi[10] == 1:
                        ennemi[0] -= 1
                    if ennemi[0] <= 0:
                        ennemi[10] = 0
                    if ennemi[0] + ennemi[8] -1 >= 255:
                        ennemi[10] = 1


            if ennemi[2] <= 0:
                if ennemi in liste:
                    liste.remove(ennemi)
                if ennemi[9] == 3:
                    self.tirchasseur[2] = 0
                self.point += ennemi[4]
                self.appchasseur1[1] += ennemi[6] - ennemi[5]

    #rayon ennemi
    def rayon(self, rayon, deg):
        rayon[7] += 1
        if rayon[7] == 12:
            rayon[7] = 0
        if rayon[0] == False:
            if pyxel.frame_count % 1 == 0:
                rayon[1] += 1
            if rayon[1] == rayon[2] - 60:
                if rayon == self.rayon1:
                    if self.vaisseau_x < 12:
                        rayon[5] = 0
                    if self.vaisseau_x >= 224:
                        rayon[5] = 224
                    if self.vaisseau_x >= 12 and self.vaisseau_x < 224 :
                        rayon[5] = random.randint(self.vaisseau_x - 12, self.vaisseau_x)
                if rayon == self.rayon2:
                    if self.vaisseau_y < 12:
                        rayon[5] = 0
                    if self.vaisseau_y >= 160:
                        rayon[5] = 160
                    if self.vaisseau_y >= 12 and self.vaisseau_y < 160 :
                        rayon[5] = random.randint(self.vaisseau_y - 12, self.vaisseau_y)
            if rayon[1] >= rayon[2]:
                rayon[0] = True
                rayon[1] = 0
                rayon[2] = random.randint(300,420)

        if rayon[0] == True:
            if pyxel.frame_count % 1 == 0:
                rayon[3] += 1
            if rayon == self.rayon1:
                if self.vaisseau_x+23 >= rayon[5] and self.vaisseau_x <= rayon[5]+31:
                    if rayon[6] == 0:
                        if self.lbouclier == False and self.pvvaisseau > 0:
                            self.pvvaisseau -= deg
                        rayon[6] = 6
                    if pyxel.frame_count % 1 == 0:
                        rayon[6] -= 1
                if rayon[3] >= rayon[4]:
                    rayon[0] = False
                    rayon[3] = 0

            if rayon == self.rayon2:
                if self.vaisseau_y + 23 >= rayon[5] and self.vaisseau_y <= rayon[5] + 31:
                    if rayon[6] == 0:
                        if self.lbouclier == False and self.pvvaisseau > 0:
                            self.pvvaisseau -= deg
                        rayon[6] = 6
                    if pyxel.frame_count % 1 == 0:
                        rayon[6] -= 1
                if rayon[3] >= rayon[4]:
                    rayon[0] = False
                    rayon[3] = 0

    def bonus(self, apparition, liste, n):
        for app in range(len(apparition)):
            if pyxel.frame_count % 1 == 0:
                apparition[app][0] += 1
            if apparition[app][0] >= apparition[app][1]:
                if app == 0 and n == 1:
                    liste.append([random.randint(0, 248), -8, 100, 30, 50, 0, 0, 0.5, 8, n])
                    apparition[app][0] = 0
                    apparition[app][1] = random.randint(300, 420)
                if app == 1 and n == 2:
                    liste.append([random.randint(0, 248), -8, 100, 15, 50, 0, 0, 0.5, 8, n])
                    apparition[app][0] = 0
                    apparition[app][1] = 600

        for bonus in liste :
            self.elimination(liste, self.ltir)
            if bonus[9] == 1:
                bonus[1] += 0.5
                if bonus[2] <= 0:
                    if bonus in liste:
                        liste.remove(bonus)
                    self.batt += bonus[3]
                    self.point += bonus[4]
                if bonus[1] > 192 :
                    liste.remove(bonus)

            if bonus[9] == 2:
                bonus[1] += 0.5
                if bonus[2] <= 0:
                    if bonus in liste:
                        liste.remove(bonus)
                    self.batt += bonus[3]
                    self.point += bonus[4]
                if bonus[1] > 192 :
                    liste.remove(bonus)

    def update(self) :
        if pyxel.frame_count % 1 == 0:
            self.anim += 1
        if self.anim >= 60:
            self.anim = 0

        if self.niveau == 0:
            self.demarage()

        if self.niveau == 1:
            self.debut()
            self.fin()
            if self.entre >=120:
                if self.pv > 0:

                    self.tir()

                    if self.temps <63:
                        if pyxel.frame_count % 120 == 0:
                            self.temps += 1.5
                        self.energie()
                        self.deplacement()
                        self.ennemi(self.lennemi)
                        self.chasseur(self.lchasseur)
                        self.appennemi(self.appennemi1, self.lennemi, random.randint(0, 240), -16, 100, 10, 100, 90, 150, 0.5, 16, 1)
                        if self.point >= 1000:
                            self.bonus(self.appbonus, self.lbonus, 1)
                            self.appennemi(self.appennemi2, self.lennemi, random.randint(0, 224), -32, 500, 30, 500, 210, 300, 0.25, 32, 2)
                            self.laser()
                        if self.point >= 2000:
                            self.bonus(self.appbonus, self.lbonus, 2)
                            self.rayon(self.rayon1, 2)
                            self.rayon(self.rayon2, 2)
                            self.bouclier()
                        if self.point >= 4000:
                            if len(self.lchasseur) < 1:
                                self.appennemi(self.appchasseur1, self.lchasseur, random.randint(0, 232), -24, 300, 30, 250, 360, 420,0.5, 24, 1)

        if self.niveau == 2:
            self.debut()
            self.fin()
            if self.entre >=120:
                if self.pv > 0:

                    self.tir()

                    if self.temps <63:
                        if pyxel.frame_count % 120 == 0:
                            self.temps += 1.5
                        self.energie()
                        self.deplacement()
                        self.ennemi(self.lennemi)
                        self.chasseur(self.lchasseur)
                        self.appennemi(self.appennemi1, self.lennemi, random.randint(0, 240), -24, 100, 10, 100, 90, 150, 0.5, 16, 1)
                        if self.point >= 1000:
                            self.bonus(self.appbonus, self.lbonus, 1)
                            if len(self.lchasseur) < 1:
                                self.appennemi(self.appchasseur1, self.lchasseur, random.randint(0, 232), -24, 200, 30, 250,360, 420, 0.5, 24, 2)
                            self.laser()
                        if self.point >= 3000:
                            self.appennemi(self.appennemi2, self.lennemi, random.randint(0, 224), -32, 500, 30, 500,300, 420, 0.25, 32, 2)
                            self.appennemi(self.appennemi3, self.lennemi, random.randint(0, 252), -8, 100, 5, 50,60, 120, 1, 8, 3)
                            self.bonus(self.appbonus, self.lbonus, 2)
                            self.bouclier()
                        if self.point >= 5000:
                            self.appennemi(self.appchasseur1, self.lchasseur, random.randint(0, 232), -24, 200, 30, 250,360, 420, 0.5, 24, 2)

    def draw(self):
        pyxel.cls(0)
        if self.niveau == 0:
            pyxel.blt(0, 0, 0, 0, 0, 256, 192)
            pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 1, 1, 7)
            pyxel.text(118, 93, "Jouer", 7,)
        if self.niveau != 0:
            pyxel.blt(0, 0, 2, 0, 64 - self.temps, 256, 193)
            pyxel.text(0, 0, str(self.pv), 7)
            pyxel.text(0, 186, str(self.batt), 7)
            pyxel.text(232, 186, str(self.point), 7)
            pyxel.text(self.vaisseau_x + 7, self.vaisseau_y + 24, str(self.pvvaisseau), 7)
            if self.temps >= 63:
                pyxel.text(110, 93, "Continuer", 7)
                pyxel.rectb(104, 80, 47, 31, 7)

        if self.pvvaisseau > 0:
            if self.anim >= 30 :
                pyxel.blt(self.vaisseau_x, self.vaisseau_y, 0, 0, 0, 24, 24, 0)
            if self.anim < 30 :
                pyxel.blt(self.vaisseau_x, self.vaisseau_y, 0, 24, 0, 24, 24, 0)

        if self.lbouclier == True :
            pyxel.blt(self.vaisseau_x - 2, self.vaisseau_y - 2, 0, 6, 38, 28, 28, 0)

        for tir in self.ltir :
            if tir[3] == 3:
                pyxel.blt(tir[0], tir[1], 0, tir[2], 24, 2, 4, 0)
            if tir[3] == 4:
                if self.anim >= 30 :
                    pyxel.blt(tir[0], tir[1], 0, 12, 24, 4, 4, 7)
                if self.anim < 30 :
                    pyxel.blt(tir[0], tir[1], 0, 16, 24, 4, 4, 7)
            if tir[3] == 5:
                pyxel.blt(tir[0], tir[1], 0, 0, 72, 50, 50, 10, self.anim * 6)
            if tir[3] == 1 or tir[3] == 2:
                pyxel.blt(tir[0], tir[1], 0, tir[2], 24, 1, 4)

        if self.llaser[0] == True :
            if self.animlaser >= 5:
                pyxel.blt(self.vaisseau_x+11, self.llaser[2], 0, 254, 0, 2, self.vaisseau_y - self.llaser[2], 0)
            if self.animlaser < 5:
                pyxel.blt(self.vaisseau_x + 11, self.llaser[2], 0, 252, 0, 2, self.vaisseau_y - self.llaser[2], 0)
            if self.animlaser == random.randint(0, 4) :
                pyxel.blt(self.vaisseau_x + 11, self.llaser[2], 0, 250, 0, 2, self.vaisseau_y - self.llaser[2], 0)
            if self.animlaser == random.randint(5, 9):
                pyxel.blt(self.vaisseau_x + 11, self.llaser[2], 0, 248, 0, 2, self.vaisseau_y - self.llaser[2], 0)

        for ennemi in self.lennemi:
            if ennemi[9] == 1:
                if self.anim >= 30:
                    pyxel.blt(ennemi[0], ennemi[1], 1, 0, 0, 16, 16, 0)
                if self.anim < 30:
                    pyxel.blt(ennemi[0], ennemi[1], 1, 16, 0, 16, 16, 0)
            if ennemi[9] == 2:
                if self.anim >= 30:
                    pyxel.blt(ennemi[0], ennemi[1], 1, 0, 16, 32, 32, 0)
                if self.anim < 30:
                    pyxel.blt(ennemi[0], ennemi[1], 1, 32, 16, 32, 32, 0)
            if ennemi[9] == 3:
                pyxel.blt(ennemi[0]-4, ennemi[1]-4, 1, 0, 136, 16, 16, 1, self.anim * 6)

        for chasseur in self.lchasseur:
            if chasseur[9] == 1:
                pyxel.blt(chasseur[0], chasseur[1], 1, 0, 88, 24, 24, 0)
            if chasseur[9] == 2:
                pyxel.blt(chasseur[0], chasseur[1], 1, 0, 112, 24, 24, 0)

        for bonus in self.lbonus :
            if bonus[9] == 1:
                pyxel.blt(bonus[0], bonus[1], 1, 0, 80, 8, 8, 0)
            if bonus[9] == 2:
                pyxel.blt(bonus[0], bonus[1], 1, 8, 80, 8, 8, 0)

        if self.rayon1[0] == False:
            if self.rayon1[1] >= self.rayon1[2] - 60:
                if self.rayon2[7] < 6:
                    pyxel.blt(self.rayon1[5], self.vaisseau_y - 4, 1, 0, 48, 32, 32, 1)
                    pyxel.rect(self.rayon1[5], 0, 1, 192, 0)
                    pyxel.rect(self.rayon1[5]+1, 0, 1, 192, 10)
                    pyxel.rect(self.rayon1[5]+31, 0, 1, 192, 10)
                    pyxel.rect(self.rayon1[5]+32, 0, 1, 192, 0)
                else:
                    pyxel.blt(self.rayon1[5], self.vaisseau_y - 4, 1, 32, 48, 32, 32, 1)
                    pyxel.rect(self.rayon1[5], 0, 1, 192, 8)
                    pyxel.rect(self.rayon1[5] + 1, 0, 1, 192, 7)
                    pyxel.rect(self.rayon1[5] + 31, 0, 1, 192, 7)
                    pyxel.rect(self.rayon1[5] + 32, 0, 1, 192, 8)

        if self.rayon1[0] == True:
            if self.rayon1[7] < 3:
                pyxel.blt(self.rayon1[5], 0, 1, 224, 0, 32, 192)
            if self.rayon1[7] >= 3 and self.rayon2[7] < 6:
                pyxel.blt(self.rayon1[5], 0, 1, 224, 8, 32, 192)
                pyxel.blt(self.rayon1[5], 184, 1, 224, 0, 32, 8)
            if self.rayon1[7] >= 6 and self.rayon2[7] < 9:
                pyxel.blt(self.rayon1[5], 0, 1, 224, 16, 32, 192)
                pyxel.blt(self.rayon1[5], 176, 1, 224, 0, 32, 16)
            if self.rayon1[7] >= 9 and self.rayon2[7] < 12:
                pyxel.blt(self.rayon1[5], 0, 1, 224, 24, 32, 192)
                pyxel.blt(self.rayon1[5], 168, 1, 224, 0, 32, 32)

        if self.rayon2[0] == False:
            if self.rayon2[1] >= self.rayon2[2] - 60:
                if self.rayon2[7] < 6:
                    pyxel.blt(self.vaisseau_x - 4, self.rayon2[5], 1, 0, 48, 32, 32, 1)
                    pyxel.rect(0, self.rayon2[5], 256, 1, 0)
                    pyxel.rect(0, self.rayon2[5]+1, 256, 1, 10)
                    pyxel.rect(0, self.rayon2[5]+31, 256, 1, 10)
                    pyxel.rect(0, self.rayon2[5]+32, 256, 1, 0)
                else:
                    pyxel.blt(self.vaisseau_x - 4, self.rayon2[5], 1, 32, 48, 32, 32, 1)
                    pyxel.rect(0, self.rayon2[5], 256, 1, 8)
                    pyxel.rect(0, self.rayon2[5] + 1, 256, 1, 7)
                    pyxel.rect(0, self.rayon2[5] + 31, 256, 1, 7)
                    pyxel.rect(0, self.rayon2[5] + 32, 256, 1, 8)

        if self.rayon2[0] == True:
            if self.rayon2[7] < 3 :
                pyxel.blt(0, self.rayon2[5], 1, 0, 224, 256, 32)
            if self.rayon2[7] >= 3 and self.rayon2[7] < 6 :
                pyxel.blt(0, self.rayon2[5], 1, 8, 224, 256, 32)
                pyxel.blt(216, self.rayon2[5], 1, 0, 224, 256, 32)
            if self.rayon2[7] >= 6 and self.rayon2[7] < 9 :
                pyxel.blt(0, self.rayon2[5], 1, 16, 224, 256, 32)
                pyxel.blt(208, self.rayon2[5], 1, 0, 224, 256, 32)
            if self.rayon2[7] >= 9 and self.rayon2[7] < 12 :
                pyxel.blt(0, self.rayon2[5], 1, 24, 224, 256, 32)
                pyxel.blt(200, self.rayon2[5], 1, 0, 224, 256, 32)

        pyxel.text(5, 5, str(self.niveau), 7)
        if self.temps >= 63:
            pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 1, 1, 7)



Jeu()