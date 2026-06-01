import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CaptoGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FAO - Générateur Profil Capto (Étapes 5 & 6)")
        self.root.geometry("1450x850")

        self.d1_var = tk.DoubleVar(value=38.0)
        self.e_var = tk.DoubleVar(value=2.0)
        self.nb_pt_var = tk.IntVar(value=1000)
        
        # filtrage (étape 4)
        self.corde_var = tk.DoubleVar(value=0.01)    # intol (mm)
        self.tol_ang_var = tk.DoubleVar(value=2.0)   # delta (deg)
        
        # Paramètres de la pièce en 3D
        self.angle_var = tk.DoubleVar(value=5.0)      # angle de dépouille alpha
        self.longueur_var = tk.DoubleVar(value=50.0)  # hauteur h de la pièce

        # Géométrie de la fraise
        self.rayon_var = tk.DoubleVar(value=5.0)     # Rayon d'outil R (fraise de diamètre 10mm)

        # Distance de sécurité pour l'approche/retrait
        self.dist_approche_var = tk.DoubleVar(value=30.0) # Distance en mm

        # Pilotage de l'affichage
        self.z_visu_var = tk.DoubleVar(value=0.0)

        self.create_widgets()
        self.update_data()

    def create_widgets(self):
        # Panneau de gauchee
        left_frame = tk.Frame(self.root, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        def bind_enter(widget):
            widget.bind("<Return>", lambda event: self.update_data())

        # Bloc Paramètres 2D et 3D
        profil_frame = tk.LabelFrame(left_frame, text="1. Géométrie Profil (2D)", padx=10, pady=5)
        profil_frame.pack(fill=tk.X, pady=(0, 5))
        tk.Label(profil_frame, text="d1 (mm):").grid(row=0, column=0, sticky="w")
        e1 = tk.Entry(profil_frame, textvariable=self.d1_var, width=10); e1.grid(row=0, column=1); bind_enter(e1)
        tk.Label(profil_frame, text="e (Excentricité):").grid(row=1, column=0, sticky="w")
        e2 = tk.Entry(profil_frame, textvariable=self.e_var, width=10); e2.grid(row=1, column=1); bind_enter(e2)
        tk.Label(profil_frame, text="Points initiaux:").grid(row=2, column=0, sticky="w")
        e3 = tk.Entry(profil_frame, textvariable=self.nb_pt_var, width=10); e3.grid(row=2, column=1); bind_enter(e3)

        z_frame = tk.LabelFrame(left_frame, text="2. Volume & Dépouille (3D)", padx=10, pady=5)
        z_frame.pack(fill=tk.X, pady=(0, 5))
        tk.Label(z_frame, text="Angle Dépouille (°):").grid(row=0, column=0, sticky="w")
        e4 = tk.Entry(z_frame, textvariable=self.angle_var, width=10); e4.grid(row=0, column=1); bind_enter(e4)
        tk.Label(z_frame, text="Hauteur h (mm):").grid(row=1, column=0, sticky="w")
        e5 = tk.Entry(z_frame, textvariable=self.longueur_var, width=10); e5.grid(row=1, column=1); bind_enter(e5)

        outil_frame = tk.LabelFrame(left_frame, text="3. Correction Outil (Étape 5)", padx=10, pady=5)
        outil_frame.pack(fill=tk.X, pady=(0, 5))
        tk.Label(outil_frame, text="Rayon Outil R (mm):").grid(row=0, column=0, sticky="w")
        e6 = tk.Entry(outil_frame, textvariable=self.rayon_var, width=10); e6.grid(row=0, column=1); bind_enter(e6)

        # Entrée/Sortie
        approche_frame = tk.LabelFrame(left_frame, text="4. Sécurité Entrée/Sortie (Étape 6)", padx=10, pady=5)
        approche_frame.pack(fill=tk.X, pady=(0, 5))
        tk.Label(approche_frame, text="Dist. approche (mm):").grid(row=0, column=0, sticky="w")
        e7 = tk.Entry(approche_frame, textvariable=self.dist_approche_var, width=10); e7.grid(row=0, column=1); bind_enter(e7)

        filtre_frame = tk.LabelFrame(left_frame, text="5. Filtrage & Tolérances (Étape 4)", padx=10, pady=5)
        filtre_frame.pack(fill=tk.X, pady=(0, 5))
        tk.Label(filtre_frame, text="Tol. Corde (mm):").grid(row=0, column=0, sticky="w")
        e8 = tk.Entry(filtre_frame, textvariable=self.corde_var, width=10); e8.grid(row=0, column=1); bind_enter(e8)
        tk.Label(filtre_frame, text="Tol. Angle (°):").grid(row=1, column=0, sticky="w")
        e9 = tk.Entry(filtre_frame, textvariable=self.tol_ang_var, width=10); e9.grid(row=1, column=1); bind_enter(e9)

        # Zone d'actions dynamiques
        action_frame = tk.Frame(left_frame, pady=5)
        action_frame.pack(fill=tk.X)
        tk.Label(action_frame, text="Aperçu plan Z:").grid(row=0, column=0, sticky="w")
        self.z_scale = tk.Scale(action_frame, variable=self.z_visu_var, from_=0, to=-self.longueur_var.get(), 
                                resolution=0.1, orient=tk.HORIZONTAL, command=lambda val: self.update_data())
        self.z_scale.grid(row=0, column=1, sticky="ew")

        tk.Button(action_frame, text="Actualiser", command=self.update_data, bg="#2196F3", fg="white").grid(row=1, columnspan=2, pady=5, sticky="we")
        tk.Button(action_frame, text="Générer Fichier points_pilotes_capto.ascii", command=self.generer_fichier, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).grid(row=2, columnspan=2, pady=10, sticky="we")

        # Tableau d'affichage des coordonnées calculées
        table_frame = tk.LabelFrame(left_frame, text="Trajectoire Finale (Points Pilotés + Approches)")
        table_frame.pack(fill=tk.BOTH, expand=True)
        columns = ("Type", "Xc", "Yc", "Zc", "Nx", "Ny", "Nz")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=55, anchor="center")
        self.tree.column("Type", width=70)
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Graphique de visualisation (Droite)
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def calculate_profile(self, target_z):
        """Calcule la géométrie de la pièce, ses normales et la position du centre de l'outil (TCP)."""
        d1 = self.d1_var.get()
        e = self.e_var.get()
        nb_pt = self.nb_pt_var.get()
        angle_depouille = np.radians(self.angle_var.get())
        R = self.rayon_var.get()

        d1_z = d1 + 2 * abs(target_z) * np.tan(angle_depouille)
        e_z = e * (d1_z / d1)

        a = np.linspace(0, 2 * np.pi, nb_pt)
        
        x = (d1_z / 2 - e_z * np.cos(3 * a)) * np.cos(a) - 3 * e_z * np.sin(3 * a) * np.sin(a)
        y = (d1_z / 2 - e_z * np.cos(3 * a)) * np.sin(a) + 3 * e_z * np.sin(3 * a) * np.cos(a)
        z = np.full_like(x, target_z)

        # Vecteurs Tan
        dx = np.gradient(x)
        dy = np.gradient(y)
        norm_2d = np.hypot(dx, dy)
        
        # Vecteurs normales 2D
        nx_2d = dy / norm_2d
        ny_2d = -dx / norm_2d

        # Calcul des normales tridimensionnelles intégrant la pente de dépouille
        nx_3d = nx_2d * np.cos(angle_depouille)
        ny_3d = ny_2d * np.cos(angle_depouille)
        nz_3d = np.full_like(nx_2d, np.sin(angle_depouille))

        # Le centre du bout de l'outil est décalé par rapport au point de contact
        xc = x + R * nx_2d * np.sin(angle_depouille)
        yc = y + R * ny_2d * np.sin(angle_depouille)
        zc = z - R * np.cos(angle_depouille)

        return x, y, z, nx_3d, ny_3d, nz_3d, xc, yc, zc

    def filter_profile(self, x, y, nx, ny, nz):
        """EXPLICATION ÉTAPE 4 : Algorithme de lissage de corde et de régulation thermique/angulaire."""
        intol = self.corde_var.get()
        delta_rad = np.radians(self.tol_ang_var.get())
        
        kept_indices = [0]
        curr = 0
        N = len(x)

        while curr < N - 1:
            best_valid = curr + 1
            next_idx = curr + 1
            
            while next_idx < N:
                # variation angulaire maximale autorisée pour préserver la cinématique machine
                dot_prod = np.clip(nx[curr]*nx[next_idx] + ny[curr]*ny[next_idx] + nz[curr]*nz[next_idx], -1.0, 1.0)
                if np.arccos(dot_prod) > delta_rad:
                    break
                
                # distance max entre les points réels et le segment rectiligne pour voir la tolérance
                x1, y1 = x[curr], y[curr]
                x2, y2 = x[next_idx], y[next_idx]
                dist_seg = np.hypot(x2 - x1, y2 - y1)
                
                if dist_seg > 1e-8 and next_idx > curr + 1:
                    d_array = np.abs((x2 - x1) * (y[curr+1:next_idx] - y1) - (x[curr+1:next_idx] - x1) * (y2 - y1)) / dist_seg
                    if np.any(d_array > intol):
                        break # Tolérance géométrique dépassée
                        
                best_valid = next_idx
                next_idx += 1
                
            curr = best_valid
            kept_indices.append(curr)
            
        if kept_indices[-1] != N - 1:
            kept_indices.append(N - 1)
            
        return kept_indices

    def add_approach_retract(self, xc_f, yc_f, zc_f, nx_f, ny_f, nz_f):
        """Calcul des trajectoires tangentielles d'entrée et de sortie d'outil."""
        dist_app = self.dist_approche_var.get()

        # Calcul de la tangente au point initial (i=0) pour définir l'axe d'approche prolongé
        tx_start = xc_f[1] - xc_f[0]
        ty_start = yc_f[1] - yc_f[0]
        norm_start = np.hypot(tx_start, ty_start)
        tx_start, ty_start = tx_start / norm_start, ty_start / norm_start

        # Point d'approche tangentiel (reculé de 30mm)
        x_app = xc_f[0] - dist_app * tx_start
        y_app = yc_f[0] - dist_app * ty_start
        z_app = zc_f[0]

        # Calcul de la tangente au point final de sortie
        tx_end = xc_f[-1] - xc_f[-2]
        ty_end = yc_f[-1] - yc_f[-2]
        norm_end = np.hypot(tx_end, ty_end)
        tx_end, ty_end = tx_end / norm_end, ty_end / norm_end

        # Point de retrait tangentiel (avancé de 30mm pour dégager la matière)
        x_ret = xc_f[-1] + dist_app * tx_end
        y_ret = yc_f[-1] + dist_app * ty_end
        z_ret = zc_f[-1]

        return x_app, y_app, z_app, x_ret, y_ret, z_ret

    def update_data(self):
        try:
            self.z_scale.configure(to=-self.longueur_var.get())
            target_z = self.z_visu_var.get()
            
            x, y, z, nx, ny, nz, xc, yc, zc = self.calculate_profile(target_z) #calcul des profils bruts et compensés
            
            kept = self.filter_profile(x, y, nx, ny, nz) #mise en place du filtre de lissage (Étape 4)
            
            x_f, y_f = x[kept], y[kept]
            xc_f, yc_f, zc_f = xc[kept], yc[kept], zc[kept]
            nx_f, ny_f, nz_f = nx[kept], ny[kept], nz[kept]

            x_app, y_app, z_app, x_ret, y_ret, z_ret = self.add_approach_retract(xc_f, yc_f, zc_f, nx_f, ny_f, nz_f)

            self.ax.clear()
            
            # Tracé de la géométrie de la pièce finale
            self.ax.plot(x, y, color='tab:blue', alpha=0.4, linestyle=':', label="Géométrie brute de la pièce")
            self.ax.plot(x_f, y_f, 'b-', linewidth=1.5, label="Profil de contact réel (Fraise/Pièce)")

            # Tracé du parcours du point piloté (étape 5)
            self.ax.plot(xc_f, yc_f, 'r--', linewidth=1.2, label="Trajectoire Point Piloté (Centre outil)")
            self.ax.plot(xc_f, yc_f, 'ro', markersize=3)

            # Tracé des liaisons d'attaque
            self.ax.plot([x_app, xc_f[0]], [y_app, yc_f[0]], 'g-o', linewidth=2, label="Segment d'approche (Étape 6)")
            self.ax.plot([xc_f[-1], x_ret], [yc_f[-1], y_ret], 'm-s', linewidth=2, label="Segment de retrait (Étape 6)")

            # Tracé des traits gris matérialisant la compensation de rayon constante
            for i in range(0, len(x_f), max(1, len(x_f)//30)):
                self.ax.plot([x_f[i], xc_f[i]], [y_f[i], yc_f[i]], color='gray', alpha=0.5, linewidth=0.8)

            self.ax.set_aspect('equal')
            self.ax.grid(True, linestyle=':', alpha=0.6)
            self.ax.set_title(f"Visualisation FAO Étape 5 & 6 à Z = {target_z:.1f} mm\nDécalage radial d'outil appliqué : +{self.rayon_var.get() * np.sin(np.radians(self.angle_var.get())):.3f} mm")
            self.ax.legend(loc="upper right", fontsize="small")
            self.canvas.draw()

            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", tk.END, values=("APPROCHE", f"{x_app:.3f}", f"{y_app:.3f}", f"{z_app:.3f}", f"{nx_f[0]:.3f}", f"{ny_f[0]:.3f}", f"{nz_f[0]:.3f}"))
            for i in range(len(kept)):
                self.tree.insert("", tk.END, values=("USINAGE", f"{xc_f[i]:.3f}", f"{yc_f[i]:.3f}", f"{zc_f[i]:.3f}", f"{nx_f[i]:.3f}", f"{ny_f[i]:.3f}", f"{nz_f[i]:.3f}"))
            self.tree.insert("", tk.END, values=("RETRAIT", f"{x_ret:.3f}", f"{y_ret:.3f}", f"{z_ret:.3f}", f"{nx_f[-1]:.3f}", f"{ny_f[-1]:.3f}", f"{nz_f[-1]:.3f}"))

        except Exception as err:
            print("Erreur globale détectée :", err)

    def generer_fichier(self):
        """Génère le nuage de points complet intégrant les corrections géométriques 5 axes."""
        longueur = self.longueur_var.get()
        z_levels = np.linspace(0, -longueur, 11)
        filename = "points_pilotes_capto.ascii"
        
        try:
            total_points = 0
            with open(filename, "w") as f:
                for z_val in z_levels:
                    x, y, z, nx, ny, nz, xc, yc, zc = self.calculate_profile(z_val)
                    kept = self.filter_profile(x, y, nx, ny, nz)
                    
                    xc_f, yc_f, zc_f = xc[kept], yc[kept], zc[kept]
                    nx_f, ny_f, nz_f = nx[kept], ny[kept], nz[kept]
                    
                    x_app, y_app, z_app, x_ret, y_ret, z_ret = self.add_approach_retract(xc_f, yc_f, zc_f, nx_f, ny_f, nz_f)
                    
                    # Écriture de la séquence pour chaque profil : Approche -> Usinage -> Retrait
                    f.write(f"{x_app:.6f} {y_app:.6f} {z_app:.6f} {nx_f[0]:.6f} {ny_f[0]:.6f} {nz_f[0]:.6f}\n")
                    total_points += 1
                    
                    for idx in range(len(kept)):
                        f.write(f"{xc_f[idx]:.6f} {yc_f[idx]:.6f} {zc_f[idx]:.6f} {nx_f[idx]:.6f} {ny_f[idx]:.6f} {nz_f[idx]:.6f}\n")
                        total_points += 1
                        
                    f.write(f"{x_ret:.6f} {y_ret:.6f} {z_ret:.6f} {nx_f[-1]:.6f} {ny_f[-1]:.6f} {nz_f[-1]:.6f}\n")
                    total_points += 1
            
            messagebox.showinfo("Exportation Terminée", f"Fichier FAO exporté pour traitement CATIA et formatage APT.\nNombre total de lignes générées : {total_points}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec lors de l'écriture sur le disque : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptoGeneratorApp(root)
    root.mainloop()
