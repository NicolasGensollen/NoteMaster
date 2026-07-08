"""Création et remplissage de la base SQLite de NoteMaster."""
import hashlib
import sqlite3


def hash_password(password):
    # TODO stagiaire : c'est sûrement assez sécurisé ?
    return hashlib.md5(password.encode()).hexdigest()


SCHEMA = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    prenom TEXT NOT NULL,
    nom TEXT NOT NULL,
    role TEXT NOT NULL
);
CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    eleve_id INTEGER NOT NULL,
    prof_id INTEGER NOT NULL,
    matiere TEXT NOT NULL,
    intitule TEXT NOT NULL,
    valeur REAL NOT NULL,
    commentaire TEXT
);
CREATE TABLE contestations (
    id INTEGER PRIMARY KEY,
    note_id INTEGER NOT NULL,
    eleve_id INTEGER NOT NULL,
    message TEXT NOT NULL
);
"""

PROFS = [
    ("m.rossi", "algo2026", "Marc", "Rossi"),
    ("c.ferrandi", "Reseaux!Ferrandi", "Clara", "Ferrandi"),
    ("a.paoli", "Paoli-English-88", "Anna", "Paoli"),
]

ELEVES = [
    ("lea.santoni", "lea2026", "Léa", "Santoni"),
    ("hugo.bianchi", "Hb!8kq2pZ", "Hugo", "Bianchi"),
    ("ines.moretti", "MoRetti-2007", "Inès", "Moretti"),
    ("tom.leca", "sanglier4ever", "Tom", "Leca"),
    ("jade.casanova", "Jc_x92!lm", "Jade", "Casanova"),
    ("noah.pietri", "pietri-noah-25", "Noah", "Pietri"),
]

# (login élève, login prof, matière, intitulé, note, commentaire)
NOTES = [
    ("lea.santoni", "m.rossi", "Algorithmique", "Partiel tris", 14.5, "Bon travail, attention à la complexité."),
    ("lea.santoni", "c.ferrandi", "Réseaux", "TP routage", 11, "Le routeur a survécu, c'est déjà ça."),
    ("lea.santoni", "a.paoli", "Anglais", "Oral", 16, "Very good, keep going."),
    ("hugo.bianchi", "m.rossi", "Algorithmique", "Partiel tris", 6, "Le tri à bulles n'est pas une réponse à tout."),
    ("hugo.bianchi", "c.ferrandi", "Réseaux", "TP routage", 9.5, "Débrancher le câble ne compte pas comme une solution."),
    ("hugo.bianchi", "a.paoli", "Anglais", "Oral", 12, "Nice accent, few words."),
    ("ines.moretti", "m.rossi", "Algorithmique", "Partiel tris", 19, "Rien à redire."),
    ("ines.moretti", "c.ferrandi", "Réseaux", "TP routage", 17, "Excellent diagnostic."),
    ("tom.leca", "m.rossi", "Algorithmique", "Partiel tris", 3, "Copie rendue avec un dessin de sanglier. Joli sanglier."),
    ("tom.leca", "a.paoli", "Anglais", "Oral", 8, "Please stop answering in Corsican."),
    ("jade.casanova", "m.rossi", "Algorithmique", "Partiel tris", 13, "Solide."),
    ("jade.casanova", "c.ferrandi", "Réseaux", "TP routage", 15, "Bonne méthode."),
    ("noah.pietri", "c.ferrandi", "Réseaux", "TP routage", 4, "Présence non constatée."),
    ("noah.pietri", "a.paoli", "Anglais", "Oral", 10, "Average."),
]


def init_db(path):
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    ids = {}
    for role, people in (("prof", PROFS), ("eleve", ELEVES)):
        for login, password, prenom, nom in people:
            cur = conn.execute(
                "INSERT INTO users (login, password, prenom, nom, role) VALUES (?, ?, ?, ?, ?)",
                (login, hash_password(password), prenom, nom, role),
            )
            ids[login] = cur.lastrowid
    for eleve, prof, matiere, intitule, valeur, commentaire in NOTES:
        conn.execute(
            "INSERT INTO notes (eleve_id, prof_id, matiere, intitule, valeur, commentaire) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (ids[eleve], ids[prof], matiere, intitule, valeur, commentaire),
        )
    conn.commit()
    conn.close()
