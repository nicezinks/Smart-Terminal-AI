# 🤖 Smart Terminal AI

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-success?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-See%20LICENSE-orange?style=for-the-badge)

---

# 📖 Sobre

**Smart Terminal AI** é um assistente de terminal desenvolvido em Python com foco em responder perguntas simples do dia a dia utilizando pesquisa na web, cache local, histórico, gerenciamento de configurações e uma interface moderna para terminal.

O projeto foi organizado de forma modular, permitindo separar responsabilidades entre pesquisa, processamento, cache, histórico, interface, configuração e comunicação com serviços externos.

> **Este projeto foi desenvolvido para responder apenas perguntas simples do dia a dia.**

Ele **não foi criado** para:

- substituir um LLM avançado;
- realizar pesquisas acadêmicas profundas;
- resolver problemas extremamente complexos;
- executar tarefas altamente especializadas;
- manter conversas muito longas.

---

# ✨ Recursos

- Interface moderna para terminal
- Sistema modular
- Pesquisa Web
- Cache local
- Histórico de perguntas
- Sistema de prompts
- Arquivos de configuração em JSON
- Gerenciamento de fontes confiáveis
- Cliente para comunicação com modelo de IA
- Sistema de logs
- Resumo de conteúdo
- Navegação automatizada
- Scraping de páginas
- Testes automatizados
- Organização por módulos
- Estrutura preparada para expansão
- 🆕 **Análise inteligente de sites** (site_analyzer.py)

---

# 🏗 Arquitetura

O projeto foi dividido em módulos independentes.

## main.py

Ponto principal da aplicação.

Responsável por iniciar todos os componentes.

---

## core/

Contém toda a lógica principal.

### ai.py

Gerencia a inteligência principal da aplicação.

### browser.py

Controla a navegação utilizada durante pesquisas.

### cache.py

Responsável pelo cache das respostas.

### config.py

Carrega as configurações.

### google_search_api.py

Realiza pesquisas utilizando mecanismo de busca.

### history.py

Gerencia o histórico.

### llm_client.py

Responsável pela comunicação com o modelo configurado.

### logger.py

Gerencia logs.

### scraper.py

Extrai conteúdo das páginas.

### search.py

Centraliza o mecanismo de pesquisa.

### summarizer.py

Resume conteúdos encontrados.

### trusted_sources.py

Gerencia fontes consideradas confiáveis.

### utils.py

Funções auxiliares utilizadas pelo restante do projeto.

### 🆕 site_analyzer.py

**NOVO!** Analisador inteligente de sites. Recebe um link, extrai o conteúdo usando a API pública Jina AI Reader e gera um resumo completo do que o site quer transmitir ao leitor, usando a Pollinations AI.

**Como usar:**
```bash
python core/site_analyzer.py https://exemplo.com
```

Ou via import:
```python
from core.site_analyzer import SiteAnalyzer
analyzer = SiteAnalyzer()
resultado = analyzer.analyze("https://exemplo.com")
print(resultado["summary"])
```

---

## terminal/

Responsável pela interface.

- ui.py
- colors.py
- animations.py

---

## tests/

Contém testes automatizados.

- test_cache.py
- test_history.py
- test_utils.py

---

# 📂 Estrutura

```text
Smart-Terminal-AI/
│
├── core/
│   ├── ai.py
│   ├── browser.py
│   ├── cache.py
│   ├── config.py
│   ├── google_search_api.py
│   ├── history.py
│   ├── llm_client.py
│   ├── logger.py
│   ├── scraper.py
│   ├── search.py
│   ├── site_analyzer.py      ← 🆕 NOVO
│   ├── summarizer.py
│   ├── trusted_sources.py
│   └── utils.py
│
├── logs/
├── plugins/
├── terminal/
│   ├── animations.py
│   ├── colors.py
│   └── ui.py
├── tests/
├── main.py
├── config.json
├── settings.json
├── prompts.json
├── trusted_sources.json
├── cache.json
├── history.json
├── requirements.txt
├── LICENSE
└── README.md
```

---

# ⚙ Funcionamento

Fluxo geral:

```
Usuário

↓

Interface

↓

Pesquisa

↓

Processamento

↓

Resumo

↓

Cache

↓

Histórico

↓

Resposta Final
```

---

# 🔍 Funcionamento Interno

## Pesquisa

A aplicação pesquisa informações utilizando o mecanismo configurado.

## Processamento

Os resultados encontrados são organizados antes da resposta.

## Cache

Resultados podem ser armazenados para evitar pesquisas repetidas.

## Histórico

As perguntas ficam registradas localmente.

## Prompts

Os prompts são carregados através do arquivo:

```
prompts.json
```

## Configuração

As configurações ficam separadas em arquivos JSON.

