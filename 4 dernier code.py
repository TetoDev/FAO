import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D

class CaptoGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FAO - Générateur Profil Capto & Usinage")
        self.root.geometry("1450x900")

        # Variables Profil
        self.d1_var = tk.DoubleVar(value=38.0)
        self.e_var = tk.DoubleVar(value=2.0)
        self.nb_pt_var = tk.IntVar(value=1000)
        
        # Variables Tolérances
        self.corde_var = tk.DoubleVar(value=0.01)
        self.tol_ang_var = tk.DoubleVar(value=2.0)
        
        # Variables 3D & Outil
        self.angle_var = tk.DoubleVar(value=5.0)
        self.longueur_var = tk.DoubleVar(value=50.0)
        self.diam_outil_var = tk.DoubleVar(value=10.0)
        self.step_down_ratio_var = tk.DoubleVar(value=0.3)
        self.dist_tang_app_var = tk.DoubleVar(value=10.0)
        self.dist_norm_app_var = tk.DoubleVar(value=5.0)
        self.dist_tang_ret_var = tk.DoubleVar(value=10.0)
        self.dist_norm_ret_var = tk.DoubleVar(value=5.0)
        self.nb_pts_tang_var = tk.IntVar(value=5)
        self.nb_pts_norm_var = tk.IntVar(value=3)
        
        # Variables Visu & Export
        self.z_visu_var = tk.DoubleVar(value=0.0)
        self.visu_3d_var = tk.BooleanVar(value=False)
        self.tool_pos_idx_var = tk.IntVar(value=0)
        self.type_export_var = tk.StringVar(value="piece")
        self.normale_export_var = tk.BooleanVar(value=True)

        # Variables Heidenhain
        self.heid_num_outil_var = tk.IntVar(value=108)
        self.heid_vitesse_var = tk.IntVar(value=10000)
        self.heid_avance_var = tk.IntVar(value=1400)
        self.heid_blk_xmin_var = tk.DoubleVar(value=-30.0)
        self.heid_blk_xmax_var = tk.DoubleVar(value=30.0)
        self.heid_blk_ymin_var = tk.DoubleVar(value=-30.0)
        self.heid_blk_ymax_var = tk.DoubleVar(value=30.0)
        self.heid_blk_zmin_var = tk.DoubleVar(value=-50.0)
        self.heid_blk_zmax_var = tk.DoubleVar(value=0.0)
        self.heid_ret_x_var = tk.DoubleVar(value=-200.0)
        self.heid_ret_y_var = tk.DoubleVar(value=225.0)

        self.create_widgets()
        self.update_data()

    def create_widgets(self):
        left_frame = tk.Frame(self.root, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        def bind_enter(widget):
            widget.bind("<Return>", lambda event: self.update_data())

        # --- PARAMETRES GEOMETRIQUES ---
        profil_frame = tk.LabelFrame(left_frame, text="Géométrie Profil (2D)", padx=5, pady=2)
        profil_frame.pack(fill=tk.X, pady=(0, 3))
        tk.Label(profil_frame, text="d1:").grid(row=0, column=0, sticky="w")
        e1 = tk.Entry(profil_frame, textvariable=self.d1_var, width=8); e1.grid(row=0, column=1)
        tk.Label(profil_frame, text="e:").grid(row=0, column=2, sticky="w", padx=(10, 0))
        e2 = tk.Entry(profil_frame, textvariable=self.e_var, width=8); e2.grid(row=0, column=3)
        tk.Label(profil_frame, text="Pts:").grid(row=0, column=4, sticky="w", padx=(10, 0))
        e3 = tk.Entry(profil_frame, textvariable=self.nb_pt_var, width=8); e3.grid(row=0, column=5)
        bind_enter(e1); bind_enter(e2); bind_enter(e3)

        z_frame = tk.LabelFrame(left_frame, text="Volume & Dépouille (3D)", padx=5, pady=2)
        z_frame.pack(fill=tk.X, pady=(0, 3))
        tk.Label(z_frame, text="Angle (°):").grid(row=0, column=0, sticky="w")
        e4 = tk.Entry(z_frame, textvariable=self.angle_var, width=8); e4.grid(row=0, column=1)
        tk.Label(z_frame, text="Hauteur:").grid(row=0, column=2, sticky="w", padx=(10, 0))
        e5 = tk.Entry(z_frame, textvariable=self.longueur_var, width=8); e5.grid(row=0, column=3)
        bind_enter(e4); bind_enter(e5)

        outil_frame = tk.LabelFrame(left_frame, text="Outil & Passes", padx=5, pady=2)
        outil_frame.pack(fill=tk.X, pady=(0, 3))
        tk.Label(outil_frame, text="Diam:").grid(row=0, column=0, sticky="w")
        e6 = tk.Entry(outil_frame, textvariable=self.diam_outil_var, width=8); e6.grid(row=0, column=1)
        tk.Label(outil_frame, text="Step%:").grid(row=0, column=2, sticky="w", padx=(10, 0))
        e_step = tk.Entry(outil_frame, textvariable=self.step_down_ratio_var, width=8); e_step.grid(row=0, column=3)
        bind_enter(e6); bind_enter(e_step)

        app_ret_frame = tk.Frame(outil_frame)
        app_ret_frame.grid(row=1, column=0, columnspan=4, sticky="we", pady=(3, 0))
        tk.Label(app_ret_frame, text="App tang:").grid(row=0, column=0, sticky="w")
        ea1 = tk.Entry(app_ret_frame, textvariable=self.dist_tang_app_var, width=7); ea1.grid(row=0, column=1)
        tk.Label(app_ret_frame, text="norm:").grid(row=0, column=2, sticky="w", padx=(5, 0))
        ea2 = tk.Entry(app_ret_frame, textvariable=self.dist_norm_app_var, width=7); ea2.grid(row=0, column=3)
        tk.Label(app_ret_frame, text="Ret tang:").grid(row=0, column=4, sticky="w", padx=(10, 0))
        er1 = tk.Entry(app_ret_frame, textvariable=self.dist_tang_ret_var, width=7); er1.grid(row=0, column=5)
        tk.Label(app_ret_frame, text="norm:").grid(row=0, column=6, sticky="w", padx=(5, 0))
        er2 = tk.Entry(app_ret_frame, textvariable=self.dist_norm_ret_var, width=7); er2.grid(row=0, column=7)
        bind_enter(ea1); bind_enter(ea2); bind_enter(er1); bind_enter(er2)

        tk.Label(outil_frame, text="Pts tang:").grid(row=2, column=0, sticky="w", pady=(3, 0))
        ep = tk.Entry(outil_frame, textvariable=self.nb_pts_tang_var, width=7); ep.grid(row=2, column=1, pady=(3, 0))
        tk.Label(outil_frame, text="Pts norm:").grid(row=2, column=2, sticky="w", padx=(10, 0), pady=(3, 0))
        en = tk.Entry(outil_frame, textvariable=self.nb_pts_norm_var, width=7); en.grid(row=2, column=3, pady=(3, 0))
        bind_enter(ep); bind_enter(en)

        filtre_frame = tk.LabelFrame(left_frame, text="Filtrage", padx=5, pady=2)
        filtre_frame.pack(fill=tk.X, pady=(0, 3))
        tk.Label(filtre_frame, text="Corde:").grid(row=0, column=0, sticky="w")
        e8 = tk.Entry(filtre_frame, textvariable=self.corde_var, width=8); e8.grid(row=0, column=1)
        tk.Label(filtre_frame, text="Angle:").grid(row=0, column=2, sticky="w", padx=(10, 0))
        e9 = tk.Entry(filtre_frame, textvariable=self.tol_ang_var, width=8); e9.grid(row=0, column=3)
        self.lbl_info_filtre = tk.Label(filtre_frame, text="Pts: - / -", fg="#d32f2f", font=("Arial", 8, "bold"))
        self.lbl_info_filtre.grid(row=0, column=4, padx=(10, 0))
        bind_enter(e8); bind_enter(e9)

        # --- ACTIONS & EXPORT ---
        action_frame = tk.Frame(left_frame, pady=2)
        action_frame.pack(fill=tk.X)
        tk.Label(action_frame, text="Z:").grid(row=0, column=0, sticky="w")
        self.z_scale = tk.Scale(action_frame, variable=self.z_visu_var, from_=0, to=0,
                                resolution=0.01, orient=tk.HORIZONTAL, command=self._on_z_scale_change)
        self.z_scale.grid(row=0, column=1, sticky="ew")
        tk.Checkbutton(action_frame, text="3D", variable=self.visu_3d_var, command=self.update_data).grid(row=0, column=2, padx=3)
        tk.Button(action_frame, text="Actualiser", command=self.update_data, bg="#2196F3", fg="white", font=("Arial", 8)).grid(row=0, column=3, padx=3)

        tool_viz_frame = tk.LabelFrame(left_frame, text="Outil", padx=5, pady=2)
        tool_viz_frame.pack(fill=tk.X, pady=(0, 3))
        tk.Label(tool_viz_frame, text="Pos:").grid(row=0, column=0, sticky="w")
        self.lbl_tool_pos = tk.Label(tool_viz_frame, text="0 / 0", fg="#d32f2f", font=("Arial", 8, "bold"))
        self.lbl_tool_pos.grid(row=0, column=1, padx=5)
        self.tool_scale = tk.Scale(tool_viz_frame, variable=self.tool_pos_idx_var, from_=0, to=0,
                                   resolution=1, orient=tk.HORIZONTAL, command=self._on_tool_pos_change)
        self.tool_scale.grid(row=0, column=2, sticky="ew")

        export_frame = tk.LabelFrame(left_frame, text="Exportation", padx=5, pady=2)
        export_frame.pack(fill=tk.X, pady=(0, 3))
        tk.Radiobutton(export_frame, text="Profil Pièce", variable=self.type_export_var, value="piece").grid(row=0, column=0, sticky="w")
        tk.Radiobutton(export_frame, text="Trajectoire Outil", variable=self.type_export_var, value="outil").grid(row=0, column=1, sticky="w")
        tk.Checkbutton(export_frame, text="Normales", variable=self.normale_export_var).grid(row=0, column=2, sticky="w", padx=(10, 0))
        tk.Button(export_frame, text="ASCII", command=self.generer_fichier_ui, bg="#FF9800", fg="white", font=("Arial", 8, "bold")).grid(row=0, column=3, padx=(10, 0))
        tk.Button(export_frame, text="APT", command=self.generer_fichier_apt, bg="#9C27B0", fg="white", font=("Arial", 8, "bold")).grid(row=0, column=4, padx=(3, 0))

        heid_frame = tk.LabelFrame(left_frame, text="Paramètres Heidenhain", padx=5, pady=2)
        heid_frame.pack(fill=tk.X, pady=(0, 5))

        heid_canvas = tk.Canvas(heid_frame, height=80, highlightthickness=0)
        heid_scroll = ttk.Scrollbar(heid_frame, orient="vertical", command=heid_canvas.yview)
        heid_inner = tk.Frame(heid_canvas)
        heid_inner.bind("<Configure>", lambda e: heid_canvas.configure(scrollregion=heid_canvas.bbox("all")))
        heid_canvas.create_window((0, 0), window=heid_inner, anchor="nw")
        heid_canvas.configure(yscrollcommand=heid_scroll.set)
        heid_canvas.pack(side="left", fill="x", expand=True)
        heid_scroll.pack(side="right", fill="y")

        tk.Label(heid_inner, text="N° Outil:").grid(row=0, column=0, sticky="w")
        tk.Entry(heid_inner, textvariable=self.heid_num_outil_var, width=6).grid(row=0, column=1, sticky="w", padx=(5, 10))
        tk.Label(heid_inner, text="Vitesse (RPM):").grid(row=0, column=2, sticky="w")
        tk.Entry(heid_inner, textvariable=self.heid_vitesse_var, width=7).grid(row=0, column=3, sticky="w", padx=(5, 0))
        tk.Label(heid_inner, text="Avance F:").grid(row=1, column=0, sticky="w")
        tk.Entry(heid_inner, textvariable=self.heid_avance_var, width=6).grid(row=1, column=1, sticky="w", padx=(5, 10))
        tk.Label(heid_inner, text="BLK X:").grid(row=2, column=0, sticky="w")
        tk.Entry(heid_inner, textvariable=self.heid_blk_xmin_var, width=6).grid(row=2, column=1, sticky="w")
        tk.Label(heid_inner, text="→").grid(row=2, column=2, sticky="w")
        tk.Entry(heid_inner, textvariable=self.heid_blk_xmax_var, width=6).grid(row=2, column=3, sticky="w")
        tk.Label(heid_inner, text="Y:").grid(row=3, column=0, sticky="w")
        tk.Entry(heid_inner, textvariable=self.heid_blk_ymin_var, width=6).grid(row=3, column=1, sticky="w")
        tk.Label(heid_inner, text="→").grid(row=3, column=2, sticky="w")
        tk.Entry(heid_inner, textvariable=self.heid_blk_ymax_var, width=6).grid(row=3, column=3, sticky="w")
        tk.Label(heid_inner, text="Z:").grid(row=4, column=0, sticky="w")
        tk.Entry(heid_inner, textvariable=self.heid_blk_zmin_var, width=6).grid(row=4, column=1, sticky="w")
        tk.Label(heid_inner, text="→").grid(row=4, column=2, sticky="w")
        tk.Entry(heid_inner, textvariable=self.heid_blk_zmax_var, width=6).grid(row=4, column=3, sticky="w")
        tk.Label(heid_inner, text="Retrait X:").grid(row=5, column=0, sticky="w")
        tk.Entry(heid_inner, textvariable=self.heid_ret_x_var, width=6).grid(row=5, column=1, sticky="w", padx=(5, 10))
        tk.Label(heid_inner, text="Y:").grid(row=5, column=2, sticky="w")
        tk.Entry(heid_inner, textvariable=self.heid_ret_y_var, width=6).grid(row=5, column=3, sticky="w")
        tk.Button(heid_inner, text="Générer Fichier Heidenhain (.H)", command=self.generer_fichier_heidenhain, bg="#4CAF50", fg="white", font=("Arial", 9, "bold")).grid(row=6, column=0, columnspan=4, pady=(10, 5), sticky="we")

        # --- TABLEAU ---
        table_frame = tk.LabelFrame(left_frame, text="Données (Trajectoire Outil Affichée)")
        table_frame.pack(fill=tk.BOTH, expand=True)
        columns = ("Type", "X", "Y", "Z", "Nx", "Ny", "Nz")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=50, anchor="center")
        self.tree.column("Type", width=75)
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # --- GRAPHIQUE ---
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _on_z_scale_change(self, value):
        snapped = self.snap_to_z_level(float(value))
        self.z_visu_var.set(snapped)
        self.update_data()

    def _on_tool_pos_change(self, value):
        self.update_data()

    def snap_to_z_level(self, value):
        z_levels = self.get_z_levels()
        idx = np.argmin(np.abs(z_levels - value))
        return z_levels[idx]

    def get_tool_rect_corners(self, x_center, y_center, nx, ny):
        diam = self.diam_outil_var.get()
        half_w = diam / 2.0

        tx = -ny
        ty = nx

        p1 = [x_center - half_w * tx, y_center - half_w * ty]
        p2 = [x_center + half_w * tx, y_center + half_w * ty]
        p3 = [x_center + half_w * tx + diam * nx, y_center + half_w * ty + diam * ny]
        p4 = [x_center - half_w * tx + diam * nx, y_center - half_w * ty + diam * ny]

        return p1, p2, p3, p4

    def calculate_profile(self, target_z):
        d1 = self.d1_var.get()
        e = self.e_var.get()
        nb_pt = self.nb_pt_var.get()
        angle_depouille = np.radians(self.angle_var.get())

        d1_z = d1 + 2 * abs(target_z) * np.tan(angle_depouille)
        e_z = e * (d1_z / d1)
        a = np.linspace(0, 2 * np.pi, nb_pt)
        
        x = (d1_z / 2 - e_z * np.cos(3 * a)) * np.cos(a) - 3 * e_z * np.sin(3 * a) * np.sin(a)
        y = (d1_z / 2 - e_z * np.cos(3 * a)) * np.sin(a) + 3 * e_z * np.sin(3 * a) * np.cos(a)
        z = np.full_like(x, target_z)

        dx_da = -(d1_z / 2) * np.sin(a) - 8 * e_z * np.cos(3 * a) * np.sin(a)
        dy_da = (d1_z / 2) * np.cos(a) + 8 * e_z * np.cos(3 * a) * np.cos(a)
        norm_2d = np.hypot(dx_da, dy_da)
        
        tx_2d = dx_da / norm_2d
        ty_2d = dy_da / norm_2d

        nx_2d = dy_da / norm_2d
        ny_2d = -dx_da / norm_2d

        nx_3d = nx_2d * np.cos(angle_depouille)
        ny_3d = ny_2d * np.cos(angle_depouille)
        nz_3d = np.full_like(nx_2d, np.sin(angle_depouille))

        R = self.diam_outil_var.get() / 2.0
        xc = x - R * tx_2d
        yc = y - R * ty_2d
        zc = z.copy()

        return x, y, z, nx_3d, ny_3d, nz_3d, xc, yc, zc, tx_2d, ty_2d

    def filter_profile(self, x, y, nx, ny, nz):
        intol = self.corde_var.get()
        delta_rad = np.radians(self.tol_ang_var.get())
        kept_indices = [0]
        curr = 0
        N = len(x)

        while curr < N - 1:
            best_valid = curr + 1
            next_idx = curr + 1
            while next_idx < N:
                dot_prod = np.clip(nx[curr]*nx[next_idx] + ny[curr]*ny[next_idx] + nz[curr]*nz[next_idx], -1.0, 1.0)
                if np.arccos(dot_prod) > delta_rad:
                    break
                
                x1, y1 = x[curr], y[curr]
                x2, y2 = x[next_idx], y[next_idx]
                dist_seg = np.hypot(x2 - x1, y2 - y1)
                
                if dist_seg > 1e-8 and next_idx > curr + 1:
                    d_array = np.abs((x2 - x1) * (y[curr+1:next_idx] - y1) - (x[curr+1:next_idx] - x1) * (y2 - y1)) / dist_seg
                    if np.any(d_array > intol):
                        break 
                        
                best_valid = next_idx
                next_idx += 1
                
            curr = best_valid
            kept_indices.append(curr)
            
        if kept_indices[-1] != N - 1:
            kept_indices.append(N - 1)
            
        return kept_indices

    def get_z_levels(self):
        longueur = self.longueur_var.get()
        diam_outil = self.diam_outil_var.get()
        ratio = self.step_down_ratio_var.get()
        step = diam_outil * ratio
        if step <= 0:
            step = 1.0
        num_passes = max(2, int(np.ceil(longueur / step)) + 1)
        total_span = (num_passes - 1) * step
        offset = total_span - longueur
        return np.array([offset - i * step for i in range(num_passes)])

    def add_approach_retract(self, xc_f, yc_f, zc_f, nx_f, ny_f, tx_start, ty_start, tx_end, ty_end):
        dist_tang_app = self.dist_tang_app_var.get()
        dist_norm_app = self.dist_norm_app_var.get()
        dist_tang_ret = self.dist_tang_ret_var.get()
        dist_norm_ret = self.dist_norm_ret_var.get()
        nb_pts_tang = self.nb_pts_tang_var.get()
        nb_pts_norm = self.nb_pts_norm_var.get()

        nx_out_start = nx_f[0]
        ny_out_start = ny_f[0]

        x_safe = xc_f[0] - dist_tang_app * tx_start + dist_norm_app * nx_out_start
        y_safe = yc_f[0] - dist_tang_app * ty_start + dist_norm_app * ny_out_start

        x_tang_start = xc_f[0] - dist_tang_app * tx_start
        y_tang_start = yc_f[0] - dist_tang_app * ty_start

        t = np.linspace(0, 1, nb_pts_norm)
        app_x = x_safe + (x_tang_start - x_safe) * t
        app_y = y_safe + (y_tang_start - y_safe) * t
        app_z = np.full(nb_pts_norm, zc_f[0])

        t2 = np.linspace(0, 1, nb_pts_tang)
        app_tang_x = x_tang_start + (xc_f[0] - x_tang_start) * t2
        app_tang_y = y_tang_start + (yc_f[0] - y_tang_start) * t2
        app_tang_z = np.full(nb_pts_tang, zc_f[0])

        nx_out_end = nx_f[-1]
        ny_out_end = ny_f[-1]

        x_tang_end = xc_f[-1] + dist_tang_ret * tx_end
        y_tang_end = yc_f[-1] + dist_tang_ret * ty_end

        t3 = np.linspace(0, 1, nb_pts_tang)
        ret_tang_x = xc_f[-1] + (x_tang_end - xc_f[-1]) * t3
        ret_tang_y = yc_f[-1] + (y_tang_end - yc_f[-1]) * t3
        ret_tang_z = np.full(nb_pts_tang, zc_f[-1])

        x_unsafe = x_tang_end + dist_norm_ret * nx_out_end
        y_unsafe = y_tang_end + dist_norm_ret * ny_out_end

        t4 = np.linspace(0, 1, nb_pts_norm)
        ret_x = x_tang_end + (x_unsafe - x_tang_end) * t4
        ret_y = y_tang_end + (y_unsafe - y_tang_end) * t4
        ret_z = np.full(nb_pts_norm, zc_f[-1])

        return app_x, app_y, app_z, app_tang_x, app_tang_y, app_tang_z, ret_tang_x, ret_tang_y, ret_tang_z, ret_x, ret_y, ret_z

    def update_data(self):
        try:
            z_levels = self.get_z_levels()
            self.z_scale.configure(from_=z_levels[0], to=z_levels[-1])
            target_z = self.snap_to_z_level(self.z_visu_var.get())
            self.z_visu_var.set(target_z)
            
            x, y, z, nx, ny, nz, xc, yc, zc, tx, ty = self.calculate_profile(target_z)
            kept = self.filter_profile(x, y, nx, ny, nz)
            
            self.lbl_info_filtre.config(text=f"Points conservés : {len(kept)} / {len(x)}")
            
            x_f, y_f, z_f = x[kept], y[kept], z[kept]
            xc_f, yc_f, zc_f = xc[kept], yc[kept], zc[kept]
            nx_f, ny_f, nz_f = nx[kept], ny[kept], nz[kept]
            tx_f, ty_f = tx[kept], ty[kept]

            max_idx = max(0, len(kept) - 1)
            self.tool_scale.configure(to=max_idx)
            tool_idx = min(self.tool_pos_idx_var.get(), max_idx)
            self.tool_pos_idx_var.set(tool_idx)
            self.lbl_tool_pos.config(text=f"{tool_idx} / {max_idx}")

            app_x, app_y, app_z, app_tang_x, app_tang_y, app_tang_z, ret_tang_x, ret_tang_y, ret_tang_z, ret_x, ret_y, ret_z = self.add_approach_retract(xc_f, yc_f, zc_f, nx_f, ny_f, tx_f[0], ty_f[0], tx_f[-1], ty_f[-1])

            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", tk.END, values=(f"APPR NORMALE ({len(app_x)})", f"{app_x[0]:.3f}", f"{app_y[0]:.3f}", f"{app_z[0]:.3f}", f"{nx_f[0]:.3f}", f"{ny_f[0]:.3f}", f"{nz_f[0]:.3f}"))
            self.tree.insert("", tk.END, values=(f"APPR TANG ({len(app_tang_x)})", f"{app_tang_x[-1]:.3f}", f"{app_tang_y[-1]:.3f}", f"{app_tang_z[-1]:.3f}", f"{nx_f[0]:.3f}", f"{ny_f[0]:.3f}", f"{nz_f[0]:.3f}"))
            for i in range(len(kept)):
                self.tree.insert("", tk.END, values=("USINAGE", f"{xc_f[i]:.3f}", f"{yc_f[i]:.3f}", f"{zc_f[i]:.3f}", f"{nx_f[i]:.3f}", f"{ny_f[i]:.3f}", f"{nz_f[i]:.3f}"))
            self.tree.insert("", tk.END, values=(f"RET TANG ({len(ret_tang_x)})", f"{ret_tang_x[-1]:.3f}", f"{ret_tang_y[-1]:.3f}", f"{ret_tang_z[-1]:.3f}", f"{nx_f[-1]:.3f}", f"{ny_f[-1]:.3f}", f"{nz_f[-1]:.3f}"))
            self.tree.insert("", tk.END, values=(f"RET NORMALE ({len(ret_x)})", f"{ret_x[-1]:.3f}", f"{ret_y[-1]:.3f}", f"{ret_z[-1]:.3f}", f"{nx_f[-1]:.3f}", f"{ny_f[-1]:.3f}", f"{nz_f[-1]:.3f}"))

            if self.visu_3d_var.get():
                self.plot_3d(x, y, z, x_f, y_f, z_f, xc_f, yc_f, zc_f, app_x, app_y, app_z, app_tang_x, app_tang_y, app_tang_z, ret_tang_x, ret_tang_y, ret_tang_z, ret_x, ret_y, ret_z, nx_f, ny_f, nz_f, target_z, tool_idx)
            else:
                self.plot_2d(x, y, x_f, y_f, xc_f, yc_f, app_x, app_y, app_tang_x, app_tang_y, ret_tang_x, ret_tang_y, ret_x, ret_y, target_z, tool_idx, nx_f, ny_f)

        except Exception as err:
            import traceback
            traceback.print_exc()
            print("Erreur globale détectée :", err)

    def plot_2d(self, x, y, x_f, y_f, xc_f, yc_f, app_x, app_y, app_tang_x, app_tang_y, ret_tang_x, ret_tang_y, ret_x, ret_y, target_z, tool_idx, nx_f, ny_f):
        if hasattr(self, 'ax') and self.ax.name == '3d':
            for widget in self.plot_frame.winfo_children():
                widget.destroy()
            self.fig.clf()
            self.ax = self.fig.add_subplot(111)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.ax.clear()
        self.ax.plot(x, y, color='tab:blue', alpha=0.4, linestyle=':', label="Géométrie brute de la pièce")
        self.ax.plot(x_f, y_f, 'b-', linewidth=1.5, label="Profil de contact (Fraise/Pièce)")
        self.ax.plot(xc_f, yc_f, 'r--', linewidth=1.2, label="Trajectoire Point Piloté (Centre outil)")
        self.ax.plot(xc_f, yc_f, 'ro', markersize=3)
        self.ax.plot(app_x, app_y, 'c-o', linewidth=2, markersize=4, label="Approche normale")
        self.ax.plot(app_tang_x, app_tang_y, 'g-o', linewidth=2, markersize=4, label="Approche tangente")
        self.ax.plot(ret_tang_x, ret_tang_y, 'm-o', linewidth=2, markersize=4, label="Retrait tangent")
        self.ax.plot(ret_x, ret_y, 'y-s', linewidth=2, markersize=4, label="Retrait normale")

        for i in range(0, len(x_f), max(1, len(x_f)//30)):
            self.ax.plot([x_f[i], xc_f[i]], [y_f[i], yc_f[i]], color='gray', alpha=0.5, linewidth=0.8)

        if tool_idx < len(x_f):
            p1, p2, p3, p4 = self.get_tool_rect_corners(xc_f[tool_idx], yc_f[tool_idx], nx_f[tool_idx], ny_f[tool_idx])
            rx = [p1[0], p2[0], p3[0], p4[0], p1[0]]
            ry = [p1[1], p2[1], p3[1], p4[1], p1[1]]
            self.ax.fill(rx, ry, color='orange', alpha=0.25)
            self.ax.plot(rx, ry, 'orange', linewidth=2, label=f"Outil (pos {tool_idx})")
            self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'orange', linewidth=3)

        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle=':', alpha=0.6)
        self.ax.set_title(f"Z = {target_z:.1f} mm | Diamètre outil : {self.diam_outil_var.get()} mm")
        self.ax.legend(loc="upper right", fontsize="small")
        self.canvas.draw()

    def plot_3d(self, x, y, z, x_f, y_f, z_f, xc_f, yc_f, zc_f, app_x, app_y, app_z, app_tang_x, app_tang_y, app_tang_z, ret_tang_x, ret_tang_y, ret_tang_z, ret_x, ret_y, ret_z, nx_f, ny_f, nz_f, target_z, tool_idx):
        if not hasattr(self, 'ax') or self.ax.name != '3d':
            for widget in self.plot_frame.winfo_children():
                widget.destroy()
            self.fig.clf()
            self.ax = self.fig.add_subplot(111, projection='3d')
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.ax.clear()

        z_levels = self.get_z_levels()

        all_xc, all_yc, all_zc = [], [], []
        all_xf, all_yf, all_zf = [], [], []

        for zv in z_levels:
            xv, yv, zv_arr, nxv, nyv, nzv, xcv, ycv, zcv, txv, tyv = self.calculate_profile(zv)
            kept_v = self.filter_profile(xv, yv, nxv, nyv, nzv)
            all_xc.extend(xcv[kept_v])
            all_yc.extend(ycv[kept_v])
            all_zc.extend(zcv[kept_v])
            all_xf.extend(xv[kept_v])
            all_yf.extend(yv[kept_v])
            all_zf.extend(zv_arr[kept_v])

        self.ax.scatter(all_xf, all_yf, all_zf, c='blue', s=5, alpha=0.4, label="Profil de contact (tous Z)")
        self.ax.scatter(all_xc, all_yc, all_zc, c='red', s=8, alpha=0.6, label="Trajectoire outil (tous Z)")

        self.ax.plot(x_f, y_f, np.full_like(x_f, target_z), 'b-', linewidth=1.5, alpha=0.8)
        self.ax.plot(xc_f, yc_f, zc_f, 'r--', linewidth=1.5, alpha=0.8)
        self.ax.plot(app_x, app_y, app_z, 'c-o', linewidth=2, markersize=4, label="Approche normale")
        self.ax.plot(app_tang_x, app_tang_y, app_tang_z, 'g-o', linewidth=2, markersize=4, label="Approche tangente")
        self.ax.plot(ret_tang_x, ret_tang_y, ret_tang_z, 'm-o', linewidth=2, markersize=4, label="Retrait tangent")
        self.ax.plot(ret_x, ret_y, ret_z, 'y-s', linewidth=2, markersize=4, label="Retrait normale")

        for i in range(0, len(x_f), max(1, len(x_f)//15)):
            self.ax.plot([x_f[i], xc_f[i]], [y_f[i], yc_f[i]], [target_z, zc_f[i]], color='gray', alpha=0.4, linewidth=0.6)

        if tool_idx < len(x_f):
            p1, p2, p3, p4 = self.get_tool_rect_corners(xc_f[tool_idx], yc_f[tool_idx], nx_f[tool_idx], ny_f[tool_idx])
            z_tool = target_z
            rx = [p1[0], p2[0], p3[0], p4[0], p1[0]]
            ry = [p1[1], p2[1], p3[1], p4[1], p1[1]]
            rz = [z_tool, z_tool, z_tool, z_tool, z_tool]
            self.ax.plot(rx, ry, rz, 'orange', linewidth=2, label=f"Outil (pos {tool_idx})")
            self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [z_tool, z_tool], 'orange', linewidth=3)

        self.ax.set_xlabel('X (mm)')
        self.ax.set_ylabel('Y (mm)')
        self.ax.set_zlabel('Z (mm)')
        self.ax.set_title(f"Vue 3D | Z courant = {target_z:.1f} mm")
        self.ax.legend(loc="upper right", fontsize="small")
        self.canvas.draw()

    def generer_fichier_ui(self):
        mode = self.type_export_var.get()
        avec_normales = self.normale_export_var.get()
        self.generer_fichier(mode, avec_normales)

    def generer_fichier(self, mode, avec_normales):
        z_levels = self.get_z_levels()
        
        prefix = "profil_piece" if mode == "piece" else "trajectoire_outil"
        suffix = "6col" if avec_normales else "3col"
        filename = f"{prefix}_{suffix}.ascii"
        
        try:
            total_points = 0
            with open(filename, "w") as f:
                for z_val in z_levels:
                    x, y, z, nx, ny, nz, xc, yc, zc, tx, ty = self.calculate_profile(z_val)
                    kept = self.filter_profile(x, y, nx, ny, nz)
                    
                    if mode == "piece":
                        x_f, y_f, z_f = x[kept], y[kept], z[kept]
                        nx_f, ny_f, nz_f = nx[kept], ny[kept], nz[kept]
                        
                        for idx in range(len(kept)):
                            # Anti-doublon: Ignore le dernier point s'il boucle sur le premier
                            if idx == len(kept) - 1 and np.allclose([x_f[idx], y_f[idx]], [x_f[0], y_f[0]]):
                                continue
                                
                            if avec_normales:
                                f.write(f"{x_f[idx]:.6f} {y_f[idx]:.6f} {z_f[idx]:.6f} {nx_f[idx]:.6f} {ny_f[idx]:.6f} {nz_f[idx]:.6f}\n")
                            else:
                                f.write(f"{x_f[idx]:.6f} {y_f[idx]:.6f} {z_f[idx]:.6f}\n")
                            total_points += 1
                            
                    elif mode == "outil":
                        xc_f, yc_f, zc_f = xc[kept], yc[kept], zc[kept]
                        nx_f, ny_f, nz_f = nx[kept], ny[kept], nz[kept]
                        tx_f, ty_f = tx[kept], ty[kept]
                        app_x, app_y, app_z, app_tang_x, app_tang_y, app_tang_z, ret_tang_x, ret_tang_y, ret_tang_z, ret_x, ret_y, ret_z = self.add_approach_retract(xc_f, yc_f, zc_f, nx_f, ny_f, tx_f[0], ty_f[0], tx_f[-1], ty_f[-1])

                        for idx in range(len(app_x)):
                            if avec_normales:
                                f.write(f"{app_x[idx]:.6f} {app_y[idx]:.6f} {app_z[idx]:.6f} {nx_f[0]:.6f} {ny_f[0]:.6f} {nz_f[0]:.6f}\n")
                            else:
                                f.write(f"{app_x[idx]:.6f} {app_y[idx]:.6f} {app_z[idx]:.6f}\n")
                            total_points += 1

                        for idx in range(len(app_tang_x)):
                            if avec_normales:
                                f.write(f"{app_tang_x[idx]:.6f} {app_tang_y[idx]:.6f} {app_tang_z[idx]:.6f} {nx_f[0]:.6f} {ny_f[0]:.6f} {nz_f[0]:.6f}\n")
                            else:
                                f.write(f"{app_tang_x[idx]:.6f} {app_tang_y[idx]:.6f} {app_tang_z[idx]:.6f}\n")
                            total_points += 1

                        for idx in range(len(kept)):
                            if avec_normales:
                                f.write(f"{xc_f[idx]:.6f} {yc_f[idx]:.6f} {zc_f[idx]:.6f} {nx_f[idx]:.6f} {ny_f[idx]:.6f} {nz_f[idx]:.6f}\n")
                            else:
                                f.write(f"{xc_f[idx]:.6f} {yc_f[idx]:.6f} {zc_f[idx]:.6f}\n")
                            total_points += 1

                        for idx in range(len(ret_tang_x)):
                            if avec_normales:
                                f.write(f"{ret_tang_x[idx]:.6f} {ret_tang_y[idx]:.6f} {ret_tang_z[idx]:.6f} {nx_f[-1]:.6f} {ny_f[-1]:.6f} {nz_f[-1]:.6f}\n")
                            else:
                                f.write(f"{ret_tang_x[idx]:.6f} {ret_tang_y[idx]:.6f} {ret_tang_z[idx]:.6f}\n")
                            total_points += 1

                        for idx in range(len(ret_x)):
                            if avec_normales:
                                f.write(f"{ret_x[idx]:.6f} {ret_y[idx]:.6f} {ret_z[idx]:.6f} {nx_f[-1]:.6f} {ny_f[-1]:.6f} {nz_f[-1]:.6f}\n")
                            else:
                                f.write(f"{ret_x[idx]:.6f} {ret_y[idx]:.6f} {ret_z[idx]:.6f}\n")
                            total_points += 1

                    # Ligne vide pour scinder les trajectoires Z
                    f.write("\n")
            
            msg = f"Fichier '{filename}' généré avec succès.\nTotal : {total_points} points."
            if mode == "piece":
                msg += "\n(Points d'approche et doublons retirés pour CATIA)."
            messagebox.showinfo("Exportation Terminée", msg)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec lors de l'écriture : {e}")

    def _normals_to_bc(self, nx, ny, nz):
        B = -np.arccos(np.clip(nz, -1.0, 1.0))
        sin_B = np.sin(B)
        
        if abs(sin_B) < 1e-8:
            return np.degrees(B), 0.0
            
        ratio = np.clip(nx / sin_B, -1.0, 1.0)

        val = ny / sin_B
        sign_val = -1.0 if val <= 0.0 else 1.0
        
        C = np.arccos(ratio) * sign_val
        return np.degrees(B), np.degrees(C)

    def generer_fichier_apt(self):
        z_levels = self.get_z_levels()
        filename = "trajectoire_outil.APT"

        try:
            total_points = 0
            with open(filename, "w") as f:
                f.write("$$ APT generated by FAO Capto Generator\n")
                f.write("$$\n")
                f.write("CUTCOM/ OFF\n")
                f.write("MULTAX\n")
                f.write("SPINDL/ 5000, RPM, CLW\n")

                for z_idx, z_val in enumerate(z_levels):
                    x, y, z, nx, ny, nz, xc, yc, zc, tx, ty = self.calculate_profile(z_val)
                    kept = self.filter_profile(x, y, nx, ny, nz)
                    xc_f, yc_f, zc_f = xc[kept], yc[kept], zc[kept]
                    nx_f, ny_f, nz_f = nx[kept], ny[kept], nz[kept]
                    tx_f, ty_f = tx[kept], ty[kept]
                    app_x, app_y, app_z, app_tang_x, app_tang_y, app_tang_z, ret_tang_x, ret_tang_y, ret_tang_z, ret_x, ret_y, ret_z = self.add_approach_retract(xc_f, yc_f, zc_f, nx_f, ny_f, tx_f[0], ty_f[0], tx_f[-1], ty_f[-1])

                    f.write(f"$$ Passe Z {z_idx + 1}/{len(z_levels)} : Z = {z_val:.3f} mm\n")
                    f.write("RAPID\n")

                    for idx in range(len(app_x)):
                        f.write(f"GOTO/ {app_x[idx]:.5f}, {app_y[idx]:.5f}, {app_z[idx]:.5f}, {nx_f[0]:.6f}, {ny_f[0]:.6f}, {nz_f[0]:.6f}\n")
                        total_points += 1

                    for idx in range(len(app_tang_x)):
                        f.write(f"GOTO/ {app_tang_x[idx]:.5f}, {app_tang_y[idx]:.5f}, {app_tang_z[idx]:.5f}, {nx_f[0]:.6f}, {ny_f[0]:.6f}, {nz_f[0]:.6f}\n")
                        total_points += 1

                    for idx in range(len(kept)):
                        f.write(f"GOTO/ {xc_f[idx]:.5f}, {yc_f[idx]:.5f}, {zc_f[idx]:.5f}, {nx_f[idx]:.6f}, {ny_f[idx]:.6f}, {nz_f[idx]:.6f}\n")
                        total_points += 1

                    for idx in range(len(ret_tang_x)):
                        f.write(f"GOTO/ {ret_tang_x[idx]:.5f}, {ret_tang_y[idx]:.5f}, {ret_tang_z[idx]:.5f}, {nx_f[-1]:.6f}, {ny_f[-1]:.6f}, {nz_f[-1]:.6f}\n")
                        total_points += 1

                    for idx in range(len(ret_x)):
                        f.write(f"GOTO/ {ret_x[idx]:.5f}, {ret_y[idx]:.5f}, {ret_z[idx]:.5f}, {nx_f[-1]:.6f}, {ny_f[-1]:.6f}, {nz_f[-1]:.6f}\n")
                        total_points += 1

                f.write("SPINDL/ OFF\n")
                f.write("REWIND/ 0\n")
                f.write("END\n")

            messagebox.showinfo("Exportation APT Terminée", f"Fichier '{filename}' généré avec succès.\nTotal : {total_points} points GOTO sur {len(z_levels)} passes Z.")

        except Exception as e:
            messagebox.showerror("Erreur", f"Échec lors de l'écriture APT : {e}")

    def _to_machine_coords(self, x, y, z, B_deg, C_deg):
        B = np.radians(B_deg)
        C = np.radians(C_deg)
        x_prime = (x * np.cos(B) * np.cos(C) + y * np.cos(B) * np.sin(C)) - z * np.sin(B)
        y_prime = -x * np.sin(C) + y * np.cos(C)
        z_prime = (x * np.sin(B) * np.cos(C) + y * np.sin(B) * np.sin(C)) + z * np.cos(B)
        return x_prime, y_prime, z_prime

    def generer_fichier_heidenhain(self):
        from datetime import datetime
        z_levels = self.get_z_levels()
        today = datetime.now().strftime("%d/%m/%Y")
        filename = f"Capto_{datetime.now().strftime('%d%m%Y')}.H"

        num_outil = self.heid_num_outil_var.get()
        vitesse = self.heid_vitesse_var.get()
        avance = self.heid_avance_var.get()
        xmin = self.heid_blk_xmin_var.get()
        xmax = self.heid_blk_xmax_var.get()
        ymin = self.heid_blk_ymin_var.get()
        ymax = self.heid_blk_ymax_var.get()
        zmin = self.heid_blk_zmin_var.get()
        zmax = self.heid_blk_zmax_var.get()
        ret_x = self.heid_ret_x_var.get()
        ret_y = self.heid_ret_y_var.get()

        try:
            all_points = []
            total_points = 0

            for z_idx, z_val in enumerate(z_levels):
                x, y, z, nx, ny, nz, xc, yc, zc, tx, ty = self.calculate_profile(z_val)
                kept = self.filter_profile(x, y, nx, ny, nz)
                xc_f, yc_f, zc_f = xc[kept], yc[kept], zc[kept]
                nx_f, ny_f, nz_f = nx[kept], ny[kept], nz[kept]
                tx_f, ty_f = tx[kept], ty[kept]
                app_x, app_y, app_z, app_tang_x, app_tang_y, app_tang_z, ret_tang_x, ret_tang_y, ret_tang_z, ret_x_arr, ret_y_arr, ret_z_arr = self.add_approach_retract(xc_f, yc_f, zc_f, nx_f, ny_f, tx_f[0], ty_f[0], tx_f[-1], ty_f[-1])

                all_points.append(("comment", f"; Passe Z {z_idx + 1}/{len(z_levels)} : Z = {z_val:.3f} mm"))

                for idx in range(len(app_x)):
                    B, C = self._normals_to_bc(nx_f[0], ny_f[0], nz_f[0])
                    C = -180.0  
                    xp, yp, zp = self._to_machine_coords(app_x[idx], app_y[idx], app_z[idx], B, C)
                    all_points.append(("data", xp, yp, zp, B, C))
                    total_points += 1

                for idx in range(len(app_tang_x)):
                    B, C = self._normals_to_bc(nx_f[0], ny_f[0], nz_f[0])
                    C = -180.0  
                    xp, yp, zp = self._to_machine_coords(app_tang_x[idx], app_tang_y[idx], app_tang_z[idx], B, C)
                    all_points.append(("data", xp, yp, zp, B, C))
                    total_points += 1

                for idx in range(len(kept)):
                    B, C = self._normals_to_bc(nx_f[idx], ny_f[idx], nz_f[idx])
                    xp, yp, zp = self._to_machine_coords(xc_f[idx], yc_f[idx], zc_f[idx], B, C)
                    all_points.append(("data", xp, yp, zp, B, C))
                    total_points += 1

                for idx in range(len(ret_tang_x)):
                    B, C = self._normals_to_bc(nx_f[-1], ny_f[-1], nz_f[-1])
                    xp, yp, zp = self._to_machine_coords(ret_tang_x[idx], ret_tang_y[idx], ret_tang_z[idx], B, C)
                    all_points.append(("data", xp, yp, zp, B, C))
                    total_points += 1

                for idx in range(len(ret_x_arr)):
                    B, C = self._normals_to_bc(nx_f[-1], ny_f[-1], nz_f[-1])
                    xp, yp, zp = self._to_machine_coords(ret_x_arr[idx], ret_y_arr[idx], ret_z_arr[idx], B, C)
                    all_points.append(("data", xp, yp, zp, B, C))
                    total_points += 1

            with open(filename, "w") as f:
                f.write(f"BEGIN PGM Capto MM\n")
                f.write(f";postprocesse le {today}\n")
                f.write(f"BLK FORM 0.1 Z X{xmin} Y{ymin} Z{zmin}\n")
                f.write(f"BLK FORM 0.2 X{xmax} Y{ymax} Z{zmax}\n")
                f.write(";\n")
                f.write("FN 18: SYSREAD Q30 = ID230 NR3 IDX3\n")
                f.write("L ZQ30 R0 FMAX M91\n")
                f.write("M129\n")
                f.write("PLANE RESET TURN FMAX\n")
                f.write(f"TOOL CALL {num_outil} Z S{vitesse} F{avance}\n")
                f.write(f"TOOL CALL S{vitesse}\n")
                f.write("M3 M8\n")
                f.write("M126\n")

                first = all_points[1]
                f.write(f"L X{first[1]:.3f} Y{first[2]:.3f} R0 FMAX\n")
                f.write(f"L B{first[4]:.3f} C{first[5]:.3f} F{avance}\n")
                f.write("M114\n")

                for pt in all_points:
                    if pt[0] == "comment":
                        f.write(f"{pt[1]}\n")
                    else:
                        f.write(f"L X{pt[1]:.3f} Y{pt[2]:.3f} Z{pt[3]:.3f} B{pt[4]:.3f} C{pt[5]:.3f}\n")

                f.write("M127 M115\n")
                f.write("M9\n")
                f.write("L M140 MB MAX\n")
                f.write("M5\n")
                f.write("M129\n")
                f.write(f"L Y{ret_y:.3f} FMAX M92\n")
                f.write("PLANE RESET TURN FMAX\n")
                f.write(f"L X{ret_x:.3f} FMAX M92\n")
                f.write("M10 M15\n")
                f.write("M2\n")
                f.write("END PGM\n")

            messagebox.showinfo("Exportation Heidenhain Terminée", f"Fichier '{filename}' généré avec succès.\nTotal : {total_points} points sur {len(z_levels)} passes Z.")

        except Exception as e:
            messagebox.showerror("Erreur", f"Échec lors de l'écriture Heidenhain : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptoGeneratorApp(root)
    root.mainloop()