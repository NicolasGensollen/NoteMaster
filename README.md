# NoteMaster

Application de gestion des notes de **MIRA**.

## La situation

NoteMaster a été développée cet été par Kévin, stagiaire de la DSI. Kévin est reparti à la fin de son stage, en laissant ce message sur le canal de l'équipe :

> « Tout marche nickel, j'ai testé sur mon PC. Bon courage pour la mise en prod lundi 😎 »

La direction a un doute. Avant de mettre en ligne l'application qui contient les notes de tous les élèves, elle vous confie une mission : **mettre en place une chaîne DevSecOps** qui détecte automatiquement les problèmes de sécurité, et corriger ce qui doit l'être.

Rumeur de couloir : certains élèves se vantent déjà de pouvoir avoir 20/20 partout.

## Préparer l'environnement de développement

Le projet utilise Python 3.13 et [uv](https://docs.astral.sh/uv/). Si Python 3.13 n'est pas installé, uv le télécharge automatiquement.

```bash
uv venv --python 3.13
source .venv/bin/activate        # Windows : .venv\Scripts\activate
uv pip install -r requirements-dev.txt
```

## Lancer l'application

Avec Docker :

```bash
docker compose up --build
```

Ou directement, dans l'environnement virtuel activé :

```bash
python app.py
```

L'application est ensuite disponible sur http://localhost:5000. La base de données est créée automatiquement au premier lancement (fichier `notemaster.db`). Supprimez ce fichier pour repartir d'une base propre.

## Comptes de démonstration

| Rôle | Identifiant | Mot de passe |
|---|---|---|
| Élève | `lea.santoni` | `lea2026` |
| Professeur | `m.rossi` | `algo2026` |

## Lancer les tests

Dans l'environnement virtuel activé :

```bash
pytest -v
```

## Règles du jeu

Vous n'attaquez **que votre propre instance** de NoteMaster, lancée sur votre machine ou dans votre pipeline. Jamais une application qui ne vous appartient pas : c'est illégal (article 323-1 du Code pénal).
