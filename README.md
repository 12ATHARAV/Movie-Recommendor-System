<p align="center">
  <img src="https://img.shields.io/badge/%F0%9F%8E%AC-CineAI_Movie_Recommender-E50914?style=for-the-badge&labelColor=0d1117" alt="CineAI"/>
</p>

<h1 align="center">CineAI | Movie Recommender System</h1>

<p align="center">
  <strong>Content-based machine learning movie recommendation engine powered by Cosine Similarity & TMDB live data.</strong>
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

**CineAI** is an advanced content-based movie recommendation system built using Python, Scikit-Learn, and Streamlit. By analyzing cinematic DNA—including plot summaries (`overview`), cast, crew, genres, and keywords—the system computes a high-dimensional **Cosine Similarity Matrix** across thousands of films to instantly discover the top 5 most similar movies to your selection.

Every recommendation is enriched in real time with **The Movie Database (TMDB) API**, displaying high-definition posters, viewer ratings, release years, and detailed storylines.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Content Similarity Engine** | Uses TF-IDF / CountVectorizer + Cosine Similarity over 4,800+ movies |
| 🍿 **Live TMDB Metadata** | Fetches official posters, ratings (`vote_average`), release years, and plot overviews |
| ⚡ **Optimized Matrix Loading** | Uses Float16 precision for ultra-fast startup (< 0.2s load time) |
| 🎨 **Premium Cinema UI** | Glassmorphism movie cards, hover zoom effects, and responsive 5-column layout |
| 🌐 **WebAssembly & Cloud Ready** | Runs via Streamlit Cloud or client-side inside the browser via **Stlite / WebAssembly** |

---

## 🚀 Live Demo & Deployment

### Option 1: Run in Browser (Stlite / WebAssembly)
You can deploy and run this project **directly on GitHub Pages** with zero backend servers required using `index.html` (powered by Pyodide/Stlite).

### Option 2: Streamlit Community Cloud (1-Click Deploy)
1. Fork this repository.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub repository and select `app.py` as the entrypoint.

---

## 💻 Quick Start (Local Development)

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

### 3. Run the App
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
Movie-Recommendor-System/
|-- app.py                   # Streamlit web application & recommendation engine
|-- index.html               # Stlite / WebAssembly entry point for browser hosting
|-- requirements.txt         # Python package dependencies
|-- movies.pickle            # Processed movie metadata dataframe
|-- similarity.pickle        # Optimized Cosine Similarity matrix (Float16)
+-- README.md                # Project documentation
```

---

## 🧠 Recommendation Algorithm

```
Raw TMDB Dataset --> Data Cleaning & Feature Engineering (Genres, Keywords, Cast, Director)
                              |
                              v
                 CountVectorizer (Bag of Words)
                              |
                              v
                 Cosine Similarity Calculation
                              |
                              v
               4809 x 4809 Similarity Matrix
```

When a user selects a movie:
1. The engine locates the index of the selected film in `movies.pickle`.
2. Retrieves its pairwise similarity vector from `similarity.pickle`.
3. Sorts all films in descending order of similarity score and returns the top 5 closest matches.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  <strong>⭐ Star this repo if you enjoyed the recommendations! ⭐</strong>
</p>
