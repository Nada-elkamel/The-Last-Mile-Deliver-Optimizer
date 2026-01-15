# 🚚 LivreurPro – IA Optimizer

## 📌 Description du projet

**LivreurPro – IA Optimizer** est une application intelligente d’aide à la décision pour la **logistique et la livraison**. Elle combine **intelligence artificielle**, **optimisation mathématique (VRP)** et **visualisation cartographique** afin d’optimiser les tournées de livraison, réduire les distances parcourues et améliorer l’utilisation de la flotte.

Le projet est conçu comme un **dashboard interactif Streamlit**, permettant de simuler des scénarios réels (trafic, demande, nombre de véhicules, volume de commandes).

---

## 🎯 Objectifs

* Prédire la **demande logistique** à partir de données historiques
* Estimer le **temps de trajet** en fonction du trafic et du contexte temporel
* Optimiser l’assignation des clients aux véhicules (**Vehicle Routing Problem – VRP**)
* Réduire les coûts opérationnels (distance, véhicules inutilisés)
* Visualiser clairement les itinéraires sur une carte interactive

---

## 🧠 Technologies utilisées

### 📦 Backend & IA

* **Python 3.9+**
* **Pandas / NumPy** – traitement des données
* **Scikit-learn** – modèles de prédiction (RandomForest)
* **Google OR-Tools** – optimisation VRP (capacités, flotte)

### 🖥️ Interface & Visualisation

* **Streamlit** – dashboard interactif
* **Folium** – cartographie des itinéraires
* **streamlit-folium** – intégration carte / UI

---

## 📂 Structure du projet

```bash
.
├── main.py                 # Application principale Streamlit
├── historical_data.csv     # Données historiques (entraînement IA)
├── LesOptimisiteProjet.ipynb  # Notebook d’analyse et tests
├── README.md               # Documentation du projet
```

---

## 📊 Données utilisées

Le fichier **historical_data.csv** contient notamment :

* `day_of_week` : jour de la semaine (0 = Lundi, 6 = Dimanche)
* `hour` : heure de départ
* `traffic_index` : indice de congestion
* `distance_km` : distance estimée
* `travel_time_min` : temps réel observé
* `demand` : volume de commandes

Ces données servent à entraîner :

* un modèle de **prédiction du temps de trajet**
* un modèle de **prévision de la demande**

---

## ⚙️ Fonctionnalités principales

### 1️⃣ Prédiction par IA

* Prédiction de la demande logistique
* Estimation du temps moyen de trajet

### 2️⃣ Optimisation VRP

* Gestion de plusieurs véhicules
* Capacités limitées par véhicule
* Désactivation automatique des camions inutiles
* Minimisation de la distance totale

### 3️⃣ Visualisation

* Carte interactive avec itinéraires colorés
* Dépôt et clients géolocalisés
* Détails par véhicule (charge, arrêts)

### 4️⃣ Indicateurs de performance

* Distance optimisée vs distance naïve
* Gain d’efficacité (%)
* Total de commandes traitées

---

## 🚀 Installation et exécution

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-username/livreurpro-optimizer.git
cd livreurpro-optimizer
```

### 2. Installer les dépendances

*(Exemple de dépendances)*

```txt
streamlit
pandas
numpy
scikit-learn
folium
streamlit-folium
ortools
```

### 3. Lancer l’application

```bash
streamlit run main.py
```

---

## 🖥️ Utilisation

1. Sélectionner le **jour**, l’**heure** et l’**indice de trafic**
2. Définir le **nombre de véhicules**, de clients et le volume de commandes
3. Cliquer sur **LANCER L’OPTIMISATION**
4. Analyser :

   * l’état de la flotte
   * les itinéraires sur la carte
   * les gains d’efficacité

---

## 📈 Exemple de cas d’usage

* Entreprise de livraison urbaine
* Optimisation du dernier kilomètre
* Simulation de scénarios logistiques
* Aide à la décision pour les dispatchers

---

## 🔮 Améliorations futures

* Intégration de données GPS réelles
* Prise en compte des fenêtres horaires clients
* Ajout des coûts carburant / CO₂
* Déploiement cloud (Docker / Streamlit Cloud)

---

## 👤 Auteur

Projet réalisé par **Les Optimisite**

---

## 📜 Licence

Ce projet est sous licence **MIT** – libre d’utilisation à des fins pédagogiques et professionnelles.

---

⭐ *N’hésitez pas à mettre une étoile au projet si vous le trouvez utile !*
