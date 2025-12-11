
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)](#)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi)](#)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js-000000?style=for-the-badge&logo=nextdotjs)](#)
[![SentenceTransformers](https://img.shields.io/badge/Embeddings-SentenceTransformers-ff69b4?style=for-the-badge)](#)
[![FAISS](https://img.shields.io/badge/Vector%20Search-FAISS-00bcd4?style=for-the-badge)](#)

---

# <img src="https://img.icons8.com/color/96/artificial-intelligence.png" width="55"/> StreamIntel360-AI             

### AI-Powered Content Intelligence, Similarity Search & Multi-Agent Recommendation System for Streaming Platforms

---

## 🎬 What is StreamIntel360-AI?

**StreamIntel360-AI** is an end-to-end **Generative AI + RAG + Multi-Agent** platform that turns a raw streaming catalog (like the Netflix titles dataset) into:

- 🔍 **Semantic search** over titles, genres, countries, and descriptions  

- 🧠 **LLM-backed multi-agent reasoning** about content and audience fit  

- 🎯 **Greenlight / pilot / do-not-invest** style recommendations  

- 💬 A **live AI chatbot agent** exposed via a modern **Next.js frontend** and **FastAPI backend**

The project is fully reproducible and structured for a real and production deployment.

---

## 🚀 Live Demo & Key Endpoints

| Component | Link |                                                                                 
|----------|------|                                                                    
| 🌐 **Frontend Web App** (Next.js) | `http://localhost:3000/` |                                                        
| ⚙️ **Backend API Root** (FastAPI) | `http://127.0.0.1:8000/` |                                                                
| 📖 **Interactive API Docs (Swagger)** | `http://127.0.0.1:8000/docs` |                                                                       
| 💬 **Chat Endpoint (AI Agent)** | `POST http://127.0.0.1:8000/api/chat` |                                                                  

---

## 📌 Project Overview

**Business Problem**

Streaming platforms invest **billions of dollars** each year in original and licensed content, but predicting which titles will succeed is still highly uncertain.

**StreamIntel360-AI** addresses this by:

- Building a **vectorized knowledge base** from catalog metadata  

- Enabling **semantic retrieval** of similar titles and patterns  

- Using **multi-agent LLM reasoning** to provide executive-ready answers such as:                                                            
  > _“Recommendation: Greenlight a pilot; strong fit with target audience in North America and India.”_


---

## 🧱 Repository Structure

```bash

StreamIntel360-AI/                                                                       
│                                                                                     
├── backend/                     # FastAPI backend — RAG + multi-agent logic                                                                     
│   ├── api/                     # API routes & request/response models                                                                      
│   ├── models/                  # Loading FAISS index, sentiment pipeline, tools                                                          
│   ├── utils/                   # Shared helpers, config, logging                                                           
│   └── main.py                  # FastAPI app entrypoint                                                     
│                                                                                       
├── frontend/                    # Next.js frontend                                                      
│   ├── app/                                                                  
│   │   ├── analyze/page.tsx     # Content analysis UI                                                          
│   │   ├── chat/page.tsx        # Chat-style interface with AI agent                                                    
│   │   └── layout.tsx           # Global layout & theming                                                     
│   ├── components/              # Reusable UI components                                           
│   └── styles/                  # Styling / Tailwind / CSS modules                                               
│                                                                         
├── data/                                                                                                                 
│   └── netflix_titles_cleaned.csv             # Cleaned Netflix catalog (8,809 titles)                                             
│                                                                                                                                        
├── notebooks/                                                                                           
│   ├── Notebook1_EDA.ipynb                    # Catalog EDA & data quality                                                  
│   ├── Notebook2_Embeddings_Index.ipynb       # Embeddings + FAISS similarity search                                                 
│   ├── Notebook3_Sentiment_Model.ipynb        # IMDB sentiment classifier (TF-IDF + LR)                                   
│   ├── Notebook4_RAG_Agents_Eval.ipynb        # RAG + multi-agent evaluation                       
│                                                     
├── models/                                                                 
│   ├── faiss.index                  # FAISS vector index                                         
│   ├── embeddings.npy               # SentenceTransformer embeddings                                   
│   ├── corpus.pkl                   # Text corpus per title                                                 
│   └── imdb_sentiment_pipeline.joblib          # Saved IMDB sentiment model                                     
│                                                        
├── diagrams/                        # Architecture & workflow diagrams (PNG, SVG)                                                 
├── documentation/                   # Additional project docs, notes, writeups                                                            
│                                                                             
├── Dockerfile
├── pyproject.toml                                                                 
├── requirements.txt                                                         
├── requirements-backend.txt                                                        
├── requirements-notebooks.txt                                                          
└── README.md                                      
```

---

## 📒 Notebooks Overview (EDA → Embeddings → RAG → Agents)

### 1️⃣ Notebook 1 – Exploratory Data Analysis (EDA)

(notebooks/Notebook1_EDA.ipynb)

**What it does**

- Loads the Netflix titles dataset with the correct encoding

- Inspects schema, dtypes, and missingness

- Visualizes:

    📊 Movies vs TV Shows count

    📆 Release year distribution (1925–2024, skewed to 2015–2021)

    🌍 Top content-producing countries (US, India, UK, etc.)

    🎭 Top 20 genres / categories

**Why it matters**

- Confirms which fields are reliable signals (title, type, release_year, listed_in, description)

- Highlights sparse but useful fields (director, cast, country)

- Guides how the RAG corpus should be constructed and how agents should interpret the catalog.


### 2️⃣ Notebook 2 – Embeddings & Semantic Similarity Search

(notebooks/Notebook2_Embeddings_Index.ipynb)

**What it does**

- Designs multiple corpus variants per title:

    - "title_only"

    - "title_description"

    - "baseline" = Title + Type + Genres + Country + Year + Description

- Uses SentenceTransformer("all-MiniLM-L6-v2") to encode all 8,809 titles → 384-dimensional embeddings

- Builds a FAISS IndexFlatL2 over the embeddings

- Implements search_similar(query, k) for top-k neighbors


**Example queries**

- “A dark crime thriller about a serial killer in a big city”

- “Feel-good family movie about a dog and children”


**Outcome**

- The baseline corpus variant gives the most intuitive results (e.g., “Dark Crimes”, “Benji”).

- This notebook creates and saves:

    - models/faiss.index

    - models/embeddings.npy

    - models/corpus.pkl

- These artifacts power the backend vector search and the RAG + agent pipeline.


### 3️⃣ Notebook 3 – IMDB Sentiment Model (TF-IDF + Logistic Regression)

(notebooks/Notebook3_Sentiment_Model.ipynb)

**What it does**

- Loads the IMDB 50k reviews dataset (IMDB_Dataset.csv)

- Cleans text and sentiment labels (positive/negative)

- Builds a Pipeline:

    - TfidfVectorizer(max_features=50000, ngram_range=(1, 2), stop_words="english")

    - LogisticRegression(max_iter=1000, n_jobs=-1)

- Trains / evaluates with an 80/20 stratified split

**Performance**

- ~90% accuracy on the test set

- Balanced precision/recall for positive & negative classes

**Output**

- Saves the entire pipeline as:

    - models/imdb_sentiment_pipeline.joblib

**Why it matters**

- The backend can load this model as an agent tool to estimate audience sentiment.

- Future iterations can combine catalog similarity + sentiment for richer ranking and recommendations.


### 4️⃣ Notebook 4 – RAG & Multi-Agent Evaluation

(notebooks/Notebook4_RAG_Agents_Eval.ipynb)

**What it does**

- Rebuilds the baseline corpus + embeddings + FAISS index

- Defines a mini evaluation set of queries + expected titles (crime thrillers, teen rom-coms, dog-family movies, sci-fi space titles)

- Computes Hit@k metrics for k = 3, 5, 10:

    - Checks if any relevant title appears in the top-k retrieved items

- Optionally calls the live FastAPI backend at /api/chat to compare:

    🔁 Retrieval-only behavior vs

    🧠 Full multi-agent, LLM-generated answer

**Outcome**

- Notebook 2 = lab for designing embeddings & similarity

- Notebook 4 = regression test & quality gate for the full RAG + agent stack

---

## 🧠 The Live AI Chatbot Agent

- The AI chatbot is implemented in the backend and exposed via:

    - POST /api/chat (FastAPI)

- This endpoint:

1. Accepts a natural-language prompt (e.g., “Suggest a thriller movie where the hero is a police officer in the US.”)

2. Runs:

    - Embedding & FAISS retrieval

    - Multi-agent reasoning (retriever, analyzer, scorer, decision agent)

3. Returns an executive-style, structured answer with:

    - Recommended titles

    - Justification & audience fit

    - A final decision statement (e.g., “Greenlight a pilot”)

- The frontend /chat page consumes this endpoint and shows the conversation in a chat-like UI.

---

## 🖥️ Frontend – Next.js App

(Folder: frontend/)

- Key Screens

    - /analyze – form-style interface to analyze or evaluate a single title/idea

    - /chat – chat UI for free-form conversation with the AI agent

    - Shared layout with responsive components and dark-theme-ready styling


```bash

# Run frontend locally                                             
cd frontend                                                               
npm install                                                                   
npm run dev                                                                  

# App will start (by default) at:                                                       
# http://localhost:3000/                                        
```

---

## ⚙️ Backend – FastAPI + RAG + Agents

(Folder: backend/)

**Core Responsibilities**

- Load:

    - faiss.index, embeddings.npy, corpus.pkl

    - imdb_sentiment_pipeline.joblib (optional sentiment agent)

- Implement:

    - /api/similar_titles – semantic similarity search

    - /api/analyze_title – structured analysis for a single title

    - /api/chat – multi-agent AI assistant endpoint

- Orchestrate:

    - Retrieval → Analysis → Scoring → Decision


```bash

# Run backend locally                                                      
cd backend                                                   
pip install -r ../requirements-backend.txt                                                          
uvicorn main:app --reload                        

# API Docs:                                        
# http://127.0.0.1:8000/docs                     
```

---

### 🔗 End-to-End Flow

```text

User (Web UI / Chat)                                                            
        │                                              
        ▼                                                       
Frontend (Next.js)                                                        
        │  HTTP (JSON)                                                
        ▼                                    
Backend API (FastAPI)                           
        │                                 
        ├── Embedding + FAISS Vector Search (similar titles)                             
        ├── Optional Sentiment Model (IMDB reviews)                                         
        ├── Multi-Agent LLM Reasoning (retriever, analyst, scorer, decision)                                     
        ▼                   
Executive Answer + Recommendations                                       
        │                                     
        ▼                                        
Rendered back to the user in the Web UI                                
```

---

## 📚 Dataset

- Main catalog: data/netflix_titles_cleaned.csv

- Includes:

    - show_id, type, title, director, cast, country

    - date_added, release_year, rating, duration

    - listed_in (genres/categories), description

- Sentiment dataset: IMDB_Dataset.csv (50k labeled reviews) – used in Notebook 3.

---

## 🧪 Quickstart – Local Setup

```bash

# 1. Clone the repo                    
git clone https://github.com/SweetySeelam2/StreamIntel360-AI.git                    
cd StreamIntel360-AI

# 2. Install shared Python dependencies                                   
pip install -r requirements.txt                                    

# 3. (Optional) Install notebook extras for experiments                                               
pip install -r requirements-notebooks.txt

# 4. Start backend                                                
cd backend                                                         
pip install -r ../requirements-backend.txt                                                      
uvicorn main:app --reload                                     

# 5. Start frontend (in another terminal)                                                  
cd ../frontend                                             
npm install                                                     
npm run dev                               
```

Then open:

    - Frontend: http://localhost:3000/

    - API Docs: http://127.0.0.1:8000/docs

---

## 🐳 Docker Deployment

```bash

# Build image                        
docker build -t streamintel360 .

# Run container (backend on port 8000)                              
docker run -p 8000:8000 streamintel360                     
```

> We can host the backend container on Render/Railway/AWS and point the Next.js frontend to the public API URL.

---

## 💼 Business Value & Impact

StreamIntel360-AI demonstrates how streaming companies can:

- 📊 Evaluate new content ideas using similar titles, genres, and historical patterns

- 💬 Explain decisions with human-readable reasoning instead of opaque scores

- 🎯 Target audiences more effectively by combining semantics + sentiment

- ⏱️ Cut the evaluation cycle from days/weeks of manual research to minutes of AI-augmented analysis

---

## 🧰 Tech Stack

- Languages: Python, TypeScript

- Data / ML: Pandas, NumPy, Scikit-learn

- Embeddings & Vector Search: SentenceTransformers, FAISS

- LLM & Agents: (designed for LangChain / LangGraph-style tool use and orchestration)

- Backend: FastAPI, Uvicorn

- Frontend: Next.js, React

- Dev & Deployment: Docker, Poetry/requirements.txt, Jupyter Notebooks

---

## 🗺️ Future Enhancements

- 🔐 Add authentication & role-based access (analyst vs executive views)

- 📈 Incorporate real watch/engagement data for ranking & uplift modeling

- 🌍 Expand to multilingual embeddings for non-English catalogs

- ⚙️ Add a ranking model that blends similarity, sentiment, and performance metrics

- ☁️ Deploy full stack via Docker Compose or Kubernetes for scalable production use

---

## 📚 References

- Pathi, L. (2020). IMDB Dataset of 50K Movie Reviews [Data set]. Kaggle.
https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews

- Vyas, R. (2020). Netflix Movies and TV Shows [Data set]. Kaggle.
https://www.kaggle.com/datasets/rahulvyasm/netflix-movies-and-tv-shows

*Disclaimer:* This project uses public datasets and is not affiliated with Netflix or any streaming platform.

---

## 👩‍💻 Author

**Sweety Seelam – Business Analyst / Aspiring Data Scientist / AI Engineer**

✉️ Email: sweetyseelam8@gmail.com

🌐 Portfolio: https://sweetyseelam2.github.io/SweetySeelam.github.io/

🧪 GitHub: https://github.com/SweetySeelam2

💼 LinkedIn: https://www.linkedin.com/in/sweetyrao670

🌐 Medium: https://medium.com/@sweetyseelam

---

## 🔒 Proprietary & All Rights Reserved

**© 2025 Sweety Seelam**. This work is proprietary and protected by copyright. 

All content, models, code, and visuals are © 2025 Sweety Seelam. No part of this project, app, code, or analysis may be copied, reproduced, distributed, or used for any purpose—commercial or otherwise—without explicit written permission from the author.