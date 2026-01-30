# Movies Watchlist 🎬
A full-stack web application for tracking movies, managing ratings, and sharing watchlists with friends. This project served as my final capstone for the Web Developer Bootcamp, demonstrating proficiency in user authentication and secure data management.

## 💡 Overview
This application was designed to test and consolidate my skills in backend development before moving on to independent, larger-scale projects like Ekonomik Inventory. It features a complete user flow, from secure registration to personalized content management.

## 🌟 Key Features

* **User Authentication:** Robust registration and login system. To ensure data integrity, all sensitive user information is hashed using the passlib library before being stored.

* **Personalized Watchlists:** Users can add movies, descriptions, cast details, and genres. Each movie page is uniquely tied to the user's account.

* **Social Sharing:** Allows users to share their movie lists and ratings with friends via direct links.

* **Dual-Theme Interface:** Features both dark and light modes, allowing for a customizable user experience.

🛠 Tech Stack

* **Backend:** Python / Flask

* **Database:** MongoDB
* 
* **Security:** Passlib (Password hashing)

* **Frontend:** HTML, CSS

## 🚀 Live Demo
Visit the application: [movie-watchlist-sgo6.onrender.com](https://movie-watchlist-sgo6.onrender.com/login)

## 🔧 Quickstart

1. Clone the repo.

2. Install dependencies: pip install -r requirements.txt.

3. Environment Setup: Create a .env file and add your DBURI (MongoDB connection string).

4. Run: flask run.
