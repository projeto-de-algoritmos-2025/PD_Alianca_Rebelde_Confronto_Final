# PD_Alianca_Rebelde_Confronto_Final
A Rebelião está em sua fase mais crítica. Apenas com estratégias otimizadas será possível vencer. Cada missão exige o uso de técnicas de Programação Dinâmica para encontrar a melhor solução diante de recursos escassos, decisões em cadeia e cenários complexos.

<h2 align="center">Star Wars: Aliança Rebelde - O Confronto Final</h2>

<div align="center">
    Figura 1: Aliança Rebelde
    <br>
    <img src="https://raw.githubusercontent.com/projeto-de-algoritmos-2025/Alianca_Rebelde-Algoritmos_Ambiciosos/refs/heads/main/Alianca_Rebelde/alianca_simbolo.png" width="500">
    <br>
    <br>
</div>

<h2 align="center">É dividindo que se consquista!</h2>

<strong>"Aliança Rebelde - O Confronto Final"</strong> é um jogo de estratégia e puzzle narrativo, que se passa depois do jogo "Aliança Rebelde-  Operações Críticas" e "Aliança Rebelde 2 - A volta dos desafios" . Nele o jogador assume o papel de um(a) Coordenador(a) de Operações da Aliança Rebelde. A Rebelião está em sua fase mais crítica. Apenas com estratégias otimizadas será possível vencer. Cada missão exige o uso de técnicas de Programação Dinâmica para encontrar a melhor solução diante de recursos escassos, decisões em cadeia e cenários complexos.

Que a Força esteja com você!

**Número da Lista**: 5
**Conteúdo da Disciplina**: Programação Dinâmica <br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 21/1039573 | Larissa Stéfane Barboza Santos |
| 21/1029497  | Mylena Angélica Silva Farias  |

## Sobre 

Esse repositório apresenta o jogo Aliança Rebelde - O Confronto Final, uma aventura textual interativa onde você assume o papel de um(a) estrategista crucial para a Aliança Rebelde. 

Para mais detalhes sobre a história, os personagens, os algoritmos abordados e a mecânica de jogo, acesse a documentação em [descrição](/PD_Alianca_Rebelde_Confronto_Final/Descricao.md)

### Missões do Jogo

- Missão 1: Sombras no Tempo - Weighted Interval Scheduling
- Missão 2: Ascensão Inesperada - Maior Subsequência Crescente
- Missão 3: Carga de Resistência - Knapsack com PD
- Missão 4: DNA de Esperança - Alinhamento de Sequências
- Missão 5: O Eco das Escolhas


Para ter acesso aos códigos dos algoritmos clique em [Aliança Rebelde- O Confronto Final](/algoritmos_pd/)

## Link do vídeo

Acesse ao vídeo [aqui](ADICIONAR LINK)

## Screenshots

Abaixo estão os screenshots do projeto

### Missão 1 - Sombras no Tempo - (Weighted Interval Scheduling)
#### Missão 1 - Introdução
![Missão 1 - Introdução](/img/missao1-1.png)
#### Missão 1 - Desafio
![Missão 1 - Desafio](/img/missao1-2.png)

#### Missão 1 - Acerto
![Missão 1 - Acerto](/img/missao1-3.png)


### Missão 2 - Ascensão Inesperada - (Maior Subsequência Crescente)


#### Missão 2 - Introdução e Desafio
![Missão 2 - Introdução](/img/missao2-1.png)
#### Missão 2 - Acerto
![Missão 2 - Desafio](/img/missao2-2.png)


#### Missão 2 - Acerto

## Instalação 

### Para mais detalhes:

Para mais detalhes e passo a passo da execução, acesse a documentação em [Aliança Rebelde - Confronto Final](/PD_Alianca_Rebelde_Confronto_Final/)

#### 1. Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados:

* **Python 3:** O jogo foi desenvolvido usando Python 3 (versão 3.7 ou superior é recomendada). Você pode baixar o Python em [python.org](https://www.python.org/downloads/).
    * Durante a instalação no Windows, marque a opção "Add Python to PATH" ou similar.
* **Git:** Necessário para clonar o repositório do jogo. Você pode baixar o Git em [git-scm.com](https://git-scm.com/downloads).
* **Tkinter:** Esta é a biblioteca gráfica que o jogo utiliza.
    * **Windows e macOS:** Geralmente, o Tkinter já vem instalado com o Python.
    * **Linux:** Se não estiver instalado, você pode instalá-lo usando o gerenciador de pacotes da sua distribuição. Por exemplo, em sistemas baseados em Debian/Ubuntu:
        ```bash
        sudo apt-get update
        sudo apt-get install python3-tk
        ```

#### 2. Configuração do Jogo

Siga os passos abaixo para configurar o jogo no seu computador:

##### a. Clonar o Repositório:

Abra o seu terminal ou prompt de comando e navegue até o diretório onde você deseja salvar o jogo. Em seguida, clone o repositório do GitHub com o seguinte comando (substitua `SEU_USUARIO_GITHUB/NOME_DO_REPOSITORIO` pelo link correto do seu projeto):

```bash
git clone [https://github.com/SEU_USUARIO_GITHUB/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO_GITHUB/NOME_DO_REPOSITORIO.git)
```

sso criará uma pasta com o nome do repositório contendo todos os arquivos do jogo. Acesse essa pasta:

```bash
cd NOME_DO_REPOSITORIO
```

##### b. (Opcional, mas Recomendado) Criar um Ambiente Virtual:

Usar um ambiente virtual é uma boa prática para isolar as dependências do projeto.

```bash
python3 -m venv venv_alianca_rebelde_confronto_final
```

Ative o ambiente virtual:

#### No Windows:

```bash.\venv_alianca_rebelde_confronto_final\Scripts\activate
```

#### No macOS e Linux:

```bash
source venv_alianca_rebelde_confronto_final/bin/activate
```

Você saberá que o ambiente virtual está ativo porque o nome dele aparecerá no início do seu prompt do terminal.

#### 3. Estrutura de Pastas Esperada
Para que o jogo funcione corretamente, especialmente o carregamento de imagens e módulos, ele espera a seguinte estrutura de pastas dentro do diretório principal do projeto:

      PD_Alianca_Rebelde_Confronto_Final/
      ├── algoritmos_pd/                 # Pasta para os algoritmos
      │            ├── __init__.py
      │            ├── alinhamento_sequencias.py
      │            ├── knapsack_com_pd.py
      │            ├── maior_subsequencia_crescente.py
      │            ├── weighted_interval_scheduling.py
      |
      ├── img/        # Pasta com imagens
      |
      ├── missoes/                    # Pasta para as missões 
      │   ├── __init__.py
      │   ├── missao1.py
      │   ├── missao2.py
      │   ├── missao3.py
      │   ├── missao4.py
      |   ├── missao5.py
      ├── main.py                     # Arquivo principal para executar o jogo 
      ├── Descricao.md                     # Arquivo de manual
      └── README.md                   


#### 4. Como Rodar o Jogo

Depois de clonar o repositório e (opcionalmente) ativar o ambiente virtual:

Navegue pelo terminal até a pasta raiz do projeto (onde o arquivo main.py está localizado).

Execute o jogo com o seguinte comando:

```bash
python3 main.py
```
(Ou python main.py dependendo da sua configuração do Python).

Isso deve iniciar a janela do jogo "Aliança Rebelde - Operações Críticas".

**Linguagem**: python<br>

