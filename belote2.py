from ascii_cards import Card, ascii_version_of_card
from random import choice, shuffle, randrange
from time import sleep
from operator import attrgetter

jeu_32 = []
couleurs = ['Pique', 'Trèfle', 'Coeur', 'Carreau']
valeurs = ['As', '10', 'Roi', 'Dame', 'Valet', '9', '8', '7']
for couleur in couleurs:
    for valeur in valeurs:
        jeu_32.append(Card(couleur, valeur))

noms = ['Benj', 'Jacques', 'Sarah', 'Antoine', 'Jean-Yves', 'JD', 'Amandine']
resultats = ['Coulée', 'Réussie', 'Capot']

ordre = {'Atout': ['Valet', '9', 'As', '10', 'Roi', 'Dame', '8', '7'],
         'Pas atout': ['As', '10', 'Roi', 'Dame', '9', '8', '7']}

cartes_jouees = {'Coeur': {'As': False,
                           '10': False,
                           'Roi': False,
                           'Dame': False,
                           'Valet': False,
                           '9': False,
                           '8': False,
                           '7': False},
                 'Carreau': {'As': False,
                             '10': False,
                             'Roi': False,
                             'Dame': False,
                             'Valet': False,
                             '9': False,
                             '8': False,
                             '7': False},
                 'Pique': {'As': False,
                           '10': False,
                           'Roi': False,
                           'Dame': False,
                           'Valet': False,
                           '9': False,
                           '8': False,
                           '7': False},
                 'Trèfle': {'As': False,
                            '10': False,
                            'Roi': False,
                            'Dame': False,
                            'Valet': False,
                            '9': False,
                            '8': False,
                            '7': False}}

fast = False


def arrondi(nombre):
    if nombre % 10 == 0:
        nb = nombre
    elif nombre % 10 > 5:
        nb = (int(nombre/10)+1)*10
    else:
        nb = int(nombre/10)*10
    return nb


def copier(liste):
    nouvelle_liste = []
    for elt in liste:
        nouvelle_liste.append(elt)
    return nouvelle_liste


def clear():
    print("\n" * 100)


def centrer(text, largeur):
    return ' ' * int((largeur - len(text)) / 2) + str(text)


def print_ascii_card(cartes, atout=''):
    if len(cartes) == 1:
        print(ascii_version_of_card(cartes[0], atout=atout))
    elif len(cartes) == 2:
        print(ascii_version_of_card(cartes[0], cartes[1], atout=atout))
    elif len(cartes) == 3:
        print(ascii_version_of_card(cartes[0], cartes[1], cartes[2], atout=atout))
    elif len(cartes) == 4:
        print(ascii_version_of_card(cartes[0], cartes[1], cartes[2], cartes[3], atout=atout))
    elif len(cartes) == 5:
        print(ascii_version_of_card(cartes[0], cartes[1], cartes[2], cartes[3], cartes[4], atout=atout))
    elif len(cartes) == 6:
        print(ascii_version_of_card(cartes[0], cartes[1], cartes[2], cartes[3], cartes[4], cartes[5], atout=atout))
    elif len(cartes) == 7:
        print(ascii_version_of_card(cartes[0], cartes[1], cartes[2], cartes[3], cartes[4], cartes[5], cartes[6], atout=atout))
    elif len(cartes) == 8:
        print(ascii_version_of_card(cartes[0], cartes[1], cartes[2], cartes[3], cartes[4], cartes[5], cartes[6], cartes[7], atout=atout))


def trier(cartes, atout=False):
    ordre_couleurs = {'Coeur':['Pique', 'Carreau', 'Trèfle', 'Coeur'],
                      'Carreau': ['Pique', 'Coeur', 'Trèfle', 'Carreau'],
                      'Pique': ['Carreau', 'Trèfle', 'Coeur', 'Pique'],
                      'Trèfle': ['Carreau', 'Pique', 'Coeur', 'Trèfle']}

    couleurs = {'Coeur': [],
                'Carreau': [],
                'Pique': [],
                'Trèfle': []}

    for carte in cartes:
        couleurs[carte.couleur].append(carte)

    nouvelle_main = []

    if atout is False:
        for couleur in ordre_couleurs['Coeur']:
            nouvelle_main.extend(sorted(couleurs[couleur], key=attrgetter('ordre')))
    else:
        for couleur in ordre_couleurs[atout]:
            if couleur == atout:
                nouvelle_main.extend(sorted(couleurs[couleur], key=attrgetter('ordre_atout')))
            else:
                nouvelle_main.extend(sorted(couleurs[couleur], key=attrgetter('ordre')))


    return nouvelle_main


