
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
│   ├── site_analyzer.py    
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
