# Movie-Recommendor-System

Overview:

This project is a content-based movie recommendation system built using Python and Streamlit. The application suggests similar movies based on the user's selection, utilizing content similarity matrices to find the most relevant recommendations. For each recommendation, the system displays the movie title along with its poster image fetched from The Movie Database (TMDB) API.

Features:

Interactive movie selection from a dropdown menu

Content-based recommendation algorithm

Visual display of movie posters

Top 5 movie recommendations based on content similarity

Error handling for API connection issues and missing posters

Technologies Used:

Python: Core programming language

Streamlit: Web application framework for creating the user interface

Scikit-learn: Used for CountVectorizer and Cosine Similarity

NumPy & Pandas: For data manipulation and processing

Pickle: For model serialization

TMDB API: External API for fetching movie posters and information

How It Works:

Data Loading & Merging: Combines credits and movie information into one dataset

Preprocessing: Parses and extracts relevant info from JSON-like columns

Tags Creation: Constructs a tags column to consolidate relevant text features

Model Creation: Applies CountVectorizer on the tags

Similarity Calculation: Calculates cosine similarity across the movie vectors

Recommendation: Given a movie title, returns the top 5 most similar movies

Installation
Prerequisites:

Python 3.7 or higher
Git

![image](https://github.com/user-attachments/assets/2d24778c-1b00-404f-8b2f-bd34cbcc6a62)