class IA:
    """Une IA"""
    def __init__(self, nom, ia=True):
        if nom in noms:
            noms.remove(nom)

        if nom == '':
            self.nom = choice(noms)
            noms.remove(self.nom)
        else:
            self.nom = nom

        self.ia = ia

        self.main = []

        self.atouts_joues = 0

        self.stats = {'Prises': 0,
                      'Prises en deux': 0,
                      'Réussie': 0,
                      'Renversée': 0,
                      'Capot': 0}

    def __repr__(self):
        """Retourne juste le nom"""
        return self.nom

    def repr_stats(self):
        return "Réussites / Prises : {}/{} (Capots : {})\nRenversées : {}".format(self.stats['Réussie'],
                                                                                  self.stats['Prises'],
                                                                                  self.stats['Capot'],
                                                                                  self.stats['Renversée'])

    def ajouter_stat(self, stat):
        self.stats[stat] += 1

    def get_cartes_valides(self, pli, atout, part_maitre):
        """Renvoie une liste de Card()"""
        if pli == []:  # Premier à jouer, toutes les cartes sont autorisées
            carte_autorisees = self.main

        else:  # Sinon
            valeur = 0
            surcoupe = False
            for carte in pli:

                if carte.couleur == atout:
                    surcoupe = True
                    if carte.get_ordre(atout) > valeur:
                        valeur = carte.get_ordre(atout)

            carte_couleur = []
            carte_atout = [[], []]  # [atouts supérieurs, atouts inférieurs]
            for carte in self.main:
                if carte.couleur == pli[0].couleur and pli[0].couleur != atout:
                    carte_couleur.append(carte)
                if carte.couleur == atout:
                    if carte.get_ordre(atout) > valeur:
                        carte_atout[0].append(carte)
                    else:
                        carte_atout[1].append(carte)

            if not not carte_couleur and pli[0].couleur != atout:
                carte_autorisees = carte_couleur
            elif surcoupe or pli[0].couleur == atout:
                if not not carte_atout[0]:
                    carte_autorisees = carte_atout[0]
                elif not not carte_atout[1]:
                    carte_autorisees = carte_atout[1]
                else:
                    carte_autorisees = self.main
            else:
                if not not carte_atout[0] or not not carte_atout[1]:
                    if part_maitre:
                        carte_autorisees = self.main
                    else:
                        carte_autorisees = carte_atout[0] + carte_atout[1]
                else:
                    carte_autorisees = self.main

        return carte_autorisees

    def trier_main(self, atout):
        """Ne renvoie rien, mais trie la main"""

        self.main = trier(self.main, atout)

    def jouer_carte(self, pli, atout, part_maitre, part_pris):
        cartes_valides = self.get_cartes_valides(pli, atout, part_maitre)

        if not pli:
            couleur_demandee = False
        else:
            couleur_demandee = pli[0].couleur

        if self.ia:
            # --- IA ---
            cartes = cartes_valides
            joue = False

            # --- SI PREMIER TOUR
            if not pli and part_pris and self.compter_atouts(atout) != 0: # Si il joue en premier et que le partenaire a pris
                carte_liste = self.jouer_atout(True, cartes_valides, atout)
                if not not carte_liste:
                    for carte in carte_liste:
                        if carte.valeur == 'Valet':
                            joue = carte
                    if joue is False:
                        joue = choice(carte_liste)

            elif not pli and part_pris is False:
                carte_liste = self.jouer_atout(False, cartes_valides, atout)
                if not not carte_liste:
                    for carte in carte_liste:
                        if carte.valeur == 'As':
                            joue = carte
                    if joue is False:
                        joue = choice(carte_liste)

            # --- SINON
            if joue is False:
                for carte in cartes_valides:
                    if self.carte_maitre(carte, atout, couleur_demandee) is not False:
                        joue = carte # On joue une carte maîtresse
                if joue is False:
                    if part_maitre:
                        joue = self.mettre_des_points(cartes_valides, atout)
                    else:
                        joue = self.pisser(cartes_valides, atout)

                if joue is False:
                    joue = choice(cartes)

            self.retirer_carte(joue)
            return joue

        else:
            pas_valide = True
            while pas_valide:
                print('\nVotre main :')
                print_ascii_card(self.main, atout=atout)
                print("Quelle carte voulez-vous jouer ?")
                choix = input()
                try:
                    choix = int(choix)
                    if self.main[choix-1] in cartes_valides:
                        pas_valide = False
                        carte = self.main[int(choix)-1]
                    else:
                        print("Tu ne peux pas jouer cette carte")
                except:
                    print("Tape un chiffre en 1 et {}".format(len(self.main)))

            self.retirer_carte(carte)
            return carte

    # --- FONCTIONS POUR PRENDRE ---
    def prendre_en_un(self, carte_atout):
        if self.ia:
            if self.get_valeur_main(carte_atout) >= 35:
                return True
            else:
                return False
        else:
            pas_choisis = True
            while pas_choisis:
                print("L'atout est :")
                print(ascii_version_of_card(carte_atout, atout=carte_atout.couleur))
                print("Votre main :")
                print_ascii_card(self.main, atout=carte_atout.couleur)
                print("Est-ce que vous voulez prendre à {} ? (Y/N)".format(carte_atout.couleur))
                choix = input()
                if choix.lower() == 'y':
                    pas_choisis = False
                    reponse = True
                elif choix.lower() == 'n':
                    pas_choisis = False
                    reponse = False
                else:
                    pass
            return reponse

    def prendre_en_deux(self, carte_atout):
        if self.ia:
            choix = copier(couleurs)
            choix.remove(carte_atout.couleur)

            valeur_max = ['', 0]
            for couleur in choix:
                n_val = self.get_valeur_main(carte_atout, couleur)
                if n_val > valeur_max[1]:
                    valeur_max = [couleur, n_val]

            if valeur_max[1] > 35:
                retour = [True, valeur_max[0]]
            else:
                retour = [False, '']

            return retour
        else:
            pas_choisi = True
            reponse = [False, '']
            while pas_choisi:
                couleur_inputs = {'Trèfle': ['trefle', 'trèfle', 'Trefle', 'Trèfle'],
                                  'Coeur': ['coeur', 'Coeur'],
                                  'Pique': ['pique','Pique'],
                                  'Carreau': ['Carreau', 'carreau', 'Carreaux', 'carreaux']}
                print(ascii_version_of_card(carte_atout))
                print("Votre main :")
                print_ascii_card(self.main)
                print('Voulez-vous prendre une autre couleur ?')
                choix = input()
                if choix.lower() == 'n':
                    reponse = [False, '']
                    pas_choisi = False
                else:
                    for couleur, typo in couleur_inputs.items():
                        if choix in typo:
                            reponse : [True, couleur]
                            pas_choisi = False
                        else:
                            pass

                return reponse

    # --- FONCTIONS D'IA ---
    def carte_maitre(self, carte, atout, couleur_demandee):
        """Renvoie l'as ou le valet""" # TODO:Renvoyer aussi le 10 ou le 9
        carte_maitre = False

        if carte.couleur == atout:
            for valeur in ordre['Atout']:
                if carte.valeur == valeur:
                    carte_maitre = carte
                elif cartes_jouees[atout][valeur]:
                    pass
                else:
                    break

        elif couleur_demandee is False or carte.couleur == couleur_demandee:
            for valeur in ordre['Pas atout']:
                if carte.valeur == valeur:
                    carte_maitre = carte
                elif cartes_jouees[carte.couleur][valeur]:
                    pass
                else:
                    break

        return carte_maitre

    def pisser(self, carte_valides, atout):
        """Renvoie la carte valide la plus faible"""
        cartes_valides = []
        for carte in carte_valides:
            if carte.couleur != atout and carte.valeur != 'As':
                cartes_valides.append(carte)

        try:
            return sorted(cartes_valides, key=attrgetter('ordre'))[0]
        except:
            return False

    def mettre_des_points(self, carte_valides, atout):
        mettre_point = []
        for carte in carte_valides:
            if carte.couleur != atout:
                if carte.valeur != 'As' and carte.valeur != '10':
                    mettre_point.append(carte)

        try:
            return sorted(mettre_point, key=lambda carte: carte.ordre[0], reverse = True)[0]
        except:
            return False

    def jouer_atout(self, bool, cartes_valides, atout):
        cartes_choisies = []
        if bool:
            for carte in cartes_valides:
                if carte.couleur == atout:
                    cartes_choisies.append(carte)
        else:
            for carte in cartes_valides:
                if carte.couleur != atout:
                    cartes_choisies.append(carte)

        return cartes_choisies

    def compter_atouts(self, atout):
        atout_dans_la_main = 0
        for carte in self.main:
            if carte.couleur == atout:
                atout_dans_la_main += 1

        atout_joues = 0
        for status in cartes_jouees[atout].values():
            if status:
                atout_joues += 1

        if atout_dans_la_main + atout_joues == 8:
            return 0
        else:
            return 8 - (atout_joues + atout_dans_la_main)



    # --- FONCTIONS DE BASE ---
    def donner_carte(self, carte):
        self.main.append(carte)

    def retirer_carte(self, carte):
        self.main.remove(carte)
        return carte

    def get_valeur_main(self, carte_atout, couleur=False):
        if couleur is False:
            couleur = carte_atout.couleur

        valeur = carte_atout.get_points(couleur)
        for carte in self.main:
            valeur += carte.get_points(couleur)
        return valeur


    def __len__(self):
        return len(self.nom)


