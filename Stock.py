from collections import deque


###    La classe AlertesManagement g�re les alertes relatives aux faibles occurrences de produits en stock.

###    Attributs:
###        alertes (deque): Une file pour stocker les noms d'alertes.

###    M�thodes:
###        ajouter_alerte(nom_alerte): Ajoute une alerte � la file.
###        supprimer_alerte(nom_alerte): Supprime une alerte de la file.
###        afficher_alertes(): Affiche la liste des alertes.
class AlertesManagement:
    alertes = deque([])


    
###        ajoute une alerte � la file d'alertes.

###        param�tres:
###            nom_alerte (str): le nom de l'alerte � ajouter.
    @staticmethod
    def ajouter_alerte(nom_alerte):
        if nom_alerte not in AlertesManagement.alertes:
            AlertesManagement.alertes.append(nom_alerte)





###        Supprime une alerte de la file d'alertes.

###        Param�tres:
###            nom_alerte (str): Le nom de l'alerte � supprimer.
    @staticmethod
    def supprimer_alerte(nom_alerte):
        if nom_alerte in AlertesManagement.alertes:
            AlertesManagement.alertes.remove(nom_alerte)





###        Affiche la liste des alertes.
    @staticmethod
    def afficher_alertes():
        if not AlertesManagement.alertes:
            print("aucune alerte.")
        else:
            print("liste des alertes:")
            for alerte in AlertesManagement.alertes:
                print(f"alerte produit: {alerte[0]}{alerte[1]}")






###    La classe GestionStock g�re l'inventaire et l'assemblage des colis.

###    Attributs:
###        inventaire (dict): Un dictionnaire pour stocker les informations sur les produits.

###    M�thodes:
###        ajouter_produits(chaine_saisie): Ajoute des produits � l'inventaire.
###        afficher_colis(colis): Affiche les produits dans un colis.
###        assembler_colis(chaine_colis): Assemble des colis � partir de produits sp�cifi�s.
###        afficher_inventaire(): Affiche l'inventaire complet.
###        controle_inventaire(alertes): Contr�le l'inventaire et g�re les alertes.
###        verification_entree(array_entree): Valide l'entr�e des produits.
class GestionStock:


###        Initialise une nouvelle instance de la classe GestionStock.
    def __init__(self):
        self.inventaire = {}




###        Ajoute des produits � l'inventaire.

###        Param�tres:
###            chaine_saisie (str): Une cha�ne contenant les produits � ajouter.
    def ajouter_produits(self, chaine_saisie):
        produits = separation_chaine(chaine_saisie.upper())
        for produit in produits:
            if self.verification_entree(produit):
                type_produit, volume = produit[0] , int(produit[:0:-1])
                cle_produit = (type_produit, volume)
                if cle_produit not in self.inventaire:
                    self.inventaire[cle_produit] = {"occurrences": 0}
                    self.inventaire[cle_produit]["stock"] = deque([])
                self.inventaire[cle_produit]["occurrences"] += 1
                self.inventaire[cle_produit]["stock"].append(cle_produit)





###        Affiche les produits dans un colis.

###        Param�tres:
###            colis (list): Une liste de produits dans le colis.
    def afficher_colis(self, colis):
        if not colis:
            print("aucun produit dans le colis.")
        else:
            print("produits dans le colis:")
            for produit in colis:
                print(f"type: {produit['type_produit']}, volume: {produit['volume']}")
    





###        Assemble des colis � partir de produits sp�cifi�s.

###        Param�tres:
###            chaine_colis (str): Une cha�ne contenant les produits � assembler.

###        Retourne:
###            list: Une liste de produits assembl�s.
    def assembler_colis(self, chaine_colis):
        ids_colis = separation_chaine(chaine_colis.upper())
        colis = []
        
        for id_colis in ids_colis:
            if self.verification_entree(id_colis):
                type_produit, volume = id_colis[:-1], int(id_colis[-1])
                cle_produit = (type_produit, volume)
                if self.verification_produit_existant(cle_produit):
                    if cle_produit in self.inventaire and self.inventaire[cle_produit]["occurrences"] > 0:
                        self.inventaire[cle_produit]["occurrences"] -= 1
                        self.inventaire[cle_produit]["stock"].popleft()
                        colis.append({"type_produit": type_produit, "volume": volume})
            return colis





