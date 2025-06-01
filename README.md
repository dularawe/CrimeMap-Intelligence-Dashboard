CrimeMap Intelligence Dashboard

Description:
This project is a full-stack GIS crime mapping and surveillance dashboard that integrates a frontend dashboard, a Laravel backend with MySQL database, and a Python-based ML service for classification and geolocation. The system visualizes real-time crime locations, detects crime types using ML, and displays nearby police station data for operational awareness.

---

1. Technologies Used:

Frontend:
- Vue 3 with Vite
- Leaflet.js
- leaflet.markercluster
- Axios

Backend:
- Laravel (REST API)
- MySQL (Relational Database)

ML Server:
- Python 3.10
- FastAPI
- Hugging Face Transformers
- OpenStreetMap Overpass API (for police station geolocation)

---

2. Data Flow:

Step 1: Data Collection
- Crime incidents are collected from RSS feeds and social media using the ML server (FastAPI).
- Each entry is classified by an ML model to determine if it is crime-related.

Step 2: Classification & Location Extraction (ML)
- The ML model uses a multilingual BERT (e.g., xlm-roberta) fine-tuned on Sinhala/Tamil crime news to classify the title.
- If classified as crime, a location extraction module (NER + geocoder) estimates coordinates.
- Output:
  - title, description, category, latitude, longitude

Step 3: Data Insertion (Laravel + MySQL)
- The Laravel API periodically pulls data from the ML server (`/get-latest-crimes`).
- A Laravel scheduled command (`php artisan fetch:crimes`) stores or updates records in the MySQL `crimes` table.

MySQL Table Structure (crimes):
- id (int)
- title (varchar)
- description (text)
- category (varchar)
- latitude (double)
- longitude (double)
- occurred_at (datetime)
- source_url (text)
- created_at (timestamp)
- updated_at (timestamp)

Step 4: Frontend Display (Vue + Leaflet)
- The Vue dashboard fetches live data from `http://localhost:8001/api/crimes`.
- The main map clusters all crimes and supports popup interactions.
- On marker click, the police response mini-map zooms to the nearest police station.
- A polyline is drawn between the crime location and the selected station.

Step 5: Police Station Data (OpenStreetMap)
- The dashboard loads real police station POIs using Overpass API.
- These are shown on the right-hand mini-map for live reference.

---

3. ML Model Pipeline:

Preprocessing:
- Sinhala and Tamil crime news dataset manually labeled (crime / not crime).
- Tokenized using xlm-roberta tokenizer.

Model:
- Base model: xlm-roberta-base
- Fine-tuned using Hugging Face Trainer on classification task.

Training:
- Train/test split: 80/20
- Optimizer: AdamW
- Epochs: 4
- Accuracy: ~92% on validation

Location Extraction:
- Named Entity Recognition (NER) detects city/place names.
- OpenCage Geocoder API or rule-based bounding is used to resolve coordinates.

FastAPI Endpoint:
- /get-latest-crimes: Returns latest classified + located crime data in JSON format

---

4. Setup Instructions

A. ML Server (FastAPI)
- Install Python dependencies:
  pip install fastapi uvicorn transformers torch feedparser requests

- Run:
  uvicorn main:app --reload

B. Laravel Backend
- Configure `.env` for MySQL
- Run migrations:
  php artisan migrate
- Schedule crime fetching:
  Add cron job for `php artisan schedule:run`
- API route:
  GET /api/crimes

C. Vue Frontend
- Install dependencies:
  npm install
- Start development server:
  npm run dev
- Access at: http://localhost:5173

---

5. Future Improvements

- Add real-time WebSocket updates
- Visual analytics: heatmaps, trend charts
- User roles and secure login (admin, viewer)
- Integration with real crime datasets from local police
- Severity-based color markers
- Multi-language UI

---

6. Deployment Considerations

- Frontend: Host via Netlify, Vercel, or static server
- Backend API: Host Laravel on shared VPS or Laravel Vapor
- ML Server: Deploy on a Python backend (e.g., Render, DigitalOcean, or containerized)
- DB: Use managed MySQL or provisioned RDS (if hosted)
