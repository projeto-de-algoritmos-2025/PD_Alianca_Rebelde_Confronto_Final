import tkinter as tk
from tkinter import messagebox
import os

class Missao5:
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base = content_frame
        self._carregar_estilos()
        self.perguntas = [
            {
                "texto": "1) Qual foi o nome do primeiro desafio da Aliança Rebelde?",
                "opcoes": ["Operações Difíceis", "Operações Críticas", "Operações Corretas"],
                "resposta": "Operações Críticas"
            },
            {
                "texto": "2) Qual o nome do desafio de Dividir e Conquistar?",
                "opcoes": ["A volta dos desafios", "O retorno", "A volta dos escolhidos"],
                "resposta": "A volta dos desafios"
            }
        ]
        self.respostas = {}

    def _carregar_estilos(self):
        try:
            self.bg          = self.game_manager.bg_color_dark
            self.fg          = self.game_manager.fg_color_light
            self.title_color = self.game_manager.title_color_accent
            self.header_font = self.game_manager.header_font_obj
            self.text_font   = self.game_manager.narrative_font_obj
        except AttributeError:
            self.bg          = "black"
            self.fg          = "white"
            self.title_color = "gold"
            self.header_font = ("Arial", 20, "bold")
            self.text_font   = ("Arial", 12)

    def _limpar(self):
        for w in self.base.winfo_children():
            w.destroy()

    def iniciar_missao_contexto(self):
        self._limpar()
        # Título
        tk.Label(
            self.base, text="MISSÃO 5: O Eco das Escolhas",
            font=self.header_font, fg=self.title_color, bg=self.bg
        ).pack(pady=(20,10))

        # Contexto
        texto = (
            "O Alto Conselho da Aliança revisita cada escolha que você fez.\n"
            "Responda corretamente para revelar partes do plano final e conquistar apoio."
        )
        tk.Label(
            self.base, text=texto, font=self.text_font,
            fg=self.fg, bg=self.bg, justify=tk.CENTER
        ).pack(padx=30, pady=(0,20))

        # Perguntas centralizadas
        for i, p in enumerate(self.perguntas):
            frame_p = tk.Frame(self.base, bg=self.bg, pady=5)
            frame_p.pack(fill=tk.X, padx=100)

            tk.Label(
                frame_p, text=p["texto"],
                font=self.text_font, fg=self.fg, bg=self.bg
            ).pack(anchor="w")

            var = tk.StringVar(value="")
            self.respostas[i] = var

            for opc in p["opcoes"]:
                rb = tk.Radiobutton(
                    frame_p, text=opc, variable=var, value=opc,
                    indicatoron=0,       # transforma em botão
                    selectcolor="purple",  # cor de fundo quando selecionado
                    bg=self.bg, fg=self.fg,
                    activebackground=self.bg,
                    activeforeground=self.fg,
                    font=self.text_font,
                    bd=1, relief="solid",
                    highlightthickness=0,
                    width=20,
                )
                rb.pack(pady=2)

        # Botão azul centralizado
        btn = tk.Button(
            self.base, text="Submeter Respostas",
            command=self._avaliar,
            bg="#0078D7", fg="white",
            font=self.text_font,
            activebackground="#005A9E",
            activeforeground="white",
            width=25, relief="raised", bd=2
        )
        btn.pack(pady=20)

    def _avaliar(self):
        acertos = sum(
            1 for idx, p in enumerate(self.perguntas)
            if self.respostas[idx].get() == p["resposta"]
        )

        if acertos == len(self.perguntas):
            self.game_manager.add_score(300)
            self._mostrar_congratulations()
            self.game_manager.mission_completed("Missao5")
        else:
            self.game_manager.add_score(-50)
            messagebox.showerror(
                "Resultado",
                f"Você acertou {acertos}/{len(self.perguntas)}. Tente novamente!"
            )

    def _mostrar_congratulations(self):
        self._limpar()
        tk.Label(
            self.base, text="Parabéns, a Aliança confia em você!",
            font=self.header_font, fg=self.title_color, bg=self.bg
        ).pack(pady=20)

        # Exibe imagem estática
        img_path = os.path.join(os.getcwd(), "img", "party.jpg")
        if os.path.exists(img_path):
            try:
                self.congrats_img = tk.PhotoImage(file=img_path)
                lbl = tk.Label(self.base, image=self.congrats_img, bg=self.bg)
                lbl.pack(pady=10)
            except Exception:
                tk.Label(
                    self.base, text="(Não foi possível carregar party.jpg)",
                    fg=self.fg, bg=self.bg
                ).pack(pady=10)
        else:
            tk.Label(
                self.base, text="(Imagem party.png não encontrada em img/)",
                fg=self.fg, bg=self.bg
            ).pack(pady=10)