###        Affiche l'inventaire complet.
    def afficher_inventaire(self):
        if not self.inventaire:
            print("l'inventaire est vide.")
        else:
            print("inventaire complet:")
            for cle_produit, info_produit in self.inventaire.items():
                print(f"produit: {cle_produit[0]}{cle_produit[1]}, occurrences: {info_produit['occurrences']}, stock: {info_produit['stock']}")






###        Contr�le l'inventaire et g�re les alertes.

###        Param�tres:
###            alertes (AlertesManagement): Une instance de la classe AlertesManagement.
    def controle_inventaire(self):
        
        for cle_produit, info_produit in self.inventaire.items():
            if self.inventaire[cle_produit]["occurrences"] < 2:
                AlertesManagement.ajouter_alerte(cle_produit)
            if self.inventaire[cle_produit]["occurrences"] >= 2:
                AlertesManagement.supprimer_alerte(cle_produit)
            

        while len(AlertesManagement.alertes) > 2:
            print(f"!! trop d'alertes - l'alerte {AlertesManagement.alertes[0][0]}{AlertesManagement.alertes[0][1]} sera traitee automatiquement !!")
            for curseur  in range(5):
                self.ajouter_produits(f"{AlertesManagement.alertes[0][0]}{AlertesManagement.alertes[0][1]}")
            self.controle_inventaire()






###        Valide l'entr�e des produits.

###        Param�tres:
###            array_entree (str): Cha�ne d'entr�e pour un produit.

###        Retourne:
###            bool: True si l'entr�e est valide, False sinon.
    def verification_entree(self, array_entree):
        try:    
            if not array_entree[0].isalpha() or not array_entree[1].isnumeric():
                raise ValueError('!! ATTENTION A SAISIR DES VALEURS VALIDES !!')
        except ValueError as e:
            print(e)
        finally:
            return True



###        Valide l'entr�e des colis.

###        Param�tres:
###            array_entree (str): Cha�ne d'entr�e pour un produit.

###        Retourne:
###            bool: True si l'entr�e est valide, False sinon.
    def verification_produit_existant(self, cle_produit_entree):
        try:    
            if cle_produit_entree not in self.inventaire:
                raise ValueError('!! ATTENTION A SAISIR DES VALEURS EXISTANTES !!')
        except ValueError as e:
            print(e)
        finally:
            return True



###        Permet de Split les entrees.

###        Param�tres:
###            chaine_entree (str): Cha�ne entr�e par l'utilisateur.

###        Retourne:
###            bool: la fonction pass�e par .split().
def separation_chaine(chaine_entree):
    return chaine_entree.split(", ")



###        Permet de tier les colis.

###        Param�tres:
###            colis_a_trier (str): Colis saisi en entr�e, qui vient d'etre cr�er.

###        Retourne:
###            bool: la list des dictionnaires tri�es.
def organisation_colis(colis_a_trier):
    return sorted(colis_a_trier, key=lambda x: x['volume'])

###    Bloc Principal

alertes_stock = AlertesManagement()   # Cr�ation du Log d'AlertesManagement
gestion_stock = GestionStock()  # Instantiation du Stock
gestion_stock.ajouter_produits("A1, A1, B5, B5, B4, B4, C1, A2, C3, C3")  #Ajout en Brut

while True:
    gestion_stock.controle_inventaire()  #Controle de l'inventaire pour les AlertesManagement


    ###     Affichage du menu
    print("\nmenu:")
    print("1. ajouter des produits")
    print("2. afficher l'inventaire")
    print("3. afficher les alertes")
    print("4. assembler des colis")
    print("5. quitter")

    choix = input("veuillez choisir une option (1-5): ")


    ###     Traitement du menu
    if choix == "1":
        produits_a_ajouter = input("veuillez saisir les produits a ajouter (par exemple, 'a1, b2, c3'): ")
        gestion_stock.ajouter_produits(produits_a_ajouter)
    elif choix == "2":
        gestion_stock.afficher_inventaire()
    elif choix == "3":
        alertes_stock.afficher_alertes()
    elif choix == "4":
        colis_a_assembler = input("veuillez saisir les produits pour assembler des colis : ")
        produits_assembles = gestion_stock.assembler_colis(colis_a_assembler)
        colis_fini = organisation_colis(produits_assembles)
        gestion_stock.afficher_colis(colis_fini)
    elif choix == "5":
        print("programme termine. au revoir!")
        break
    else:
        print("veuillez faire un choix valide (1-5)")
