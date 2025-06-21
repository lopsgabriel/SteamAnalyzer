
# Steamlyzer API 🚀 *(under development)*

**Status**: 🚧 Under development  
**Current version**: `0.x`  
**Last update**: `2025-06-22`

---

## 📌 Description

The **Steamlyzer API** is an application that analyzes a Steam user's profile based on public data provided by the Steam Web API.  
The goal is to offer a deep insight into the user's gaming behavior by analyzing their game library, genres played, categories, playtime, and achievements.  
At the end of the analysis, the system determines the player's "type" based on their habits.

---

## 🤖 Artificial Intelligence

The API uses **large language models (LLMs)** to generate personalized insights based on the collected Steam profile data.  
Currently, the integration is being done with:

- **Google Gemini**: used to dynamically generate player-type descriptions tailored to the user's gaming habits. The AI receives information such as genres played, categories, and playtime to generate interpretive analyses.

These integrations are done dynamically through contextual prompts and aggregated usage data. The result is a rich, human-like response tailored to each profile.

---

## 📚 Features Implemented

- [x] Basic Steam profile analysis via Steam ID or custom URL  
- [x] Collection and grouping of game genres and categories  
- [x] Automatic player type definition based on usage data  
- [x] AI integration for narrative and interpretive response  
- [x] Interactive display of charts and analysis on the frontend  
- [x] REST API using Django REST Framework

---

## ⚙️ Technologies Used

- **Backend:** Django + Django REST Framework  
- **Async:** Aiohttp, asyncio  
- **HTTP Requests:** Requests  
- **Testing:** Pytest  
- **Database:** SQLite (in development)  
- **Frontend:** React + Vite + Tailwind CSS  
- **AI / NLP:** Google Gemini

---

## 🛠️ Running Locally

```bash
git clone https://github.com/your-user/steamlyzer-api.git
cd steamlyzer-api
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
cd Backend
pip install -r requirements.txt
python manage.py runserver
```

## 🖥️ Running the Frontend

Make sure Node.js is installed. From the project root execute:

```bash
cd Frontend
npm install
npm run dev
```

Vite will start the development server at `http://localhost:5173`. For more
details, including how to build for production, see
[../Frontend/README.md](../Frontend/README.md).

---

## 🔍 Available Endpoints

The API currently has only a single entry point, which serves the main page where all logic occurs:

| Route | Method | Description |
|-------|--------|-------------|
| `/`   | GET    | Main page — receives `steam_id` and displays the interactive analysis based on AI-generated responses. |

> Note: The `steam_id` parameter can be either the full Steam ID64 or a custom vanity URL.

---

## 🧪 Tests

To run the tests:

```bash
pytest
```

---

## 🧩 Contribution

This project is **under active development**, and any suggestions, fixes, or contributions are welcome.  
We follow the commit message convention defined by [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) and documented in this repository.

---

## 📌 Notes

> 🔧 This is a **work-in-progress** version of the API.  
> Some features are incomplete or subject to change.  
> Use at your own risk! Feedback and contributions are welcome.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](../LICENSE) for more details.