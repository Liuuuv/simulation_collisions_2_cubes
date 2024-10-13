import pygame as py
import math

py.init()
# py.display.set_caption("base")



blanc=(255,255,255)
noir=(0,0,0)

class Cube:
    def __init__(self,pos,taille,masse):
        self.pos=pos
        self.taille=taille
        self.masse=masse
        self.vitesse=[0,0]

class Sol:
    def __init__(self,hauteur):
        self.hauteur=hauteur


class Affichage:
    def __init__(self,facteur):
        # self.dimensions=(int(1920*facteur),int(1080*facteur))
        self.dimensions=(int(1080*facteur),int(1920*facteur))
        self.fenetre=py.display.set_mode(self.dimensions)

        self.dt=1/1000
        self.fps=3000

        self.police=py.font.Font(None,30)

        self.sol=Sol(500)
        self.x_mur=50

        self.liste_cubes=[]

        self.nb_collisions=0

    def creer_cube(self,pos,taille,masse):
        cube=Cube(pos,taille,masse)
        self.liste_cubes.append(cube)

    def dessiner_sol(self):
        py.draw.line(self.fenetre,noir,[0,self.sol.hauteur],[self.dimensions[0],self.sol.hauteur],2)

    def dessiner_cube(self):
        for cube in self.liste_cubes:
            UL=cube.pos
            UR=[cube.pos[0]+cube.taille,cube.pos[1]]
            DR=[cube.pos[0]+cube.taille,cube.pos[1]+cube.taille]
            DL=[cube.pos[0],cube.pos[1]+cube.taille]

            py.draw.polygon(self.fenetre,noir,[UL,UR,DR,DL],1)

    def dessiner_mur(self):
        py.draw.line(self.fenetre,noir,[self.x_mur,0],[self.x_mur,self.dimensions[1]])

    def collision(self):
        cube=self.liste_cubes[0]
        autre_cube=self.liste_cubes[1]

        if cube.vitesse[0]<0:
            if cube.pos[0]<autre_cube.pos[0]+autre_cube.taille:
                return True

        elif cube.vitesse[0]>=0:
            if autre_cube.pos[0]+autre_cube.taille>cube.pos[0]:
                return True






    def mettre_a_jour_cubes(self):
        for cube in self.liste_cubes:
            cube.pos[0]+=cube.vitesse[0]*self.dt

        cube=self.liste_cubes[0]    # gros
        autre_cube=self.liste_cubes[1]  # petit

        if self.collision():
            self.nb_collisions+=1

            cube.pos[0]-=cube.vitesse[0]*self.dt
            autre_cube.pos[0]-=autre_cube.vitesse[0]*self.dt

            cube_vitesse=cube.vitesse[0]
            autre_cube_vitesse=autre_cube.vitesse[0]

            cube.vitesse[0]=((cube.masse-autre_cube.masse)/(cube.masse+autre_cube.masse))*cube_vitesse+((2*autre_cube.masse)/(cube.masse+autre_cube.masse))*autre_cube_vitesse

            autre_cube.vitesse[0]=((autre_cube.masse-cube.masse)/(cube.masse+autre_cube.masse))*autre_cube_vitesse+((2*cube.masse)/(cube.masse+autre_cube.masse))*cube_vitesse



        elif autre_cube.pos[0]<self.x_mur:
            self.nb_collisions+=1

            autre_cube.pos[0]-=autre_cube.vitesse[0]*self.dt
            autre_cube.vitesse[0]*=-1

            cube.pos[0]-=cube.vitesse[0]*self.dt


        elif cube.pos[0]>1200:
            cube.pos[0]-=cube.vitesse[0]*self.dt
            cube.vitesse[0]*=-1


            autre_cube.pos[0]-=autre_cube.vitesse[0]*self.dt

        # print(self.nb_collisions)
        # print(cube.vitesse[0],autre_cube.vitesse[0])







    def loop(self):
        horloge=py.time.Clock()


        self.liste_cubes[0].vitesse=[-200,0]


        # boucle de jeu
        continuer=True
        while continuer:
            for event in py.event.get():
                if event.type==py.QUIT:
                    continuer=False
                if event.type==py.KEYDOWN:
                    if event.key==py.K_ESCAPE:
                        continuer=False
            horloge.tick(self.fps)
            py.display.set_caption(str(round(horloge.get_fps(),1)))


            self.fenetre.fill(blanc)

            self.mettre_a_jour_cubes()

            self.dessiner_sol()
            self.dessiner_cube()
            self.dessiner_mur()

            texte_surface1=self.police.render("number of collisions: "+str(self.nb_collisions),True,noir)
            self.fenetre.blit(texte_surface1,(200,270))

            texte_surface2=self.police.render("mass ratio:  "+str(self.liste_cubes[0].masse//self.liste_cubes[1].masse),True,noir)
            self.fenetre.blit(texte_surface2,(200,250))

            py.display.flip()

        py.quit()


facteur=0.5
affichage=Affichage(facteur)

affichage.creer_cube([400,400],100,10000)  # gros
affichage.creer_cube([170,450],50,1)  # petit

affichage.loop()