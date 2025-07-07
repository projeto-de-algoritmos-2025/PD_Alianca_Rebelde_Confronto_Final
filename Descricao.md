# Star Wars: Aliança Rebelde – O Confronto Final

## Uma nova era de estratégias

### O Império está ferido, mas longe de derrotado. A Rebelião precisa evoluir. Nesta fase crítica da guerra, apenas as decisões mais otimizadas poderão garantir a sobrevivência da esperança. Você, Coordenador(a) de Operações, terá em mãos os desafios mais intricados da campanha rebelde, e só a Programação Dinâmica será capaz de guiar o caminho.

## SUA ASTUCIA É NOSSA MELHOR ARMA!

## Descrição do Jogo

<strong>"Aliança Rebelde - O Confronto Final"</strong> é um jogo de estratégia e puzzle narrativo, que se passa depois do jogo "Aliança Rebelde-  Operações Críticas" e "Aliança Rebelde 2 - A volta dos desafios" . Nele o jogador assume o papel de um(a) Coordenador(a) de Operações da Aliança Rebelde. A Rebelião está em sua fase mais crítica. Apenas com estratégias otimizadas será possível vencer. Cada missão exige o uso de técnicas de **Programação Dinâmica** para encontrar a melhor solução diante de recursos escassos, decisões em cadeia e cenários complexos.

Cada missão foi pensada para explorar não só os fundamentos dos algoritmos, mas também como eles podem ser aplicados em situações críticas, onde o tempo, a precisão e a estratégia são vitais.

## Público-Alvo

- Estudantes da disciplina de Projeto de Algoritmos;
- Entusiastas de jogos de puzzle e estratégia;
- Fãs de ficção científica com temas de rebelião, espionagem e operações táticas.

## Objetivos do Jogo

- **Para o Jogador:** Concluir com sucesso todas as missões ao aplicar a estratégia de Programação Dinâmica para resolver problemas em larga escala, avançando na narrativa e minando as operações complexas do Império.
- **Educacional:** Proporcionar uma compreensão intuitiva e prática da aplicação e do funcionamento de diferentes algoritmos baseados em Programação Dinâmica em contextos variados e significativos.

## Missões

### MISSÃO 1: “Sombras no Tempo”

- **Algoritmo**: Weighted Interval Scheduling
- **Contexto:** Diversas células rebeldes enviam pedidos de extração e sabotagem em diferentes sistemas estelares. No entanto, há sobreposição de tempos e recursos limitados para atender todos.
- **Descrição:** O jogador recebe uma lista de missões com início, fim e impacto estratégico. A missão é selecionar o conjunto ótimo que não se sobrepõe e maximize o impacto total.
- **Desafio:** Implementar a tabela de programação dinâmica, calcular a maior soma possível de valores e reconstruir a sequência de operações selecionadas.

### MISSÃO 2: “Ascensão Inesperada”

- **Algoritmo**: Maior Subsequência Crescente (LIS)
- **Contexto**: Um novo grupo de pilotos iniciantes quer provar seu valor, mas suas chances dependem de uma escalada correta nos simuladores. Cada treinamento tem uma dificuldade crescente.
- **Descrição**: O jogador deve identificar a sequência mais longa de treinamentos que cada recruta pode seguir, com dificuldades sempre maiores — maximizando o crescimento tático da nova geração.
- **Desafio**:  Criar a matriz de DP que identifica o maior número de treinos possíveis em ordem crescente e mostrar a trajetória do recruta selecionado.

### MISSÃO 3: “Carga de Resistência”

- **Algoritmo**: Knapsack (PD)
- **Contexto**: A nave cargueira da Rebelião pode levar apenas uma quantidade limitada de suprimentos até uma base sitiada. É necessário decidir o que levar para maximizar o impacto na resistência.
- **Descrição**:Cada item possui peso e valor. O jogador deve montar a carga mais eficiente sem ultrapassar o limite da nave.
- **Desafio**: Preencher a matriz de DP, identificar a solução ótima e listar os itens selecionados para o carregamento final.

### MISSÃO 4: “DNA de Esperança”

- **Algoritmo**: Alinhamento de Sequências (Sequence Alignment)
- **Contexto**:  A Rebelião interceptou sequências genéticas de um experimento imperial. A única maneira de descobrir sua origem é alinhar as sequências com as bases de dados da Velha República.
- **Descrição**: O jogador deve alinhar duas sequências com penalidades para desalinhamento e identificar a similaridade entre elas.
- **Desafio**:  Preencher a matriz de pontuação, aplicar backtracking para encontrar o alinhamento ótimo e decidir se o código genético é natural ou modificado.

### MISSÃO 5: “O Eco das Escolhas”

- **Contexto**:  O Alto Conselho da Aliança convoca você para uma última reunião estratégica. Cada decisão tomada ao longo da campanha será revisitada. É hora de refletir sobre o impacto de cada missão.
- **Descrição**: O jogador responde perguntas baseadas nas missões anteriores. Cada resposta correta revela uma parte do plano final. Ao final, o Conselho vota unanimemente pela execução do plano que você ajudou a construir.
- **Desafio**:  Missão de recapitulação e reforço de aprendizado, com escolhas múltiplas, cenários visuais e epílogo alternativo baseado no desempenho geral.