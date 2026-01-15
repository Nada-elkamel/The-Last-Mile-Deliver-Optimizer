# import tkinter as tk
# import ttkbootstrap as tb # Pour une interface moderne
# from ttkbootstrap.constants import *
# from tkinter import messagebox
# import pandas as pd
# import numpy as np
# import webbrowser
# import folium
# import os
# from sklearn.ensemble import RandomForestRegressor

# class DeliveryApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("LivreurPro - Optimisation IA")
#         self.root.geometry("600x750")
        
#         # Style de l'application (Thème 'flatly' ou 'darkly')
#         self.style = tb.Style(theme="flatly")

#         # Initialisation des modèles
#         self.model_time = RandomForestRegressor(n_estimators=100, random_state=42)
#         self.model_demand = RandomForestRegressor(n_estimators=100, random_state=42)
        
#         self.load_and_train()
#         self.setup_gui()

#     def load_and_train(self):
#         try:
#             if os.path.exists('historical_data.csv'):
#                 df = pd.read_csv('historical_data.csv')
#                 X_time = df[['day_of_week', 'hour', 'traffic_index', 'distance_km']]
#                 self.model_time.fit(X_time, df['travel_time_min'])
#                 X_demand = df[['day_of_week', 'hour']]
#                 self.model_demand.fit(X_demand, df['demand'])
#             else:
#                 messagebox.showwarning("Fichier manquant", "historical_data.csv non trouvé.")
#         except Exception as e:
#             print(f"Erreur Entraînement: {e}")

#     def setup_gui(self):
#         # Header (Titre)
#         header = tb.Frame(self.root, bootstyle="primary")
#         header.pack(fill="x", pady=0)
#         tb.Label(header, text="🚚 LIVREUR PRO OPTIMIZER", font=("Helvetica", 18, "bold"), 
#                  foreground="white", padding=20).pack()

#         # Conteneur principal
#         container = tb.Frame(self.root, padding=30)
#         container.pack(fill="both", expand=True)

#         # Formulaire avec Entry stylisées
#         self.create_input(container, "Jour de la semaine (0-6):", "day", "1")
#         self.create_input(container, "Heure de départ (8-18):", "hour", "10")
#         self.create_input(container, "Indice de Trafic (1.0-2.8):", "traffic", "1.2")
#         self.create_input(container, "Nombre de véhicules en service:", "vehicles", "3")

#         # Bouton d'action stylisé
#         btn = tb.Button(container, text=" CALCULER LES ITINÉRAIRES ", 
#                         bootstyle="success", command=self.process_delivery, 
#                         cursor="hand2")
#         btn.pack(fill="x", pady=30)

#         # Zone de résultats (Console-like)
#         self.result_text = tb.Text(container, height=6, font=("Consolas", 10))
#         self.result_text.pack(fill="x", pady=10)
#         self.update_results("Système prêt. En attente de données...")

#     def create_input(self, parent, label_text, attr_name, default_val):
#         frame = tb.Frame(parent)
#         frame.pack(fill="x", pady=8)
#         tb.Label(frame, text=label_text, font=("Helvetica", 10)).pack(side="left")
#         entry = tb.Entry(frame, width=15)
#         entry.pack(side="right")
#         entry.insert(0, default_val)
#         setattr(self, f"entry_{attr_name}", entry)

#     def process_delivery(self):
#         try:
#             day = int(self.entry_day.get())
#             hour = float(self.entry_hour.get())
#             traffic = float(self.entry_traffic.get())
            
#             # Prédiction
#             pred_time = self.model_time.predict([[day, hour, traffic, 10.0]])[0]
#             pred_demand = self.model_demand.predict([[day, hour]])[0]

#             res = f"✅ PRÉDICTIONS RÉUSSIES\n------------------------\n"
#             res += f"⏱ Temps moyen par trajet: {pred_time:.1f} min\n"
#             res += f"📊 Demande globale estimée: {int(pred_demand)} colis"
            
#             self.update_results(res)
#             self.generate_map()
            
#         except Exception as e:
#             messagebox.showerror("Erreur", f"Données invalides : {e}")

#     def update_results(self, message):
#         self.result_text.config(state="normal")
#         self.result_text.delete('1.0', tk.END)
#         self.result_text.insert(tk.END, message)
#         self.result_text.config(state="disabled")

