# missoes_pd/missao3.py
import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont
import random
from algoritmos_pd.knapsack_com_pd import knapsack_01_pd # Importa o algoritmo de Knapsack

class Missao3:
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame

        self.valores_itens = []
        self.pesos_itens = []
        self.nomes_itens = [] 
        self.capacidade_mochila = 0
        self.dp_table_correta = None 
        self.valor_final_correto = 0 
        self.itens_selecionados_corretos = [] 

        self.player_dp_table = []    
        self.cell_entries = {} 

        self.selected_items_vars = [] 
        self.current_step = 1 

        self.last_focused_cell = (1, 1) # Inicializa para ter um foco válido
        self.current_item_idx = 1
        self.current_weight_idx = 1

        self._carregar_estilos()

    def _carregar_estilos(self):
        """Carrega os estilos e fontes do GameManager ou define fallbacks."""
        try:
            self.bg_color = self.game_manager.bg_color_dark
            self.fg_color = self.game_manager.fg_color_light
            self.title_color = self.game_manager.title_color_accent
            self.header_font = self.game_manager.header_font_obj
            self.narrative_font = self.game_manager.narrative_font_obj
            self.button_font = self.game_manager.button_font_obj
            self.small_bold_font = self.game_manager.small_bold_font_obj
        except AttributeError:
            print("AVISO Missao3: Cores/Fontes do GameManager não encontradas. Usando fallbacks.")
            self.bg_color = "black"
            self.fg_color = "white"
            self.title_color = "gold"
            self.header_font = ("Arial", 20, "bold")
            self.narrative_font = ("Arial", 12)
            self.button_font = ("Arial", 10, "bold")
            self.small_bold_font = ("Arial", 10, "bold")

        self.dp_cell_font = ("Courier New", 10)
        self.item_info_font = ("Courier New", 11, "bold")
        self.table_header_font = ("Courier New", 10, "bold")
        self.entry_cell_bg = "#3a3a3a" # Um cinza escuro para células de input
        self.entry_cell_fg = "white"
        self.correct_cell_bg = "green" 
        self.incorrect_cell_bg = "red" 
        self.active_cell_border = "yellow"
        self.default_cell_border = self.bg_color # Cor de borda padrão das células

    def _limpar_frame(self):
        """Limpa todos os widgets do frame de conteúdo da missão."""
        for widget in self.base_content_frame.winfo_children():
            widget.destroy()

    def iniciar_missao_contexto(self):
        """Inicia a missão exibindo o contexto e o botão para a primeira etapa."""
        self._limpar_frame()
        self.current_step = 1 # Garante que a missão sempre começa da Etapa 1

        self._gerar_problema_knapsack() 

        tk.Label(
            self.base_content_frame,
            text="MISSÃO CF-3: O Dilema do Armamento Jedi",
            font=self.header_font,
            fg=self.title_color,
            bg=self.bg_color
        ).pack(pady=(10, 15))

        contexto = (
            "Fulcrum: \"Comandante, um posto avançado Jedi secreto está sob ataque. Precisamos evacuar o máximo de artefatos e armas antigas possível. O transporte de emergência tem uma capacidade limitada, e cada item é único. Você só pode levar o artefato inteiro ou deixá-lo para trás. É uma questão de tudo ou nada para cada item.\"\n\n"
            "\"Sua missão é determinar a combinação ideal para maximizar o valor total, respeitando a capacidade da nave. **Preencha a tabela de Programação Dinâmica** para encontrar a solução ótima!\"" 
        )
        tk.Label(
            self.base_content_frame,
            text=contexto,
            wraplength=700,
            justify=tk.LEFT,
            font=self.narrative_font,
            fg=self.fg_color,
            bg=self.bg_color
        ).pack(pady=10, padx=20)

        ttk.Button(
            self.base_content_frame,
            text="Iniciar Análise de Artefatos...",
            command=self.iniciar_etapa_preenchimento_tabela,
            style="Accent.Dark.TButton"
        ).pack(pady=20)

    def _gerar_problema_knapsack(self):
        """
        Gera um novo problema de Knapsack com itens e capacidade aleatórios.
        Filtra itens para que o peso não seja maior que a capacidade da mochila.
        """
        all_possible_items = [
            {"nome": "Cristal Kyber", "valor": 38, "peso": 4},
            {"nome": "Sabre de Luz Antigo", "valor": 76, "peso": 7},
            {"nome": "Holocron Jedi", "valor": 45, "peso": 3},
            {"nome": "Manual de Força Proibido", "valor": 60, "peso": 5},
            {"nome": "Medalhão Sith Raro", "valor": 80, "peso": 6},
            {"nome": "Mapa Estelar Secreto", "valor": 25, "peso": 2},
            {"nome": "Dispositivo de Comunicação Antigo", "valor": 30, "peso": 3},
            {"nome": "Capa de Mestre Jedi", "valor": 20, "peso": 1},
            {"nome": "Artefato Sith Corrompido", "valor": 90, "peso": 8}, 
            {"nome": "Poção de Cura Rara", "valor": 12, "peso": 1},
            {"nome": "Diário de Expedição Jedi", "valor": 50, "peso": 4},
            {"nome": "Armadura de Batalha (Leve)", "valor": 35, "peso": 5},
            {"nome": "Pistola Blaster Antiga", "valor": 22, "peso": 3},
            {"nome": "Granada de Íons Desativada", "valor": 18, "peso": 2},
            {"nome": "Composto Explosivo (Estabilizado)", "valor": 55, "peso": 6}, 
            {"nome": "Esfera de Treinamento de Força", "valor": 40, "peso": 3},
            {"nome": "Kit de Ferramentas Droid", "valor": 10, "peso": 2},
            {"nome": "Documentos Secretos Imperiais", "valor": 70, "peso": 5},
            {"nome": "Bateria de Energia Pesada", "valor": 28, "peso": 6}, 
            {"nome": "Amuleto da Antiga República", "valor": 65, "peso": 4},
        ]

        self.capacidade_mochila = 8 # Capacidade máxima da nave: FIXO em 8 para este cenário
        
        
        num_items_to_select_desired = random.randint(4, 5) 

        valid_items_for_capacity = [
            item for item in all_possible_items if item["peso"] <= self.capacidade_mochila
        ]

        num_items_to_select = min(num_items_to_select_desired, len(valid_items_for_capacity))
        
        if num_items_to_select == 0:
            if all_possible_items:
                min_weight_item = min(all_possible_items, key=lambda x: x["peso"])
                if min_weight_item["peso"] > self.capacidade_mochila:
                    self.capacidade_mochila = min_weight_item["peso"] + random.randint(1, 3) 
                    messagebox.showwarning("Ajuste de Missão", f"A capacidade da nave foi ajustada para {self.capacidade_mochila} para garantir que itens possam ser selecionados.")
                    valid_items_for_capacity = [
                        item for item in all_possible_items if item["peso"] <= self.capacidade_mochila
                    ]
                    num_items_to_select = min(num_items_to_select_desired, len(valid_items_for_capacity))
                
                if num_items_to_select == 0 and valid_items_for_capacity: 
                    num_items_to_select = 1 
            else: 
                messagebox.showerror("Erro de Geração", "A lista de itens disponíveis para a missão está vazia. Verifique os dados do jogo.")
                self.game_manager.root.quit()
                return

        if num_items_to_select == 0:
            messagebox.showerror("Erro de Geração", "Não foi possível gerar um problema válido para a missão. Por favor, reinicie o jogo.")
            self.game_manager.root.quit()
            return

        selected_items_data = random.sample(valid_items_for_capacity, num_items_to_select) 

        self.nomes_itens = [item["nome"] for item in selected_items_data]
        self.valores_itens = [item["valor"] for item in selected_items_data]
        self.pesos_itens = [item["peso"] for item in selected_items_data]
        
        
        print("\n--- DEBUG: Inputs para knapsack_01_pd ---")
        print(f"Valores: {self.valores_itens}")
        print(f"Pesos: {self.pesos_itens}")
        print(f"Capacidade: {self.capacidade_mochila}")

        
        temp_dp_table, _, temp_itens_selecionados = \
            knapsack_01_pd(self.valores_itens, self.pesos_itens, self.capacidade_mochila)
        
        self.dp_table_correta = temp_dp_table
        
        
        self.valor_final_correto = self.dp_table_correta[len(self.valores_itens)][self.capacidade_mochila]
        
        self.itens_selecionados_corretos = temp_itens_selecionados

       
        print("\n--- DEBUG: Resultados de knapsack_01_pd (Após Atribuição) ---")
        print("Tabela DP Correta:")
        for row in self.dp_table_correta:
            
            print([f"{x:3}" for x in row]) 
        print(f"Valor Ótimo Final (derivado da tabela DP): {self.valor_final_correto}")
        print(f"Itens Selecionados (índices): {self.itens_selecionados_corretos}")
        
        selected_items_info_debug = [f"{self.nomes_itens[idx]} (V={self.valores_itens[idx]}, P={self.pesos_itens[idx]})" for idx in self.itens_selecionados_corretos]
        print(f"Itens Selecionados (nomes e detalhes): {', '.join(selected_items_info_debug)}")
        print("-------------------------------------------\n")

        
        n_items = len(self.valores_itens)
        self.player_dp_table = [[0 for _ in range(self.capacidade_mochila + 1)] for _ in range(n_items + 1)] 
        
    def iniciar_etapa_preenchimento_tabela(self):
        """Inicia a primeira etapa da missão: preenchimento manual da tabela DP."""
        self._limpar_frame()

        tk.Label(
            self.base_content_frame,
            text="Etapa 1/2: Preenchimento da Tabela de Programação Dinâmica", 
            font=self.button_font,
            fg="#FF64F2",
            bg=self.bg_color
        ).pack(pady=10)

        info_frame = tk.Frame(self.base_content_frame, bg=self.bg_color)
        info_frame.pack(pady=5, padx=20, fill=tk.X)

        tk.Label(info_frame, text=f"Capacidade da Nave: {self.capacidade_mochila} unidades",
                 font=self.narrative_font, fg=self.fg_color, bg=self.bg_color).pack(anchor="w")
        
        tk.Label(info_frame, text="\nArtefatos Disponíveis:",
                 font=self.small_bold_font, fg=self.fg_color, bg=self.bg_color).pack(anchor="w")

        for i, (name, v, p) in enumerate(zip(self.nomes_itens, self.valores_itens, self.pesos_itens)):
            tk.Label(info_frame, text=f"Item {i+1} ({name}): Valor={v}, Peso={p}",
                     font=self.item_info_font, fg=self.fg_color, bg=self.bg_color).pack(anchor="w", padx=10)
        
        tk.Label(
            self.base_content_frame,
            text="\nPreencha a tabela M[i][w] abaixo. Cada célula M[i][w] representa o valor máximo que pode ser obtido\n"
                 "considerando os primeiros 'i' itens com uma capacidade de 'w'.",
            wraplength=700,
            justify=tk.CENTER,
            font=self.narrative_font, 
            fg=self.fg_color,
            bg=self.bg_color
        ).pack(pady=(10, 5), padx=20)

        table_canvas_frame = tk.Frame(self.base_content_frame, bg=self.bg_color)
        table_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.table_canvas = tk.Canvas(table_canvas_frame, bg=self.bg_color, highlightbackground=self.fg_color, highlightthickness=1)
        self.table_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.table_scrollbar_y = ttk.Scrollbar(table_canvas_frame, orient="vertical", command=self.table_canvas.yview)
        self.table_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.table_canvas.config(yscrollcommand=self.table_scrollbar_y.set)

        self.table_scrollbar_x = ttk.Scrollbar(self.base_content_frame, orient="horizontal", command=self.table_canvas.xview)
        self.table_scrollbar_x.pack(fill=tk.X)
        self.table_canvas.config(xscrollcommand=self.table_scrollbar_x.set)

        self.table_frame = tk.Frame(self.table_canvas, bg=self.bg_color)
        self.table_canvas.create_window((0,0), window=self.table_frame, anchor="nw")
        self.table_frame.bind("<Configure>", lambda e: self.table_canvas.configure(scrollregion = self.table_canvas.bbox("all")))

        self._criar_tabela_interativa()

        control_frame = tk.Frame(self.base_content_frame, bg=self.bg_color)
        control_frame.pack(pady=10)

        self.check_cell_button = ttk.Button(control_frame, text="Verificar Célula", command=self._verificar_celula_atual, style="Dark.TButton") 
        self.check_cell_button.pack(side=tk.LEFT, padx=5)

        self.hint_button = ttk.Button(control_frame, text="Dica Geral (PD)", command=self._mostrar_dica_geral_pd, style="Dark.TButton") 
        self.hint_button.pack(side=tk.LEFT, padx=5)
        
        
        self.analyze_all_button = ttk.Button(control_frame, text="Analisar Tabela Completa", command=self._analisar_todas_as_celulas, style="Dark.TButton")
        self.analyze_all_button.pack(side=tk.LEFT, padx=5)

        self.confirm_table_button = ttk.Button(control_frame, text="Confirmar Tabela e Avançar", command=self._confirmar_tabela_e_avancar, style="Accent.Dark.TButton", state=tk.NORMAL) 
        self.confirm_table_button.pack(side=tk.LEFT, padx=5)
        
        self._on_cell_focus(1,1) 

    def _criar_tabela_interativa(self):
        """Cria os widgets da tabela interativa, inicialmente vazios (exceto as células base 0)."""
        self.cell_entries = {} 

        tk.Label(self.table_frame, text="i\\W", font=self.table_header_font, bg=self.bg_color, fg=self.fg_color, relief="solid", bd=1).grid(row=0, column=0, sticky="nsew")
        for w in range(self.capacidade_mochila + 1):
            lbl = tk.Label(self.table_frame, text=str(w), font=self.table_header_font, bg=self.bg_color, fg=self.fg_color, relief="solid", bd=1)
            lbl.grid(row=0, column=w+1, sticky="nsew")

        for i in range(len(self.pesos_itens) + 1):
            row_header_text = ""
            if i == 0:
                row_header_text = "Linha Base (0 Itens)"
            else:
                current_item_name = self.nomes_itens[i-1]
                if i == 1:
                    row_header_text = f"Considerando Item 1 ({current_item_name})"
                else:
                    row_header_text = f"Considerando até Item {i} ({current_item_name})"

            tk.Label(self.table_frame, text=row_header_text, font=self.table_header_font, bg=self.bg_color, fg=self.fg_color, relief="solid", bd=1).grid(row=i+1, column=0, sticky="nsew")
            
            for w in range(self.capacidade_mochila + 1):
                entry = tk.Entry(
                    self.table_frame,
                    width=5,
                    font=self.dp_cell_font,
                    bg=self.entry_cell_bg,
                    fg=self.entry_cell_fg,
                    justify=tk.CENTER,
                    relief="flat",
                    insertbackground="white", # Cor do cursor
                    highlightbackground=self.default_cell_border,
                    highlightcolor=self.default_cell_border,
                    highlightthickness=1
                )
                entry.grid(row=i+1, column=w+1, sticky="nsew")
                self.cell_entries[(i, w)] = entry

                
                if i == 0 or w == 0:
                    entry.insert(0, "0")
                    entry.config(state=tk.DISABLED, bg=self.bg_color, fg=self.fg_color)
                    entry.bind("<Button-1>", lambda e: "break")
                else: # Habilita o foco para células editáveis e o highlight
                    entry.bind("<FocusIn>", lambda e, r=i, c=w: self._on_cell_focus(r, c))
                    entry.bind("<Return>", lambda e: self._verificar_celula_atual()) # Para testar com Enter
                    
                    entry.delete(0, tk.END)


        for col in range(self.capacidade_mochila + 2):
            self.table_frame.grid_columnconfigure(col, weight=1)
        for row in range(len(self.pesos_itens) + 2):
            self.table_frame.grid_rowconfigure(row, weight=1)

    def _on_cell_focus(self, r, c):
        """Gerencia o foco da célula, aplicando highlight e selecionando o texto.
        A rolagem é manual, mas o highlight segue o foco."""
        if hasattr(self, 'last_focused_cell') and self.last_focused_cell:
            prev_r, prev_c = self.last_focused_cell
            if (prev_r, prev_c) in self.cell_entries:
                
                prev_entry_bg = self.cell_entries[(prev_r, prev_c)].cget('bg')
                if prev_entry_bg not in [self.correct_cell_bg, self.incorrect_cell_bg]:
                    self.cell_entries[(prev_r, prev_c)].config(highlightbackground=self.default_cell_border, highlightcolor=self.default_cell_border)
                elif prev_entry_bg == self.incorrect_cell_bg: # Se era vermelha, mantém borda vermelha
                    self.cell_entries[(prev_r, prev_c)].config(highlightbackground=self.incorrect_cell_bg, highlightcolor=self.incorrect_cell_bg)


        self.current_item_idx = r
        self.current_weight_idx = c
        self.last_focused_cell = (r, c)
        
        current_entry = self.cell_entries.get((self.current_item_idx, self.current_weight_idx))
        if current_entry and current_entry.cget('state') != tk.DISABLED:
            current_entry.config(highlightbackground=self.active_cell_border, highlightcolor=self.active_cell_border)
            current_entry.focus_set() 
            current_entry.select_range(0, tk.END) 
            
    def _verificar_celula_atual(self):
        """
        Verifica se o valor da célula atualmente focada está correto (opcional para o jogador).
        Pinta a célula de verde se correto e desabilita, de vermelho se incorreto.
        Não avança automaticamente, apenas serve como feedback.
        """
        
        if not hasattr(self, 'current_item_idx') or self.current_item_idx == 0 or self.current_weight_idx == 0:
            messagebox.showinfo("Aviso", "Por favor, selecione uma célula da tabela (não da linha/coluna 0) para verificar.")
            return

        r = self.current_item_idx
        c = self.current_weight_idx
        entry = self.cell_entries.get((r, c))

        if not entry or entry.cget('state') == tk.DISABLED: 
            messagebox.showinfo("Aviso", "Esta célula já foi preenchida e verificada, ou é uma célula base.")
            return

        try:
            player_value = int(entry.get().strip()) 
            correct_value = self.dp_table_correta[r][c]

            if player_value == correct_value:
                entry.config(bg=self.correct_cell_bg, state=tk.DISABLED, fg="white", highlightbackground=self.correct_cell_bg, highlightcolor=self.correct_cell_bg)
                messagebox.showinfo("Correto!", "Valor inserido corretamente!")
                
                self.player_dp_table[r][c] = player_value 
            else:
                entry.config(bg=self.incorrect_cell_bg, fg="white", highlightbackground=self.incorrect_cell_bg, highlightcolor=self.incorrect_cell_bg)
                self.game_manager.add_score(-10) 
                messagebox.showerror("Incorreto!", "Valor incorreto. Revise sua lógica para esta célula.")
                self._mostrar_dica_especifica_knapsack_com_valores(r, c) 
                entry.focus_set() 
                entry.select_range(0, tk.END) 

        except ValueError:
            messagebox.showerror("Entrada Inválida", "Por favor, insira um número inteiro na célula.")
            entry.focus_set()
            entry.select_range(0, tk.END)
        
    def _mostrar_dica_especifica_knapsack_com_valores(self, r, c): 
        """Mostra uma dica mais detalhada para uma célula, usando os valores CORRETOS para explicação."""
        
        peso_item_atual = self.pesos_itens[r-1]
        valor_item_atual = self.valores_itens[r-1]
        nome_item_atual = self.nomes_itens[r-1]
        
        
        valor_se_nao_incluir = self.dp_table_correta[r-1][c] 
        
        valor_se_incluir_calculado = 0
        if (c - peso_item_atual) >= 0: 
            valor_se_incluir_calculado = valor_item_atual + self.dp_table_correta[r-1][c - peso_item_atual]

        dica_detalhada = (
            f"Como M[{r}][{c}] (considerando '{nome_item_atual}') é calculado:\n\n"
        )
        
        if peso_item_atual > c: 
            dica_detalhada += (f"**Atenção:** O artefato '{nome_item_atual}' (Peso: {peso_item_atual}) é muito pesado para a capacidade atual de {c}. "
                                "Portanto, ele NÃO pode ser incluído nesta célula.\n\n"
                               f"O valor correto é copiado da célula acima: M[{r-1}][{c}] = {valor_se_nao_incluir}.")
        else: 
            dica_detalhada += (
                f"**1. Opção: NÃO INCLUIR '{nome_item_atual}':**\n"
                f"   Valor = M[{r-1}][{c}] = {valor_se_nao_incluir} (valor da célula diretamente acima).\n\n"
                f"**2. Opção: INCLUIR '{nome_item_atual}':**\n"
                f"   Valor = {valor_item_atual} (Valor do item) + M[{r-1}][{c - peso_item_atual}] = {valor_item_atual} + {self.dp_table_correta[r-1][c - peso_item_atual]} = {valor_se_incluir_calculado}.\n\n"
                f"O valor final de M[{r}][{c}] é o MAIOR entre essas duas opções: {valor_se_nao_incluir} ou {valor_se_incluir_calculado}."
            )
        
        messagebox.showinfo(f"Cálculo de M[{r}][{c}]", dica_detalhada)
        self.game_manager.add_score(-15) 


    def _mostrar_dica_geral_pd(self): 
        """Exibe uma dica geral sobre a lógica da Programação Dinâmica para Knapsack."""
        dica_geral = (
            "Comandante, lembre-se da fórmula da Programação Dinâmica para o problema da mochila:\n\n"
            "M[i][w] = o valor máximo considerando os primeiros 'i' itens com capacidade 'w'.\n\n"
            "Se o Peso do Item 'i' (P_i) for maior que a capacidade 'w':\n"
            "  M[i][w] = M[i-1][w] (Você não pode levar o item 'i', então o valor é o mesmo de não tê-lo)\n\n"
            "Se o Peso do Item 'i' (P_i) for menor ou igual à capacidade 'w':\n"
            "  M[i][w] = MAX (M[i-1][w], Valor_i + M[i-1][w - P_i])\n"
            "  (Compare: não levar o item 'i' vs. levar o item 'i' e o valor restante com a capacidade diminuída)"
        )
        messagebox.showinfo("Dica de Programação Dinâmica (Geral)", dica_geral)
        self.game_manager.add_score(-10)

    def _analisar_todas_as_celulas(self):
        """
        Coleta e verifica todas as células editáveis da tabela, marcando-as como
        corretas (verde) ou incorretas (vermelho).
        Dá feedback geral sobre o preenchimento, mas não avança a missão.
        """
        n_items = len(self.pesos_itens)
        w_capacity = self.capacidade_mochila
        
        total_celulas_preenchidas = 0
        total_celulas_corretas = 0
        
        
        for r in range(n_items + 1):
            for c in range(w_capacity + 1):
                entry = self.cell_entries.get((r,c))
                if entry and entry.cget('state') == tk.NORMAL: 
                    entry.config(bg=self.entry_cell_bg, fg=self.entry_cell_fg, 
                                 highlightbackground=self.default_cell_border, highlightcolor=self.default_cell_border)

        
        for r in range(n_items + 1):
            for c in range(w_capacity + 1):
                entry = self.cell_entries.get((r,c))
                if entry and entry.cget('state') == tk.NORMAL: 
                    try:
                        val = entry.get()
                        if not val.strip(): 
                            continue 
                        
                        self.player_dp_table[r][c] = int(val)
                        total_celulas_preenchidas += 1

                    except ValueError: 
                        entry.config(bg=self.incorrect_cell_bg, fg="white", 
                                     highlightbackground=self.incorrect_cell_bg, highlightcolor=self.incorrect_cell_bg)
                        messagebox.showwarning("Erro de Entrada", f"Célula M[{r}][{c}] contém valor inválido ('{val}'). Insira números inteiros para analisar.")
                        entry.focus_set()
                        return 

        
        for r in range(n_items + 1):
            for c in range(w_capacity + 1):
                entry = self.cell_entries.get((r,c))
                # Verifica apenas as células que o jogador pode editar e preencheu
                if entry and entry.cget('state') == tk.NORMAL and entry.get().strip(): 
                    player_val = self.player_dp_table[r][c] 
                    correct_val = self.dp_table_correta[r][c]

                    if player_val == correct_val:
                        entry.config(bg=self.correct_cell_bg, fg="white", 
                                     highlightbackground=self.correct_cell_bg, highlightcolor=self.correct_cell_bg)
                        total_celulas_corretas += 1
                    else:
                        entry.config(bg=self.incorrect_cell_bg, fg="white", 
                                     highlightbackground=self.incorrect_cell_bg, highlightcolor=self.incorrect_cell_bg)
        
        feedback_msg = f"Análise da Tabela:\n\nTotal de células preenchidas (excluindo linhas/colunas 0): {total_celulas_preenchidas}\nCélulas corretas: {total_celulas_corretas}"
        
        
        total_rows_editable = len(self.pesos_itens)
        total_cols_editable = self.capacidade_mochila
        total_editable_cells = total_rows_editable * total_cols_editable 

        if total_celulas_preenchidas == total_editable_cells and total_celulas_corretas == total_editable_cells:
            feedback_msg += "\n\nExcelente! Todas as células preenchidas estão corretas. Prossiga para 'Confirmar Tabela e Avançar'."
            
            self.analyze_all_button.config(state=tk.DISABLED) 
        elif total_celulas_preenchidas > 0:
            feedback_msg += "\n\nAs células corretas foram marcadas em verde e as incorretas em vermelho. Corrija as células em vermelho."
        else:
            feedback_msg += "\n\nNenhuma célula editável foi preenchida para análise."

        messagebox.showinfo("Análise de Tabela", feedback_msg)
        self.game_manager.add_score(-20) 


    def _confirmar_tabela_e_avancar(self):
        """
        Valida a tabela DP preenchida pelo jogador. Se correta, avança para a etapa de seleção de itens.
        Caso contrário, informa os erros e permite ao jogador corrigir.
        """
        n_items = len(self.pesos_itens)
        w_capacity = self.capacidade_mochila
        
        # Primeiro, limpa qualquer destaque de erro anterior de todas as células editáveis
        for r in range(n_items + 1):
            for c in range(w_capacity + 1):
                entry = self.cell_entries.get((r,c))
                if entry and entry.cget('state') == tk.NORMAL: 
                    entry.config(bg=self.entry_cell_bg, highlightbackground=self.default_cell_border, highlightcolor=self.default_cell_border)

        all_cells_correct_now = True 

        
        for r in range(n_items + 1):
            for c in range(w_capacity + 1):
                entry = self.cell_entries.get((r, c))
                
                if entry.cget('state') == tk.NORMAL: 
                    val = entry.get().strip()
                    if not val: 
                        messagebox.showwarning("Erro de Preenchimento", f"Célula M[{r}][{c}] está vazia. Por favor, preencha todas as células com números inteiros para avançar.")
                        entry.focus_set()
                        entry.config(highlightbackground="red", highlightcolor="red")
                        return 
                    try:
                        self.player_dp_table[r][c] = int(val)
                    except ValueError: # Valor não numérico
                        messagebox.showwarning("Erro de Preenchimento", f"Célula M[{r}][{c}] contém valor inválido ('{val}'). Por favor, insira apenas números inteiros para avançar.")
                        entry.focus_set()
                        entry.config(highlightbackground="red", highlightcolor="red")
                        return 

                    
                    if self.player_dp_table[r][c] != self.dp_table_correta[r][c]:
                        all_cells_correct_now = False 
                        entry.config(bg=self.incorrect_cell_bg, fg="white", 
                                     highlightbackground=self.incorrect_cell_bg, highlightcolor=self.incorrect_cell_bg)
                    else: # Célula correta
                        entry.config(bg=self.correct_cell_bg, fg="white", 
                                     highlightbackground=self.correct_cell_bg, highlightcolor=self.correct_cell_bg, 
                                     state=tk.DISABLED) 
                elif entry.cget('state') == tk.DISABLED: 
                    try:
                        self.player_dp_table[r][c] = int(entry.get())
                        
                        if self.player_dp_table[r][c] != self.dp_table_correta[r][c]:
                            all_cells_correct_now = False
                            entry.config(bg=self.incorrect_cell_bg, fg="white", 
                                         highlightbackground=self.incorrect_cell_bg, highlightcolor=self.incorrect_cell_bg)
                    except ValueError:
                        print(f"AVISO: Célula desabilitada M[{r}][{c}] com valor não numérico '{entry.get()}'. Default para 0.")
                        self.player_dp_table[r][c] = 0
                        all_cells_correct_now = False 
                        entry.config(bg=self.incorrect_cell_bg, fg="white", 
                                     highlightbackground=self.incorrect_cell_bg, highlightcolor=self.incorrect_cell_bg)


        
        print(f"\n--- DEBUG: Comparação Final (Parte 1 - Knapsack) ---")
        print(f"Valor Final Correto (self.valor_final_correto): {self.valor_final_correto}")
        print(f"Valor Final do Jogador (player_dp_table[{n_items}][{w_capacity}]): {self.player_dp_table[n_items][w_capacity]}")
        print(f"Resultado da Comparação (all_cells_correct_now): {all_cells_correct_now}")
        print("-------------------------------------------------------\n")


        if all_cells_correct_now:
            
            for r_final in range(n_items + 1):
                for c_final in range(w_capacity + 1):
                    entry_final = self.cell_entries[(r_final,c_final)]
                    entry_final.config(state=tk.DISABLED, highlightbackground=self.default_cell_border, highlightcolor=self.default_cell_border)
            self.check_cell_button.config(state=tk.DISABLED)
            self.hint_button.config(state=tk.DISABLED)
            self.analyze_all_button.config(state=tk.DISABLED)
            self.confirm_table_button.config(state=tk.DISABLED)
            
            pontos = 250 
            if self.game_manager.player_score >= 0: 
                pontos += 50
            self.game_manager.add_score(pontos)
            messagebox.showinfo("Missão Concluída (Parte 1)!", f"Excelente trabalho, Comandante! Você preencheu a tabela DP corretamente. O valor máximo que pode ser salvo é {self.valor_final_correto}.")
            
            self.current_step = 2 
            self._iniciar_etapa_selecao_itens() 
        else:
            self.game_manager.add_score(-100) 
            messagebox.showerror("Falha Estratégica (Tabela)", f"Sua tabela contém erros. O valor total máximo que poderia ser salvo era {self.valor_final_correto}. As células incorretas foram destacadas em vermelho. Por favor, corrija-as e tente novamente.")
            
            
            self.confirm_table_button.config(state=tk.NORMAL) 
            self.check_cell_button.config(state=tk.NORMAL)
            self.analyze_all_button.config(state=tk.NORMAL)
            self.hint_button.config(state=tk.NORMAL)
           

    def _iniciar_etapa_selecao_itens(self):
        """Inicia a segunda etapa da missão: seleção dos itens ótimos."""
        self._limpar_frame()

        tk.Label(
            self.base_content_frame,
            text="Etapa 2/2: Decifrando a Carga Ótima", 
            font=self.header_font,
            fg=self.title_color,
            bg=self.bg_color
        ).pack(pady=(10, 15))

        contexto = (
            "Fulcrum: \"Você preencheu a tabela com maestria! Agora que sabemos o valor máximo, precisamos descobrir *exatamente* quais artefatos devem ser salvos para obter essa carga vital. Revise a tabela que você preencheu (mostrada abaixo) e selecione os artefatos que, juntos, compõem a solução ótima para o valor máximo da mochila!\""
        )
        tk.Label(
            self.base_content_frame,
            text=contexto,
            wraplength=700,
            justify=tk.LEFT,
            font=self.narrative_font,
            fg=self.fg_color,
            bg=self.bg_color
        ).pack(pady=10, padx=20)

        
        correct_names_debug = [self.nomes_itens[idx] for idx in sorted(self.itens_selecionados_corretos)]
        print(f"\n--- DEBUG: ITENS CORRETOS PARA SELEÇÃO (COLA): {', '.join(correct_names_debug)} ---")
        total_val_debug = sum(self.valores_itens[idx] for idx in self.itens_selecionados_corretos)
        total_peso_debug = sum(self.pesos_itens[idx] for idx in self.itens_selecionados_corretos)
        print(f"--- DEBUG: Valor: {total_val_debug}, Peso: {total_peso_debug} (Esperado: V={self.valor_final_correto}, P<={self.capacidade_mochila}) ---\n")


        tk.Label(
            self.base_content_frame,
            text="Sua Tabela DP Preenchida (para referência e rastreamento):",
            font=self.small_bold_font,
            fg=self.fg_color,
            bg=self.bg_color
        ).pack(pady=(10, 5))

        
        table_display_canvas_frame = tk.Frame(self.base_content_frame, bg=self.bg_color)
        table_display_canvas_frame.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        display_canvas = tk.Canvas(table_display_canvas_frame, bg=self.bg_color, highlightbackground=self.fg_color, highlightthickness=1)
        display_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        display_scrollbar_y = ttk.Scrollbar(table_display_canvas_frame, orient="vertical", command=display_canvas.yview)
        display_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        display_canvas.config(yscrollcommand=display_scrollbar_y.set)
        display_scrollbar_x = ttk.Scrollbar(self.base_content_frame, orient="horizontal", command=display_canvas.xview)
        display_scrollbar_x.pack(fill=tk.X)
        display_canvas.config(xscrollcommand=display_scrollbar_x.set)

        display_table_inner_frame = tk.Frame(display_canvas, bg=self.bg_color)
        display_canvas.create_window((0,0), window=display_table_inner_frame, anchor="nw")
        display_table_inner_frame.bind("<Configure>", lambda e: display_canvas.configure(scrollregion = display_canvas.bbox("all")))

        
        for w in range(self.capacidade_mochila + 1):
            lbl = tk.Label(display_table_inner_frame, text=str(w), font=self.table_header_font, bg=self.bg_color, fg=self.fg_color, relief="solid", bd=1)
            lbl.grid(row=0, column=w+1, sticky="nsew")
        
        for i in range(len(self.pesos_itens) + 1):
            row_header_text = ""
            if i == 0: row_header_text = "Linha Base (0 Itens)"
            else:
                current_item_name = self.nomes_itens[i-1]
                if i == 1: row_header_text = f"Até Item 1 ({current_item_name})"
                else: row_header_text = f"Até Item {i} ({current_item_name})"
            tk.Label(display_table_inner_frame, text=row_header_text, font=self.table_header_font, bg=self.bg_color, fg=self.fg_color, relief="solid", bd=1).grid(row=i+1, column=0, sticky="nsew")
            
            for w in range(self.capacidade_mochila + 1):
                val = self.player_dp_table[i][w] 
                
                cell_fg_color = "lightgreen" if self.player_dp_table[i][w] == self.dp_table_correta[i][w] else "red"
                lbl = tk.Label(display_table_inner_frame, text=str(val), font=self.dp_cell_font, bg=self.bg_color, fg=cell_fg_color, relief="solid", bd=1) 
                lbl.grid(row=i+1, column=w+1, sticky="nsew")
        

        tk.Label(
            self.base_content_frame,
            text="\nSelecione todos os artefatos que, juntos, formam a carga de valor máximo (sem exceder a capacidade):",
            wraplength=700,
            justify=tk.CENTER,
            font=self.narrative_font,
            fg=self.fg_color,
            bg=self.bg_color
        ).pack(pady=(10, 5), padx=20)

        self.selected_items_vars = [] 
        checkbox_frame = tk.Frame(self.base_content_frame, bg=self.bg_color)
        checkbox_frame.pack(pady=5, padx=20)

        for i, nome_item in enumerate(self.nomes_itens):
            var = tk.IntVar()
            cb = tk.Checkbutton(
                checkbox_frame,
                text=f"Item {i+1}: {nome_item} (V={self.valores_itens[i]}, P={self.pesos_itens[i]})",
                variable=var,
                bg=self.bg_color,
                fg=self.fg_color,
                selectcolor="gray", 
                activebackground=self.bg_color,
                activeforeground=self.fg_color,
                font=self.narrative_font,
                anchor="w"
            )
            cb.pack(fill=tk.X, pady=2)
            self.selected_items_vars.append(var)

        ttk.Button(
            self.base_content_frame,
            text="Confirmar Seleção de Artefatos",
            command=self._validar_selecao_itens, 
            style="Accent.Dark.TButton"
        ).pack(pady=20)


    def _validar_selecao_itens(self):
        """Valida a seleção de itens feita pelo jogador na Parte 2 da missão."""
        player_selected_indices = []
        for i, var in enumerate(self.selected_items_vars):
            if var.get() == 1: # Se o checkbox foi marcado
                player_selected_indices.append(i)
        
        player_selected_indices.sort()
        correct_sorted_indices = sorted(self.itens_selecionados_corretos) 

        print("\n--- DEBUG: Rastreamento do Jogador vs. Correto (Parte 2) ---")
        print(f"Itens Selecionados pelo Jogador (índices): {player_selected_indices}")
        print(f"Itens Selecionados Corretamente (índices): {correct_sorted_indices}")
        print("-----------------------------------------------------------\n")

        if player_selected_indices == correct_sorted_indices:
            pontos = 300 # Pontos pelo rastreamento correto
            self.game_manager.add_score(pontos)
            nomes_selecionados_final = [self.nomes_itens[idx] for idx in correct_sorted_indices]
            messagebox.showinfo("Sucesso na Missão (Parte 2)!", f"Conforme sua análise, os artefatos {', '.join(nomes_selecionados_final)} foram recuperados. Missão cumprida!")
            self.game_manager.mission_completed("Missao3") # Missão concluída!
        else:
            self.game_manager.add_score(-150) # Penalidade por rastreamento incorreto
            correct_names = [self.nomes_itens[idx] for idx in correct_sorted_indices]
            messagebox.showerror("Falha no Rastreamento", f"Sua seleção de artefatos está incorreta. A combinação ideal era: {', '.join(correct_names)}. Revise a lógica de rastreamento na tabela DP.")
            self.game_manager.mission_failed_options(
                self,
                "Erro de Decifração de Dados",
                "Fulcrum: \"Uma tabela preenchida com perfeição não basta; precisamos traduzi-la em ações. Continue praticando o rastreamento!\""
            )

    def retry_mission(self):
        """Reseta a missão para o início (primeira etapa) caso o jogador queira tentar novamente."""
        print("Missao3: retry_mission chamada. Resetando estado para START_MISSION_3.")
        self.game_manager.set_game_state("START_MISSION_3")