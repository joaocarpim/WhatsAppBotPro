# 📱 WhatsApp Bot Pro (v2.0)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green)
![Selenium](https://img.shields.io/badge/Bot-Selenium-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**WhatsApp Bot Pro** é uma ferramenta desktop de automação para envio massivo de mensagens. Desenvolvido em Python com arquitetura modular, utiliza **PySide6** para uma interface moderna em Dark Mode e **Selenium** para controlar o WhatsApp Web.

---

![Demonstração do WhatsApp Bot Pro](assets/whatsBot.gif)

---

## 🚀 Funcionalidades Principais

* **🤖 Automação Web:** Controla o navegador para enviar mensagens automaticamente.
* **📱 Validação de Números:** Formata e verifica números antes do envio.
* **🛡️ Sistema Anti-Bloqueio:** Implementa delays de segurança (8s) entre mensagens.
* **📊 Relatórios em Tempo Real:** Métricas de sucesso, falhas e taxa de êxito na interface.
* **🎨 Interface Biohacker:** Design moderno, responsivo e com efeitos de brilho (Glow).
* **⚡ Arquitetura Modular:** Código limpo separado em Bot, UI e Threads.

---

# 💼 Estudo de Caso: WhatsApp Bot Pro v2.0
> **Da Automação Monolítica à Arquitetura Modular Escalável**

Este documento detalha o processo de engenharia, as decisões arquiteturais e os desafios técnicos superados no desenvolvimento do **WhatsApp Bot Pro v2.0**.

---

## 1. O Desafio (O Problema)

A versão inicial do projeto (Legacy v1.0) consistia em um único script (`app.py`) de aproximadamente 400 linhas. Embora funcional para testes rápidos, apresentava problemas críticos de engenharia:

* **Bloqueio de Interface (UI Freezing):** O loop do Selenium rodava na *Main Thread* da interface gráfica, fazendo com que a janela travasse e exibisse "Não Respondendo" durante o envio de mensagens.
* **Baixa Manutenibilidade:** Lógica de negócio, interface e controle de estado estavam misturados. Adicionar uma nova feature (ex: envio de imagens) exigiria reescrever grandes partes do código.
* **Acoplamento Forte:** Não era possível reutilizar o componente de bot em outros projetos sem levar a interface gráfica junto.

---

## 2. A Solução (Arquitetura Proposta)

O objetivo da versão 2.0 foi desacoplar responsabilidades e profissionalizar a base de código. Adotamos o padrão **Modular Architecture**, organizando o sistema em camadas lógicas distintas para garantir a separação de interesses (*Separation of Concerns*):

### 2.1 Stack Tecnológico
* **Linguagem:** Python 3.10+
* **GUI Engine:** PySide6 (Qt for Python) - Para interfaces modernas e responsivas.
* **Automação:** Selenium WebDriver - Para controle preciso do navegador.
* **Concorrência:** QThread & Signals/Slots - Para processamento assíncrono.

### 2.2 Organização dos Módulos
A estrutura monolítica foi substituída por módulos coesos e independentes:

1.  **Módulo de Bot (Core Logic):**
    Responsável exclusivamente pela automação do navegador (Selenium). Contém os métodos de conexão, validação de números e injeção de mensagens, totalmente isolado da interface gráfica.

2.  **Módulo de Interface (UI Layer):**
    Gerencia a apresentação visual utilizando PySide6. Inclui a janela principal, componentes estilizados (como botões com efeito Glow) e o sistema de estilos (QSS).

3.  **Módulo de Processamento (Workers/Threads):**
    A camada crítica que conecta a UI ao Bot. Utiliza *Threads* dedicadas para realizar operações pesadas (como o loop de envio) em segundo plano, mantendo a interface fluida e responsiva.

4.  **Utilitários (Helpers):**
    Funções auxiliares para formatação de dados, logs e tratamento de strings, acessíveis por todo o sistema.

---

## 3. Desafios Técnicos e Implementações

### ⚡ Concorrência e Multithreading
O maior desafio em aplicações GUI com Python é manter a interface responsiva enquanto tarefas de I/O (Input/Output) ocorrem.

* **Solução:** Implementação de `QThread`.
* **Implementação:** Criamos a classe `SendThread`. Em vez de o botão "Enviar" chamar o Selenium diretamente, ele dispara a thread.
* **Comunicação:** A thread comunica o progresso de volta para a UI usando `Signals` (padrão Observer), atualizando barras de progresso e logs sem conflito de memória.

### 🛡️ Persistência de Sessão e Segurança
Para evitar que o usuário precise escanear o QR Code a cada execução:

* **Profile Management:** O bot configura o Chrome para usar um diretório de perfil específico.
* **Segurança:** O arquivo `.gitignore` foi configurado estritamente para impedir que a pasta de sessão (contendo cookies e tokens de acesso) fosse enviada ao repositório git.

### 🎨 Design System "Biohacker"
A interface padrão do Qt é sóbria. Para dar uma identidade moderna ao produto:

* **QSS (Qt Style Sheets):** Criamos um arquivo de estilos CSS-like para customizar todos os widgets.
* **Custom Widgets:** Desenvolvemos classes que herdam de `QPushButton` e adicionam efeitos de sombra e brilho (`QGraphicsDropShadowEffect`), criando um visual neon/cyberpunk.

---

## 4. Otimizações de Performance (Anti-Ban)

Um bot de WhatsApp precisa agir como humano para evitar bloqueios. Implementamos:

1.  **Delays Aleatórios:** Intervalos de segurança (Sleep) não-lineares entre ações.
2.  **Validação Prévia:** Antes de tentar enviar, o bot limpa e formata o número (Regex). Se o número for inválido, ele nem abre o chat, economizando recursos e reduzindo comportamento suspeito.
3.  **Digitação Humana:** O texto não é colado de uma vez; ele é inserido simulando eventos de teclado, inclusive o uso de `Shift+Enter` para quebras de linha.

---

## 5. Resultados Alcançados

| Métrica | Versão 1.0 (Monolito) | Versão 2.0 (Modular) |
| :--- | :--- | :--- |
| **Responsividade da UI** | Travava durante envio | 100% Fluida (60fps) |
| **Manutenibilidade** | Difícil (Código Espaguete) | Alta (Módulos isolados) |
| **Escalabilidade** | Baixa | Alta (Fácil adicionar novas features) |
| **Reutilização** | Nenhuma | Bot pode ser usado via CLI ou API |

---

## 🛠️ Stack Tecnológico

* **Linguagem:** Python 3.10+
* **Interface Gráfica (GUI):** PySide6 (Qt for Python)
* **Web Scraping:** Selenium WebDriver
* **Gerenciamento de Driver:** Webdriver-Manager

---

## 📂 Estrutura do Projeto

```text
WhatsAppBot/
│
├── main.py                 # 🚀 Ponto de entrada
├── requirements.txt        # Dependências
│
└── src/                    # Código Fonte
    ├── bot/                # 🧠 Lógica do Selenium
    │   └── whatsapp_bot.py
    │
    ├── ui/                 # 🎨 Interface Gráfica
    │   ├── main_window.py
    │   ├── widgets.py
    │   └── styles.py
    │
    ├── threads/            # ⚡ Execução em Background
    │   ├── connection_thread.py
    │   └── send_thread.py
    │
    └── utils/              # 🛠️ Utilitários
        └── helpers.py
```

## 🚀 Como Instalar e Executar

Siga este guia rápido para rodar o projeto na sua máquina:

### 1. Prepare o Ambiente
Certifique-se de ter o [Python 3.10+](https://www.python.org/downloads/) e o **Google Chrome** instalados (o bot utiliza o navegador oficial para automação).

### 2. Clone e Instale
Abra seu terminal (Git Bash, Powershell ou CMD) e rode:

```bash
# 1. Clone o repositório
git clone [https://github.com/joaocarpim/whatsapp-bot-pro.git](https://github.com/joaocarpim/whatsapp-bot-pro.git)

# 2. Entre na pasta
cd WhatsAppBot

# 3. Crie um ambiente virtual (Opcional, mas recomendado)
python -m venv venv

# No Windows ative com:
.\venv\Scripts\activate

# No Linux/Mac ative com:
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt
```

## ▶️ Como Usar
Com o ambiente virtual ativado, execute o arquivo principal:

```bash
python main.py
```

### A interface abrirá. Siga os passos:

1. Clique no botão CONECTAR no canto superior esquerdo.

2. Um navegador abrirá. Leia o QR Code do WhatsApp Web com seu celular.

3. Aguarde o status na interface mudar para CONECTADO (Verde).

4. Digite sua Mensagem na caixa de texto central.

5. Cole a lista de Números (um por linha, ex: 11999999999) na caixa de alvos.

6. Clique em EXECUTAR e acompanhe o progresso no terminal lateral.

### ⚠️ Aviso Legal
#### Este software foi desenvolvido apenas para fins educacionais e de automação legítima (ex: comunicação com clientes que autorizaram o contato). O uso de bots para envio de SPAM ou mensagens não solicitadas viola os Termos de Serviço do WhatsApp e pode resultar no banimento permanente do número. Utilize com responsabilidade.

## 🤝 Contribuição

Contribuições são bem-vindas!

1. Faça um **Fork** do projeto.
2. Crie uma **Branch** para sua Feature:
```bash
   git checkout -b feat/IncrivelFeature
```
3. Faça o Commit:
```bash
git commit -m 'Add some IncrivelFeature'
```
4. Faça o Push:
```bash
git push origin feat/IncrivelFeature
```
5. Abra um Pull Request.

<p align="center">
Desenvolvido com 💙 por <a href="https://github.com/joaocarpim">joaocarpim</a>
</p>
