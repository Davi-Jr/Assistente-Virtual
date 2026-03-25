# 🤖 Isa - Assistente Virtual

Isa é uma assistente virtual desenvolvida em Python, capaz de realizar tarefas por comando de voz, como informar a hora, abrir sites, tocar músicas e muito mais. O projeto tem fins acadêmicos e demonstra o uso de automação com voz e web. Futuramente, será integrada com IA local via Ollama.

---

## 📋 Índice

- [🛠️ Tecnologias](#tecnologias)
- [✅ Funcionalidades](#funcionalidades)
- [📋 Pré-requisitos](#pré-requisitos)
- [📥 Instalação](#instalação)
- [🚀 Como usar](#como-usar)
- [🎥 Demonstração](#demonstração)
- [📄 Licença](#licença)

---

## 🛠️ Tecnologias <a id="tecnologias"></a>

O projeto foi inicialmente desenvolvido com **Anaconda Navigator** e **PyCharm**, mas neste guia será apresentada uma alternativa utilizando **VS Code**, pela sua leveza e preferência pessoal.

**Principais ferramentas:**
- Python
- Anaconda / Miniconda
- VS Code (ou PyCharm)
- Bibliotecas: speech_recognition, pyttsx3, pywhatkit, requests, entre outras (veja [requirements.txt](Isa/requirements.txt))

---

## ✅ Funcionalidades <a id="funcionalidades"></a>

| Ícone | Funcionalidade | Status |
|-------|---------------|--------|
| 🕒 | Informar a data e hora atual | ✅ Disponivel |
| 🌐 | Acessar sites como Google, YouTube, etc. | ✅ Disponivel |
| 🎵 | Tocar músicas no YouTube Music | ✅ Disponivel |
| ☁️ | Consultar a meteorologia via API OpenWeatherMap | ✅ Disponivel |

---

## 📋 Pré-requisitos <a id="pré-requisitos"></a>

Antes de começar, certifique-se de ter:

- [✅] Python instalado (Versão para uso : **3.9.23**)
- [✅] [Anaconda ou Miniconda](https://www.anaconda.com/products/distribution) instalado
- [✅] [Google Chrome](https://www.google.com/chrome/) instalado
- [✅] [VS Code](https://code.visualstudio.com/) (ou PyCharm, opcional)
- [✅] Repositório clonado

---

## 📥 Instalação <a id="instalação"></a>

### 1. Clone o repositório

```bash
git clone https://github.com/Davi-Jr/Assistente-Virtual.git

cd Isa
```

### 2. Crie o ambiente virtual

Como estamos utilizando o Anaconda, **não é necessário baixar uma versão específica do Python separadamente.** O ambiente `isa` será criado para isolar as dependências do projeto.

```bash
conda create -n isa python==3.9.23

conda activate isa
```

![Criar ambiente](Isa/img/create-conda.png)

<img src="Isa/img/activate-conda.png" width="62%">

> **Dica:** Após criar o ambiente, selecione o interpretador no VS Code. Use o atalho `Ctrl+Shift+P` e selecione a versão do Python do ambiente `isa`.

![Selecionar interpretador](Isa/img/interpretador.png)

### 3. Instale as dependências

Última etapa: baixar todas as dependências necessárias. Leva menos de *1 minuto*.

```bash
pip install -r requirements.txt
```

![Instalar dependências](Isa/img/requirements.png)

---

## 🚀 Como usar <a id="como-usar"></a>

1. Execute o arquivo principal:
   ```bash
   python Isa.py
   ```

2. A assistente ouvirá seus comandos de voz e responderá automaticamente.

---

## 🎥 Demonstração <a id="demonstração"></a>

<div align="left">
  <a href="https://youtu.be/RFPc1wYizew" target="_blank">
    <img 
      src="https://img.youtube.com/vi/RFPc1wYizew/maxresdefault.jpg" 
      alt="▶ Assistente em Vídeo — clique para assistir" 
      width="600"
      style="border-radius: 12px; border: 2px solid #333;"
    />
  </a>
  <br/>
  <sub>▶ Clique na imagem para assistir ao vídeo de demonstração</sub>
</div>

---

## 📄 Licença <a id="licença"></a>

Este projeto é de uso acadêmico. Sinta-se livre para estudar e modificar conforme necessário.

---

