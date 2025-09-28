# MLOps Sentiment Analysis Pipeline 🚀
## 📂 Struktur Project

```
mlops-sentiment/
├── data/                 # data mentah & hasil preprocessing (pake DVC)
│   └── raw/
├── src/
│   ├── prepare.py        # preprocessing data
│   ├── train.py          # training model + log ke MLflow
│   ├── eval.py           # evaluasi model
│   └── app.py            # FastAPI serving
├── models/               # output model (MLflow artifacts)
├── dvc.yaml              # definisi pipeline DVC (prepare → train → eval)
├── params.yaml           # hyperparameter
├── requirements.txt      # dependencies
├── Dockerfile            # containerization API
├── .github/workflows/    # CI/CD workflows
│   └── cicd.yaml
├── .env.example          # template environment variables
└── README.md             # dokumentasi

````


## ✨ Fitur Pipeline

- **Data & Pipeline Versioning** → reproducible experiment dengan DVC
- **Experiment Tracking** → semua run tercatat di MLflow (params, metrics, artifacts, model)
- **Serving API** → endpoint `/predict` untuk inferensi teks
- **Containerization** → aplikasi dikemas ke Docker image
- **CI/CD** → otomatis build & test dengan GitHub Actions
- **Monitoring** → logging request & healthcheck endpoint

---

## 🔧 Setup & Instalasi

### 0. Download data
https://drive.google.com/drive/folders/1r82OahtkIN0_qNqV0xTwp3h5xaAPaAZq?usp=sharing

### 1. Prerequisites
- Python 3.10+
- Git + Git LFS
- Docker Desktop (running)
- DVC (`pip install dvc[gdrive]`)
- MLflow (`pip install mlflow`)
- Akun GitHub


### 2. Clone Repository
```bash
git clone https://github.com/<your-user>/mlops-sentiment.git
cd mlops-sentiment
````

### 3. Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
.\venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 4. Setup Git LFS

```bash
git lfs install
```

### 5. Setup DVC

```bash
dvc init
dvc add data/raw/dataset.csv
dvc pull
```

> **Note:** Ganti `<FOLDER_ID_GOOGLE_DRIVE>` dengan ID folder Google Drive Anda.

### 6. Jalankan MLflow UI (lokal)

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --host 0.0.0.0 --port 5000
```

Akses: [http://localhost:5000](http://localhost:5000)

---

## 🚀 Menjalankan Pipeline

### Step 1: Jalankan pipeline DVC

```bash
dvc repro
```

### Step 2: Cek metrics

```bash
dvc metrics show
```

### Step 3: Lihat hasil di MLflow UI

* Semua run terekam dengan params, metrics, dan artifacts model

---

## 🌐 Menjalankan API (FastAPI + Docker)

### Step 1: Build Docker image

```bash
docker build -t sentiment-api .
```

### Step 2: Run container

```bash
docker run -p 8000:8000 sentiment-api
```

### Step 3: Test API

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "I really love this product!"}'
```

Expected response:

```json
{"label": "positive", "probability": 0.92}
```

---

## 🔄 CI/CD Workflow

GitHub Actions otomatis berjalan ketika `git push`:

1. Checkout repo
2. Setup Python + dependencies
3. Pull data dari DVC remote
4. Run unit tests
5. Build Docker image
6. (Opsional) Deploy ke Hugging Face Spaces

---

## 📊 Monitoring & Troubleshooting

* **Logs API**:

  ```bash
  docker logs <container_id>
  ```
* **Healthcheck**: akses endpoint `/health`
* **Model drift**: jalankan ulang pipeline `dvc repro` dengan data baru


---