class Belote:
    """Objet Belote principal"""
    def __init__(self, joueurs, points):
        self.joueurs = joueurs
        self.points_max = points

        self.jeu = copier(jeu_32)

        self.stats_generales = {'Prises': 0, 'Réussies': 0}

        self.equipes = {'Equipe 1': {'joueurs': [joueurs[0], joueurs[1]],
                                     'points': 0},
                        'Equipe 2': {'joueurs': [joueurs[2], joueurs[3]],
                                     'points': 0}}

        self.ordre_de_jeu = [joueurs[0], joueurs[2], joueurs[1], joueurs[3]]

        self.placement = copier(self.ordre_de_jeu)



        self.preneur = ''
        self.atout = ''

        clear()
        print("BIENVENUE SUR BELOTE TRUC\n")
        self.commencer_partie()

        pourcentage = (self.stats_generales['Réussies']/self.stats_generales['Prises'])*100
        print("Pourcentage de réussite : {}%".format(int(pourcentage)))

    def commencer_partie(self):
        print("Début d'une partie à {} points\n".format(self.points_max))
        print("Equipe 1 : {} et {}".format(self.equipes['Equipe 1']['joueurs'][0],
                                           self.equipes['Equipe 1']['joueurs'][1]))
        print("Equipe 2 : {} et {}".format(self.equipes['Equipe 2']['joueurs'][0],
                                           self.equipes['Equipe 2']['joueurs'][1]))
        self.choisir_premier_joueur()
        shuffle(self.jeu)

        continuer = True
        manche = 1
        while continuer:
            if self.equipes['Equipe 1']['points'] >= self.points_max or self.equipes['Equipe 2']['points'] >= self.points_max:
                if self.equipes['Equipe 1']['points'] != self.equipes['Equipe 2']['points']:
                    continuer = False
                    break
            print("Manche {}".format(manche))
            self.commencer_manche()
            manche += 1
            self.changer_ordre_de_jeu(self.ordre_de_jeu)

            self.print_points()

    def commencer_manche(self):

        print("\nC'est {} qui commence".format(self.ordre_de_jeu[0]))
        self.couper()
        self.distribuer(2)
        self.distribuer(3)
        print("Les cartes sont distribuées")

        carte_atout = self.jeu.pop(0)
        self.atout = carte_atout.couleur
        print("\nAtout : {}".format(carte_atout))

        self.trier_mains()

        preneur = self.demander_atout(carte_atout)

        if preneur is False:
            print('Personne n\'a pris')
            self.rendre_cartes(carte_atout)
            if fast is False:
                sleep(2)
        else:
            print("{} prends à {}".format(preneur, self.atout))
            if fast is False:
                sleep(2)
            self.distribuer(3, preneur)
            self.trier_mains()

            self.jouer_manche(preneur)

    def demander_atout(self, carte_atout):
        personne_na_pris = True
        preneur = False
        while personne_na_pris:
            for joueur in self.ordre_de_jeu:

                prends = joueur.prendre_en_un(carte_atout)
                if prends:
                    personne_na_pris = False
                    preneur = joueur
                    self.atout = carte_atout.couleur
                    joueur.donner_carte(carte_atout)
                    break
                else:
                    print("{} ne prends pas en un".format(joueur))
                    if fast is False:
                        sleep(1)
            if personne_na_pris:
                for joueur in self.ordre_de_jeu:
                    prends = joueur.prendre_en_deux(carte_atout)
                    if prends[0]:
                        personne_na_pris = False
                        preneur = joueur
                        self.atout = prends[1]
                        joueur.donner_carte(carte_atout)
                        break
                    else:
                        print("{} ne prends pas en deux".format(joueur))
                        if fast is False:
                            sleep(1)
            personne_na_pris = False

        if preneur is not False:
            preneur.ajouter_stat('Prises')
            self.stats_generales['Prises'] += 1

        return preneur

    def jouer_manche(self, preneur):
        tour = 0
        proxy_ordre = copier(self.ordre_de_jeu)

        cartes_equipes = {'Equipe 1': [],
                          'Equipe 2': []}

        points = {'Equipe 1': 0,
                  'Equipe 2': 0}

        self.raz_cartes_jouees()

        while tour < 8:
            tour += 1
            pli = []
            valeur_pli = 0
            for joueur in proxy_ordre:
                # -- FONCTIONS D'IA ---
                part_maitre = self.partenaire_est_maitre(joueur, pli, proxy_ordre)
                part_pris = self.partenaire_a_pris(joueur, preneur)

                carte = joueur.jouer_carte(pli, self.atout, part_maitre, part_pris)
                pli.append(carte)

                valeur_pli += carte.get_points(self.atout)

                self.display_table(pli, proxy_ordre, preneur, points)
                print("{} joue : {}".format(joueur, carte))

                if fast is False:
                    sleep(2)

            for carte in pli:
                self.se_souvenir(carte)

            vain_cart = self.qui_est_maitre(pli, proxy_ordre)
            vainqueur = vain_cart[0]
            carte_maitresse = vain_cart[1]

            der = 0
            if tour == 8:
                der = 10

            points[self.get_equipe(vainqueur)] += valeur_pli + der

            print("\nTour {} : {}".format(tour, pli))
            print("{} remporte le pli avec {}\n".format(vainqueur, carte_maitresse))
            if fast is False:
                sleep(2)

            cartes_equipes[self.get_equipe(vainqueur)].extend(pli)

            while proxy_ordre[0] != vainqueur:
                self.changer_ordre_de_jeu(proxy_ordre)

        self.tester_contrat(preneur, points)
        for cartes in cartes_equipes.values():
            self.jeu.extend(cartes)

    def tester_contrat(self, preneur, points):
        """Teste si le contrart est accompli, renvoie 0, 1 ou 2"""
        equ_preneur = self.get_equipe(preneur)
        if equ_preneur == 'Equipe 1':
            equ_autre = 'Equipe 2'
        else:
            equ_autre = 'Equipe 1'

        if points[equ_preneur] < 82:
            resultat = 0
            self.gagner_points(equ_autre, 160)
        elif points[equ_preneur] == 162:
            resultat = 2
            self.gagner_points(equ_preneur, 250)
        else:
            resultat = 1
            self.gagner_points(equ_preneur, arrondi(points[equ_preneur]))
            self.gagner_points(equ_autre, arrondi(points[equ_autre]))

        print('{} | {} : {}'.format(points[equ_preneur], points[equ_autre], resultats[resultat]))

        if resultat == 0:
            for joueur in self.equipes[equ_autre]['joueurs']:
                joueur.ajouter_stat('Renversée')
        elif resultat == 2:
            preneur.ajouter_stat('Réussie')
            preneur.ajouter_stat('Capot')
            self.stats_generales['Réussies'] += 1
        elif resultat == 1:
            preneur.ajouter_stat('Réussie')
            self.stats_generales['Réussies'] += 1
        return resultat

    def qui_est_maitre(self, pli, ordre):
        """Fonction qui renvoie le joueur maître et la carte maîtresse"""
        couleur_demandee = pli[0].couleur

        maitre = 0
        i = 0
        valeur = 0

        for carte in pli:
            if i == 0:
                valeur = carte.get_ordre(self.atout)
            else:
                if carte.couleur == couleur_demandee and carte.get_ordre(self.atout) > valeur:
                    valeur = carte.get_ordre(self.atout)
                    maitre = i
                elif carte.couleur == self.atout and carte.get_ordre(self.atout) > valeur:
                    valeur = carte.get_ordre(self.atout)
                    maitre = i
            i += 1

        return [ordre[maitre], pli[maitre]]

    def partenaire_est_maitre(self, joueur, pli, ordre):
        if not pli:
            return True
        else:
            maitre = self.qui_est_maitre(pli, ordre)[0]
            equ_joueur = self.get_equipe(joueur)
            if self.get_equipe(maitre) == equ_joueur:
                return True
            else:
                return False

    def partenaire_a_pris(self, joueur, preneur):
        if self.get_equipe(joueur) == self.get_equipe(preneur):
            return True
        else:
            return False

    # --- FONCTIONS D'ORDRE DE JEU
    def choisir_premier_joueur(self):
        premier = choice(self.ordre_de_jeu)
        while self.ordre_de_jeu[0] != premier:
            self.changer_ordre_de_jeu(self.ordre_de_jeu)

    def changer_ordre_de_jeu(self, ordre):
        ordre.append(ordre.pop(0))

    # --- FONCTIONS DE BASE ---
    def rendre_cartes(self, carte_atout):
        """Personne n'a pris, on remet les cartes sur le paquet"""
        self.jeu.append(carte_atout)

        for joueur in self.joueurs:
            for carte in joueur.main:
                joueur.retirer_carte(carte)
                self.jeu.append(carte)

    def get_cartes_valides(self, joueur, pli, atout, ordre):
        """Renvoie une liste de Card()"""
        if pli == []:  # Premier à jouer, toutes les cartes sont autorisées
            carte_autorisees = joueur.main

        else:  # Sinon
            valeur = 0
            surcoupe = False
            for carte in pli:

                if carte.couleur == atout:
                    surcoupe = True
                    if carte.get_ordre(atout) > valeur:
                        valeur = carte.get_ordre(atout)

            carte_couleur = []
            carte_atout = [[], []]  # [atouts supérieurs, atouts inférieurs]
            for carte in joueur.main:
                if carte.couleur == pli[0].couleur and pli[0].couleur != atout:
                    carte_couleur.append(carte)
                if carte.couleur == atout:
                    if carte.get_ordre(atout) > valeur:
                        carte_atout[0].append(carte)
                    else:
                        carte_atout[1].append(carte)

            if not not carte_couleur and pli[0].couleur != atout:
                carte_autorisees = carte_couleur
            elif surcoupe or pli[0].couleur == atout:
                if self.partenaire_est_maitre(joueur,pli, ordre):
                    carte_autorisees = joueur.main
                elif not not carte_atout[0]:
                    carte_autorisees = carte_atout[0]
                elif not not carte_atout[1]:
                    carte_autorisees = carte_atout[1]
                else:
                    carte_autorisees = joueur.main
            else:
                if not not carte_atout[0] or not not carte_atout[1]:
                    carte_autorisees = carte_atout[0] + carte_atout[1]
                else:
                    carte_autorisees = joueur.main

        return carte_autorisees

    def trier_mains(self):
        for joueur in self.joueurs:
            joueur.trier_main(self.atout)

    def repr_equipe(self, equipe):
        equ = "{} et {}".format(self.equipes[equipe]['joueurs'][0], self.equipes[equipe]['joueurs'][1])
        return equ

    def couper(self):
        """Sépare le paquet en deux, mets le paquet du bas en haut"""

        split = randrange(0,32)
        i = 0
        while i < split:
            card = self.jeu.pop(0)
            self.jeu.append(card)
            i += 1

    def distribuer(self, nombre, preneur=False):
        for joueur in self.ordre_de_jeu:
            if preneur == joueur:
                i = 1
            else:
                i = 0

            while i < nombre:
                joueur.donner_carte(self.jeu.pop(0))
                i += 1

    def get_equipe(self, joueur):
        """Renvoie le nom de l'équipe de 'joueur'"""
        if joueur in self.equipes['Equipe 1']['joueurs']:
            return 'Equipe 1'
        elif joueur in self.equipes['Equipe 2']['joueurs']:
            return 'Equipe 2'

    def gagner_points(self, equipe, points):
        """Rajoute 'points' aux points de 'equipe'"""
        self.equipes[equipe]['points'] += points

    def print_points(self):
        for equipe in self.equipes:
            print("{}: {} points".format(self.repr_equipe(equipe), self.equipes[equipe]['points']))

    def display_table(self, pli, ordre_de_tour, preneur, points):
        clear()

        position = {self.placement[0]: 'bas',
                    self.placement[1]: 'gauche',
                    self.placement[2]: 'haut',
                    self.placement[3]: 'droite'}

        demande = position[ordre_de_tour[0]]
        pli_trie = self.trier_pli(pli, demande)

        afficher_carte = self.print_pli(pli_trie, self.atout, print_lignes=False)

        col_gauche = 10
        milieu = 30
        col_droite = 10

        couleurs = {'Pique': '♠',
                    'Carreau': '♦',
                    'Coeur': '♥',
                    'Trèfle': '♣'}

        prise = "[{}]".format(couleurs[self.atout])

        prises = {'haut': '',
                  'bas': '',
                  'gauche': '',
                  'droite': ''}

        prises[position[preneur]] = prise

        for equipe, points in points.items():
            print("{} : {} points".format(self.repr_equipe(equipe), points))

        print("\n")

        print("%-{}s %-{}s %{}s".format(col_gauche, milieu, col_droite) %
              ('', centrer(self.placement[2], milieu), ''))

        print("%-{}s %-{}s %{}s".format(col_gauche, milieu, col_droite) %
              ('', centrer(prises['haut'], milieu), ''))

        i = 0
        for ligne in afficher_carte:
            if i == 5:
                joueur_g = self.placement[1]
                joueur_d = self.placement[3]
            elif i == 6:
                joueur_d = prises['droite']
                joueur_g = prises['gauche']
            else:
                joueur_d = ''
                joueur_g = ''

            print("%-{}s %-{}s %{}s".format(col_gauche, milieu, col_droite) %
                  (centrer(joueur_g, col_gauche), '' * int((milieu - len(ligne)) / 2) + ligne,
                   centrer(joueur_d, col_droite)))
            i += 1

        print("%-{}s %-{}s %{}s".format(col_gauche, milieu, col_droite) %
              ('', centrer(self.placement[0], milieu), ''))
        print("%-{}s %-{}s %{}s".format(col_gauche, milieu, col_droite) %
              ('', centrer(prises['bas'], milieu), ''))

    def trier_pli(self, pli, demande):
        tri = {'haut': 0,
               'droite': 1,
               'bas': 2,
               'gauche': 3}
        ordre_pli = ['haut', 'droite', 'bas', 'gauche']

        i = 0
        for carte in pli:

            cote = tri[demande] + i
            if cote > 3:
                cote -= 4

            ordre_pli[cote] = carte
            i += 1

        return ordre_pli

    def print_pli(self, pli, atout, print_lignes=False):
        vide = ' ' * 9
        ligne_vide = [vide, vide, vide, vide, vide, vide, vide]

        try:
            haut = ascii_version_of_card(pli[0], return_string=False, atout=atout)
        except:
            haut = ligne_vide
        try:
            droite = ascii_version_of_card(pli[1], return_string=False, atout=atout)
        except:
            droite = ligne_vide
        try:
            bas = ascii_version_of_card(pli[2], return_string=False, atout=atout)
        except:
            bas = ligne_vide
        try:
            gauche = ascii_version_of_card(pli[3], return_string=False, atout=atout)
        except:
            gauche = ligne_vide

        lignes_list = []
        ligne = 0
        while ligne < 14:
            if ligne < 3:
                i_ligne = "{}{}".format(' ' * 9, haut[ligne])
                lignes_list.append(i_ligne)
            elif ligne in range(3, 7):
                i_ligne = "{}{}{}".format(gauche[ligne - 3], haut[ligne], droite[ligne - 3])
                lignes_list.append(i_ligne)
            elif ligne in range(7, 10):
                i_ligne = "{}{}{}".format(gauche[ligne - 3], bas[ligne - 7], droite[ligne - 3])
                lignes_list.append(i_ligne)
            else:
                i_ligne = "{}{}".format(' ' * 9, bas[ligne - 7])
                lignes_list.append(i_ligne)
            ligne += 1

        if print_lignes:
            for ligne in lignes_list:
                print(ligne)

        return lignes_list

    def raz_cartes_jouees(self):
        for couleur in cartes_jouees:
            for valeur in couleur:
                cartes_jouees[couleur][valeur] = False

    def se_souvenir(self, carte):
        cartes_jouees[carte.couleur][carte.valeur] = True

joueurs = [IA('Benj', ia=False), IA(''), IA(''), IA('')]


belote = Belote(joueurs, 200)
