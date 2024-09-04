import tkinter as tk
import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import sys

ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("/Users/nathan/Documents/mpsi/TIPE/code/theme TIPE.json")  # Themes intégrés : "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        def select_run_file():
            file_path = ctk.filedialog.askopenfilename()
            app.run_path_var.set(file_path)

        def select_cali_file():
            file_path = ctk.filedialog.askopenfilename()
            app.cali_path_var.set(file_path)
        
        # fenetre principale
        self.title("TIPE télémétrie")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.state('zoomed')

        # frames panneau latéral & écran central
        self.main_frame = ctk.CTkFrame(self, width=screen_width, height=screen_height)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Bandeau supérieur
        top_bar_height = screen_height // 15
        self.top_bar = ctk.CTkFrame(self.main_frame, height=top_bar_height, bg_color="#ffd866", fg_color='#ffd866')
        self.top_bar.pack(side=tk.TOP, fill=tk.X)
        title_label = ctk.CTkLabel(self.top_bar, text="TIPE télémétrie - par Nathan Cruzel", text_color='black', font=("Arial", 24, "bold"))
        title_label.pack(side="left", padx=(20, 0))
            # Bouton "Quitter"
        quit_button = ctk.CTkButton(self.top_bar, text="Quitter", text_color='black', command=self.quit_program, height=30, fg_color="transparent", border_color="black", border_width=2)
        quit_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(top_bar_height - 30) // 2)

        # Panneau latéral
        self.side_panel_width = screen_width // 8
        self.side_panel = ctk.CTkFrame(self.main_frame, width=self.side_panel_width, bg_color="gray20")
        self.side_panel.pack(side=tk.LEFT, fill=tk.BOTH)
            # Onglets du panneau latéral
        self.tabview = ctk.CTkTabview(self.side_panel, width=self.side_panel_width)
        self.tabview.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tabview.add("Fichier run")
        self.tabview.add("Setup")
        
        # Ajouter un large bouton 'Générer' en bas de l'onglet 'Run'
        ctk.CTkButton(self.tabview.tab("Fichier run"), text="Générer", width=200, command=self.analyze_data).pack(side=tk.BOTTOM, padx=(20, 0), pady=(20, 10))
        # Ajouter un large bouton 'Générer' en bas de l'onglet 'Réglages'
        ctk.CTkButton(self.tabview.tab("Setup"), text="Générer", width=200, command=self.analyze_data).pack(side=tk.BOTTOM, padx=(20, 0), pady=(20, 10))
        
        # Widgets onglet 'Run'
        run_tab = self.tabview.tab("Fichier run")
        self.nrun = tk.IntVar()
        self.saut_de_chaine = tk.BooleanVar()
        self.chute = tk.BooleanVar()
        self.crevaison = tk.BooleanVar()
        self.correction_temps = tk.BooleanVar()
        self.vitesse_log = tk.BooleanVar(value=True)
        self.Tmoyennage = tk.DoubleVar(value=0.2)
        self.nbbottom = tk.BooleanVar(value=True)
        self.run_path_var = tk.StringVar()
        ctk.CTkLabel(run_tab, text="Fichier du run").pack(pady=(10, 0))
        ctk.CTkEntry(run_tab, width=200, textvariable=self.run_path_var).pack(fill=tk.X, padx=10, pady=(5, 0))
        ctk.CTkButton(run_tab, text="Parcourir", command=self.open_run_file_dialog).pack(pady=(10, 0))
        ctk.CTkLabel(run_tab, text="Choisir le numéro de la descente :").pack(pady=(10, 0))
        ctk.CTkOptionMenu(run_tab, variable=self.nrun, values=[str(i) for i in range(16)]).pack(pady=(5, 10))
        ctk.CTkCheckBox(run_tab, text="Chute", variable=self.chute).pack(pady=(5, 0))
        ctk.CTkCheckBox(run_tab, text="Déraillement", variable=self.saut_de_chaine).pack(pady=(5, 0))
        ctk.CTkCheckBox(run_tab, text="Crevaison", variable=self.crevaison).pack(pady=(5, 5))
            #instants de pause
        ctk.CTkSwitch(run_tab, text="Couper les pauses", variable=self.correction_temps).pack(pady=(20, 0))
            #derniers boutons
        ctk.CTkLabel(run_tab, text="Période de moyennage (s)").pack(pady=(10, 0))
        ctk.CTkEntry(run_tab, textvariable=self.Tmoyennage).pack(pady=(10, 0))
        ctk.CTkSwitch(run_tab, text="Échelle log pour la vitesse", variable=self.vitesse_log).pack(pady=(20, 0))
        ctk.CTkSwitch(run_tab, text="Bottoms en nombre", variable=self.nbbottom).pack(pady=(10, 20))

        # Widgets onglet Réglages
        settings_tab = self.tabview.tab("Setup")
        self.cali_path_var = tk.StringVar()
        self.pot_invers = tk.BooleanVar(value=True)
        self.debattement_avant = tk.DoubleVar(value=130) #en mm   
        self.debattement_arriere = tk.DoubleVar(value=130) #en mm
        self.debattement_shock = tk.DoubleVar(value=47) #en mm
        self.longueur_pot_av = tk.DoubleVar(value=150) #en mm
        self.longueur_pot_ar = tk.DoubleVar(value=100) #en mm
        self.max_pot_av = tk.DoubleVar(value=26270)
        self.max_pot_ar = tk.DoubleVar(value=26270)
        ctk.CTkLabel(settings_tab, text="Fichier de calibration").pack(pady=(10, 0))
        ctk.CTkEntry(settings_tab, width=200, textvariable=self.cali_path_var).pack(fill=tk.X, padx=10, pady=(5, 0))
        ctk.CTkButton(settings_tab, text="Parcourir", command=self.open_cali_file_dialog).pack(pady=(10, 0))
        ctk.CTkSwitch(settings_tab, text="Potentiomètres inversés", variable=self.pot_invers).pack(pady=(20, 5))
        ctk.CTkLabel(settings_tab, text="Débattement avant").pack(pady=(5, 0))
        ctk.CTkEntry(settings_tab, textvariable=self.debattement_avant).pack(pady=(5, 0))
        ctk.CTkLabel(settings_tab, text="Débattement arrière").pack(pady=(5, 0))
        ctk.CTkEntry(settings_tab, textvariable=self.debattement_arriere).pack(pady=(5, 0))
        ctk.CTkLabel(settings_tab, text="Course amortisseur").pack(pady=(5, 0))
        ctk.CTkEntry(settings_tab, textvariable=self.debattement_shock).pack(pady=(5, 0))
        ctk.CTkLabel(settings_tab, text="Course potentiomètre avant").pack(pady=(5, 0))
        ctk.CTkEntry(settings_tab, textvariable=self.longueur_pot_av).pack(pady=(5, 0))
        ctk.CTkLabel(settings_tab, text="Course potentiomètre arrière").pack(pady=(5, 0))
        ctk.CTkEntry(settings_tab, textvariable=self.longueur_pot_ar).pack(pady=(5, 0))
        ctk.CTkLabel(settings_tab, text="Valeur max potentiomètre AV").pack(pady=(5, 0))
        ctk.CTkEntry(settings_tab, textvariable=self.max_pot_av).pack(pady=(5, 0))
        ctk.CTkLabel(settings_tab, text="Valeur max potentiomètre AR").pack(pady=(5, 0))
        ctk.CTkEntry(settings_tab, textvariable=self.max_pot_ar).pack(pady=(5, 0))
            # Options Hautes / basses vitesses
        self.fReb = tk.BooleanVar(value=True)
        self.fComp = tk.BooleanVar(value=True)
        self.rReb = tk.BooleanVar(value=True)
        self.rComp = tk.BooleanVar(value=False)
        self.fHSLS = tk.BooleanVar(value=False)
        self.rHSLS = tk.BooleanVar(value=False)
        ctk.CTkLabel(settings_tab, text="Réglages fourche :").pack(pady=(5, 0))
        ctk.CTkCheckBox(settings_tab, text='Comp', variable=self.fComp).pack(pady=(2, 0))
        ctk.CTkCheckBox(settings_tab, text='Rebond', variable=self.fReb).pack(pady=(2, 0))
        ctk.CTkCheckBox(settings_tab, text='LS / HS', variable=self.fHSLS).pack(pady=(2, 0))
        ctk.CTkLabel(settings_tab, text="Réglages amortisseur :").pack(pady=(5, 0))
        ctk.CTkCheckBox(settings_tab, text='Comp', variable=self.rComp).pack(pady=(2, 0))
        ctk.CTkCheckBox(settings_tab, text='Rebond', variable=self.rReb).pack(pady=(2, 0))
        ctk.CTkCheckBox(settings_tab, text='LS / HS', variable=self.rHSLS).pack(pady=(2, 0))

        # Ecran central
        main_screen_width = screen_width - self.side_panel_width
        self.main_screen = ctk.CTkFrame(self.main_frame, width=main_screen_width, bg_color="gray80")
        self.main_screen.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            # onglets de l'ecran central
        self.maintabs = ctk.CTkTabview(self.main_screen, width=main_screen_width)
        self.maintabs.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.maintabs.add("Run")
        self.maintabs.add("Stats")
        self.maintabs.add("Réglages")
            # page vide pour Matplotlib
        self.fig = None 
            # onglet réglages
        self.regs_tab = self.maintabs.tab("Réglages")
        self.radiobutton_frame = ctk.CTkFrame(self.regs_tab).pack(side=tk.BOTTOM, padx=20, pady=(10, 0))
        #self.radiobutton_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 0))

    def open_run_file_dialog(self):
        file_path = ctk.filedialog.askopenfilename()
        self.run_path_var.set(file_path)

    def open_cali_file_dialog(self):
        file_path = ctk.filedialog.askopenfilename()
        self.cali_path_var.set(file_path)

    def quit_program(self):
        sys.exit()

    def analyze_data(self):
            # obtention des variables définies dans le logiciel
        fichier = self.run_path_var.get()
        fichier_calibration = self.cali_path_var.get()
        nrun = str(self.nrun.get())
        saut_de_chaine = self.saut_de_chaine.get()
        chute = self.chute.get()
        crevaison = self.crevaison.get()
        correction_temps = self.correction_temps.get()
        vitesse_log = self.vitesse_log.get()        
        Tmoyennage = self.Tmoyennage.get()
        pot_invers = self.pot_invers.get()
        nbbottoms = self.nbbottom.get()

        debattement_avant = int(self.debattement_avant.get())
        debattement_arriere = int(self.debattement_arriere.get())
        debattement_shock = self.debattement_shock.get()
        longueur_pot_av = self.longueur_pot_av.get()
        longueur_pot_ar = self.longueur_pot_ar.get()
        max_pot_av = self.max_pot_av.get()
        max_pot_ar = self.max_pot_ar.get()

        cali = np.loadtxt(fichier_calibration, skiprows=1, unpack=True, delimiter=',')

            # progressivité du vélo 
        shock_travel = [0, 3.3, 6.6, 10, 13.4, 16.9, 20.5, 24.1, 27.7, 31.4, 35.1, 38.9, 42.7, 46.5]
        rear_travel = np.linspace(0, 130, 14)
        rc = np.polyfit(shock_travel, rear_travel, 3)

        if pot_invers:
            cali[1] = [max_pot_ar - cali[1][i] for i in range(len(cali[1]))]
            cali[2] = [max_pot_av - cali[2][i] for i in range(len(cali[2]))]
        pot_ar_max_travel = (max(cali[1]) - min(cali[1])) * (longueur_pot_ar / max_pot_ar)

            # fonctions de traitement
        def wheel_travel(pot: list, front=True) -> list: #conversion potentiometre -> wheel travel
            n = len(pot)
            pot_conv = [0]*n
            if front:
                zero_av = min(pot) * (longueur_pot_av / max_pot_av)
                for i in range(n):
                    pot_conv[i] = pot[i] * (longueur_pot_av / max_pot_av) - zero_av
            else: #rear
                zero_ar = min(pot) * (longueur_pot_ar / max_pot_ar)    
                for i in range(n):
                    pot_conv[i] = (pot[i] * (longueur_pot_ar / max_pot_ar) - zero_ar) * (debattement_shock / pot_ar_max_travel)
                #conversion de pot à wheel travel
                for i in range(n):
                    pot_conv[i] = rc[3] + rc[2]*pot_conv[i] + rc[1]*pot_conv[i]**2 + rc[0]*pot_conv[i]**3      
            return pot_conv

        def wheel_speed(t, av, ar):
            dav = [(av[i+1]-av[i-1])/(t[i+1]-t[i-1]) for i in range(1, len(t)-1)]
            dar = [(ar[i+1]-ar[i-1])/(t[i+1]-t[i-1]) for i in range(1, len(t)-1)]
            dt = t[1:-1]
            return dt, dav, dar

        def repartition_vitesse(dav, dar):
            """
            in : dav et dar sont les outputs de wheel_speed
            out : liste de repartion des couples de vitesse dans l'ordre :
                0, haut gauche 
                1, haut droite
                2, bas gauche
                3, bas droite
            """
            repart_d = [0]*4
            n = len(dar)
            for i in range(n):
                if dar[i] > 0:
                    if dav[i] > 0:
                        repart_d[1] += 100/n
                    else:
                        repart_d[3] += 100/n
                else:
                    if dav[i] > 0:
                        repart_d[0] += 100/n
                    else:
                        repart_d[2] += 100/n
            return repart_d

        def var_nuage_pos(av, ar):
            reg_nuage = np.polyfit(ar, av, 1)
            x_nuage = np.linspace(0, 130, 14)
            y_nuage = [reg_nuage[0]*x_nuage[i] + reg_nuage[1] for i in range(len(x_nuage))]
            return x_nuage, y_nuage, reg_nuage[0]

        def tranche_vitesse(dav: list, dar: list, echelle_log=False, max_v=4000, largeur_v=50) -> list: #affichage graphique
            """
            av et ar sont les outputs de wheel_speed
            renvoie des listes de % d'utilisation des suspensions par tranche de vitesse
            """
            y_plage_dav, x_plage_dav = np.histogram(dav, bins=np.linspace(-max_v, max_v, int(2*max_v/largeur_v)))
            y_plage_dar, x_plage_dar = np.histogram(dar, bins=np.linspace(-max_v, max_v, int(2*max_v/largeur_v)))
            lenav, lenar = len(av), len(ar)
            if vitesse_log:
                y_plage_dav, y_plage_dar = np.log(1+100*y_plage_dav/lenav), np.log(1+100*y_plage_dar/lenar)
            else:
                y_plage_dav, y_plage_dar = 100*y_plage_dav/lenav, 100*y_plage_dar/lenar
            return x_plage_dav, x_plage_dar, y_plage_dav, y_plage_dar

        def tranche_vitesse_max(dav: list, dar: list, max_v=500) -> list: #affichage valeur
            """
            av et ar sont les outputs de wheel_speed
            renvoie des listes de % d'utilisation des suspensions par tranche de vitesse
            """
            y_plage_dav_fin, x_plage_dav_fin = np.histogram(dav, bins=np.linspace(-max_v, max_v, 2*max_v+1))
            y_plage_dar_fin, x_plage_dar_fin = np.histogram(dar, bins=np.linspace(-max_v, max_v, 2*max_v+1))
            y_max_dar = max(y_plage_dar_fin)
            for i in range(len(x_plage_dar_fin)-1):
                if y_plage_dar_fin[i] == y_max_dar:
                    x_max_dar = int(x_plage_dar_fin[i])
                    break       
            y_max_dav = max(y_plage_dav_fin)
            for i in range(len(x_plage_dav_fin)-1):
                if y_plage_dav_fin[i] == y_max_dav:
                    x_max_dav = int(x_plage_dav_fin[i])
                    break        
            return x_max_dav, x_max_dar

        def data_sag(pav, par, plage_av, plage_ar):
            mav = max(pav[15:])
            for i in range(len(pav)):
                if pav[i] == mav:
                    sagav = int(plage_av[i])
            mar = max(par[15:])
            for i in range(len(par)):
                if par[i] == mar:
                    sagar = int(plage_ar[i])
            return sagav, sagar

        def delta_hist(delta) -> list:
            """
            av et ar sont les outputs de wheel_travel
            renvoie des listes de % de temps passé par delta de debattement
            """
            delta_use_y, delta_use_x = np.histogram(Delta_pot, bins=np.linspace(-100, 100, 201))
            ndelta = len(Delta_pot)
            delta_use_y = 100/ndelta*delta_use_y
            return delta_use_x, delta_use_y

        def stat_delta(delta_use_x, delta_use_y):
            delta_use_y_max = max(delta_use_y)
            for i in range(len(delta_use_x)-1):
                if delta_use_y[i] == delta_use_y_max:
                    delta_max = int(delta_use_x[i])
                    return delta_max    

        def Vect_Acc(Ax, Ay, Az):
            Acc = [0]*len(Ax)
            for i in range(len(Ax)):
                Acc[i] = np.sqrt(Ax[i]**2 + Ay[i]**2 + Az[i]**2) - 10
            return Acc

        def data_acc(Acc):
            return round(np.mean(Acc)/10, 2), round(max(Acc)/10, 1)

        def bottom_compte(t, av, ar, nombre=True):
            """
            Renvoie le temps passé à bottom les suspensions
            """
            botav, botar = 0, 0
            for i in range(len(t)):
                if av[i] > 0.96*debattement_avant:
                    botav += 1
                if ar[i] > 0.96*debattement_arriere:
                    botar += 1
            if not nombre:
                periode = t[-1]/len(t)
                botav *= periode
                botar *= periode
            return botav, botar

        def indice(val, li):
            """
            Renvoie l'indice de la valeur la plus proche de 'val' dans une liste ordonnée
            """
            n = len(li)
            i = 0
            while val > li[i] and i < n-1:
                i += 1
            if abs(val-li[i-1]) < abs(val-li[i]):
                return i-1
            return i

        def détection_pauses(tm, Accm, tol=1.6):
            Fmoyennage = Tmoyennage*len(tm)/tm[-1]
            pauses = []
            k = -1
            for i in range(len(Accm)):
                if abs(Accm[i]) < tol and k == -1:
                    k = i
                if abs(Accm[i]) > tol and k != -1:
                    if i > k+Fmoyennage:
                        pauses += [k, i]
                    k = -1
                if k != -1 and i == len(Accm)-1:
                    pauses += [k, i]
            for i in range(len(pauses)):
                pauses[i] = round(tm[pauses[i]], 1)
            return pauses

        def cut_pauses(pauses, t, X):
            t = list(t)
            l_indices = []
            for p in pauses:
                l_indices.append(indice(p, t))
            X = list(X)
            Y = []
            n = len(l_indices)//2
            i = 0
            for k in range(n):
                j = l_indices[2*k]
                Y += X[i:j]
                i = l_indices[2*k+1]
            Y += X[i:-1]
            if X == t:
                T = t[-1]/len(t)
                Y = np.linspace(0, T*len(Y), len(Y))
            return Y
        
        def moyennage(t: list, X: list, T=1, align='center'):
            """
            Renvoie une version moyennée sur T secondes glissantes de la liste X et sa liste de temps adaptée
            IN : liste t de temps en secondes ordonée, liste X à lisser, T la période de moyennage
            OUT : tm et Xm les deux listes moyennées
            
            si align='center' les valeurs de tm sont décalées d'un demi intervalle
            si align='left' elles prennent la valeur de t au début de l'intervalle
            si align='right' elles prennent la valeur de t au début de l'intervalle
            """
            import numpy as np
            assert T <= t[-1]/2, 'On ne peut pas moyenner sur une période si longue !'
            tm, Xm = [], []
            dt = len(t)*T/t[-1]
            n = 0
            while (n+1)*T <= t[-1]:
                a, b = int(round(n*dt, 0)), int(round((n+1)*dt, 0))
                if align=='left':
                    tm.append((n)*T)
                elif align=='right':
                    tm.append((n+1)*T)
                else:
                    tm.append((n+0.5)*T)
                Xm.append(np.mean(X[a:b]))
                n += 1
            return tm, Xm
        
        def intersection_histo(x1: list, y1: list, x2: list, y2: list, sortie_multiple=False) -> float:
            """
            Tous les arguments sont des outputs de np.histogram donc len(x)=n+1 et len(y)=n
            Les deux histogrammes doivent etre comparables, ie x1 = x2
            """
            largeur = (max(x1)-min(x1))/(len(x1)-1)
            n = len(y1)
            Sav, Sar, Sinter = 0, 0, 0
            for i in range(n):
                Sav += largeur*y1[i]
                Sar += largeur*y2[i]
                Sinter += largeur*min((y1[i], y2[i]))
            intersect = 100*Sinter/((Sav+Sar)/2) #en %
            if sortie_multiple:
                return Sav, Sar, Sinter, intersect
            else:
                return intersect
        
            # import du fichier de télémétrie puis traitement
        t, pot0, pot1, Ax, Ay, Az = np.loadtxt(fichier, skiprows=1, unpack=True, delimiter=',')
        if pot_invers:
            pot0 = [max_pot_ar - pot0[i] for i in range(len(pot0))]
            pot1 = [max_pot_av - pot1[i] for i in range(len(pot1))]
        if correction_temps:
            Acc = Vect_Acc(Ax, Ay, Az)
            tm, Accm = moyennage(t, Acc, Tmoyennage)
            pauses = détection_pauses(tm, Accm)
            pot0 = cut_pauses(pauses, t, pot0)
            pot1 = cut_pauses(pauses, t, pot1)
            Ax = cut_pauses(pauses, t, Ax)
            Ay = cut_pauses(pauses, t, Ay)
            Az = cut_pauses(pauses, t, Az)
            t = cut_pauses(pauses, t, t)
        if pot_invers:
            ar, av = wheel_travel(pot0, False), wheel_travel(pot1, True)
        else: 
            av, ar = wheel_travel(pot0, True), wheel_travel(pot1, False)

            # variables d'exploitation 
        botav, botar = bottom_compte(t, av, ar, nbbottoms) # ax1: bottoms
        par, plage_ar = np.histogram(ar, bins=np.linspace(0, debattement_arriere, debattement_arriere+1))
        pav, plage_av = np.histogram(av, bins=np.linspace(0, debattement_avant, debattement_avant+1))
        pav, par = 100*pav/len(t), 100*par/len(t)
        inter_pos = intersection_histo(plage_av, pav, plage_ar, par)
        sagav, sagar = data_sag(pav, par, plage_av, plage_ar) # ax2 : sag avant et arriere
        x_nuage, y_nuage, coef_nuage = var_nuage_pos(av, ar) # ax3 : coefficients et liste de regression du nuage de position
        dt, dav, dar = wheel_speed(t, av, ar) # ax4 : temps adapté aux dérivées de av et ar : vitesses
        Delta_pot = [100/130 * (av[i]-ar[i]) for i in range(len(av))] # ax4 : debattement avant - arriere en %
        x_plage_dav, x_plage_dar, y_plage_dav, y_plage_dar = tranche_vitesse(dav, dar) #ax5
        x_max_dav, x_max_dar = tranche_vitesse_max(dav, dar) #ax5
        inter_vitesse = intersection_histo(x_plage_dav, y_plage_dav, x_plage_dar, y_plage_dar)
        repart_d = repartition_vitesse(dav, dar) # ax6 : liste de repartion des couples de vitesse
        max_scatter = 4500 #ax6
        delta_use_x, delta_use_y = delta_hist(Delta_pot) #ax7
        delta_max = stat_delta(delta_use_x, delta_use_y) #ax7
        Acc = Vect_Acc(Ax, Ay, Az) # ax8 : accélération
        tm, Accm = moyennage(t, Acc, Tmoyennage) # ax8 : accélération
        A_avg, A_max = data_acc(Acc) # ax8 : accélération

        #texte problemes rencontrés
        probleme = ""
        pb_vide = True
        if saut_de_chaine:
            pb_vide = False
            probleme += "saut de chaine"
        if crevaison:
            pb_vide = False
            if len(probleme) != 0:
                probleme += ", "
            probleme += "crevaison"
        if chute:
            pb_vide = False
            if len(probleme) != 0:
                probleme += ", "
            probleme += "chute"
        if correction_temps:
            pb_vide = False
            if len(probleme) != 0:
                probleme += ", "
            probleme += "temps corrigé"
        if not pb_vide:
            probleme = "("+probleme+")"

        if self.fig is not None:
            for child in self.stats_tab.winfo_children():
                child.destroy()
            for child in self.mainrun.winfo_children():
                child.destroy()
        
        #plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(60, 64), layout="tight")
        ax1 = plt.subplot(3,2,1)
        ax2 = plt.subplot(3,4,3)
        ax3 = plt.subplot(3,4,4)
        ax4 = plt.subplot(3,2,3)
        ax5 = plt.subplot(3,4,7)
        ax6 = plt.subplot(3,4,8)
        ax7 = plt.subplot(3,2,5)
        ax8 = plt.subplot(3,2,6)

        ax1.plot(t, av, label="Avant", linewidth=0.6, alpha=0.9)
        ax1.plot(t, ar, label="Arrière", linewidth=0.6, alpha=0.9)
        ax1.legend(loc="upper right", fontsize=9)
        ax1.set_xlim((min(t), max(t)))
        ax1.set_ylim([0, 130])
        ax1.set_yticks(np.linspace(0, 120, 7))
        ax1.set_xlabel("Temps en s")
        ax1.set_ylabel("Débattement en mm")
        ax1.set_title("Evolution temporelle du débattement des suspensions")

        ax2.bar(plage_av[:-1], pav, width=1, alpha=0.65, label='Av '+str(sagav)+'mm ('+str(int(100*sagav/debattement_avant)) + '%)')
        ax2.bar(plage_ar[:-1], par, width=1, alpha=0.65, label='Ar '+str(sagar)+'mm ('+str(int(100*sagar/debattement_arriere)) + '%)')
        ax2.legend(loc='upper right', title='overlap = '+str(round(inter_pos, 1))+'%')
        ax2.set_title("Histogramme des écrasements")
        ax2.set_xlabel("Tranche de débattement de 1mm")
        ax2.set_ylabel("Temps passé en %")

        ax3.plot(ar, av, '.', markersize=3, alpha=0.35)
        ax3.plot(x_nuage, x_nuage)
        ax3.plot(x_nuage, y_nuage, label='a = ' + str(round(coef_nuage, 3)))
        ax3.legend(loc='upper right')
        ax3.set_title("Nuage des couples de débattement")
        ax3.set_ylabel("Roue avant en mm")
        ax3.set_xlabel("Roue arrière en mm")
        ax3.set_xlim(0)
        ax3.set_ylim(0)

        ax4.plot(t, Delta_pot, linewidth=0.6, alpha=0.9)
        ax4.plot((0, t[-1]), (0, 0))
        ax4.set_xlim((min(t), max(t)))
        ax4.set_ylim((-100, 100))
        ax4.set_xlabel("Temps en s")
        ax4.set_ylabel("arriere <- Delta en % -> avant")
        ax4.set_title("Différence temporelle d'écrasement en %")

        ax5.bar(x_plage_dav[:-1], y_plage_dav, width=50, alpha=0.65, align='edge', label='Av ' + str(x_max_dav) + ' mm/s')
        ax5.bar(x_plage_dar[:-1], y_plage_dar, width=50, alpha=0.65, align='edge', label='Ar ' + str(x_max_dar) + ' mm/s')
        if vitesse_log:
            ax5.set_xlim(-4000, 4000)
            ax5.set_title("Histogramme des vitesses (éch. log)")
            ax5.set_ylabel("log(1+Temps passé en %)")
        else:
            ax5.set_xlim(-2000, 2000)
            ax5.set_title("Histogramme des vitesses")
            ax5.set_ylabel("Temps passé en %")
        ax5.set_xlabel("Tranche de vitesse de 50 mm/s")
        ax5.legend(loc='upper right', title='overlap = '+str(round(inter_vitesse, 1))+'%')

        ax6.plot(dar, dav, '.', markersize=3, alpha=0.5)
        ax6.plot([-1.1*max_scatter, 1.1*max_scatter], [0, 0], 'k', alpha=0.25)
        ax6.plot([0, 0], [-1.1*max_scatter, 1.1*max_scatter], 'k', alpha=0.25)
        ax6.text(-0.9*max_scatter, 0.8*max_scatter, str(round(repart_d[0], 1)) + '%') #0, haut gauche 
        ax6.text(0.65*max_scatter, 0.8*max_scatter, str(round(repart_d[1], 1)) + '%') #1, haut droite
        ax6.text(-0.9*max_scatter, -0.9*max_scatter, str(round(repart_d[2], 1)) + '%') #2, bas gauche
        ax6.text(0.65*max_scatter, -0.9*max_scatter, str(round(repart_d[3], 1)) + '%') #3, bas droite
        ax6.set_xlim((-max_scatter, max_scatter))
        ax6.set_ylim((-max_scatter, max_scatter))
        ax6.set_title("Nuage de compression et rebond")
        ax6.set_xlabel('<- rebond : Roue arrière : Compression ->')
        ax6.set_ylabel('<- rebond : Roue avant : Compression ->')

        ax7.bar(delta_use_x[:-1], delta_use_y, width=1, alpha=0.8, label='max : '+str(delta_max)+'%')
        ax7.bar(0, 1.2*max(delta_use_y), width=1)
        ax7.legend()
        ax7.set_title("Histogramme du Delta avant/arrière")
        ax7.set_xlabel("arrière <- 1 mm de Delta av/ar -> avant")
        ax7.set_ylabel("Temps passé en %")

        ax8.plot(tm, Accm, linewidth=0.8)
        ax8.plot((0), (0), color='tab:blue', label='mean = '+str(round(np.mean(Accm)/9.81, 2))+' g')
        ax8.plot((0), (0), color='tab:blue', label='max = '+str(round(max(Acc)/9.81, 1))+' g')
        ax8.set_xlabel("Temps en s")
        ax8.set_ylabel("Accélérations en m/s^2")
        ax8.set_title("Accélération du triangle principal en fonction du temps")
        ax8.set_xlim((min(t), max(t)))
        ax8.legend(loc='upper right')

        plt.suptitle("Exploitation des données de télémétrie : essai n°"+nrun+" "+probleme)

            # Ajouter le graphique à l'écran central
        self.mainrun = self.maintabs.tab("Run")
        canvas = FigureCanvasTkAgg(self.fig, master=self.mainrun)
        toolbar = NavigationToolbar2Tk(canvas, self.mainrun)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # onglet stats
        self.stats_tab = self.maintabs.tab("Stats")
        for widget in self.stats_tab.winfo_children():
            widget.destroy()
                # variables stats
        temps_texte = "Temps : {} s".format(round(t[-1], 1))
        if nbbottoms:
            bottom_avant_texte = "Bottom avant : {} fois".format(round(botav, 3))
            bottom_arriere_texte = "Bottom arriere : {} fois".format(round(botar, 3))
        else:
            bottom_avant_texte = "Bottom avant : {} s".format(round(botav, 3))
            bottom_arriere_texte = "Bottom arriere : {} s".format(round(botar, 3))
        acceleration_moyenne_texte = "Acceleration moyenne : {} m/s²".format(A_avg)
        acceleration_max_texte = "Acceleration max : {} m/s²".format(A_max)
            # Créer des widgets CTkFrame pour contenir les labels dans l'onglet 'Stats'
        temps_frame = ctk.CTkFrame(self.stats_tab, width=self.side_panel_width)
        bottom_avant_frame = ctk.CTkFrame(self.stats_tab, width=self.side_panel_width)
        bottom_arriere_frame = ctk.CTkFrame(self.stats_tab, width=self.side_panel_width)
        acceleration_moyenne_frame = ctk.CTkFrame(self.stats_tab, width=self.side_panel_width)
        acceleration_max_frame = ctk.CTkFrame(self.stats_tab, width=self.side_panel_width)
            # Créer des widgets CTkLabel pour afficher les légendes dans l'onglet 'Stats'
        temps_label = ctk.CTkLabel(temps_frame, text=temps_texte, anchor="w", font=("Arial", 18))
        bottom_avant_label = ctk.CTkLabel(bottom_avant_frame, text=bottom_avant_texte, anchor="w", font=("Arial", 18))
        bottom_arriere_label = ctk.CTkLabel(bottom_arriere_frame, text=bottom_arriere_texte, anchor="w", font=("Arial", 18))
        acceleration_moyenne_label = ctk.CTkLabel(acceleration_moyenne_frame, text=acceleration_moyenne_texte, anchor="w", font=("Arial", 18))
        acceleration_max_label = ctk.CTkLabel(acceleration_max_frame, text=acceleration_max_texte, anchor="w", font=("Arial", 18))
            # Ajouter les widgets CTkLabel aux widgets CTkFrame
        temps_label.pack(side=tk.LEFT, padx=(10, 0))
        bottom_avant_label.pack(side=tk.LEFT, padx=(10, 0))
        bottom_arriere_label.pack(side=tk.LEFT, padx=(10, 0))
        acceleration_moyenne_label.pack(side=tk.LEFT, padx=(10, 0))
        acceleration_max_label.pack(side=tk.LEFT, padx=(10, 0))
            # Ajouter les widgets CTkFrame à l'onglet 'Stats'
        temps_frame.pack(side=tk.TOP, fill=tk.X, pady=(10, 0))
        bottom_avant_frame.pack(side=tk.TOP, fill=tk.X, pady=(5, 0))
        bottom_arriere_frame.pack(side=tk.TOP, fill=tk.X, pady=(5, 0))
        acceleration_moyenne_frame.pack(side=tk.TOP, fill=tk.X, pady=(5, 0))
        acceleration_max_frame.pack(side=tk.TOP, fill=tk.X, pady=(5, 0))

if __name__ == "__main__":
    app = App()
    app.mainloop()