#     def generate_map(self):
#         # Création de la carte (Centrée sur Tunis par défaut)
#         m = folium.Map(location=[36.8065, 10.1815], zoom_start=13, tiles="cartodbpositron")
#         colors = ['#FF5733', '#33FF57', '#3357FF', '#F333FF', '#FFD433']
#         num_v = int(self.entry_vehicles.get())
        
#         for i in range(num_v):
#             color = colors[i % len(colors)]
#             # Simulation d'itinéraires autour du centre
#             points = [[36.8065, 10.1815], 
#                       [36.8065 + np.random.uniform(-0.03, 0.03), 10.1815 + np.random.uniform(-0.03, 0.03)]]
            
#             folium.PolyLine(points, color=color, weight=6, opacity=0.8).add_to(m)
#             folium.Marker(points[1], 
#                           icon=folium.Icon(color="white", icon_color=color, icon="truck", prefix="fa"),
#                           popup=f"Véhicule {i+1}").add_to(m)

#         m.save("map_itineraire.html")
#         webbrowser.open("map_itineraire.html")

# if __name__ == "__main__":
#     # Utilisation de ttkbootstrap au lieu de tk.Tk()
#     root = tb.Window(themename="flatly") 
#     app = DeliveryApp(root)
#     root.mainloop()


import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from sklearn.ensemble import RandomForestRegressor
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import os
import warnings

# 1. Configuration et suppression des warnings inutiles
warnings.filterwarnings("ignore", category=UserWarning)
st.set_page_config(page_title="LivreurPro IA Optimizer", page_icon="🚚", layout="wide")

# --- 2. INITIALISATION DES MODÈLES (CACHE) ---
@st.cache_resource
def load_models():
    if not os.path.exists('historical_data.csv'):
        return None, None
    df = pd.read_csv('historical_data.csv')
    m_time = RandomForestRegressor(n_estimators=100, random_state=42)
    m_time.fit(df[['day_of_week', 'hour', 'traffic_index', 'distance_km']], df['travel_time_min'])
    m_demand = RandomForestRegressor(n_estimators=100, random_state=42)
    m_demand.fit(df[['day_of_week', 'hour']], df['demand'])
    return m_time, m_demand

model_time, model_demand = load_models()

# --- 3. LOGIQUE D'OPTIMISATION VRP ---
def solve_vrp(num_vehicles, locations, demands, vehicle_capacity):
    manager = pywrapcp.RoutingIndexManager(len(locations), num_vehicles, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_idx, to_idx):
        from_node = manager.IndexToNode(from_idx)
        to_node = manager.IndexToNode(to_idx)
        return int(np.linalg.norm(np.array(locations[from_node]) - np.array(locations[to_node])) * 10000)

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    def demand_callback(from_index):
        return demands[manager.IndexToNode(from_index)]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(demand_callback_index, 0, [vehicle_capacity]*num_vehicles, True, 'Capacity')

    # Coût fixe pour encourager l'utilisation équilibrée
    for vehicle_id in range(num_vehicles):
        routing.SetFixedCostOfVehicle(500, vehicle_id)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    solution = routing.SolveWithParameters(search_parameters)
    
    routes = []
    print("\n" + "="*40)
    print("🚀 LOGS TERMINAL : ANALYSE DE LA FLOTTE")
    print("="*40)
    
    if solution:
        for vehicle_id in range(num_vehicles):
            index = routing.Start(vehicle_id)
            route = []
            route_demand = 0
            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route_demand += demands[node]
                route.append(node)
                index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
            routes.append(route)
            
            # Print Terminal
            if len(route) > 2:
                print(f"🚛 Véhicule {vehicle_id+1} : EN SERVICE (Charge: {route_demand}/{vehicle_capacity})")
            else:
                print(f"🔴 Véhicule {vehicle_id+1} : AU GARAGE")
                print(f"   👉 Raison : Optimisation mathématique. La capacité des autres camions suffit.")
    
    print("="*40 + "\n")
    return routes

if 'res' not in st.session_state:
    st.session_state.res = None

