"""NoteMaster : gestion des notes de MIRA.

Code écrit par le stagiaire. Mise en production prévue lundi.
"""
import os
import sqlite3

import yaml
from flask import Flask, abort, g, redirect, render_template, request, session, url_for

import config
from database import hash_password, init_db

app = Flask(__name__)
app.secret_key = "notemaster-secret-2026"

DB_PATH = os.environ.get("NOTEMASTER_DB", "notemaster.db")

with open(os.path.join(os.path.dirname(__file__), "config.yaml")) as f:
    SETTINGS = yaml.load(f, Loader=yaml.Loader)


def get_db():
    if "db" not in g:
        if not os.path.exists(DB_PATH):
            init_db(DB_PATH)
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.context_processor
def inject_settings():
    return {"settings": SETTINGS, "user": session.get("user")}


@app.route("/")
def index():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))
    if user["role"] == "prof":
        return redirect(url_for("espace_prof"))
    return redirect(url_for("notes_eleve", eleve_id=user["id"]))


@app.route("/login", methods=["GET", "POST"])
def login():
    erreur = None
    if request.method == "POST":
        identifiant = request.form.get("login", "")
        mot_de_passe = hash_password(request.form.get("password", ""))
        query = (
            f"SELECT * FROM users WHERE login = '{identifiant}' "
            f"AND password = '{mot_de_passe}'"
        )
        row = get_db().execute(query).fetchone()
        if row:
            session["user"] = {
                "id": row["id"],
                "login": row["login"],
                "prenom": row["prenom"],
                "nom": row["nom"],
                "role": row["role"],
            }
            return redirect(url_for("index"))
        erreur = "Identifiant ou mot de passe incorrect."
    return render_template("login.html", erreur=erreur)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/eleve/<int:eleve_id>/notes")
def notes_eleve(eleve_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    db = get_db()
    eleve = db.execute("SELECT * FROM users WHERE id = ?", (eleve_id,)).fetchone()
    if eleve is None:
        abort(404)
    notes = db.execute(
        "SELECT notes.*, users.nom AS prof_nom FROM notes "
        "JOIN users ON users.id = notes.prof_id WHERE eleve_id = ?",
        (eleve_id,),
    ).fetchall()
    moyenne = round(sum(n["valeur"] for n in notes) / len(notes), 2) if notes else None
    return render_template("notes_eleve.html", eleve=eleve, notes=notes, moyenne=moyenne)


@app.route("/notes/<int:note_id>/contester", methods=["POST"])
def contester(note_id):
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))
    db = get_db()
    db.execute(
        "INSERT INTO contestations (note_id, eleve_id, message) VALUES (?, ?, ?)",
        (note_id, user["id"], request.form.get("message", "")),
    )
    db.commit()
    return redirect(url_for("notes_eleve", eleve_id=user["id"]))


@app.route("/prof")
def espace_prof():
    user = session.get("user")
    if not user or user["role"] != "prof":
        return redirect(url_for("login"))
    db = get_db()
    notes = db.execute(
        "SELECT notes.*, users.prenom, users.nom FROM notes "
        "JOIN users ON users.id = notes.eleve_id WHERE prof_id = ? ORDER BY users.nom",
        (user["id"],),
    ).fetchall()
    contestations = db.execute(
        "SELECT contestations.*, users.prenom, users.nom, notes.intitule FROM contestations "
        "JOIN users ON users.id = contestations.eleve_id "
        "JOIN notes ON notes.id = contestations.note_id WHERE notes.prof_id = ?",
        (user["id"],),
    ).fetchall()
    return render_template("prof.html", notes=notes, contestations=contestations)


@app.route("/prof/recherche")
def recherche():
    user = session.get("user")
    if not user or user["role"] != "prof":
        return redirect(url_for("login"))
    q = request.args.get("q", "")
    query = (
        "SELECT id, prenom, nom FROM users WHERE role = 'eleve' "
        f"AND (nom LIKE '%{q}%' OR prenom LIKE '%{q}%')"
    )
    eleves = get_db().execute(query).fetchall()
    message = None
    if not eleves:
        message = f"Aucun élève ne correspond à « {q} »."
    return render_template("recherche.html", eleves=eleves, q=q, message=message)


@app.route("/notes/<int:note_id>/modifier", methods=["GET", "POST"])
def modifier_note(note_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    db = get_db()
    note = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if note is None:
        abort(404)
    if request.method == "POST":
        db.execute(
            "UPDATE notes SET valeur = ?, commentaire = ? WHERE id = ?",
            (float(request.form["valeur"]), request.form.get("commentaire", ""), note_id),
        )
        db.commit()
        return redirect(url_for("index"))
    return render_template("modifier.html", note=note)


@app.route("/sante")
def sante():
    return {"statut": "ok", "ent_configure": bool(config.ENT_API_TOKEN)}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
