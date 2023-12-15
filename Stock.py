from collections import deque


###    La classe Alertes gère les alertes relatives aux faibles occurrences de produits en stock.

###    Attributs:
###        alertes (deque): Une file pour stocker les noms d'alertes.

###    Méthodes:
###        ajouter_alerte(nom_alerte): Ajoute une alerte à la file.
###        supprimer_alerte(nom_alerte): Supprime une alerte de la file.
###        afficher_alertes(): Affiche la liste des alertes.
class Alertes:
    alertes = deque([])


    
###        ajoute une alerte à la file d'alertes.

###        paramètres:
###            nom_alerte (str): le nom de l'alerte à ajouter.
    @staticmethod
    def ajouter_alerte(nom_alerte):
        if nom_alerte not in Alertes.alertes:
            Alertes.alertes.append(nom_alerte)





###        Supprime une alerte de la file d'alertes.

###        Paramètres:
###            nom_alerte (str): Le nom de l'alerte à supprimer.
    def supprimer_alerte(nom_alerte):
        if nom_alerte in Alertes.alertes:
            Alertes.alertes.remove(nom_alerte)





###        Affiche la liste des alertes.
    @staticmethod
    def afficher_alertes():
        if not Alertes.alertes:
            print("aucune alerte.")
        else:
            print("liste des alertes:")
            for alerte in Alertes.alertes:
                print(f"alerte produit: {alerte[0]}{alerte[1]}")






###    La classe GestionStock gère l'inventaire et l'assemblage des colis.

###    Attributs:
###        inventaire (dict): Un dictionnaire pour stocker les informations sur les produits.

###    Méthodes:
###        ajouter_produits(chaine_saisie): Ajoute des produits à l'inventaire.
###        afficher_colis(colis): Affiche les produits dans un colis.
###        assembler_colis(chaine_colis): Assemble des colis à partir de produits spécifiés.
###        afficher_inventaire(): Affiche l'inventaire complet.
###        controle_inventaire(alertes): Contrôle l'inventaire et gère les alertes.
###        verification_entree(array_entree): Valide l'entrée des produits.
class GestionStock:


###        Initialise une nouvelle instance de la classe GestionStock.
    def __init__(self):
        self.inventaire = {}




###        Ajoute des produits à l'inventaire.

###        Paramètres:
###            chaine_saisie (str): Une chaîne contenant les produits à ajouter.
    def ajouter_produits(self, chaine_saisie):
        produits = chaine_saisie.upper().split(", ")
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

###        Paramètres:
###            colis (list): Une liste de produits dans le colis.
    def afficher_colis(self, colis):
        if not colis:
            print("aucun produit dans le colis.")
        else:
            print("produits dans le colis:")
            for produit in colis:
                print(f"type: {produit['type_produit']}, volume: {produit['volume']}")
    





###        Assemble des colis à partir de produits spécifiés.

###        Paramètres:
###            chaine_colis (str): Une chaîne contenant les produits à assembler.

###        Retourne:
###            list: Une liste de produits assemblés.
    def assembler_colis(self, chaine_colis):
        ids_colis = chaine_colis.upper().split(", ")
        colis = []
        for id_colis in ids_colis:
            if self.verification_entree(id_colis):
                type_produit, volume = id_colis[:-1], int(id_colis[-1])
                cle_produit = (type_produit, volume)
                if cle_produit in self.inventaire and self.inventaire[cle_produit]["occurrences"] > 0:
                    self.inventaire[cle_produit]["occurrences"] -= 1
                    self.inventaire[cle_produit]["stock"].popleft()
                    colis.append({"type_produit": type_produit, "volume": volume})
                colis.sort(key=lambda x: x["volume"], reverse=True)
                return colis





###        Affiche l'inventaire complet.
    def afficher_inventaire(self):
        if not self.inventaire:
            print("l'inventaire est vide.")
        else:
            print("inventaire complet:")
            for cle_produit, info_produit in self.inventaire.items():
                print(f"produit: {cle_produit[0]}{cle_produit[1]}, occurrences: {info_produit['occurrences']}, stock: {info_produit['stock']}")






###        Contrôle l'inventaire et gère les alertes.

###        Paramètres:
###            alertes (Alertes): Une instance de la classe Alertes.
    def controle_inventaire(self):
        
        for cle_produit, info_produit in self.inventaire.items():
            if self.inventaire[cle_produit]["occurrences"] < 2:
                Alertes.ajouter_alerte(cle_produit)
            if self.inventaire[cle_produit]["occurrences"] >= 2:
                Alertes.supprimer_alerte(cle_produit)
            

        while len(Alertes.alertes) == 3:
            print(f"!! trop d'alertes - l'alerte {Alertes.alertes[0][0]}{Alertes.alertes[0][1]} sera traitee automatiquement !!")
            for curseur  in range(5):
                self.ajouter_produits(f"{Alertes.alertes[0][0]}{Alertes.alertes[0][1]}")
            self.controle_inventaire()
            Alertes.afficher_alertes()






###        Valide l'entrée des produits.

###        Paramètres:
###            array_entree (str): Chaîne d'entrée pour un produit.

###        Retourne:
###            bool: True si l'entrée est valide, False sinon.
    def verification_entree(self, array_entree):
        try:    
            if not array_entree[0].isalpha() or not array_entree[1].isnumeric():
                raise ValueError('attention a saisir des valeurs valides')
        except ValueError as e:
            print(e.args)
        finally:
            pass
            return True






###    Bloc Principal

alertes_stock = Alertes()   # Création du Log d'Alertes
gestion_stock = GestionStock()  # Instantiation du Stock
gestion_stock.ajouter_produits("a1, a1, b5, b5, b4, b4, c1, a2, c3, c3")  #Ajout en Brut

while True:
    gestion_stock.controle_inventaire()  #Controle de l'inventaire pour les Alertes


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
        gestion_stock.afficher_colis(produits_assembles)
    elif choix == "5":
        print("programme termine. au revoir!")
        break
    else:
        print("veuillez faire un choix valide (1-5)")
