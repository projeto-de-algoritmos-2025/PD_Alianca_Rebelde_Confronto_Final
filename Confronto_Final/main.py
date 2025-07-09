# main.py 
import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont, PhotoImage
import random 
import os 
import sys

# --- Importações das missões (Comente/descomente conforme desenvolve) ---
try:
    from missoes_pd.missao1 import Missao1
    from missoes_pd.missao2 import Missao2
    #from missoes_pd.missao3 import missao3
   # from missoes_pd.missao4 import missao4
    from missoes_pd.missao5 import Missao5

except ImportError as e:    
    print(f"ALERTA DE IMPORTAÇÃO DE MÓDULO: {e}")

class GameManager:
    def __init__(self, root_tk):
        self.root = root_tk
        self.root.title("Aliança Rebelde - O Confronto Final") 
        self.root.configure(bg="black") 

        try:
            largura_tela = self.root.winfo_screenwidth()
            altura_tela = self.root.winfo_screenheight()
            self.root.geometry(f"{largura_tela}x{altura_tela}+0+0")
        except tk.TclError:
            self.root.state('zoomed') # Fallback para Windows/outros sistemas

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
       

        # --- Carregar TODAS as Imagens ---
        self.imagens = {} # um dicionário para organizar as imagens
        nomes_imagens = [
            "alianca_simbolo.png", "Cena1.png", "Cena2.png", 
            "Cena3.png", "Cena4.png", "Cena5.png", "Cena6.png", "party.png"
        ]
        for nome_img in nomes_imagens:
            try:
                caminho_img = os.path.join(self.script_dir, nome_img)
                if os.path.exists(caminho_img):
                    self.imagens[nome_img] = PhotoImage(file=caminho_img)
                    print(f"DEBUG: Imagem '{nome_img}' carregada.")
                else:
                    print(f"AVISO: Imagem '{nome_img}' NÃO ENCONTRADA.")
                    self.imagens[nome_img] = None # Define como None se não encontrar
            except Exception as e_img:
                print(f"AVISO: Erro ao carregar '{nome_img}': {e_img}")
                self.imagens[nome_img] = None

        # --- Cores e Fontes ---
        self.bg_color_dark = "black"
        self.fg_color_light = "white"
        self.title_color_accent = "orangered" 
        self.default_font_family = "Arial" 
        try:
            self.header_font_obj = tkFont.Font(family=self.default_font_family, size=20, weight="bold")
            self.narrative_font_obj = tkFont.Font(family=self.default_font_family, size=12)
            self.button_font_obj = tkFont.Font(family=self.default_font_family, size=11, weight="bold")
            self.small_bold_font_obj = tkFont.Font(family=self.default_font_family, size=10, weight="bold")
            self.points_font_obj = tkFont.Font(family=self.default_font_family, size=12, weight="bold", slant="italic")
        except tk.TclError: 
            print("Aviso: Fontes tkFont.Font não configuradas. Usando fallback.")
            self.header_font_obj = ("Arial", 20, "bold")
            self.narrative_font_obj = ("Arial", 12)
            self.button_font_obj = ("Arial", 11, "bold")
            self.small_bold_font_obj = ("Arial", 10, "bold")
            self.points_font_obj = ("Arial", 12, "bold", "italic")
        
        # --- Estilo ttk ---
        style = ttk.Style()
        try: style.theme_use('clam')
        except tk.TclError: pass
        style.configure("Black.TFrame", background=self.bg_color_dark)
        style.configure("Points.TLabel", background=self.bg_color_dark, foreground="#87CEFA", font=self.points_font_obj)
        style.configure("Accent.Dark.TButton", font=self.button_font_obj, foreground="white", background="#0078D7", padding=10)
        style.map("Accent.Dark.TButton", background=[('active', "#C50B9D")])
        style.configure("Dark.TButton", font=self.button_font_obj, foreground="white", background="#333333", padding=5)
        style.map("Dark.TButton", background=[('active', '#444444')])

        self.player_score = 0 
        self.current_mission_obj = None 
        self.content_frame = None 
        self.game_state = "INTRO_CF_A" 
        self.update_display()
        
    def _clear_content_frame(self):
        if self.content_frame: self.content_frame.destroy()
        self.content_frame = ttk.Frame(self.root, padding="20", style="Black.TFrame") 
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    def _display_text_screen(self, title_text, narrative_text_lines, button_text, 
                             next_state_or_command, button_style="Dark.TButton", 
                             image_to_display=None): 
        self._clear_content_frame()
        title_label = tk.Label(self.content_frame, text=title_text, font=self.header_font_obj, anchor="center", bg=self.bg_color_dark, fg=self.title_color_accent, pady=5) 
        title_label.pack(pady=(10, 15), fill=tk.X)
        text_widget = tk.Text(self.content_frame, wrap=tk.WORD, height=10, relief=tk.FLAT, background=self.bg_color_dark, foreground=self.fg_color_light, insertbackground=self.fg_color_light, font=self.narrative_font_obj, padx=10, pady=10, borderwidth=0, highlightthickness=0)
        text_widget.insert(tk.END, "\n\n".join(narrative_text_lines))
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill=tk.BOTH, padx=40, pady=5)
        if image_to_display: 
            imagem_label = tk.Label(self.content_frame, image=image_to_display, bg=self.bg_color_dark) 
            imagem_label.pack(pady=(10, 5))
        if isinstance(next_state_or_command, str): command_to_run = lambda: self.set_game_state(next_state_or_command)
        else: command_to_run = next_state_or_command
        button_container = ttk.Frame(self.content_frame, style="Black.TFrame")
        pady_button = (5 if image_to_display else 15, 10) 
        button_container.pack(pady=pady_button, side=tk.BOTTOM, anchor="s")
        actual_button_style = "Accent.Dark.TButton" if button_style == "Accent.TButton" else "Dark.TButton"
        ttk.Button(button_container, text=button_text, command=command_to_run, style=actual_button_style).pack(pady=5)

    def update_display(self):
        self._clear_content_frame()

        # --- INTRODUÇÃO PARA O CONFRONTO FINAL ---
        if self.game_state == "INTRO_CF_A":
            narrativa = ["Meses se passaram desde que você, Comandante RZ-479, desvendou os padrões ocultos do Império com sua mente analítica.",
        "Mas a guerra está longe do fim. Relatórios recentes revelam uma nova movimentação estratégica do inimigo: silenciosa, profunda e quase impossível de prever."]
            self._display_text_screen("Sombras no Hiperespaço", narrativa, "Continuar...", "INTRO_CF_B", button_style="Accent.Dark.TButton", image_to_display=self.imagens.get("Cena1.png"))
        elif self.game_state == "INTRO_CF_B":
            narrativa = ["Fulcrum aparece em uma transmissão codificada. Seu semblante é sério.",
        "\"Comandante, detectamos um padrão de ataques calculados. Eles não são aleatórios... estão otimizando recursos, escolhendo alvos com máxima eficiência. É como se usassem algoritmos de guerra.\"",
        "\"Acreditamos que o Império esteja usando uma nova unidade de inteligência baseada em programação avançada para prever nossas jogadas.\""]
            self._display_text_screen("Inteligência Artificial Imperial", narrativa, "Estou ouvindo, Fulcrum...", "INTRO_CF_C", image_to_display=self.imagens.get("Cena2.png"))
        elif self.game_state == "INTRO_CF_C":
            narrativa = [ "\"Para vencer essa nova ameaça, não bastará reagir. Precisamos antecipar. Precisamos de **Programação Dinâmica**. Não apenas no campo de batalha, mas em cada decisão.\"\n",
        "\"Cada missão será um teste: eficiência em intervalos, decisões binárias, estratégias ótimas em tempo real... E você será nossa última esperança de vitória.\""]
            self._display_text_screen("O Fim Começa Agora", narrativa, "Aceito o desafio. Preparar para a Missão 1","START_MISSION_1", button_style="Accent.Dark.TButton", image_to_display=self.imagens.get("Cena4.png"))
            

        
        # --- FLUXO DAS NOVAS MISSÕES ---
        elif self.game_state == "START_MISSION_1":
            if 'Missao1' in globals():
                self._clear_content_frame()
                self.current_mission_obj = Missao1(self.root, self, self.content_frame)
                self.current_mission_obj.iniciar_missao_contexto()
            else: messagebox.showerror("Erro Crítico", "Classe missao1 não foi carregada.")
        elif self.game_state == "MISSION_1_SUCCESS":
            dialogo = ["Fulcrum: \"Extrações perfeitas, comandante. Otimizamos nosso tempo e impacto em todos os setores. O próximo passo exigirá ainda mais cálculo estratégico...\""]
            self._display_text_screen("Análise Concluída", dialogo, "Aguardando ordens.", "START_MISSION_2", button_style="Accent.Dark.TButton", image_to_display=self.imagens.get("alianca_simbolo.png"))
        elif self.game_state == "START_MISSION_2":
            if 'Missao2' in globals():
                self._clear_content_frame()
                self.current_mission_obj = Missao2(self.root, self, self.content_frame)
                self.current_mission_obj.iniciar_missao_contexto()
            else: messagebox.showerror("Erro Crítico", "Classe Missao2 não foi carregada.")
        elif self.game_state == "MISSION_2_SUCCESS":
            self._display_text_screen("Operação Concluída", ["Fulcrum: \"A evolução dos recrutas foi surpreendente. Sua lógica sequencial nos permitiu formar uma nova elite. Vamos ao próximo transporte crucial.\""], "Avançar para Missão 3", "START_MISSION_DC_3", button_style="Accent.Dark.TButton", image_to_display=self.imagens.get("alianca_simbolo.png"))
        elif self.game_state == "START_MISSION_3":
            if 'Missao3' in globals():
                self._clear_content_frame()
                self.current_mission_obj = missao3(self.root, self, self.content_frame)
                self.current_mission_obj.iniciar_missao_contexto()
            else: messagebox.showerror("Erro Crítico", "Classe Missao3 não foi carregada.")
        elif self.game_state == "MISSION_3_SUCCESS":
             dialogo = ["Fulcrum: \"Com sua escolha de carga, a resistência não apenas sobreviveu — ela floresceu. Agora, decodificar esse DNA pode revelar segredos perigosos...\""]
             self._display_text_screen("Carga Entregue", dialogo, "Avançar para Missão 4", "START_MISSION_4", button_style="Accent.Dark.TButton", image_to_display=self.imagens.get("alianca_simbolo.png"))
        
        elif self.game_state == "START_MISSION_4":
            if 'Missao4' in globals():
                self._clear_content_frame()
                self.current_mission_obj = missao4(self.root, self, self.content_frame)
                self.current_mission_obj.iniciar_missao_contexto()
            else: messagebox.showerror("Erro Crítico", "Classe missao4 não foi carregada.")
        elif self.game_state == "MISSION_4_SUCCESS":
             dialogo = ["Fulcrum: \"Impressionante. O alinhamento revelou manipulações genéticas escondidas pelo Império. Resta uma última missão... e ela é pessoal.\""]
             self._display_text_screen("Segredos Decifrados", dialogo, "Avançar para a Próxima Missão", "START_MISSION_5", button_style="Accent.Dark.TButton", image_to_display=self.imagens.get("alianca_simbolo.png"))
        
        elif self.game_state == "START_MISSION_5":
            if 'Missao5' in globals():
                self._clear_content_frame()
                self.current_mission_obj = Missao5(self.root, self, self.content_frame)
                self.current_mission_obj.iniciar_missao_contexto()
            else:
                messagebox.showerror("Erro Crítico", "Classe Missao5 não foi carregada.")
        elif self.game_state == "MISSION_5_SUCCESS":
            dialogo = ["Conselho da Aliança: \"Você guiou esta campanha com sabedoria, estratégia e coragem. A Rebelião não esquecerá sua liderança.\""]
            self._display_text_screen("O Eco das Escolhas", dialogo, "Ver o Epílogo", "ALL_MISSIONS_COMPLETED_V3", image_to_display=self.imagens.get("alianca_simbolo.png"))

        elif self.game_state == "ALL_MISSIONS_COMPLETED_V3":
            # 1) Tela base com título, texto e botão:
            self._display_text_screen(
                "A Rebelião Resiste",
                [
                    "A última fase da guerra ainda está por vir, mas graças às decisões que você tomou, a galáxia tem uma nova esperança.",
                    "Líderes inspirados, bases reforçadas, códigos quebrados... tudo começou com você."
                ],
                "Encerrar Jornada",
                self.root.quit,
                button_style="Accent.Dark.TButton",
                image_to_display=None   # desliga a imagem aqui
            )

            # 2) Agora empacota a imagem abaixo do botão:
            img = self.imagens.get("party.png")
            if img:
                tk.Label(self.content_frame, image=img, bg=self.bg_color_dark).pack(pady=(10,5))
            else:
                tk.Label(
                    self.content_frame,
                    text="(Imagem party.png não encontrada)",
                    fg=self.fg_color_light,
                    bg=self.bg_color_dark
                ).pack(pady=(10,5))
        
        else: 
            self._clear_content_frame()
            tk.Label(self.content_frame, text=f"Estado de jogo desconhecido: {self.game_state}", font=self.header_font_obj, fg="red", bg=self.bg_color_dark).pack(pady=20)

    def add_score(self, points):
        self.player_score += points
        print(f"Pontos de Influência: {points}. Total: {self.player_score}")

    def set_game_state(self, new_state):
        print(f"Mudando estado de '{self.game_state}' para: {new_state}") 
        self.game_state = new_state
        self.root.after_idle(self.update_display)

    def mission_completed(self, mission_id):
        print(f"GameManager: Missão {mission_id} concluída.") 
        if mission_id == "Missao1": self.set_game_state("MISSION_1_SUCCESS") 
        elif mission_id == "Missao2": self.set_game_state("MISSION_2_SUCCESS")
        elif mission_id == "Missao3": self.set_game_state("MISSION_3_SUCCESS")
        elif mission_id == "Missao4": self.set_game_state("MISSION_4_SUCCESS")
        elif mission_id == "Missao5": self.set_game_state("ALL_MISSIONS_COMPLETED_V3")
    
    def mission_failed_options(self, mission_obj, msg1, msg2):
        self._clear_content_frame()
        tk.Label(self.content_frame, text="Falha na Missão!", font=self.header_font_obj, fg="red", bg=self.bg_color_dark).pack(pady=10)
        tk.Label(self.content_frame, text=random.choice([msg1, msg2]), font=self.narrative_font_obj, bg=self.bg_color_dark, fg=self.fg_color_light, wraplength=700).pack(pady=15, padx=30)
        button_frame = ttk.Frame(self.content_frame, style="Black.TFrame")
        button_frame.pack(pady=20)
        if mission_obj and hasattr(mission_obj, 'retry_mission'):
            ttk.Button(button_frame, text="Tentar Novamente", command=mission_obj.retry_mission, style="Accent.Dark.TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Abandonar Operação", command=self.root.quit, style="Dark.TButton").pack(side=tk.LEFT, padx=10)

if __name__ == "__main__":
    root = None 
    try:
        root = tk.Tk()
        app = GameManager(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro fatal ao iniciar a aplicação: {e}")