## Interface

Toda a interação ocorre pelo terminal.

---

# 💻 Tecnologias

- Python
- JSON
- Requests
- BeautifulSoup
- Rich
- Prompt Toolkit
- Colorama
- Markdown
- LXML

---

# 📦 Dependências

As dependências são instaladas através do:

```
requirements.txt
```

Exemplo:

```bash
pip install -r requirements.txt
```

---

# 🚀 Instalação

Clone o projeto:

```bash
git clone "gh repo clone nicezinks/Smart-Terminal-AI"
```

Entre na pasta:

```bash
cd Smart-Terminal-AI
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python main.py
```

---

# ⚙ Configuração

O projeto utiliza diversos arquivos JSON.

| Arquivo | Função |
|----------|---------|
| config.json | Configuração geral |
| settings.json | Preferências da aplicação |
| prompts.json | Prompts utilizados |
| trusted_sources.json | Fontes confiáveis |
| cache.json | Cache local |
| history.json | Histórico |

---

# 📚 Exemplos

Pergunta:

```
Qual é a capital do Brasil?
```

Resposta esperada:

```
Brasília.
```

---

Pergunta:

```
Quem criou Python?
```

Resposta:

```
Guido van Rossum.
```

---

# 🆕 Análise de Sites

Analise qualquer site e descubra o que ele quer transmitir:

```bash
python core/site_analyzer.py https://openai.com
```

O módulo irá:
1. Extrair o conteúdo textual do site via **Jina AI Reader** (API pública gratuita)
2. Gerar um resumo completo via **Pollinations AI** (API pública gratuita)
3. Explicar: mensagem principal, público-alvo, intenção e pontos-chave

---

# ❓ FAQ

### O projeto utiliza IA?

Sim.

---

### Funciona offline?

Alguns recursos dependem de acesso à internet.

---

### Posso modificar?

Sim.

---

### O cache pode ser apagado?

Sim.

---

### O histórico pode ser limpo?

Sim.

---

### Funciona no Windows?

Sim.

---

### Funciona no Linux?

Sim.

---

### Funciona no macOS?

Sim.

---

# 🛣 Roadmap

- Melhorar desempenho
- Mais testes
- Mais plugins
- Melhor documentação
- Interface ainda mais rica
- Novos provedores
- Melhor gerenciamento de cache
- Otimizações internas

---

# 🤝 Contribuindo

Contribuições são bem-vindas.

1. Faça um Fork.

2. Crie uma Branch.

3. Faça suas alterações.

4. Commit.

5. Push.

6. Abra um Pull Request.

---

# 🔒 Segurança

Boas práticas:

- Não exponha chaves de API.
- Revise alterações antes de executar.
- Utilize dependências atualizadas.
- Mantenha o Python atualizado.
- Utilize apenas fontes confiáveis.

Caso encontre algum problema de segurança, abra uma **Issue** descrevendo o ocorrido.

---

# ⚠ Limitações

Este projeto possui algumas limitações por projeto e escopo:

- Não substitui modelos avançados de linguagem.
- Foi desenvolvido para perguntas simples.
- A qualidade das respostas depende das informações obtidas.
- Algumas funcionalidades exigem conexão com a internet.
- O desempenho pode variar conforme o ambiente.

---

# 📜 Aviso Legal (Disclaimer)

Este software foi desenvolvido exclusivamente para fins educacionais, aprendizado e demonstração técnica.

O desenvolvedor não incentiva, apoia ou autoriza qualquer utilização que viole leis, regulamentos, direitos de terceiros ou termos de serviço de plataformas.

Toda a responsabilidade pelo uso deste projeto é exclusivamente do usuário.

O desenvolvedor não poderá ser responsabilizado por uso inadequado do software, alterações realizadas por terceiros, atividades ilegais, perda de dados, danos diretos ou indiretos, ou quaisquer consequências decorrentes da utilização deste projeto.

Caso sejam identificados bugs, falhas ou vulnerabilidades, recomenda-se abrir uma **Issue** para que possam ser analisados e corrigidos.

Ao utilizar este software, o usuário declara estar ciente e concordar com os termos apresentados nesta documentação.

---

# 📄 Licença

Este projeto acompanha um arquivo **LICENSE**.

Consulte-o para conhecer todos os termos de utilização, distribuição e modificação do software.

---

# 👨‍💻 Desenvolvedor

Projeto desenvolvido por um desenvolvedor independente com foco em Python, organização de código, arquitetura modular e projetos Open Source.

Caso queira contribuir com melhorias, correções ou novas funcionalidades, fique à vontade para abrir uma **Issue** ou enviar um **Pull Request**.

---

**⭐ Se este projeto foi útil para você, considere deixar uma estrela no repositório.**
