import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

class CarnetAdresse:
    def __init__(self, root):
        self.root = root
        self.root.title("Carnet d'adresses")
        self.root.geometry("370x600")  # Taille de la fenêtre
        self.etat_bouton = "affichage"
        
        # Couleur de fond
        self.root.configure(bg='#1e1e1e')


        # Création de la base de données
        self.conn = sqlite3.connect('Carnet.db')
        self.c = self.conn.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                num_tel TEXT NOT NULL,
                nom TEXT,
                prenom TEXT,
                email TEXT,
                filtres TEXT,
                user INTEGER,
                PRIMARY KEY (num_tel, user),
                FOREIGN KEY (user) REFERENCES users(id)
            )
        ''')

        self.c.execute('''
           CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL,
               password TEXT NOT NULL,
               UNIQUE(username)
           )
        ''')
        self.conn.commit()


        self.label_username = tk.Label(self.root, text='Nom d\'utilisateur:', bg='#1e1e1e', fg='white', font=("Helvetica", 12))
        self.label_password = tk.Label(self.root, text='Mot de passe:', bg='#1e1e1e', fg='white', font=("Helvetica", 12))

        self.entry_username = tk.Entry(self.root, font=("Helvetica", 12))
        self.entry_password = tk.Entry(self.root, show='*', font=("Helvetica", 12))  # Le paramètre show='*' masque le mot de passe

        self.label_username.grid(row=0, column=0, pady=5)
        self.label_password.grid(row=1, column=0, pady=5)
        self.entry_username.grid(row=0, column=1, pady=5)
        self.entry_password.grid(row=1, column=1, pady=5)

        
        self.btn_connexion = tk.Button(root, text='Connexion', command=self.verifier_connexion, bg='#292929', fg='white', font=("Helvetica", 12), relief=tk.FLAT)
        self.btn_connexion.grid(row=2, column=0, columnspan=1, pady=10)
        self.btn_creationUser = tk.Button(root, text='Créer utilisateur', command=self.ajouter_utilisateur, bg='#292929', fg='white', font=("Helvetica", 12), relief=tk.FLAT)
        self.btn_creationUser.grid(row=2, column=1, columnspan=2, pady=10)

        # Associez les changements de couleur des boutons au survol
        self.btn_connexion.bind("<Enter>", self.on_enter)
        self.btn_connexion.bind("<Leave>", self.on_leave)
        self.btn_creationUser.bind("<Enter>", self.on_enter)
        self.btn_creationUser.bind("<Leave>", self.on_leave)
        
    

    
    def show_all(self):
        # Création des widgets avec une police plus grande
        self.label_nom = tk.Label(root, text='Nom:', bg='#1e1e1e', fg='white', font=("Helvetica", 12))
        self.label_prenom = tk.Label(root, text='Prénom:', bg='#1e1e1e', fg='white', font=("Helvetica", 12))
        self.label_email = tk.Label(root, text='E-mail:', bg='#1e1e1e', fg='white', font=("Helvetica", 12))
        self.label_num_tel = tk.Label(root, text='Numéro de téléphone:', bg='#1e1e1e', fg='white', font=("Helvetica", 12))
        self.label_filtres = tk.Label(root, text='Filtres:', bg='#1e1e1e', fg='white', font=("Helvetica", 12))



        self.entry_nom = tk.Entry(root, font=("Helvetica", 12))
        self.entry_prenom = tk.Entry(root, font=("Helvetica", 12))
        self.entry_email = tk.Entry(root, font=("Helvetica", 12))
        self.entry_num_tel = tk.Entry(root, font=("Helvetica", 12))
        self.entry_filtres = tk.Entry(root, font=("Helvetica", 12))

        self.btn_ajouter = tk.Button(root, text='Ajouter', command=self.ajouter_contact, bg='#292929', fg='white', font=("Helvetica", 12), relief=tk.FLAT)
        self.btn_rechercher = tk.Button(root, text='Rechercher', command=self.rechercher_contact, bg='#292929', fg='white', font=("Helvetica", 12), relief=tk.FLAT)
        self.btn_modifier = tk.Button(root, text='Modifier', command=self.modifier_contact, bg='#292929', fg='white', font=("Helvetica", 12), relief=tk.FLAT)
        self.btn_supprimer = tk.Button(root, text='Supprimer', command=self.supprimer_contact, bg='#292929', fg='white', font=("Helvetica", 12), relief=tk.FLAT)

        

        self.btn_modifier.grid(row=7, column=0, columnspan=2, pady=10)
        self.btn_supprimer.grid(row=8, column=0, columnspan=2, pady=10)

        # Associer les changements de couleur des boutons au survol

        self.image_plus = Image.open("C:/Users/axelf/OneDrive/Documents/scolarite/ECE/B2/Hackaton/Projet/images/logo_plus.png")  # Remplacez le chemin par le chemin réel de votre image
        self.image_plus = self.image_plus.resize((100, 100), Image.ANTIALIAS)  # Ajustez la taille de l'image
        self.image_plus = ImageTk.PhotoImage(self.image_plus)


        # Chargement de l'image pour le bouton "rechercher"
        self.image_rechercher = Image.open("C:/Users/axelf/OneDrive/Documents/scolarite/ECE/B2/Hackaton/Projet/images/logo_loupe.png")  # Remplacez le chemin par le chemin réel de votre image
        self.image_rechercher = self.image_rechercher.resize((100, 100), Image.ANTIALIAS)  # Ajustez la taille de l'image
        self.image_rechercher = ImageTk.PhotoImage(self.image_rechercher)

        self.bouton_plus = tk.Button(self.root, image=self.image_plus, command=self.ajout, padx=10)
        self.bouton_plus.grid(row=0, column=0, sticky='ne')
        
        self.bouton_rechercher = tk.Button(self.root, image=self.image_rechercher, command=self.recherche, padx=10)
        self.bouton_rechercher.grid(row=0, column=1, sticky='ne')



        self.image_droite = Image.open("C:/Users/axelf/OneDrive/Documents/scolarite/ECE/B2/Hackaton/Projet/images/gauche.png")  # Remplacez le chemin par le chemin réel de votre image
        self.image_droite = ImageTk.PhotoImage(self.image_droite)
        self.image_gauche = Image.open("C:/Users/axelf/OneDrive/Documents/scolarite/ECE/B2/Hackaton/Projet/images/droite.png")  # Remplacez le chemin par le chemin réel de votre image
        self.image_gauche = ImageTk.PhotoImage(self.image_gauche)

        # Label pour afficher l'image en dessous du bouton "plus"
        self.label_image_gauche = tk.Label(self.root, image=self.image_droite)
        self.label_image_gauche.grid(row=1, column=0, pady=5)

        # Label pour afficher l'image en dessous du bouton "rechercher"
        self.label_image_droite = tk.Label(self.root, image=self.image_gauche)
        self.label_image_droite.grid(row=1, column=1, pady=5)
        
        self.btn_modifier.bind("<Enter>", self.on_enter)
        self.btn_modifier.bind("<Leave>", self.on_leave)
        self.btn_supprimer.bind("<Enter>", self.on_enter)
        self.btn_supprimer.bind("<Leave>", self.on_leave)

        self.label_username.grid_forget()
        self.label_password.grid_forget()
        self.entry_username.grid_forget()
        self.entry_password.grid_forget()
        self.btn_connexion.grid_forget()
        self.btn_creationUser.grid_forget()

        self.ajouter_liste_contacts()

        
    def refreshliste(self):
        self.liste_contacts.grid_forget()
        self.scrollbar.grid_forget()
        self.ajouter_liste_contacts()
    

    def hide_entries(self):
        self.entry_nom.grid_forget()
        self.entry_prenom.grid_forget()
        self.entry_email.grid_forget()
        self.entry_num_tel.grid_forget()
        self.entry_filtres.grid_forget()
        # Utilisez les attributs de la classe pour les labels
        self.label_nom.grid_forget()
        self.label_prenom.grid_forget()
        self.label_email.grid_forget()
        self.label_num_tel.grid_forget()
        self.label_filtres.grid_forget()
    
    def toggle_entries(self):
        if self.etat_bouton == "affichage":
            self.label_nom.grid(row=2, column=0, pady=5)
            self.label_prenom.grid(row=3, column=0, pady=5)
            self.label_email.grid(row=4, column=0, pady=5)
            self.label_num_tel.grid(row=5, column=0, pady=5)
            self.label_filtres.grid(row=6, column=0, pady=5)

            self.entry_nom.grid(row=2, column=1, pady=5)
            self.entry_prenom.grid(row=3, column=1, pady=5)
            self.entry_email.grid(row=4, column=1, pady=5)
            self.entry_num_tel.grid(row=5, column=1, pady=5)
            self.entry_filtres.grid(row=6, column=1, pady=5)

            self.etat_bouton = "affiché"
            
        else:
            # Exécutez la fonction appropriée en fonction de l'état actuel
            if self.etat_bouton == "recherche":
                self.rechercher_contact()
            elif self.etat_bouton == "ajout":
                self.ajouter_contact()
    
            # Réinitialisez l'état du bouton après l'utilisation
            self.etat_bouton = "affichage"

    def recherche(self):
        if self.etat_bouton == "affichage":
            self.toggle_entries()
        else :
            self.hide_entries()
            self.rechercher_contact()
            self.etat_bouton = "affichage"
    
    def ajout(self):
        if self.etat_bouton == "affichage":
            self.toggle_entries()
        else :
            self.hide_entries()
            self.ajouter_contact()
            self.etat_bouton = "affichage"


    def on_enter(self, event):
        event.widget.config(bg='#1e1e1e')

    def on_leave(self, event):
        event.widget.config(bg='#292929')


    def ajouter_utilisateur(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username and password:
            try:
                self.c.execute('''
                    INSERT INTO users (username, password)
                    VALUES (?, ?)
                ''', (username, password))

                self.conn.commit()
                self.message_reussite('Utilisateur ajouté avec succès!')
                self.verifier_connexion()
            except sqlite3.Error as e:
                self.message_erreur(f'Erreur lors de l\'ajout de l\'utilisateur : {e}')
        else :
            self.message_reussite('Veuillez remplir nom d\'utilisateur et mot de passe')


    def verifier_connexion(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        try:
            self.c.execute('''
                SELECT * FROM users
                WHERE username=? AND password=?
            ''', (username, password))

            utilisateur = self.c.fetchone()

            if utilisateur:
                self.id_user =  utilisateur[0]
                self.show_all()
            else:
                self.message_erreur('Nom d\'utilisateur ou mot de passe incorrect.')
                return False
        except sqlite3.Error as e:
            self.message_erreur(f'Erreur lors de la vérification de la connexion : {e}')
            return False

    def ajouter_contact(self):
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        email = self.entry_email.get()
        num_tel = self.entry_num_tel.get()
        filtre = self.entry_filtres.get()
        if nom and prenom and email and num_tel:
            try:
                self.c.execute('''
                    INSERT INTO contacts (nom, prenom, email, num_tel, filtres, user)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (nom, prenom, email, num_tel, filtre, self.id_user, ))

                self.conn.commit()
                self.message_reussite('Contact ajouté avec succès!')
                self.refreshliste()
            except sqlite3.Error as e:
                self.message_erreur(f'Erreur lors de l\'ajout du contact : {e}')

        

    def rechercher_contact(self):
        # Ajouter la logique de recherche de contact ici
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        num = self.entry_num_tel.get()
        mail = self.entry_email.get()

        if nom or prenom or mail or num:
            try:
                self.c.execute('''
                    SELECT * FROM contacts
                    WHERE nom LIKE ? AND prenom LIKE ?  AND email LIKE ? AND num_tel LIKE ? AND user = ?
                ''', (f'%{nom}%', f'%{prenom}%', f'%{mail}%', f'%{num}%', f'{self.id_user}'))

                result = self.c.fetchall()
                self.afficher_resultat(result)
            except sqlite3.Error as e:
                self.message_erreur(f'Erreur lors de la recherche du contact : {e}')
        

    def modifier_contact(self):
        num_tel = self.entry_num_tel.get()

        if num_tel:
            try:
                # Vérifier si le numéro de téléphone existe
                self.c.execute('''
                    SELECT * FROM contacts
                    WHERE num_tel=? AND user = ?
                ''', (num_tel, self.id_user,))

                existing_contact = self.c.fetchone()

                if existing_contact:
                    # Mettre à jour le contact
                    self.c.execute('''
                        UPDATE contacts
                        SET nom=?, prenom=?, email=?, filtres=?
                        WHERE num_tel=? AND user = ?
                    ''', (self.entry_nom.get(), self.entry_prenom.get(), self.entry_email.get(), self.entry_filtres.get(), num_tel, self.id_user, ))

                    self.conn.commit()
                    self.message_reussite('Contact modifié avec succès!')
                    self.maj_liste_contacts()  # Met à jour la liste des contacts après modification
                else:
                    self.message_erreur('Aucun contact trouvé avec ce numéro de téléphone.')
            except sqlite3.Error as e:
                self.message_erreur(f'Erreur lors de la modification du contact : {e}')
        self.message_erreur('Veuillez spécifier un numéro de téléphone pour la modification.')

    def supprimer_contact(self):
        num_tel = self.entry_num_tel.get()

        if num_tel:
            try:
                self.c.execute('''
                    DELETE FROM contacts
                    WHERE num_tel=? AND user = ?
                ''', (num_tel, self.id_user, ))

                self.conn.commit()
                self.message_reussite('Contact supprimé avec succès!')
                self.ajouter_liste_contacts()
            except sqlite3.Error as e:
                self.message_erreur(f'Erreur lors de la suppression du contact : {e}')
        else:
            self.message_erreur('Veuillez spécifier un numéro de téléphone pour la suppression.')

    # Ajoutez la liste des contacts pour la sélection
    def ajouter_liste_contacts(self):
        self.liste_contacts = tk.Listbox(self.root, font=("Helvetica", 12), selectmode=tk.SINGLE, bg='#292929', fg='white')
        self.liste_contacts.grid(row=9, column=0, columnspan=4, pady=10, sticky='ew')

        self.scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.liste_contacts.yview)
        self.scrollbar.grid(row=9, column=4, sticky='ns')
        self.liste_contacts.config(yscrollcommand=self.scrollbar.set)

        self.liste_contacts.bind("<ButtonRelease-1>", self.selectionner_contact)

        self.maj_liste_contacts()

    def maj_liste_contacts(self):
        self.liste_contacts.delete(0, tk.END)
        self.c.execute('''
            SELECT nom, prenom, num_tel FROM contacts
            WHERE user = ?
        ''', (self.id_user,))
        contacts = self.c.fetchall()
        for contact in contacts:
            self.liste_contacts.insert(tk.END, f'{contact[0]} {contact[1]} ({contact[2]})')

    def selectionner_contact(self, event):
        # Met à jour les champs de saisie avec les informations du contact sélectionné.
        selection = self.liste_contacts.curselection()
        if selection:
            num_tel = self.liste_contacts.get(selection)[1:-1].split()[-1]  # Récupère le numéro de téléphone
            numtel = num_tel[1:len(num_tel)]
            self.c.execute('''
                SELECT * FROM contacts
                WHERE num_tel=? AND user = ?
            ''', (numtel, self.id_user, ))
            contact = self.c.fetchone()

            # Vérifie si la requête a renvoyé un résultat valide
            if contact:
                # Affiche les détails du contact dans une nouvelle fenêtre
                self.afficher_details_contact(contact)
            else:
                self.message_erreur('Aucun contact trouvé avec ce numéro de téléphone.')
        else:
            self.message_erreur('Veuillez sélectionner un contact.')

    def afficher_details_contact(self, contact):
        # Crée une nouvelle fenêtre pour afficher les détails du contact
        fenetre_details = tk.Toplevel(self.root)
        fenetre_details.title('Détails du contact')

        # Affiche les détails du contact dans la nouvelle fenêtre
        tk.Label(fenetre_details, text=f'Nom: {contact[0]}', font=("Helvetica", 12)).grid()
        tk.Label(fenetre_details, text=f'Prénom: {contact[1]}', font=("Helvetica", 12)).grid()
        tk.Label(fenetre_details, text=f'E-mail: {contact[2]}', font=("Helvetica", 12)).grid()
        tk.Label(fenetre_details, text=f'Numéro de téléphone: {contact[3]}', font=("Helvetica", 12)).grid()
        tk.Label(fenetre_details, text=f'Filtres: {contact[4]}', font=("Helvetica", 12)).grid()

    def afficher_resultat(self, result):
        if result:
            messagebox.showinfo('Résultat de la recherche', f'Résultat de la recherche : {result}')
        else:
            messagebox.showinfo('Résultat de la recherche', 'Aucun résultat trouvé.')

    def message_reussite(self, message):
        messagebox.showinfo('Succès', message)

    def message_erreur(self, message):
        messagebox.showerror('Erreur', message)
        

if __name__ == '__main__':
    #création appliS
    #création appliS

    root = tk.Tk()
    app = CarnetAdresse(root)
    root.mainloop()
 