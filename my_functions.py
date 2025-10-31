import sqlite3
from tkinter import *
from tkinter import messagebox
import csv


# ============================ INITIALISATION ============================

def init_base_donne(profs, etudiants):
    with sqlite3.connect("base_de_donnees.db") as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS professor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS notes_etudiants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                prenom TEXT,
                python NUMERIC,
                C NUMERIC,
                UNIQUE(nom, prenom)
            )
        """)

        for prof in profs:
            db.execute("INSERT OR IGNORE INTO professor (username, password) VALUES (?, ?)", (prof[0], prof[1]))

        for etudiant in etudiants:
            db.execute("INSERT OR IGNORE INTO notes_etudiants (nom, prenom) VALUES (?, ?)", (etudiant[0], etudiant[1]))

        db.commit()


# ============================ AUTHENTIFICATION ============================

def open_window_login():
    window = Tk()
    window.geometry("800x600")
    window.title("Authentification Page")

    frame = Frame(window)
    frame.pack(expand=True)

    Label(frame, text="Nom d'utilisateur :").grid(row=0, column=0, padx=10, pady=20, sticky="e")
    Label(frame, text="Mot de passe :").grid(row=1, column=0, padx=10, pady=20, sticky="e")

    username = StringVar()
    password = StringVar()

    Entry(frame, textvariable=username, width=50).grid(row=0, column=1, padx=10, pady=20)
    Entry(frame, textvariable=password, width=50, show="*").grid(row=1, column=1, padx=10, pady=20)

    Button(
        frame, text="Se connecter",
        command=lambda: [window.destroy(), check_user(username.get(), password.get())]
    ).grid(row=2, column=0, columnspan=2, pady=20)

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


# ============================ MENU PRINCIPAL ============================

def open_window_module():
    window = Tk()
    window.title("Choix du module")
    window.geometry("800x600")

    Button(window, text='C', command=lambda: [window.destroy(), open_window_action(1)], width=20, height=2).pack(pady=20)
    Button(window, text='Python', command=lambda: [window.destroy(), open_window_action(2)], width=20, height=2).pack(pady=20)

    window.mainloop()


def open_window_action(choix):
    window = Tk()
    window.title("Choix de l'action")
    window.geometry("800x600")

    Button(window, text="Ajouter les notes", command=lambda: [window.destroy(), open_window_ajouter(choix)], width=25).pack(pady=20)
    Button(window, text="Modifier une note", command=lambda: [window.destroy(), open_window_modifier(choix)], width=25).pack(pady=20)
    Button(window, text="Exporter les notes", command=lambda: [window.destroy(), open_window_export(choix)], width=25).pack(pady=20)

    window.mainloop()


# ============================ AJOUT / MODIFICATION ============================

def open_window_ajouter(choix):
    with sqlite3.connect("base_de_donnees.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.execute("SELECT * FROM notes_etudiants")
        rows = cursor.fetchall()

    window = Tk()
    window.title("Ajout des notes")
    window.geometry("800x600")

    frame = Frame(window)
    frame.pack(expand=True)

    Label(frame, text="Étudiant", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=10, pady=10)
    Label(frame, text="Note", font=('Arial', 12, 'bold')).grid(row=0, column=1, padx=10, pady=10)

    notes_list = []
    row_nom = []

    for index, row in enumerate(rows):
        full_name = f"{row['nom']} {row['prenom']}"
        Label(frame, text=full_name, width=30, anchor="w").grid(row=index + 1, column=0, pady=5, padx=10)
        var = DoubleVar()
        Entry(frame, textvariable=var, width=10).grid(row=index + 1, column=1, pady=5)
        notes_list.append(var)
        row_nom.append((row["nom"], row["prenom"]))

    Button(frame, text="Enregistrer", command=lambda: [window.destroy(), add_grades(choix, row_nom, notes_list)]).grid(row=len(row_nom) + 2, columnspan=2, pady=20)

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


def open_window_modifier(choix):
    window = Tk()
    window.title("Modifier les notes")
    window.geometry("600x400")

    Label(window, text='Nom :').grid(column=0, row=0, pady=10, padx=10)
    Label(window, text='Prénom :').grid(column=0, row=1, pady=10, padx=10)
    Label(window, text='Nouvelle note :').grid(column=0, row=2, pady=10, padx=10)

    nom = StringVar()
    prenom = StringVar()
    note = DoubleVar()

    Entry(window, textvariable=nom).grid(column=1, row=0)
    Entry(window, textvariable=prenom).grid(column=1, row=1)
    Entry(window, textvariable=note).grid(column=1, row=2)

    Button(window, text='Valider', command=lambda: [window.destroy(), verify(nom.get(), prenom.get(), note.get(), choix)]).grid(column=1, row=3, pady=20)

    window.mainloop()


def verify(nom, prenom, note, choix):
    with sqlite3.connect("base_de_donnees.db") as db:
        result = db.execute("SELECT * FROM notes_etudiants WHERE nom = ? AND prenom = ?", (nom, prenom)).fetchone()
        if result is None:
            messagebox.showerror("Erreur", "Étudiant introuvable !")
            return

        if choix == 1:
            db.execute("UPDATE notes_etudiants SET C = ? WHERE nom = ? AND prenom = ?", (note, nom, prenom))
        elif choix == 2:
            db.execute("UPDATE notes_etudiants SET python = ? WHERE nom = ? AND prenom = ?", (note, nom, prenom))

        db.commit()

    messagebox.showinfo("Succès", f"Note {note} enregistrée pour {nom} {prenom}")
    open_window_module()


# ============================ EXPORT ============================

def open_window_export(choix):
    window = Tk()
    window.geometry("400x200")
    window.title("Exportation des notes")

    frame = Frame(window)
    frame.pack(expand=True)

    Button(frame, text="Exporter les notes (CSV)", command=lambda: [window.destroy(),export(choix)], width=25).pack(pady=40)

    window.mainloop()


def export(choix):
    with sqlite3.connect("base_de_donnees.db") as conn:
        cursor = conn.cursor()
        if choix == 1:
            cursor.execute("SELECT nom || ' ' || prenom AS nom_complet, C AS note FROM notes_etudiants")
        elif choix == 2:
            cursor.execute("SELECT nom || ' ' || prenom AS nom_complet, python AS note FROM notes_etudiants")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        if choix == 1:
            with open("exported_notes_C.csv", "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(rows)
        elif choix ==2:
            with open("exported_notes_python.csv", "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(rows)

    messagebox.showinfo("Succès", "Les notes ont été exportées vers 'exported_notes.csv' !")
    open_window_module()


# ============================ LANCEMENT ============================

if __name__ == "__main__":
    profs = [("prof1", "1234"), ("admin", "admin")]
    etudiants = [("Ali", "Ben"), ("Sara", "Amine"), ("Youssef", "Khalid")]
    init_base_donne(profs, etudiants)
    open_window_login()
