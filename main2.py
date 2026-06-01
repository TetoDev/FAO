import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CaptoGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FAO - Générateur Profil Capto")
        self.root.geometry("1400x800")

        # Valeurs par défaut
        self.d1_var = tk.DoubleVar(value=38.0)
        self.e_var = tk.DoubleVar(value=2.0)
        self.nb_pt_var = tk.IntVar(value=1000)
        
        # tolérances
        self.corde_var = tk.DoubleVar(value=0.01) # intol en mm
        self.tol_ang_var = tk.DoubleVar(value=2.0) # delta en degrés
        
        # param. 3D
        self.angle_var = tk.DoubleVar(value=5.0) # Dépouille
        self.longueur_var = tk.DoubleVar(value=50.0)

        self.z_visu_var = tk.DoubleVar(value=0.0)

        self.create_widgets()
        self.update_data()

    def create_widgets(self):
        left_frame = tk.Frame(self.root, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        def bind_enter(widget):
            widget.bind("<Return>", lambda event: self.update_data())

        # ================= Paramètres 2D =================
        profil_frame = tk.LabelFrame(left_frame, text="Paramètres 2D", padx=10, pady=5)
        profil_frame.pack(fill=tk.X, pady=(0, 5))

        tk.Label(profil_frame, text="d1 (mm):").grid(row=0, column=0, sticky="w")
        e1 = tk.Entry(profil_frame, textvariable=self.d1_var, width=10)
        e1.grid(row=0, column=1); bind_enter(e1)

        tk.Label(profil_frame, text="e:").grid(row=1, column=0, sticky="w")
        e2 = tk.Entry(profil_frame, textvariable=self.e_var, width=10)
        e2.grid(row=1, column=1); bind_enter(e2)

        tk.Label(profil_frame, text="Points initiaux:").grid(row=2, column=0, sticky="w")
        e3 = tk.Entry(profil_frame, textvariable=self.nb_pt_var, width=10)
        e3.grid(row=2, column=1); bind_enter(e3)

        filtre_frame = tk.LabelFrame(left_frame, text="Filtrage (Étape 4)", padx=10, pady=5)
        filtre_frame.pack(fill=tk.X, pady=(0, 5))

        tk.Label(filtre_frame, text="Tol. Corde (mm):").grid(row=0, column=0, sticky="w")
        e4 = tk.Entry(filtre_frame, textvariable=self.corde_var, width=10)
        e4.grid(row=0, column=1); bind_enter(e4)

        tk.Label(filtre_frame, text="Tol. Angle (°):").grid(row=1, column=0, sticky="w")
        e5 = tk.Entry(filtre_frame, textvariable=self.tol_ang_var, width=10)
        e5.grid(row=1, column=1); bind_enter(e5)

        z_frame = tk.LabelFrame(left_frame, text="Paramètres 3D", padx=10, pady=5)
        z_frame.pack(fill=tk.X, pady=(0, 5))

        tk.Label(z_frame, text="Angle Dépouille (°):").grid(row=0, column=0, sticky="w")
        e6 = tk.Entry(z_frame, textvariable=self.angle_var, width=10)
        e6.grid(row=0, column=1); bind_enter(e6)

        tk.Label(z_frame, text="Longueur h (mm):").grid(row=1, column=0, sticky="w")
        e7 = tk.Entry(z_frame, textvariable=self.longueur_var, width=10)
        e7.grid(row=1, column=1); bind_enter(e7)

        action_frame = tk.Frame(left_frame, pady=5)
        action_frame.pack(fill=tk.X)

        tk.Label(action_frame, text="Cote Z (Visu):").grid(row=0, column=0, sticky="w")
        self.z_scale = tk.Scale(action_frame, variable=self.z_visu_var, from_=0, to=-self.longueur_var.get(), 
                                resolution=0.1, orient=tk.HORIZONTAL, command=lambda val: self.update_data())
        self.z_scale.grid(row=0, column=1, sticky="ew")

        tk.Button(action_frame, text="Actualiser Visu", command=self.update_data, bg="#2196F3", fg="white").grid(row=1, columnspan=2, pady=5, sticky="we")
        tk.Button(action_frame, text="Générer ASCII (Étapes 3 & 4)", command=self.generer_fichier, bg="#FF9800", fg="white", font=("Arial", 10, "bold")).grid(row=2, columnspan=2, pady=10, sticky="we")

        table_frame = tk.LabelFrame(left_frame, text="Coordonnées (Points Filtrés)")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("i", "X", "Y", "Z", "Nx", "Ny", "Nz")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=50, anchor="center")
        self.tree.column("i", width=40)
        
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def calculate_profile(self, target_z):
        """Génère les points et normales 3D pour un Z donné."""
        d1 = self.d1_var.get()
        e = self.e_var.get()
        nb_pt = self.nb_pt_var.get()
        angle_depouille = np.radians(self.angle_var.get())

        d1_z = d1 + 2 * abs(target_z) * np.tan(angle_depouille) #diametre qui va augmenter
        e_z = e * (d1_z / d1)

        a = np.linspace(0, 2 * np.pi, nb_pt)

        # équations du profil
        x = (d1_z / 2 - e_z * np.cos(3 * a)) * np.cos(a) - 3 * e_z * np.sin(3 * a) * np.sin(a)
        y = (d1_z / 2 - e_z * np.cos(3 * a)) * np.sin(a) + 3 * e_z * np.sin(3 * a) * np.cos(a)
        z = np.full_like(x, target_z)

        dx = np.gradient(x) #tangentes 
        dy = np.gradient(y)
        norm_2d = np.hypot(dx, dy)
        
        nx_2d = dy / norm_2d #normales 2D
        ny_2d = -dx / norm_2d

        nx_3d = nx_2d * np.cos(angle_depouille)
        ny_3d = ny_2d * np.cos(angle_depouille)
        nz_3d = np.full_like(nx_2d, np.sin(angle_depouille))

        return x, y, z, nx_3d, ny_3d, nz_3d

    def filter_profile(self, x, y, nx, ny, nz):
        """Filtre vectorisé selon l'erreur de corde et l'angle."""
        intol = self.corde_var.get()
        delta_rad = np.radians(self.tol_ang_var.get())
        
        kept_indices = [0]
        curr = 0
        N = len(x)

        while curr < N - 1:
            best_valid = curr + 1
            next_idx = curr + 1
            
            while next_idx < N: # vérifs angulaires
                dot_prod = np.clip(nx[curr]*nx[next_idx] + ny[curr]*ny[next_idx] + nz[curr]*nz[next_idx], -1.0, 1.0)
                angle_diff = np.arccos(dot_prod)
                
                if angle_diff > delta_rad:
                    break
                
                x1, y1 = x[curr], y[curr]
                x2, y2 = x[next_idx], y[next_idx]
                dist_seg = np.hypot(x2 - x1, y2 - y1)
                
                if dist_seg > 1e-8 and next_idx > curr + 1:
                    xk = x[curr+1:next_idx]
                    yk = y[curr+1:next_idx]
                    # Produit vectoriel pour avoir la distance de chaque point à la corde P1-P2
                    d_array = np.abs((x2 - x1) * (yk - y1) - (xk - x1) * (y2 - y1)) / dist_seg
                    
                    if np.any(d_array > intol):
                        break # Un des points intermédiaires sort de la tolérance
                        
                best_valid = next_idx
                next_idx += 1
                
            curr = best_valid
            kept_indices.append(curr)
            
        if kept_indices[-1] != N - 1:
            kept_indices.append(N - 1)
            
        return kept_indices

    def update_data(self):
        try:
            self.z_scale.configure(to=-self.longueur_var.get())
            
            target_z = self.z_visu_var.get()
            x, y, z, nx, ny, nz = self.calculate_profile(target_z)
            
            # Visu étape 4
            kept_indices = self.filter_profile(x, y, nx, ny, nz)
            
            x_f = x[kept_indices]
            y_f = y[kept_indices]
            nx_f = nx[kept_indices]
            ny_f = ny[kept_indices]
            nz_f = nz[kept_indices]

            # Maj graphique
            self.ax.clear()
            self.ax.plot(x, y, color='lightgray', linestyle='--', label=f"Points d'origine ({len(x)})")
            self.ax.plot(x_f, y_f, 'b-o', markersize=3, label=f"Profil filtré ({len(x_f)} pts)")
            
            self.ax.quiver(x_f, y_f, nx_f, ny_f, color='r', alpha=0.6, scale=15, label='Normales 3D (X,Y)')

            self.ax.plot(x_f[0], y_f[0], 'go', markersize=8, label="Point de départ")
            self.ax.set_aspect('equal')
            self.ax.grid(True, linestyle=':', alpha=0.7)
            self.ax.set_title(f"Profil à Z={target_z:.1f}mm | D1={self.d1_var.get()+2*abs(target_z)*np.tan(np.radians(self.angle_var.get())):.2f}mm\nRéduction: {len(x)} -> {len(x_f)} points")
            self.ax.legend(loc="upper right", fontsize="small")
            self.canvas.draw()

            # Maj tableau
            self.tree.delete(*self.tree.get_children())
            for i, idx in enumerate(kept_indices):
                row = (i, f"{x_f[i]:.4f}", f"{y_f[i]:.4f}", f"{z[idx]:.4f}", f"{nx_f[i]:.4f}", f"{ny_f[i]:.4f}", f"{nz_f[i]:.4f}")
                self.tree.insert("", tk.END, values=row)

        except Exception as err:
            print("Erreur lors de la mise à jour :", err)

    def generer_fichier(self):
        longueur = self.longueur_var.get()
        # Génération des 11 profils tous les paliers de 5
        z_levels = np.linspace(0, -longueur, 11)
        filename = "profils_capto_filtres.ascii"
        
        try:
            total_points = 0
            with open(filename, "w") as f:
                for z_val in z_levels:
                    x, y, z, nx, ny, nz = self.calculate_profile(z_val)
                    kept = self.filter_profile(x, y, nx, ny, nz)
                    
                    for idx in kept:
                        # Format X Y Z Nx Ny Nz pour le ASCII à verifier si ca marche
                        f.write(f"{x[idx]:.6f} {y[idx]:.6f} {z[idx]:.6f} {nx[idx]:.6f} {ny[idx]:.6f} {nz[idx]:.6f}\n")
                        total_points += 1
            
            messagebox.showinfo("Export réussi", f"Fichier généré avec succès !\n11 profils exportés.\nTotal points conservés : {total_points}\nEnregistré sous : {filename}")
        except Exception as e:
            messagebox.showerror("Erreur d'export", f"Erreur pendant l'export : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptoGeneratorApp(root)
    root.mainloop()

#pas mal pas mal le programme mon ptit Octavio
