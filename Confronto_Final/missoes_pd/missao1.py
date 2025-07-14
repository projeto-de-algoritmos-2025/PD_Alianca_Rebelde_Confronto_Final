import tkinter as tk
from tkinter import ttk, messagebox
import random
from algoritmos_pd.weigthed_interval_scheduling import Intervalo, weighted_interval_scheduling

class Missao1:
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame

        self.entries = {}
        self.instancias = []
        self.solucao_correta = []
        self._carregar_estilos()

    def _carregar_estilos(self):
        try:
            self.cor_fundo_base = self.game_manager.bg_color_dark
            self.cor_texto_principal = self.game_manager.fg_color_light
            self.cor_texto_titulo_missao = self.game_manager.title_color_accent
            self.cor_info = "#FF64F2"
            self.header_font_obj = self.game_manager.header_font_obj
            self.narrative_font_obj = self.game_manager.narrative_font_obj
            self.button_font_obj = self.game_manager.button_font_obj
        except AttributeError:
            self.cor_fundo_base = "black"
            self.cor_texto_principal = "white"
            self.cor_texto_titulo_missao = "lightblue"
            self.header_font_obj = ("Arial", 20, "bold")
            self.narrative_font_obj = ("Arial", 12)

    def _limpar_frame(self):
        for widget in self.base_content_frame.winfo_children():
            widget.destroy()

    def iniciar_missao_contexto(self):
        self._limpar_frame()
        tk.Label(
            self.base_content_frame,
            text="MISSÃO CF-1: Sombras No Tempo",
            font=self.header_font_obj,
            fg=self.cor_texto_titulo_missao,
            bg=self.cor_fundo_base
        ).pack(pady=(10, 15))

        imagem_missao = self.game_manager.imagens.get("Cena4.png")
        if imagem_missao:
            tk.Label(self.base_content_frame, image=imagem_missao, bg=self.cor_fundo_base).pack(pady=10)

        contexto = (
            "Fulcrum: \"Interceptamos uma sequência de movimentações imperiais altamente estratégicas. Cada uma tem uma janela de tempo e um impacto potencial.\"\n\n"
            "Sua missão é interceptar o maior número possível sem sobreposição, maximizando o impacto total da Aliança.\n\n"
            "**Use programação dinâmica para calcular a melhor combinação de ataques a serem interceptados.**"
        )

        tk.Label(
            self.base_content_frame,
            text=contexto,
            wraplength=700,
            justify=tk.LEFT,
            font=self.narrative_font_obj,
            fg=self.cor_texto_principal,
            bg=self.cor_fundo_base
        ).pack(pady=10, padx=20)

        ttk.Button(
            self.base_content_frame,
            text="Iniciar Análise Tática...",
            command=self.iniciar_etapa_analise,
            style="Accent.Dark.TButton"
        ).pack(pady=20)

    def iniciar_etapa_analise(self):
        self._limpar_frame()
        self.instancias = sorted([
            Intervalo(random.randint(0, 10), random.randint(11, 20), random.randint(5, 20))
            for _ in range(6)
        ], key=lambda x: x.fim)

        _, solucao_intervalos = weighted_interval_scheduling(self.instancias)
        self.solucao_correta = [self.instancias.index(i) for i in solucao_intervalos]
        self.solucao_correta.sort()
        
        # --- NOVO PRINT ADICIONADO AQUI ---
        print(f"DEBUG (Missao1): Solução Correta Esperada: {self.solucao_correta}")
        # -----------------------------------

        tk.Label(
            self.base_content_frame,
            text="Etapa: Análise Tática",
            font=self.button_font_obj,
            fg=self.cor_info,
            bg=self.cor_fundo_base
        ).pack(pady=10)

        for idx, item in enumerate(self.instancias):
            tk.Label(
                self.base_content_frame,
                text=f"Ataque {idx}: Início = {item.inicio}, Fim = {item.fim}, Valor = {item.valor}",
                font=("Courier", 12),
                fg=self.cor_texto_principal,
                bg=self.cor_fundo_base
            ).pack()

        tk.Label(
            self.base_content_frame,
            text="\nDigite os índices dos ataques a interceptar (ex: 0,2,5):",
            font=self.narrative_font_obj,
            fg=self.cor_texto_principal,
            bg=self.cor_fundo_base
        ).pack(pady=(10, 5))

        self.entries['resposta'] = tk.Entry(
            self.base_content_frame,
            width=30,
            font=("Courier", 14),
            bg="black",
            fg="white",
            insertbackground="white"
        )
        self.entries['resposta'].pack()

        ttk.Button(
            self.base_content_frame,
            text="Confirmar Escolhas",
            command=self.validar_resposta,
            style="Accent.Dark.TButton"
        ).pack(pady=20)

    def validar_resposta(self):
        entrada = self.entries['resposta'].get().strip()
        try:
            resposta = sorted([int(x.strip()) for x in entrada.split(",") if x.strip() != ""])
        except ValueError:
            messagebox.showerror("Erro", "Insira apenas números separados por vírgula.")
            return

        if resposta == self.solucao_correta:
            pontos = 350
            self.game_manager.add_score(pontos)
            
            messagebox.showinfo("Sucesso", f"Excelente escolha! Ataques interceptados com precisão tática.\n+{pontos} pontos de influência.")
            
            self.root.after_idle(lambda: self.game_manager.mission_completed("Missao1"))
            
        else:
            valor_correto = ", ".join(map(str, self.solucao_correta))
            self.game_manager.add_score(-75)
            messagebox.showerror("Falha Estratégica", f"A sequência ideal era: {valor_correto}\nEstude os padrões com mais atenção.")
            self.game_manager.mission_failed_options(
                self,
                "Erro de Planejamento",
                "Fulcrum: \"Nem todas as escolhas foram as mais estratégicas... mas ainda há tempo de ajustar a rota.\""
            )