# MediaHub 🎧🎨🔍  
A web application for searching and interacting with openly licensed media via the [Openverse API](https://api.openverse.org/). Built with Django REST Framework and a lightweight HTML/CSS/JavaScript frontend.

## 🚀 Features

- 🔐 User Registration and Authentication
- 🔍 Search Interface for Openverse API (Images, Audio)
- ❤️ Save/Delete Recent Searches (per user)
- 🖼️ Media Preview and Filtering
- 📦 Containerized using Docker
- ✅ Automated Testing Strategy
- 🛠️ Modular, Scalable Architecture (OOP + Design Patterns)
- 🔒 Secure Data Handling

## 📁 Project Structure

```bash
MediaHub/
├── backend/
│   ├── manage.py
│   ├── mediahub/               # Django project
│   └── core/                   # App: APIs, auth, search, models
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── main.js
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
