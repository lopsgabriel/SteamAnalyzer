> 📘 This README is also available in [English](docs/README.en.md)
# Steamlyzer API 🚀 *(em desenvolvimento)*

**Status**: 🚧 Em desenvolvimento  
**Versão atual**: `0.x`  
**Última atualização**: `30/05/2025`

---

## 📌 Descrição

A **Steamlyzer API** é uma aplicação que analisa o perfil de um usuário da Steam com base em dados públicos fornecidos pela Steam Web API. A proposta é oferecer uma análise profunda do estilo de jogo do usuário, utilizando informações como a biblioteca de jogos do jogador, gêneros jogados, categorias, tempo de jogo e conquistas. Ao final da análise, o sistema define o "tipo de jogador" baseado em seus hábitos.

---

## 🤖 Inteligência Artificial

A API utiliza **modelos de linguagem (LLMs)** para gerar insights personalizados com base nos dados coletados do perfil Steam do usuário.  
Atualmente, a integração está sendo feita com:

- **Google Gemini**: utilizado para gerar descrições do tipo de jogador de forma dinâmica e adaptada aos hábitos do usuário. A IA recebe informações como gêneros jogados, categorias e tempo de jogo para retornar análises interpretativas.

Essas integrações são feitas de forma dinâmica, com base em prompts contextuais e dados agregados das categorias, gêneros e padrões de uso do jogador. O resultado é uma resposta rica, humanizada e adaptável ao perfil analisado.

---

## 📚 Funcionalidades já implementadas

- [x] Análise básica de perfil Steam via Steam ID ou URL personalizada  
- [x] Coleta e agrupamento de gêneros e categorias dos jogos  
- [x] Definição automática de "tipo de jogador" com base nos dados  
- [x] Integração com IA para resposta narrativa e interpretativa  
- [x] Exibição interativa de gráficos e análises no front-end  
- [x] API REST utilizando Django REST Framework

---

## ⚙️ Tecnologias utilizadas

- **Backend:** Django + Django REST Framework  
- **Assíncrono:** Aiohttp, asyncio  
- **Requisições HTTP:** Requests  
- **Testes:** Pytest  
- **Banco de dados:** SQLite (em desenvolvimento)  
- **Frontend:** React + Vite + Tailwind CSS  
- **IA / NLP:** Google Gemini 

---

## 🛠️ Como rodar localmente

```bash
git clone https://github.com/seu-usuario/steamlyzer-api.git
cd steamlyzer-api
python -m venv venv
source venv/bin/activate  # no Windows use venv\Scripts\activate
cd Backend
pip install -r requirements.txt
python manage.py runserver
```

---

## 🔍 Endpoints disponíveis

| Rota             | Método | Descrição                               |
|------------------|--------|------------------------------------------|
| `/`      | GET    |Página inicial. Recebe o steam_id(codigo do perfil da steam) e exibe a análise interativa com base nas respostas da IA. |


> Obs: Para utilizar os endpoints, o parâmetro `steam_id` pode ser tanto o ID64 quanto uma vanity URL da Steam.

---

## 🧪 Testes

Para rodar os testes:

```bash
pytest
```

---

## 🧩 Contribuição

Este projeto está em **processo de desenvolvimento**, e qualquer sugestão, correção ou contribuição será muito bem-vinda.  
Estamos seguindo os padrões de commit descritos em [Conventional Commits](https://www.conventionalcommits.org/pt-br/) e documentados neste repositório.

---

## 📌 Observações

> 🔧 Esta é uma **versão em desenvolvimento** da API.  
> Algumas funcionalidades estão incompletas ou sujeitas a alterações significativas.  
> Use por sua conta e risco! Contribuições e feedbacks são bem-vindos.
