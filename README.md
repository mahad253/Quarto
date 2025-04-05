# ♟️ QUARTO – Jeu de stratégie en Python (Pygame)

Ce projet est une implémentation interactive et ludique du jeu de société **Quarto**, avec une interface graphique immersive, plusieurs niveaux d’intelligence artificielle, et une prise en charge multilingue 🇫🇷🇪🇸.

---

## 🎮 Fonctionnalités

- ✅ **Modes de jeu** :
    - Joueur vs Joueur
    - Joueur vs IA (Niveau 1, 2, Minimax)
- 🧠 **IA intégrée** :
    - Niveau 1 : aléatoire
    - Niveau 2 : stratégie opportuniste
    - Niveau 3 : algorithme Minimax
- 🌍 **Langues** : français 🇫🇷 et espagnol 🇪🇸
- 📜 **Règles** accessibles en jeu
- 📄 **Rapport PDF** intégré
- 🎨 Design responsive & animations Pygame

---

## ⚙️ Lancer le projet

```bash
# 1. Cloner le dépôt
git clone https://github.com/<ton-nom-utilisateur>/Quarto.git
cd Quarto

# 2. Créer et activer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate

# 3. Installer les dépendances
pip install pygame

# 4. Lancer le projet
cd src
python main.py
