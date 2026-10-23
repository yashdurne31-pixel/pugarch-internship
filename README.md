# Pugarch Internship

A collection of practical assignments and projects completed during the Pugarch Internship Technical Training and Domain Assessment Program.

This repository contains programming exercises, data analysis, machine learning, frontend and backend development, database integration, and project documentation.

## 📚 Internship Progress

| Day    | Domain                               | Technologies                                                     | Status      |
| ------ | ------------------------------------ | ---------------------------------------------------------------- | ----------- |
| Day 1  | Programming Fundamentals             | JavaScript                                                       | Completed   |
| Day 2  | Python Programming                   | Python                                                           | Completed   |
| Day 3  | Data Analysis & Visualization        | Python, NumPy, pandas, Matplotlib                                | Completed   |
| Day 4  | Machine Learning                     | Python, scikit-learn                                             | Completed   |
| Day 5  | Modern JavaScript Development        | JavaScript, HTML, CSS, Fetch API, JSON, localStorage             | Completed   |
| Day 6  | Frontend Development                 | TypeScript, React                                                | Completed   |
| Day 7  | Full-Stack Development               | Next.js, Node.js, Express.js, REST APIs                          | Completed   |
| Day 8  | Backend & Database Development       | PHP, Laravel, MySQL                                              | Completed   |
| Day 9  | Frontend Framework Development       | Angular, TypeScript, REST APIs                                   | Implemented |
| Day 10 | Smart Hygiene Risk Prediction System | Python, Machine Learning, FastAPI, SQLite, HTML, CSS, JavaScript | Implemented |

## 🚀 Featured Project: Day 10

### AegisHygiene AI — Smart Hygiene Risk Prediction System

**Project directory:** `day-10/final-project/`

A machine-learning application designed to estimate hygiene risk from facility inspection data and present results through a web dashboard and REST API.

### Key Features

* **Data Preprocessing:** Data cleaning, missing-value handling, encoding, and scaling.
* **Exploratory Data Analysis:** Charts and statistical summaries to explore inspection data.
* **Feature Selection:** Identifies relevant input features for model training.
* **Machine Learning:** Classification and regression models for hygiene risk assessment.
* **Model Evaluation:** Evaluation metrics and saved model artifacts.
* **Risk Prediction:** Supports inspection-level risk prediction.
* **Batch Prediction:** Processes multiple inspection records using CSV input.
* **REST API:** FastAPI backend for predictions and application data.
* **Database Integration:** SQLite database for storing facility and inspection information.
* **Interactive Dashboard:** Browser-based interface for predictions, inspections, and analytics.
* **Testing:** Automated backend and machine-learning tests are included.

### Technology Stack

| Component            | Technologies            |
| -------------------- | ----------------------- |
| Programming Language | Python                  |
| Data Processing      | pandas, NumPy           |
| Machine Learning     | scikit-learn            |
| API Framework        | FastAPI                 |
| Database             | SQLite                  |
| Frontend             | HTML5, CSS3, JavaScript |
| Visualization        | Matplotlib              |
| Testing              | pytest                  |
| Development Tools    | VS Code, Git, GitHub    |

## ⚙️ Installation and Setup

### Prerequisites

* Python 3.10 or newer recommended
* Git
* Visual Studio Code (recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/yashdurne31-pixel/pugarch-internship.git
cd pugarch-internship
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Backend Dependencies

```bash
python -m pip install -r day-10/final-project/backend/requirements.txt
```

### 5. Start the Application

```powershell
cd day-10/final-project/backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 6. Open the Application

Once the server starts, open these addresses in your browser:

| Resource                      | Address                     |
| ----------------------------- | --------------------------- |
| Web Dashboard                 | http://127.0.0.1:8000/      |
| Interactive API Documentation | http://127.0.0.1:8000/docs  |
| ReDoc API Documentation       | http://127.0.0.1:8000/redoc |

**Note:** These addresses work on your own computer while the server is running. If the project uses a different frontend or startup configuration, follow the instructions in `day-10/final-project/README.md`.

## 🧪 Run Tests

From the repository root, with the appropriate dependencies installed:

```bash
python -m pytest day-10/final-project/backend/tests -v
```

Check the test output to confirm whether the tests pass in your environment.

## 📊 Machine Learning Workflow

The Day 10 project follows this workflow:

1. Dataset generation or loading
2. Data inspection and preprocessing
3. Exploratory data analysis
4. Feature selection
5. Model training
6. Model evaluation
7. Model artifact saving
8. Single-record prediction
9. Batch prediction
10. Visualization and API integration

**Important:** The project includes synthetic training data. Metrics obtained from synthetic data do not prove real-world prediction accuracy. Independent validation with representative inspection data is required before using the model for operational decisions.

## 💻 Technologies Across the Internship

### Programming Languages

* Python
* JavaScript
* TypeScript
* SQL
* PHP
* HTML
* CSS

### Frontend Development

* React
* Next.js
* Angular
* HTML5
* CSS3
* JavaScript

### Backend Development

* Node.js
* Express.js
* FastAPI
* Laravel
* REST APIs

### Data Analysis and Machine Learning

* NumPy
* pandas
* Matplotlib
* scikit-learn
* Data preprocessing
* Exploratory data analysis
* Feature selection
* Classification and regression

### Databases and Tools

* MySQL
* SQLite
* Git
* GitHub
* Visual Studio Code
* pytest

## 📁 Repository Structure

```text
pugarch-internship/
├── README.md
├── day-01/
├── day-02/
├── day-03/
├── day-04/
├── day-05/
├── day-06/
├── day-07/
├── day-08/
├── day-09/
└── day-10/
    ├── README.md
    ├── api.py
    ├── data/
    ├── models/
    ├── notebooks/
    ├── outputs/
    ├── src/
    └── final-project/
        ├── README.md
        ├── backend/
        ├── database/
        ├── frontend/
        └── ml/
```

Each day directory contains the relevant source code, exercises, project files, or documentation for that assignment.

## 🎯 Project Highlights

* Employee Management CLI
* Python programming exercises
* Data analysis and visualization
* Machine-learning classification
* JavaScript Employee Dashboard
* React and TypeScript Employee Management Dashboard
* Next.js and Node.js Employee Portal
* Laravel and MySQL Facility Management API
* Angular Facility Inspection Dashboard
* **AegisHygiene AI — Smart Hygiene Risk Prediction System**

## 👨‍💻 Author

**Yash Durne**

Electronics and Telecommunication Engineering
Pugarch Internship Technical Training and Domain Assessment Program

---

⭐ If you find this repository useful, consider giving it a star!
