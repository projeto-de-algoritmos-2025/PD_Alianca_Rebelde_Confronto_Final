import tkinter as tk
from tkinter import ttk, messagebox
from algoritmos_pd.maior_subsequencia_crescente import lis_recursive

class Missao2:
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame

        self.blocos = []
        self.alvo = []
        self.entrada = [2, 3, 14, 5, 9, 8, 4] # Aqui está a entrada fixa para a missão
        self.drag_data = {"widget": None, "x": 0, "y": 0}

        self._carregar_estilos()

    def _carregar_estilos(self):
        try:
            self.cor_fundo_base = self.game_manager.bg_color_dark
            self.cor_texto_principal = self.game_manager.fg_color_light
            self.cor_texto_titulo = self.game_manager.title_color_accent
            self.header_font = self.game_manager.header_font_obj
            self.narrative_font = self.game_manager.narrative_font_obj
            self.button_font = self.game_manager.button_font_obj
        except AttributeError:
            self.cor_fundo_base = "black"
            self.cor_texto_principal = "white"
            self.cor_texto_titulo = "pink"
            self.header_font = ("Arial", 20, "bold")
            self.narrative_font = ("Arial", 12)
            self.button_font = ("Arial", 10, "bold")

    def _limpar_frame(self):
        for w in self.base_content_frame.winfo_children():
            w.destroy()

    def iniciar_missao_contexto(self):
        """Chamado pelo game_manager para exibir a missão."""
        self._limpar_frame()

        # Título centralizado
        ttk.Label(
            self.base_content_frame,
            text="MISSÃO 2: Ascensão Inesperada",
            font=self.header_font,
            foreground=self.cor_texto_titulo,
            background=self.cor_fundo_base
        ).pack(pady=(20,10))

        # Explicação narrativa
        texto = (
            "Fulcrum: \"As novas gerações de pilotos da Aliança estão em treinamento intensivo.\\n"
            "Cada sessão possui um nível de dificuldade distinto. Apenas aqueles que seguirem\\n"
            "uma trajetória de crescimento consistente serão aprovados.\\n"
            "Arraste os blocos numéricos para formar a maior sequência crescente possível!\""
            "Lembrando que podem não ser utilizado todos!\""
        )
        ttk.Label(
            self.base_content_frame,
            text=texto,
            font=self.narrative_font,
            foreground=self.cor_texto_principal,
            background=self.cor_fundo_base,
            justify=tk.CENTER
        ).pack(padx=30, pady=(0,20))

        # --- CÁLCULO E PRINT DA SOLUÇÃO CORRETA ---
        # Calcular a LIS para a entrada fixa e imprimir no console
        self.solucao_correta, self.tamanho_lis = lis_recursive(self.entrada)
        print(f"DEBUG (Missao2): Entrada: {self.entrada}")
        print(f"DEBUG (Missao2): Maior Subsequência Crescente (LIS) esperada: {self.solucao_correta} (Tamanho: {self.tamanho_lis})")
        # ------------------------------------------

        # Área de drag & drop
        self._criar_canvas_e_alvo()
        self._criar_blocos_iniciais()

        # Botão para verificar
        ttk.Button(
            self.base_content_frame,
            text="Verificar Solução",
            command=self.verificar_solucao,
            style="Accent.TButton"
        ).pack(pady=15)

    def _criar_canvas_e_alvo(self):
        # Canvas que conterá os blocos soltos
        self.canvas = tk.Canvas(
            self.base_content_frame,
            bg=self.cor_fundo_base,
            height=300,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=False)

        # Frame alvo onde o jogador solta os blocos
        self.area_alvo = tk.Frame(
            self.canvas,
            bg="lightblue",
            height=80
        )
        self.canvas.create_window(350, 200, window=self.area_alvo, width=600, height=80)

    def _criar_blocos_iniciais(self):
        # Cria e posiciona os blocos no topo
        for idx, val in enumerate(self.entrada):
            bloco = tk.Label(
                self.canvas,
                text=str(val),
                bg="orange",
                fg="black",
                font=("Courier", 14, "bold"),
                relief="raised",
                bd=2,
                width=4
            )
            x0 = 50 + idx * 80
            bloco.place(x=x0, y=20)
            bloco.bind("<Button-1>", self._iniciar_drag)
            bloco.bind("<B1-Motion>", self._mover_drag)
            bloco.bind("<ButtonRelease-1>", self._soltar_drag)
            self.blocos.append(bloco)

    def _iniciar_drag(self, event):
        w = event.widget
        self.drag_data["widget"] = w
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def _mover_drag(self, event):
        w = self.drag_data["widget"]
        if not w: return
        new_x = w.winfo_x() + event.x - self.drag_data["x"]
        new_y = w.winfo_y() + event.y - self.drag_data["y"]
        w.place(x=new_x, y=new_y)

    def _soltar_drag(self, event):
        w = self.drag_data["widget"]
        if w and self._sobre_area_alvo(w):
            # só adiciona se ainda não tiver sido solto ali
            valor = int(w["text"])
            if valor not in self.alvo: # Garante que não adiciona valores duplicados
                self.alvo.append(valor)
                # Reposiciona todos os blocos na área alvo para manter a ordem visual
                self.alvo.sort() # Ordena para manter a sequência crescente visualmente se arrastar e soltar em qualquer ordem
                
                # Limpa a área alvo e redesenha os blocos nela
                for child in self.area_alvo.winfo_children():
                    child.destroy()
                
                for i, val in enumerate(self.alvo):
                    bloco_existente = [b for b in self.blocos if int(b["text"]) == val][0] # Encontra o bloco original
                    pos_x = 20 + i * 60
                    bloco_existente.place(in_=self.area_alvo, x=pos_x, y=10)
        self.drag_data = {"widget": None, "x": 0, "y": 0}

    def _sobre_area_alvo(self, w):
        wx, wy = w.winfo_rootx(), w.winfo_rooty()
        ax, ay = self.area_alvo.winfo_rootx(), self.area_alvo.winfo_rooty()
        aw, ah = self.area_alvo.winfo_width(), self.area_alvo.winfo_height()
        return ax <= wx <= ax+aw and ay <= wy <= ay+ah

    def verificar_solucao(self):
        if not self.alvo:
            messagebox.showwarning("Aviso", "Arraste ao menos um bloco para a área de sequência.")
            return

        # checa ordem crescente
        # A lista `self.alvo` já é mantida ordenada durante o `_soltar_drag`
        # então a verificação de ordem crescente é mais simples aqui.
        crescente = all(self.alvo[i] < self.alvo[i+1] for i in range(len(self.alvo)-1))
        
        # Comparar com a LIS pré-calculada
        # self.solucao_correta e self.tamanho_lis são definidos em iniciar_missao_contexto
        pontos = 0

        if crescente:
            if len(self.alvo) == self.tamanho_lis and self.alvo == self.solucao_correta: # Verifica se a sequência é EXATAMENTE a LIS
                pontos = 300
                msg = " Perfeito! Sequência ótima e no tamanho ideal."
            elif len(self.alvo) == self.tamanho_lis and self.alvo != self.solucao_correta:
                pontos = 150 # Pontuação intermediária se o tamanho for ótimo, mas a sequência não a LIS exata (pode ter múltiplas LIS)
                msg = f"Sequência crescente e com o tamanho ideal ({self.tamanho_lis} blocos), mas não é a sequência específica esperada."
            else:
                pontos = 100
                msg = f"Sequência crescente, mas falta aumentar até o tamanho ideal ({self.tamanho_lis} blocos)."
        else:
            msg = " A ordem não está crescente."

        if pontos:
            self.game_manager.add_score(pontos)
            # Para evitar múltiplos acionamentos como na Missao1, use after_idle aqui também
            messagebox.showinfo("Resultado", f"{msg}\nSua sequência: {self.alvo}")
            self.root.after_idle(lambda: self.game_manager.mission_completed("Missao2"))
        else:
            messagebox.showinfo("Resultado", f"{msg}\nSua sequência: {self.alvo}")
            # Se a missão falhar, ofereça opções
            self.game_manager.mission_failed_options(
                self,
                "Falha na Estratégia de Recrutamento",
                "Fulcrum: \"Precisamos otimizar a progressão dos nossos recrutas. Tente novamente!\""
            )