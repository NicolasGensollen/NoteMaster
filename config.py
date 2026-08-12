"""Identifiants des services externes (ENT et serveur mail de l'école)."""
import os

ENT_API_TOKEN = os.environ.get("ENT_API_TOKEN", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