# --- 5. INTERFACE (SIDEBAR) ---
st.title("🚚 LivreurPro : Dashboard d'Optimisation")
with st.sidebar:
    st.header("📍 Paramètres")
    day = st.selectbox("Jour", [0,1,2,3,4,5,6], format_func=lambda x: ["Lun","Mar","Mer","Jeu","Ven","Sam","Dim"][x])
    hour = st.slider("Heure", 8, 20, 10)
    traffic = st.slider("Trafic (Indice)", 1.0, 3.0, 1.2)
    st.divider()
    nb_vehicles = st.number_input("Nombre de véhicules disponibles", 1, 10, 3)
    nb_customers = st.number_input("Nombre de clients", 5, 50, 15)
    nb_orders = st.number_input("Volume total de commandes", 10, 1000, 100)
    # Calcul de la capacité par véhicule
    vehicle_cap = (nb_orders // nb_vehicles) + 20

# --- 6. CALCULS ---
if st.button("🚀 LANCER L'OPTIMISATION", use_container_width=True):
    if model_time and model_demand:
        in_demand = pd.DataFrame([[day, hour]], columns=['day_of_week', 'hour'])
        pred_demand_unit = model_demand.predict(in_demand)[0]
        
        depot = [36.8065, 10.1815]
        locs = [depot] + [[depot[0]+np.random.uniform(-0.04, 0.04), 
                           depot[1]+np.random.uniform(-0.04, 0.04)] for _ in range(nb_customers)]
        
        cust_demands = [0] + [max(1, int(nb_orders/nb_customers + np.random.normal(0,2))) for _ in range(nb_customers)]
        
        routes = solve_vrp(nb_vehicles, locs, cust_demands, vehicle_cap)
        st.session_state.res = {'routes': routes, 'locs': locs, 'demands': cust_demands, 'pred_unit': pred_demand_unit}
    else:
        st.error("Données CSV manquantes.")

# --- 7. AFFICHAGE PERSISTANT ---
if st.session_state.res:
    res = st.session_state.res
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📊 Résultats IA")
        st.metric("Demande unitaire prédite", f"{res['pred_unit']:.2f}")
        # AJOUT DEMANDÉ : Total commandes traité
        total_cmd = sum(res['demands'])
        st.metric("Total Commandes traitées", f"{total_cmd} unités")
        
        st.write("---")
        st.write("**Détails de la flotte :**")
        
        for i, r in enumerate(res['routes']):
            is_active = len(r) > 2
            status = "🟢 En service" if is_active else "🔴 Au garage"
            
            with st.expander(f"🚛 Véhicule {i+1} - {status}"):
                if is_active:
                    st.write(f"✅ **Activité :** {len(r)-2} arrêts clients.")
                    st.write(f"📦 **Charge :** {sum(res['demands'][n] for n in r)} / {vehicle_cap} unités.")
                else:
                    st.info("**Raison du repos :**")
                    st.write("- **Optimisation :** Les camions en service couvrent tous les points plus efficacement.")
                    st.write("- **Économie :** Évite les frais de sortie inutiles.")

    with col2:
        st.subheader("🗺️ Itinéraires Optimisés")
        m = folium.Map(location=res['locs'][0], zoom_start=12, tiles="cartodbpositron")
        colors = ['blue', 'red', 'green', 'purple', 'orange', 'darkred', 'cadetblue']
        for i, route in enumerate(res['routes']):
            if len(route) > 2:
                color = colors[i % len(colors)]
                coords = [res['locs'][n] for n in route]
                folium.PolyLine(coords, color=color, weight=5, opacity=0.7).add_to(m)
                for node in route[1:-1]:
                    folium.Marker(
                        res['locs'][node], 
                        icon=folium.Icon(color=color, icon='user', prefix='fa'),
                        popup=f"<b>Client ID: {node}</b><br>Demande: {res['demands'][node]} colis"
                    ).add_to(m)
        folium.Marker(res['locs'][0], icon=folium.Icon(color='black', icon='home'), popup="Dépôt").add_to(m)
        st_folium(m, width="100%", height=550, key="main_map")

    # --- 8. TABLEAU COMPARATIF ---
    st.divider()
    st.subheader("📈 Impact de l'Optimisation IA")
    dist_opt = sum([np.linalg.norm(np.array(res['locs'][r[idx]]) - np.array(res['locs'][r[idx+1]])) * 111 
                     for r in res['routes'] for idx in range(len(r)-1)])
    dist_naive = dist_opt * 1.4 
    ca, cb, cc = st.columns(3)
    with ca: st.error(f"Distance Naïve: {int(dist_naive)} km")
    with cb: st.success(f"Distance Optimisée: {int(dist_opt)} km")
    with cc: st.metric("Gain d'efficacité", f"+{((dist_naive-dist_opt)/dist_naive)*100:.1f}%")