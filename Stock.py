#!/usr/bin/env python 
# -*- coding: utf-8 -*-
from collections import deque

class Alertes:
    alertes = deque([])

    @staticmethod
    def ajouter_alerte(nom_alerte):
        if nom_alerte not in Alertes.alertes:
            Alertes.alertes.append(nom_alerte)

    @staticmethod
    def afficher_alertes():
        if not Alertes.alertes:
            print("Aucune alerte.")
        else:
            print("Liste des alertes:")
            for alerte in Alertes.alertes:
                print(f"ALERTE Produit: {alerte[0]}{alerte[1]}")

    #@staticmethod
    #def generer_alertes(seuil):
        #Alertes.alertes = []  # Réinitialiser la liste des alertes à chaque génération
        #for type_produit in set(tp[0] for tp in self.inventaire.keys()):
            #volume_total = sum(cle[1] * info["occurrences"] for cle, info in self.inventaire.items() if cle[0] == type_produit)
            #if volume_total < seuil:
                #alerte = {"type_produit": type_produit, "volume_total": volume_total}
                #self.alertes.append(alerte)



class GestionStock:
    def __init__(self):
        self.inventaire = {}

    def ajouter_produits(self, chaine_saisie):
        produits = chaine_saisie.split(", ")
        for produit in produits:
            type_produit, volume = produit[:-1], int(produit[-1])
            cle_produit = (type_produit, volume)
            if cle_produit not in self.inventaire:
                self.inventaire[cle_produit] = {"occurrences": 0}
                self.inventaire[cle_produit]["stock"] = deque([])
            self.inventaire[cle_produit]["occurrences"] += 1
            self.inventaire[cle_produit]["stock"].append(cle_produit)

    def afficher_colis(self, colis):
        if not colis:
            print("Aucun produit dans le colis.")
        else:
            print("Produits dans le colis:")
            for produit in colis:
                print(f"Type: {produit['type_produit']}, Volume: {produit['volume']}")

    def assembler_colis(self, chaine_colis):
        ids_colis = chaine_colis.split(", ")
        colis = []
        for id_colis in ids_colis:
            type_produit, volume = id_colis[:-1], int(id_colis[-1])
            cle_produit = (type_produit, volume)
            if cle_produit in self.inventaire and self.inventaire[cle_produit]["occurrences"] > 0:
                self.inventaire[cle_produit]["occurrences"] -= 1
                self.inventaire[cle_produit]["stock"].popleft()
                colis.append({"type_produit": type_produit, "volume": volume})
        colis.sort(key=lambda x: x["volume"], reverse=True)
        return colis

    def afficher_inventaire(self):
        if not self.inventaire:
            print("L'inventaire est vide.")
        else:
            print("Inventaire complet:")
            for cle_produit, info_produit in self.inventaire.items():
                print(f"Produit: {cle_produit[0]}{cle_produit[1]}, Occurrences: {info_produit['occurrences']}, Stock: {info_produit['stock']}")

    def controle_inventaire(self):
        for cle_produit, info_produit in self.inventaire.items():
            if self.inventaire[cle_produit]["occurrences"] < 2:
                Alertes.ajouter_alerte(cle_produit)



# Exemple d'utilisation

alertes_stock = Alertes()
gestion_stock = GestionStock()
gestion_stock.ajouter_produits("A1, A1, B5, B5, B4, B4, C1, A2, C3, C3")

while True:
    gestion_stock.controle_inventaire()

    print("\nMenu:")
    print("1. Ajouter des produits")
    print("2. Afficher l'inventaire")
    print("3. Afficher les alertes")
    print("4. Assembler des colis")
    print("5. Quitter")

    choix = input("Veuillez choisir une option (1-5): ")

    if choix == "1":
        produits_a_ajouter = input("Veuillez saisir les produits a ajouter (par exemple, 'A1, B2, C3'): ")
        gestion_stock.ajouter_produits(produits_a_ajouter)
    #elif choix == "2":
        #seuil_alerte = int(input("Veuillez saisir le seuil d'alerte : "))
        #gestion_stock.generer_alertes(seuil_alerte)
    elif choix == "2":
        gestion_stock.afficher_inventaire()
    elif choix == "3":
        alertes_stock.afficher_alertes()
    elif choix == "4":
        colis_a_assembler = input("Veuillez saisir les produits pour assembler des colis : ")
        produits_assembles = gestion_stock.assembler_colis(colis_a_assembler)
        gestion_stock.afficher_colis(produits_assembles)
    elif choix == "5":
        print("Programme termine. Au revoir!")
        break
    else:
        print("veuillez faire un choix valide (1-5)")
