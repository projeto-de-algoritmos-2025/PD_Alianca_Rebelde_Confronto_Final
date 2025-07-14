import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont
import random
from algoritmos_pd.alinhamento_sequencias import alinhamento_sequencias_pd # Importa o algoritmo de alinhamento

class Missao4:
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame

        self.seq1 = ""
        self.seq2 = ""
        self.custo_gap = 0
        self.custo_mismatch = 0
        self.dp_table_correta = None
        self.min_cost_correto = 0
        self.alinhamento_seq1_correto = ""
        self.alinhamento_seq2_correto = ""
        self.alinhamento_operacoes_correto = [] 

        self.player_dp_table = [] 
        self.cell_entries = {} 

        # Atributos para o rastreamento interativo (Parte 2) 
        self.current_i_trace = -1 
        self.current_j_trace = -1 
        self.ops_table_entries = [] 
        self.ops_table_frame = None 
        self.ops_canvas = None 
        self.trace_highlight_rect_id = None 
        self.display_table_frame_canvas_item_id = None 

        self.last_focused_cell = (1, 1) 
        self.current_item_idx = 1 
        self.current_weight_idx = 1 

        self._carregar_estilos()

    def _carregar_estilos(self):
        try:
            self.bg_color = self.game_manager.bg_color_dark
            self.fg_color = self.game_manager.fg_color_light
            self.title_color = self.game_manager.title_color_accent
            self.header_font = self.game_manager.header_font_obj
            self.narrative_font = self.game_manager.narrative_font_obj 
            self.button_font = self.game_manager.button_font_obj
            self.small_bold_font = self.game_manager.small_bold_font_obj
        except AttributeError:
            print("AVISO Missao4: Cores/Fontes do GameManager não encontradas. Usando fallbacks.")
            self.bg_color = "black"
            self.fg_color = "white"
            self.title_color = "lightblue"
            self.header_font = ("Arial", 20, "bold")
            self.narrative_font = ("Arial", 12)
            self.button_font = ("Arial", 10, "bold")
            self.small_bold_font = ("Arial", 10, "bold")
        
        self.dp_cell_font = ("Courier New", 14, "bold") 
        self.seq_font = ("Courier New", 14, "bold")
        self.table_header_font = ("Courier New", 10, "bold")
        self.entry_cell_bg = "#3a3a3a"
        self.entry_cell_fg = "white" 

        self.correct_cell_bg = "green"
        self.incorrect_cell_bg = "red"
        self.active_cell_border = "yellow"
        self.default_cell_border = "gray" 
        
        self.base_cell_fg = self.fg_color 
        self.correct_cell_fg = "#00FFFF" 
        
        # Cores para a tabela de operações
        self.ops_header_bg = "#333333"
        self.ops_entry_bg = "#222222"
        self.ops_correct_bg = "#006400" # Verde escuro
        self.ops_incorrect_bg = "#8B0000" # Vermelho escuro

    def _limpar_frame(self):
        for widget in self.base_content_frame.winfo_children():
            widget.destroy()

    def iniciar_missao_contexto(self):
        self._limpar_frame()
        self._gerar_problema_alinhamento()

        tk.Label(
            self.base_content_frame,
            text="MISSÃO CF-4: DNA de Esperança",
            font=self.header_font,
            fg=self.title_color,
            bg=self.bg_color
        ).pack(pady=(10, 15))

        contexto = (
            "Fulcrum: \"Comandante, interceptamos duas amostras de código genético [DNA] muito similares. Suspeitamos que sejam variantes de um patógeno imperial recém-descoberto. Precisamos alinhá-las para encontrar a similaridade mínima e identificar as mutações ou diferenças exatas!\"\n\n"
            "\"Você usará Programação Dinâmica para encontrar o custo mínimo de alinhamento entre essas sequências. Cada diferença ou 'salto' terá um custo. Seu objetivo é minimizar o custo total.\""
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
            text="Iniciar Análise de Sequências...",
            command=self.iniciar_etapa_preenchimento_tabela,
            style="Accent.Dark.TButton"
        ).pack(pady=20)

    def _gerar_problema_alinhamento(self):
        bases_dna = ['A', 'C', 'G', 'T']
        
       
        len1 = random.randint(3, 5) 
        len2 = random.randint(3, 5) 
        
        seq1_temp = [random.choice(bases_dna) for _ in range(len1)]
        seq2_temp = [random.choice(bases_dna) for _ in range(len2)]
        
        
        min_len = min(len1, len2)
        if min_len > 0: 
            start_copy = random.randint(0, min_len // 2)
            end_copy = random.randint(start_copy + 1, min_len) if start_copy + 1 <= min_len else min_len
            for i in range(start_copy, end_copy):
                seq2_temp[i] = seq1_temp[i] 

        
        num_mismatches = random.randint(1, max(1, min_len // 2 + 1)) 
        for _ in range(num_mismatches): 
            idx_s1 = random.randint(0, len1 - 1)
            original_base_s1 = seq1_temp[idx_s1]
            new_base_s1 = random.choice([b for b in bases_dna if b != original_base_s1])
            seq1_temp[idx_s1] = new_base_s1

            idx_s2 = random.randint(0, len2 - 1)
            original_base_s2 = seq2_temp[idx_s2]
            new_base_s2 = random.choice([b for b in bases_dna if b != original_base_s2])
            seq2_temp[idx_s2] = new_base_s2


        self.seq1 = "".join(seq1_temp)
        self.seq2 = "".join(seq2_temp)
        
        self.custo_gap = random.randint(3, 7) 
        self.custo_mismatch = random.randint(8, 15) 

        print("\n--- DEBUG: Problema de Alinhamento Gerado ---")
        print(f"Sequência 1 (X): {self.seq1} (Tamanho: {len(self.seq1)})")
        print(f"Sequência 2 (Y): {self.seq2} (Tamanho: {len(self.seq2)})")
        print(f"Custo de Gap (alpha): {self.custo_gap}")
        print(f"Custo de Mismatch (delta): {self.custo_mismatch}")

        self.dp_table_correta, self.min_cost_correto, self.alinhamento_seq1_correto, self.alinhamento_seq2_correto = \
            alinhamento_sequencias_pd(self.seq1, self.seq2, self.custo_gap, self.custo_mismatch)
        
        self._calcular_alinhamento_operacoes_correto()

        print("\n--- DEBUG: Resultados do Alinhamento (Correto) ---")
        print("Tabela DP Correta:")
        for row in self.dp_table_correta:
            print([f"{x:3}" for x in row])
        print(f"Custo Mínimo Correto: {self.min_cost_correto}")
        print(f"Alinhamento Correto Seq1: {self.alinhamento_seq1_correto}")
        print(f"Alinhamento Correto Seq2: {self.alinhamento_seq2_correto}")
        print("\nCaminho de Operações Correto (Tipo, Custo, Char1, Char2):")
        for op in self.alinhamento_operacoes_correto:
            print(f"  {op}")
        print("--------------------------------------------------\n")

        self.player_dp_table = [[0 for _ in range(len(self.seq2) + 1)] for _ in range(len(self.seq1) + 1)]

    def _calcular_alinhamento_operacoes_correto(self):
        m, n = len(self.seq1), len(self.seq2)
        i, j = m, n
        temp_ops_path = []

        while i > 0 or j > 0:
            char_x = self.seq1[i-1] if i > 0 else None
            char_y = self.seq2[j-1] if j > 0 else None
            
            val_current = self.dp_table_correta[i][j]

            cost_diag_path = float('inf')
            penalidade_mismatch_atual = 0 
            if i > 0 and j > 0:
                penalidade_mismatch_atual = self.custo_mismatch if char_x != char_y else 0
                cost_diag_path = self.dp_table_correta[i-1][j-1] + penalidade_mismatch_atual
            
            cost_up_path = float('inf')
            if i > 0:
                cost_up_path = self.dp_table_correta[i-1][j] + self.custo_gap
            
            cost_left_path = float('inf')
            if j > 0:
                cost_left_path = self.dp_table_correta[i][j-1] + self.custo_gap

            if val_current == cost_diag_path and i > 0 and j > 0:
                op_type = "Match" if char_x == char_y else "Mismatch"
                op_cost = penalidade_mismatch_atual 
                temp_ops_path.append((op_type, op_cost, char_x, char_y))
                i -= 1
                j -= 1
            elif val_current == cost_up_path and i > 0:
                op_type = "Gap X" 
                op_cost = self.custo_gap
                temp_ops_path.append((op_type, op_cost, char_x, '-'))
                i -= 1
            elif val_current == cost_left_path and j > 0:
                op_type = "Gap Y" 
                op_cost = self.custo_gap
                temp_ops_path.append((op_type, op_cost, '-', char_y))
                j -= 1
            else:
                print(f"AVISO: Nenhuma opção de traceback clara para ({i}, {j}) com valor {val_current}. Tentando fallback.")
                if i > 0 and j > 0:
                    op_type = "Match (Fallback)" if char_x == char_y else "Mismatch (Fallback)"
                    op_cost = penalidade_mismatch_atual
                    temp_ops_path.append((op_type, op_cost, char_x, char_y))
                    i -= 1
                    j -= 1
                elif i > 0:
                    op_type = "Gap X (Fallback)"
                    op_cost = self.custo_gap
                    temp_ops_path.append((op_type, op_cost, char_x, '-'))
                    i -= 1
                elif j > 0:
                    op_type = "Gap Y (Fallback)"
                    op_cost = self.custo_gap
                    temp_ops_path.append((op_type, op_cost, '-', char_y))
                    j -= 1
                else: 
                    break

        self.alinhamento_operacoes_correto = temp_ops_path[::-1] 

    def iniciar_etapa_preenchimento_tabela(self):
        self._limpar_frame()

        tk.Label(
            self.base_content_frame,
            text="Etapa 1/2: Preenchimento da Tabela de Alinhamento de Sequências",
            font=self.button_font,
            fg="#FF64F2",
            bg=self.bg_color
        ).pack(pady=10)

        info_frame = tk.Frame(self.base_content_frame, bg=self.bg_color)
        info_frame.pack(pady=5, padx=20, fill=tk.X)

        tk.Label(info_frame, text=f"Sequência 1 (X): {self.seq1}", font=self.seq_font, fg=self.fg_color, bg=self.bg_color).pack(anchor="w")
        tk.Label(info_frame, text=f"Sequência 2 (Y): {self.seq2}", font=self.seq_font, fg=self.fg_color, bg=self.bg_color).pack(anchor="w")
        tk.Label(info_frame, text=f"Custo de Gap (α): {self.custo_gap}", font=self.narrative_font, fg=self.fg_color, bg=self.bg_color).pack(anchor="w")
        tk.Label(info_frame, text=f"Custo de Mismatch (δ): {self.custo_mismatch}", font=self.narrative_font, fg=self.fg_color, bg=self.bg_color).pack(anchor="w")

        tk.Label(
            self.base_content_frame,
            text="\nPreencha a tabela OPT(i, j) abaixo. Cada célula representa o custo mínimo de alinhamento\n"
                 "entre o prefixo X[1...i] e Y[1...j].",
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

        self.hint_button = ttk.Button(control_frame, text="Dica Geral (Alinhamento)", command=self._mostrar_dica_geral_alinhamento, style="Dark.TButton")
        self.hint_button.pack(side=tk.LEFT, padx=5)

        self.analyze_all_button = ttk.Button(control_frame, text="Analisar Tabela Completa", command=self._analisar_todas_as_celulas, style="Dark.TButton")
        self.analyze_all_button.pack(side=tk.LEFT, padx=5)

        self.confirm_table_button = ttk.Button(control_frame, text="Confirmar Tabela e Avançar", command=self._confirmar_tabela_e_avancar, style="Accent.Dark.TButton", state=tk.NORMAL)
        self.confirm_table_button.pack(side=tk.LEFT, padx=5)

        self._on_cell_focus(1,1)


    def _criar_tabela_interativa(self):
        m = len(self.seq1)
        n = len(self.seq2)
        self.cell_entries = {}

        tk.Label(self.table_frame, text="X\\Y", font=self.table_header_font, bg=self.bg_color, fg=self.fg_color, relief="solid", bd=1).grid(row=0, column=0, sticky="nsew")
        tk.Label(self.table_frame, text="-", font=self.table_header_font, bg=self.bg_color, fg=self.fg_color, relief="solid", bd=1).grid(row=0, column=1, sticky="nsew") 
        for j in range(n):
            lbl = tk.Label(self.table_frame, text=self.seq2[j], font=self.table_header_font, bg=self.bg_color, fg=self.fg_color, relief="solid", bd=1).grid(row=0, column=j+2, sticky="nsew")

        tk.Label(self.table_frame, text="-", font=self.table_header_font, bg=self.bg_color, fg=self.fg_color, relief="solid", bd=1).grid(row=1, column=0, sticky="nsew") 
        for i in range(m):
            lbl = tk.Label(self.table_frame, text=self.seq1[i], font=self.table_header_font, bg=self.bg_color, fg=self.fg_color, relief="solid", bd=1).grid(row=i+2, column=0, sticky="nsew")

        for i in range(m + 1):
            for j in range(n + 1):
                entry = tk.Entry(
                    self.table_frame,
                    width=5,
                    font=self.dp_cell_font, 
                    bg=self.entry_cell_bg,
                    justify=tk.CENTER,
                    relief="flat",
                    insertbackground="white",
                    highlightbackground=self.default_cell_border,
                    highlightcolor=self.default_cell_border,
                    highlightthickness=1
                )
                entry.grid(row=i+1, column=j+1, sticky="nsew")
                self.cell_entries[(i, j)] = entry

                if i == 0:
                    entry.insert(0, str(j * self.custo_gap))
                    entry.config(state=tk.DISABLED, bg=self.bg_color, fg=self.correct_cell_fg) 
                    entry.bind("<Button-1>", lambda e: "break")
                elif j == 0:
                    entry.insert(0, str(i * self.custo_gap))
                    entry.config(state=tk.DISABLED, bg=self.bg_color, fg=self.correct_cell_fg) 
                    entry.bind("<Button-1>", lambda e: "break")
                else: 
                    entry.bind("<FocusIn>", lambda e, r_bind=i, c_bind=j: self._on_cell_focus(r_bind, c_bind))
                    entry.bind("<Return>", lambda e: self._verificar_celula_atual())
                    entry.delete(0, tk.END) 
                    entry.config(fg=self.entry_cell_fg) 

        for col in range(n + 2):
            self.table_frame.grid_columnconfigure(col, weight=1)
        for row in range(m + 2):
            self.table_frame.grid_rowconfigure(row, weight=1)

    def _on_cell_focus(self, r, c):
        if hasattr(self, 'last_focused_cell') and self.last_focused_cell:
            prev_r, prev_c = self.last_focused_cell
            if (prev_r, prev_c) in self.cell_entries:
                prev_entry_bg = self.cell_entries[(prev_r, prev_c)].cget('bg')
                if prev_entry_bg not in [self.correct_cell_bg, self.incorrect_cell_bg]:
                     self.cell_entries[(prev_r, prev_c)].config(highlightbackground=self.default_cell_border, highlightcolor=self.default_cell_border)
                elif prev_entry_bg == self.incorrect_cell_bg: 
                    self.cell_entries[(prev_r, prev_c)].config(highlightbackground=self.incorrect_cell_bg, highlightcolor=self.incorrect_cell_bg)
                    

        self.current_item_idx = r
        self.current_weight_idx = c
        self.last_focused_cell = (r, c)
        
        current_entry = self.cell_entries.get((self.current_item_idx, self.current_weight_idx))
        if current_entry and current_entry.cget('state') == tk.NORMAL: 
            current_entry.config(highlightbackground=self.active_cell_border, highlightcolor=self.active_cell_border)
            current_entry.focus_set()
            current_entry.select_range(0, tk.END)
        else: 
            self._move_focus_to_next_editable_cell()


    def _move_focus_to_next_editable_cell(self):
        m = len(self.seq1)
        n = len(self.seq2)

        start_r = self.current_item_idx
        start_c = self.current_weight_idx + 1

        for r_next in range(start_r, m + 1):
            c_start = start_c if r_next == start_r else 1 
            for c_next in range(c_start, n + 1):
                if self.cell_entries[(r_next, c_next)].cget('state') == tk.NORMAL:
                    self._on_cell_focus(r_next, c_next) 
                    return
        messagebox.showinfo("Tabela Quase Completa", "Parece que você preencheu todas as células editáveis ou as restantes estão bloqueadas. Clique em 'Confirmar Tabela e Avançar' para finalizar.")


    def _verificar_celula_atual(self):
        m = len(self.seq1)
        n = len(self.seq2)

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
                entry.config(bg=self.correct_cell_bg, state=tk.DISABLED, fg=self.correct_cell_fg, highlightbackground=self.correct_cell_bg, highlightcolor=self.correct_cell_bg)
                messagebox.showinfo("Correto!", "Valor inserido corretamente!")
                self.player_dp_table[r][c] = player_value 
            else:
                entry.config(bg=self.incorrect_cell_bg, fg="white", highlightbackground=self.incorrect_cell_bg, highlightcolor=self.incorrect_cell_bg)
                self.game_manager.add_score(-10) 
                messagebox.showerror("Incorreto!", "Valor incorreto. A célula ficará vermelha para você corrigir.")
                self._mostrar_dica_especifica_alinhamento_com_valores(r, c) 
                entry.focus_set() 
                entry.select_range(0, tk.END) 

        except ValueError:
            messagebox.showerror("Entrada Inválida", "Por favor, insira um número inteiro na célula.")
            entry.focus_set()
            entry.select_range(0, tk.END)
        
    def _mostrar_dica_especifica_alinhamento_com_valores(self, r, c): 
        char_x = self.seq1[r-1]
        char_y = self.seq2[c-1]
        
        penalidade_mismatch_atual = self.custo_mismatch if char_x != char_y else 0

        custo_diagonal_correto = self.dp_table_correta[r-1][c-1] + penalidade_mismatch_atual
        custo_acima_correto = self.dp_table_correta[r-1][c] + self.custo_gap
        custo_esquerda_correto = self.dp_table_correta[r][c-1] + self.custo_gap

        dica_detalhada = (
            f"Como OPT({r}, {c}) (alinhando '{char_x}' de X e '{char_y}' de Y) é calculado:\n\n"
            f"**Opção 1 (Match/Mismatch):** Alinhe '{char_x}' com '{char_y}'.\n"
            f"   Custo = OPT({r-1}, {c-1}) + Custo de {'mismatch' if char_x != char_y else 'match (0)'} ({penalidade_mismatch_atual})\n"
            f"   Valor = {self.dp_table_correta[r-1][c-1]} + {penalidade_mismatch_atual} = {custo_diagonal_correto}\n\n"
            f"**Opção 2 (Gap em X):** Deixe '{char_x}' desemparelhado (gap em Y).\n" 
            f"   Custo = OPT({r-1}, {c}) + Custo de Gap ({self.custo_gap})\n"
            f"   Valor = {self.dp_table_correta[r-1][c]} + {self.custo_gap} = {custo_acima_correto}\n\n"
            f"**Opção 3 (Gap em Y):** Deixe '{char_y}' desemparelhado (gap em X).\n" 
            f"   Custo = OPT({r}, {c-1}) + Custo de Gap ({self.custo_gap})\n"
            f"   Valor = {self.dp_table_correta[r][c-1]} + {self.custo_gap} = {custo_esquerda_correto}\n\n"
            f"O valor final de OPT({r}, {c}) é o MENOR entre essas três opções: {custo_diagonal_correto}, {custo_acima_correto}, {custo_esquerda_correto}."
        )
        
        messagebox.showinfo(f"Cálculo de OPT({r},{c})", dica_detalhada)
        self.game_manager.add_score(-15) 
        
    def _mostrar_dica_geral_alinhamento(self):
        dica_geral = (
            "Comandante, para o Alinhamento de Sequências, a célula OPT(i, j) é o custo mínimo de alinhamento\n"
            "para os prefixos X[1...i] e Y[1...j]. Há três caminhos possíveis para chegar a OPT(i, j):\n\n"
            "1.  **Alinhar X[i] com Y[j]:** Pegue o valor de OPT(i-1, j-1) (diagonal superior esquerda) e adicione o custo de mismatch (ou 0 se for match).\n"
            "2.  **Deixar X[i] desemparelhado (Gap em Y):** Pegue o valor de OPT(i-1, j) (acima) e adicione o custo de gap.\n"
            "3.  **Deixar Y[j] desemparelhado (Gap em X):** Pegue o valor de OPT(i, j-1) (à esquerda) e adicione o custo de gap.\n\n"
            "A célula OPT(i, j) deve conter o MENOR custo entre essas três opções."
        )
        messagebox.showinfo("Dica de Programação Dinâmica (Geral)", dica_geral)
        self.game_manager.add_score(-10)


    def _analisar_todas_as_celulas(self): 
        m = len(self.seq1)
        n = len(self.seq2)
        
        total_celulas_preenchidas = 0
        total_celulas_corretas = 0
        
        
        for r in range(m + 1):
            for c in range(n + 1):
                entry = self.cell_entries.get((r,c))
                if entry and entry.cget('state') == tk.NORMAL:
                    entry.config(bg=self.entry_cell_bg, fg=self.entry_cell_fg, highlightbackground=self.default_cell_border, highlightcolor=self.default_cell_border)

        for r in range(m + 1):
            for c in range(n + 1):
                entry = self.cell_entries.get((r,c))
                if entry and entry.cget('state') == tk.NORMAL: 
                    try:
                        val = entry.get()
                        if not val.strip():
                            continue 
                        
                        self.player_dp_table[r][c] = int(val)
                        total_celulas_preenchidas += 1

                    except ValueError:
                        entry.config(bg=self.incorrect_cell_bg, fg="white", highlightbackground=self.incorrect_cell_bg, highlightcolor=self.incorrect_cell_bg)
                        messagebox.showwarning("Erro de Entrada", f"Célula OPT({r}, {c}) contém valor inválido ('{val}'). Insira números inteiros para analisar.")
                        entry.focus_set()
                        return 

        for r in range(m + 1):
            for c in range(n + 1):
                entry = self.cell_entries.get((r,c))
                if entry and entry.cget('state') == tk.NORMAL: 
                    player_val = self.player_dp_table[r][c] 
                    correct_val = self.dp_table_correta[r][c]

                    if player_val == correct_val:
                        entry.config(bg=self.correct_cell_bg, fg=self.correct_cell_fg, highlightbackground=self.correct_cell_bg, highlightcolor=self.correct_cell_bg)
                        total_celulas_corretas += 1
                    else:
                        entry.config(bg=self.incorrect_cell_bg, fg="white", highlightbackground=self.incorrect_cell_bg, highlightcolor=self.incorrect_cell_bg)

        feedback_msg = f"Análise da Tabela:\n\nTotal de células preenchidas (excluindo linhas/colunas 0): {total_celulas_preenchidas}\nCélulas corretas: {total_celulas_corretas}"
        total_editable_cells = (m * n) 

        if total_celulas_preenchidas == total_editable_cells and total_celulas_corretas == total_editable_cells:
            feedback_msg += "\n\nExcelente! Todas as células preenchidas estão corretas. Prossiga para 'Confirmar Tabela e Avançar'."
        elif total_celulas_preenchidas > 0:
            feedback_msg += "\n\nAs células corretas foram marcadas em verde e as incorretas em vermelho. Corrija as células em vermelho."
        else:
            feedback_msg += "\n\nNenhuma célula editável foi preenchida para análise."

        messagebox.showinfo("Análise de Tabela", feedback_msg)
        self.game_manager.add_score(-20) 


    def _confirmar_tabela_e_avancar(self):
        m = len(self.seq1)
        n = len(self.seq2)
        
        all_cells_filled_and_valid = True 
        
        
        for r in range(m + 1):
            for c in range(n + 1):
                entry = self.cell_entries.get((r,c))
                if entry.cget('state') == tk.NORMAL: 
                    val = entry.get().strip()
                    if not val: 
                        messagebox.showwarning("Erro de Preenchimento", f"Célula OPT({r}, {c}) está vazia. Por favor, preencha todas as células com números inteiros para avançar.")
                        entry.focus_set()
                        entry.config(highlightbackground="red", highlightcolor="red")
                        return 
                    try:
                        self.player_dp_table[r][c] = int(val)
                    except ValueError:
                        messagebox.showwarning("Erro de Preenchimento", f"Célula OPT({r}, {c}) contém valor inválido ('{val}'). Por favor, insira apenas números inteiros para avançar.")
                        entry.focus_set()
                        entry.config(highlightbackground="red", highlightcolor="red")
                        return 
                elif entry.cget('state') == tk.DISABLED: 
                    try:
                        self.player_dp_table[r][c] = int(entry.get())
                    except ValueError:
                        
                        print(f"AVISO: Célula desabilitada OPT({r},{c}) com valor não numérico '{entry.get()}'. Default para 0.")
                        self.player_dp_table[r][c] = 0 
        
        
        is_table_correct = True
        for i in range(m + 1):
            for j in range(n + 1):
                if self.player_dp_table[i][j] != self.dp_table_correta[i][j]:
                    is_table_correct = False
                    
                    
                    if self.cell_entries[(i, j)].cget('state') == tk.NORMAL: 
                        self.cell_entries[(i, j)].config(bg=self.incorrect_cell_bg, highlightbackground=self.incorrect_cell_bg, highlightcolor=self.incorrect_cell_bg)
                else:
                    
                    self.cell_entries[(i, j)].config(bg=self.correct_cell_bg, fg=self.correct_cell_fg, 
                                                     highlightbackground=self.correct_cell_bg, 
                                                     highlightcolor=self.correct_cell_bg, state=tk.DISABLED)
        
        
        if is_table_correct:
            
            for r_final in range(m + 1):
                for c_final in range(n + 1):
                    entry_final = self.cell_entries[(r_final,c_final)]
                    
                    entry_final.config(state=tk.DISABLED, highlightbackground=self.default_cell_border, highlightcolor=self.default_cell_border) 

            self.check_cell_button.config(state=tk.DISABLED)
            self.hint_button.config(state=tk.DISABLED)
            self.analyze_all_button.config(state=tk.DISABLED) 
            self.confirm_table_button.config(state=tk.DISABLED) 

            print(f"\n--- DEBUG: Comparação Final (Parte 1 - Alinhamento) ---")
            print(f"Custo Mínimo Correto: {self.min_cost_correto}")
            print(f"Custo Mínimo do Jogador: {self.player_dp_table[m][n]}")
            print(f"Resultado da Comparação (is_table_correct): {is_table_correct}")
            print("-------------------------------------------------------\n")

            pontos = 250 
            if self.game_manager.player_score >= 0: 
                pontos += 50
            self.game_manager.add_score(pontos)
            messagebox.showinfo("Missão Concluída (Parte 1)!", f"Excelente trabalho, Comandante! Você preencheu a tabela de alinhamento corretamente. O custo mínimo é {self.min_cost_correto}.")
            
            self._iniciar_etapa_selecao_alinhamento()
        else:
            self.game_manager.add_score(-100) 
            messagebox.showerror("Falha Estratégica (Tabela)", f"Sua tabela contém erros. O custo mínimo correto era {self.min_cost_correto}, mas sua análise resultou em um resultado incorreto. Revise a lógica da Programação Dinâmica. As células incorretas foram destacadas em vermelho.")
            
            self.confirm_table_button.config(state=tk.NORMAL) 
            self.check_cell_button.config(state=tk.NORMAL)
            self.analyze_all_button.config(state=tk.NORMAL)
            self.hint_button.config(state=tk.NORMAL)
            self.game_manager.mission_failed_options(
                self,
                "Erro de Cálculo Crítico",
                "Fulcrum: \"A lógica de otimização é a chave para a vitória. Precisamos de precisão cirúrgica em cada decisão.\""
            )

    def _iniciar_etapa_selecao_alinhamento(self):
        self._limpar_frame()

        tk.Label(
            self.base_content_frame,
            text="Etapa 2/2: Construindo o Alinhamento Ótimo",
            font=self.header_font,
            fg=self.title_color,
            bg=self.bg_color
        ).pack(pady=(10, 15))

        contexto = (
            "Fulcrum: \"A tabela está completa! Agora use-a para reconstruir o alinhamento de custo mínimo. Preencha cada passo da sequência de operações (Match, Mismatch, Gap X, Gap Y) e seu custo exato. Lembre-se, o objetivo é encontrar a rota de menor custo do final ao início da tabela!\"\n\n"
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

        tk.Label(
            self.base_content_frame,
            text="Sua Tabela DP Preenchida (para referência):",
            font=self.small_bold_font,
            fg=self.fg_color,
            bg=self.bg_color
        ).pack(pady=(10, 5))

        
        table_display_canvas_frame = tk.Frame(self.base_content_frame, bg=self.bg_color)
        table_display_canvas_frame.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        self.display_canvas = tk.Canvas(table_display_canvas_frame, bg=self.bg_color, highlightbackground=self.fg_color, highlightthickness=1)
        self.display_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        display_scrollbar_y = ttk.Scrollbar(table_display_canvas_frame, orient="vertical", command=self.display_canvas.yview)
        display_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.display_canvas.config(yscrollcommand=display_scrollbar_y.set)
        
        display_scrollbar_x = ttk.Scrollbar(self.base_content_frame, orient="horizontal", command=self.display_canvas.xview)
        display_scrollbar_x.pack(fill=tk.X)
        self.display_canvas.config(xscrollcommand=display_scrollbar_x.set) 

        self.display_table_inner_frame = tk.Frame(self.display_canvas, bg=self.bg_color)
        self.display_table_frame_canvas_item_id = self.display_canvas.create_window((0,0), window=self.display_table_inner_frame, anchor="nw")
        self.display_table_inner_frame.bind("<Configure>", lambda e: self.display_canvas.configure(scrollregion = self.display_canvas.bbox("all")))

        m = len(self.seq1)
        n = len(self.seq2)
        tk.Label(self.display_table_inner_frame, text="X\\Y", font=self.table_header_font, bg=self.bg_color, fg=self.fg_color, relief="solid", bd=1).grid(row=0, column=0, sticky="nsew")
        tk.Label(self.display_table_inner_frame, text="-", font=self.table_header_font, bg=self.bg_color, fg=self.fg_color, relief="solid", bd=1).grid(row=0, column=1, sticky="nsew") 
        for j in range(n):
            lbl = tk.Label(self.display_table_inner_frame, text=self.seq2[j], font=self.table_header_font, bg=self.bg_color, fg=self.fg_color, relief="solid", bd=1).grid(row=0, column=j+2, sticky="nsew")
        for i in range(m):
            lbl = tk.Label(self.display_table_inner_frame, text=self.seq1[i], font=self.table_header_font, bg=self.bg_color, fg=self.fg_color, relief="solid", bd=1).grid(row=i+2, column=0, sticky="nsew")

        self.display_labels = {} 
        for i in range(m + 1):
            for j in range(n + 1):
                val = self.player_dp_table[i][j] 
                lbl = tk.Label(self.display_table_inner_frame, text=str(val), font=self.dp_cell_font, bg=self.bg_color, fg=self.correct_cell_fg, relief="solid", bd=1) 
                lbl.grid(row=i+1, column=j+1, sticky="nsew")
                self.display_labels[(i,j)] = lbl 

        
        tk.Label(
            self.base_content_frame,
            text="\nPreencha os passos de Alinhamento Ótimo (do final para o início):",
            font=self.small_bold_font,
            fg=self.fg_color,
            bg=self.bg_color
        ).pack(pady=(10, 5))

        ops_table_canvas_frame = tk.Frame(self.base_content_frame, bg=self.bg_color)
        ops_table_canvas_frame.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        self.ops_canvas = tk.Canvas(ops_table_canvas_frame, bg=self.bg_color, highlightbackground=self.fg_color, highlightthickness=1)
        self.ops_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ops_scrollbar_y = ttk.Scrollbar(ops_table_canvas_frame, orient="vertical", command=self.ops_canvas.yview)
        ops_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.ops_canvas.config(yscrollcommand=ops_scrollbar_y.set)
        
        self.ops_table_frame = tk.Frame(self.ops_canvas, bg=self.bg_color)
        self.ops_canvas.create_window((0,0), window=self.ops_table_frame, anchor="nw")
        self.ops_table_frame.bind("<Configure>", lambda e: self.ops_canvas.configure(scrollregion = self.ops_canvas.bbox("all")))

        
        self.ops_table_entries = []
        
        self._criar_tabela_operacoes_simplificada() # Chamada para a nova função de criação

        ops_control_frame = tk.Frame(self.base_content_frame, bg=self.bg_color)
        ops_control_frame.pack(pady=10)
        
        self.confirm_alinhamento_button = ttk.Button(ops_control_frame, text="Confirmar Alinhamento Final", command=self._confirmar_alinhamento_final, style="Accent.Dark.TButton", state=tk.NORMAL)
        self.confirm_alinhamento_button.pack(pady=10) # Centraliza o botão

        # Inicializa o destaque na célula final
        self.current_i_trace = len(self.seq1)
        self.current_j_trace = len(self.seq2)

        self.trace_highlight_rect_id = None 
        self.root.update_idletasks() 
        self._update_trace_highlight_on_display_table(self.current_i_trace, self.current_j_trace) 
        
    def _criar_tabela_operacoes_simplificada(self):
        headers = ["Operação", "Custo", "Char X", "Char Y"]
        self.ops_table_entries = [] 

        # Cabeçalhos
        for col, header_text in enumerate(headers):
            lbl = tk.Label(self.ops_table_frame, text=header_text, font=self.small_bold_font, bg=self.ops_header_bg, fg="white", relief="solid", bd=1)
            lbl.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
        
        num_expected_steps = len(self.alinhamento_operacoes_correto)
        
        for row_idx in range(num_expected_steps): 
            row_entries = []
            for col in range(len(headers)):
                entry = tk.Entry(
                    self.ops_table_frame,
                    width=10 if col == 0 else 5, 
                    font=self.narrative_font,
                    bg=self.ops_entry_bg,
                    fg="white",
                    justify=tk.CENTER,
                    relief="flat",
                    insertbackground="white",
                    highlightbackground="gray", highlightcolor="yellow", highlightthickness=1
                )
                entry.grid(row=row_idx+1, column=col, sticky="nsew", padx=1, pady=1)
                entry.config(state=tk.NORMAL) # Habilita todas as células para preenchimento
                row_entries.append(entry)
            self.ops_table_entries.append(row_entries)

        for col in range(len(headers)):
            self.ops_table_frame.grid_columnconfigure(col, weight=1)

        if self.ops_table_entries:
            self.ops_table_entries[0][0].focus_set()


    def _update_trace_highlight_on_display_table(self, i, j):
        if self.trace_highlight_rect_id is not None: 
            self.display_canvas.delete(self.trace_highlight_rect_id)
            self.trace_highlight_rect_id = None

        if i >= 0 and j >= 0 and (i,j) in self.display_labels:
            label_widget = self.display_labels[(i, j)]
            
            self.root.update_idletasks() 

            lx1 = label_widget.winfo_x()
            ly1 = label_widget.winfo_y()
            lw = label_widget.winfo_width()
            lh = label_widget.winfo_height()

            if self.display_table_frame_canvas_item_id is None:
                print("ERRO: display_table_frame_canvas_item_id não foi definido.")
                return

            frame_coords = self.display_canvas.coords(self.display_table_frame_canvas_item_id)
            if not frame_coords:
                print("ERRO: Não foi possível obter coordenadas do display_table_inner_frame no canvas.")
                return

            frame_x_on_canvas = frame_coords[0]
            frame_y_on_canvas = frame_coords[1]

            x1 = frame_x_on_canvas + lx1
            y1 = frame_y_on_canvas + ly1
            x2 = x1 + lw
            y2 = y1 + lh

            self.trace_highlight_rect_id = self.display_canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="yellow", width=4, tags="trace_highlight"
            )
            self.display_canvas.tag_raise("trace_highlight") 
            
            canvas_width = self.display_canvas.winfo_width()
            canvas_height = self.display_canvas.winfo_height()
            
            scroll_region = self.display_canvas.bbox("all")
            if scroll_region:
                content_width = scroll_region[2] - scroll_region[0]
                content_height = scroll_region[3] - scroll_region[1]
            else: 
                content_width = canvas_width
                content_height = canvas_height

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            scroll_x_fraction = (center_x / content_width) - (canvas_width / (2 * content_width))
            scroll_y_fraction = (center_y / content_height) - (canvas_height / (2 * content_height))

            scroll_x_fraction = max(0.0, min(1.0, scroll_x_fraction))
            scroll_y_fraction = max(0.0, min(1.0, scroll_y_fraction))

            self.display_canvas.xview_moveto(scroll_x_fraction)
            self.display_canvas.yview_moveto(scroll_y_fraction)
        else:
            print(f"AVISO: Célula ({i},{j}) não encontrada em display_labels. Não foi possível destacar.")


    def _confirmar_alinhamento_final(self):
        expected_steps = len(self.alinhamento_operacoes_correto)
        num_player_steps = len(self.ops_table_entries) 

        
        for row_idx in range(num_player_steps):
            for col_idx in range(4): # 'Operação', 'Custo', 'Char X', 'Char Y'
                entry = self.ops_table_entries[row_idx][col_idx]
                val = entry.get().strip()

                
                entry.config(highlightbackground="gray", highlightcolor="gray")

                if not val:
                    messagebox.showwarning("Erro de Preenchimento", f"Célula da linha {row_idx+1}, coluna {col_idx+1} está vazia. Por favor, preencha todas as células.")
                    entry.focus_set()
                    entry.config(highlightbackground="red", highlightcolor="red")
                    return
                if col_idx == 1: 
                    try:
                        int(val)
                    except ValueError:
                        messagebox.showwarning("Erro de Entrada", f"Custo na linha {row_idx+1} deve ser um número inteiro. Verifique o campo e tente novamente.")
                        entry.focus_set()
                        entry.config(highlightbackground="red", highlightcolor="red")
                        return
            
        
        all_steps_correct = True
        
        
        for row_idx in range(max(num_player_steps, expected_steps)):
            player_op = {} # Para armazenar a entrada do jogador de forma estruturada
            current_row_entries = None

            
            if row_idx < num_player_steps:
                current_row_entries = self.ops_table_entries[row_idx]
                try:
                    player_op['type'] = current_row_entries[0].get().strip().upper()
                    player_op['cost'] = int(current_row_entries[1].get().strip())
                    player_op['char_x'] = current_row_entries[2].get().strip().upper()
                    player_op['char_y'] = current_row_entries[3].get().strip().upper()
                except ValueError:
                    
                    all_steps_correct = False
                    if current_row_entries:
                        for entry in current_row_entries:
                            entry.config(bg=self.ops_incorrect_bg, fg="white")
                    continue 
            else: 
                all_steps_correct = False
                continue # Pula para a próxima linha

            # Compara com a operação correta, se ela existe para esta linha
            if row_idx < expected_steps:
                correct_op_tuple = self.alinhamento_operacoes_correto[row_idx]
                correct_op = {
                    'type': correct_op_tuple[0].upper(),
                    'cost': correct_op_tuple[1],
                    'char_x': str(correct_op_tuple[2]).upper(),
                    'char_y': str(correct_op_tuple[3]).upper()
                }

                is_step_correct = (player_op['type'] == correct_op['type'] and
                                   player_op['cost'] == correct_op['cost'] and           
                                   player_op['char_x'] == correct_op['char_x'] and 
                                   player_op['char_y'] == correct_op['char_y'])
                
                if not is_step_correct:
                    all_steps_correct = False
                    if current_row_entries:
                        for entry in current_row_entries:
                            entry.config(bg=self.ops_incorrect_bg, fg="white")
                else:
                    if current_row_entries:
                        for entry in current_row_entries:
                            entry.config(bg=self.ops_correct_bg, state=tk.DISABLED, fg="white")
            else: 
                all_steps_correct = False
                if current_row_entries:
                    for entry in current_row_entries:
                        entry.config(bg=self.ops_incorrect_bg, fg="white", state=tk.DISABLED) 
        
        
        if all_steps_correct and num_player_steps == expected_steps:
            
            final_aligned_s1_list = [op[2] for op in self.alinhamento_operacoes_correto]
            final_aligned_s2_list = [op[3] for op in self.alinhamento_operacoes_correto]

            final_aligned_s1 = "".join(str(x) if x is not None else '' for x in final_aligned_s1_list) 
            final_aligned_s2 = "".join(str(y) if y is not None else '' for y in final_aligned_s2_list)

            
            if final_aligned_s1 == self.alinhamento_seq1_correto and final_aligned_s2 == self.alinhamento_seq2_correto:
                pontos = 300 
                self.game_manager.add_score(pontos)
                messagebox.showinfo("Sucesso na Missão (Parte 2)!", f"Alinhamento genético decifrado com sucesso! Custo mínimo: {self.min_cost_correto}.\nPatógeno identificado!\n\nAlinhamento Final:\nSeq1: {final_aligned_s1}\nSeq2: {final_aligned_s2}")
                self.game_manager.mission_completed("Missao4")
            else:
                pontos = -150 
                messagebox.showerror("Erro de Reconstrução Interna", f"Os passos estão corretos, mas o alinhamento final reconstruído não corresponde ao esperado. Custo mínimo: {self.min_cost_correto}.")
                self.game_manager.mission_failed_options(self, "Reconstrução Inconsistente", "Erro de consistência interna.")
        else:
            self.game_manager.add_score(-200) 
            messagebox.showerror("Falha no Rastreamento Final", f"Seus passos de alinhamento contêm erros ou o número de passos não está correto. Revise as linhas marcadas em vermelho.")
            
            self.game_manager.mission_failed_options(self, "Traceback Falho", "O caminho ótimo não foi totalmente decifrado.")


    def retry_mission(self):
        print("Missao4: retry_mission chamada. Resetando estado para START_MISSION_4.")
        self.game_manager.set_game_state("START_MISSION_4")