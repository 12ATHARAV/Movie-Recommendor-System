<p align="center">
  <img src="https://img.shields.io/badge/%F0%9F%8E%AC-CineAI_Movie_Recommender-E50914?style=for-the-badge&labelColor=0d1117" alt="CineAI"/>
</p>

<h1 align="center">CineAI | Movie Recommender System</h1>

<p align="center">
  <strong>Hybrid Dual-Engine Movie Recommendation Platform combining Custom Machine Learning Cosine Similarity & Live Global TMDB Discovery.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" alt="Scikit-Learn"/>
  <img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white" alt="NumPy"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/TMDB_API-01B4E4?style=flat-square&logo=themoviedatabase&logoColor=white" alt="TMDB"/>
  <img src="https://img.shields.io/badge/WebAssembly-654FF0?style=flat-square&logo=webassembly&logoColor=white" alt="WebAssembly"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="MIT License"/>
</p>

---

## ⚡ Overview

**CineAI** is an advanced dual-mode movie recommendation application built with Python, Scikit-Learn, Streamlit, and The Movie Database (TMDB) API. It offers two distinct recommendation engines within a single unified interface:

1. **🧠 Trained ML Engine (Offline Dataset — 4,800+ Movies):**  
   Uses a custom-trained **Cosine Similarity** model over historical film metadata (`overview`, genres, keywords, cast, and crew) to recommend similar films from our ML dataset.
2. **🌐 Live Global Search Engine (Any Movie up to 2026):**  
   Allows users to search any movie title ever released worldwide and instantly fetch live recommendations directly from TMDB's global movie graph.

Every recommendation is enriched in real-time with official high-definition movie posters, live viewer ratings (`vote_average`), release years, and detailed storyline overviews.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **Trained ML Recommendation Engine** | Uses TF-IDF / CountVectorizer + Cosine Similarity over 4,809 curated movies |
| 🌐 **Live Global Movie Search** | Search and discover recommendations for **any film ever released (up to 2026)** |
| ⚡ **Ultra-Fast Startup (< 0.5s)** | Precomputed top-recommendation matrix compressed down to **270 KB** (160x faster loading) |
| 🍿 **Live Real-Time TMDB Metadata** | Fetches official posters, live audience scores, release years, and plot overviews |
| 🎨 **Premium Cinema UI** | Responsive glassmorphic movie cards, tabbed interface, and hover micro-animations |
| 🌐 **100% Client-Side WebAssembly** | Runs entirely in your browser via **Stlite / Pyodide WebAssembly** on GitHub Pages |

---

## 🚀 Live Demo & Deployment

### Option 1: Run Instantly in Browser (GitHub Pages / Stlite WebAssembly)
👉 **[https://12atharav.github.io/Movie-Recommendor-System/](https://12atharav.github.io/Movie-Recommendor-System/)**  
*Runs full Python and Streamlit client-side inside your browser with zero backend server needed!*

### Option 2: Streamlit Community Cloud (1-Click Deploy)
1. Fork this repository.
2. Visit [share.streamlit.io](https://share.streamlit.io/).
3. Connect your fork and select `app.py` as your entry point.

---

## 🏗️ System Architecture

```
                       +-----------------------------------+
                       |         CineAI Web UI             |
                       |       (Streamlit / Stlite)        |
                       +-----------------+-----------------+
                                         |
               +-------------------------+-------------------------+
               |                                                   |
               v                                                   v
  [Tab 1: Trained ML Engine]                       [Tab 2: Live Global Search]
               |                                                   |
  +------------v-------------+                      +--------------v-------------+
  |  Load movies.pickle &    |                      | Query TMDB Live Search API |
  |  Precomputed top_recs    |                      | (Any movie up to 2026)     |
  +------------+-------------+                      +--------------+-------------+
               |                                                   |
               +-------------------------+-------------------------+
                                         |
                                         v
                         [Live TMDB Metadata Enrichment]
                     (Posters, Ratings, Years, Storylines)
```

---

## 💻 Local Development & Setup

### Prerequisites
- Python 3.8+
- `pip` package manager

### 1. Clone the Repository
```bash
git clone https://github.com/12ATHARAV/Movie-Recommendor-System.git
cd Movie-Recommendor-System
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
streamlit run app.py
```
Open your web browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
Movie-Recommendor-System/
|-- app.py                   # Streamlit dual-tab application & hybrid recommender
|-- index.html               # Stlite / WebAssembly entry point for browser deployment
|-- requirements.txt         # Python package dependencies
|-- movies.pickle            # Processed movie metadata dataframe (4,809 films)
|-- top_recs.pkl             # Ultra-fast precomputed top-10 recommendations (270 KB)
|-- similarity.pickle        # Full Float16 Cosine Similarity matrix fallback (44 MB)
+-- README.md                # Comprehensive project documentation
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  <strong>⭐ Star this repository if you found these recommendations helpful! ⭐</strong>
</p>
