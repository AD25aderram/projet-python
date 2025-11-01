import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import csv


def init_base_donne(profs, etudiants):
    with sqlite3.connect("base_de_donnees.db") as db:
        db.execute("CREATE TABLE IF NOT EXISTS professor (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE,password TEXT)")
        db.execute("CREATE TABLE IF NOT EXISTS notes_etudiants (id INTEGER PRIMARY KEY AUTOINCREMENT,nom TEXT,prenom TEXT,python NUMERIC,C NUMERIC,UNIQUE(nom, prenom))")
        for prof in profs:
            db.execute("INSERT OR IGNORE INTO professor (username, password) VALUES (?, ?)", (prof[0], prof[1]))
        for etudiant in etudiants:
            db.execute("INSERT OR IGNORE INTO notes_etudiants (nom, prenom) VALUES (?, ?)", (etudiant[0], etudiant[1]))
        db.commit()



def open_window_login():
    window = Tk()
    window.geometry("500x350")
    window.title("Authentification")
    window.resizable(False, False)


    frame = ttk.Frame(window, padding=40)
    frame.pack(expand=True)

    ttk.Label(frame, text="Connexion au système", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

    ttk.Label(frame, text="Nom d'utilisateur :").grid(row=1, column=0, sticky="e", padx=10, pady=10)
    ttk.Label(frame, text="Mot de passe :").grid(row=2, column=0, sticky="e", padx=10, pady=10)

    username = StringVar()
    password = StringVar()

    ttk.Entry(frame, textvariable=username, width=30).grid(row=1, column=1)
    ttk.Entry(frame, textvariable=password, width=30, show="*").grid(row=2, column=1)

    ttk.Button(frame, text="Se connecter",
               command=lambda: [window.destroy(), check_user(username.get(), password.get())]
               ).grid(row=3, column=0, columnspan=2, pady=20)

    window.mainloop()


def check_user(user, pswd):
    with sqlite3.connect("base_de_donnees.db") as db:
        cursor = db.execute("SELECT * FROM professor WHERE username = ? AND password = ?", (user, pswd))
        row = cursor.fetchone()

    if row:
        messagebox.showinfo("Succès", "Connexion réussie !")
        open_window_module()
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe invalide !")
        open_window_login()



def open_window_module():
    window = Tk()
    window.title("Choix du module")
    window.geometry("400x300")
    window.resizable(False, False)
    

    frame = ttk.Frame(window, padding=40)
    frame.pack(expand=True)

    ttk.Label(frame, text="Sélectionnez un module", font=("Segoe UI", 14, "bold")).pack(pady=20)
    ttk.Button(frame, text="C", command=lambda: [window.destroy(), open_window_action(1)], width=25).pack(pady=10)
    ttk.Button(frame, text="Python", command=lambda: [window.destroy(), open_window_action(2)], width=25).pack(pady=10)

    window.mainloop()



def open_window_action(choix):
    window = Tk()
    window.title("Choix de l'action")
    window.geometry("400x350")
    window.resizable(False, False)
    

    frame = ttk.Frame(window, padding=40)
    frame.pack(expand=True)

    ttk.Label(frame, text="Sélectionnez une action", font=("Segoe UI", 14, "bold")).pack(pady=20)
    ttk.Button(frame, text="Ajouter les notes", command=lambda: [window.destroy(), open_window_ajouter(choix)], width=25).pack(pady=10)
    ttk.Button(frame, text="Modifier une note", command=lambda: [window.destroy(), open_window_modifier(choix)], width=25).pack(pady=10)
    ttk.Button(frame, text="Exporter les notes", command=lambda: [window.destroy(), open_window_export(choix)], width=25).pack(pady=10)

    window.mainloop()

def open_window_modifier(choix):
    window = Tk()
    window.title("Modifier une note")
    window.geometry("450x350")
    window.resizable(False, False)
    

    frame = ttk.Frame(window, padding=40)
    frame.pack(expand=True)

    ttk.Label(frame, text="Modifier une note", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

    ttk.Label(frame, text="Nom :").grid(row=1, column=0, pady=10, sticky="e")
    ttk.Label(frame, text="Prénom :").grid(row=2, column=0, pady=10, sticky="e")
    ttk.Label(frame, text="Nouvelle note :").grid(row=3, column=0, pady=10, sticky="e")

    nom = StringVar()
    prenom = StringVar()
    note = DoubleVar()

    ttk.Entry(frame, textvariable=nom, width=30).grid(row=1, column=1)
    ttk.Entry(frame, textvariable=prenom, width=30).grid(row=2, column=1)
    ttk.Entry(frame, textvariable=note, width=30).grid(row=3, column=1)

    ttk.Button(frame, text="Valider",
               command=lambda: [window.destroy(), verify(nom.get(), prenom.get(), note.get(), choix)]
               ).grid(row=4, column=0, columnspan=2, pady=25)

    window.mainloop()


def verify(nom, prenom, note, choix):
    with sqlite3.connect("base_de_donnees.db") as db:
        result = db.execute("SELECT * FROM notes_etudiants WHERE nom = ? AND prenom = ?", (nom, prenom)).fetchone()
        if result is None:
            messagebox.showerror("Erreur", "Étudiant introuvable !")
            open_window_module()
            return

        if choix == 1:
            db.execute("UPDATE notes_etudiants SET C = ? WHERE nom = ? AND prenom = ?", (note, nom, prenom))
        elif choix == 2:
            db.execute("UPDATE notes_etudiants SET python = ? WHERE nom = ? AND prenom = ?", (note, nom, prenom))

        db.commit()

    messagebox.showinfo("Succès", f"Note mise à jour pour {nom} {prenom} : {note}")
    open_window_module()


def open_window_ajouter(choix):
    with sqlite3.connect("base_de_donnees.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.execute("SELECT * FROM notes_etudiants")
        rows = cursor.fetchall()

    window = Tk()
    window.title("Ajout des notes")
    window.geometry("600x600")
    

    canvas = Canvas(window)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar = ttk.Scrollbar(window, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    ttk.Label(frame, text="Étudiant", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(frame, text="Note", font=("Segoe UI", 12, "bold")).grid(row=0, column=1, padx=10, pady=10)

    notes_list = []
    row_nom = []

    for index, row in enumerate(rows):
        full_name = f"{row['nom']} {row['prenom']}"
        ttk.Label(frame, text=full_name).grid(row=index + 1, column=0, pady=5, padx=10, sticky="w")
        var = DoubleVar()
        ttk.Entry(frame, textvariable=var, width=10).grid(row=index + 1, column=1, pady=5)
        notes_list.append(var)
        row_nom.append((row["nom"], row["prenom"]))

    ttk.Button(frame, text="Enregistrer",
               command=lambda: [window.destroy(), add_grades(choix, row_nom, notes_list)]
               ).grid(row=len(row_nom) + 1, columnspan=2, pady=20)

    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    window.mainloop()


def add_grades(choix, row_nom, notes_list):
    with sqlite3.connect("base_de_donnees.db") as db:
        for index, (nom, prenom) in enumerate(row_nom):
            note = notes_list[index].get()
            if choix == 1:
                db.execute("UPDATE notes_etudiants SET C = ? WHERE nom = ? AND prenom = ?", (note, nom, prenom))
            elif choix == 2:
                db.execute("UPDATE notes_etudiants SET python = ? WHERE nom = ? AND prenom = ?", (note, nom, prenom))
        db.commit()

    messagebox.showinfo("Succès", "Les notes ont été enregistrées avec succès !")
    open_window_module()


def open_window_export(choix):
    window = Tk()
    window.geometry("400x250")
    window.title("Exportation des notes")
    

    frame = ttk.Frame(window, padding=40)
    frame.pack(expand=True)

    ttk.Label(frame, text="Exporter les notes au format CSV", font=("Segoe UI", 12, "bold")).pack(pady=20)
    ttk.Button(frame, text="Exporter", command=lambda: [window.destroy(), export(choix)], width=25).pack(pady=20)

    window.mainloop()


def export(choix):
    with sqlite3.connect("base_de_donnees.db") as conn:
        cursor = conn.cursor()
        if choix == 1:
            cursor.execute("SELECT nom || ' ' || prenom AS nom_complet, C AS note FROM notes_etudiants")
            filename = "exported_notes_C.csv"
        else:
            cursor.execute("SELECT nom || ' ' || prenom AS nom_complet, python AS note FROM notes_etudiants")
            filename = "exported_notes_python.csv"

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)

    messagebox.showinfo("Succès", f"Les notes ont été exportées vers '{filename}' !")
    open_window_module()
