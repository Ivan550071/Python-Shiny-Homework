# Python Shiny Applications

A collection of interactive Python Shiny applications demonstrating data visualization and manipulation capabilities.

## Applications

### 1. Data Cleaner (a4_ex1)
An interactive CSV data cleaning tool with the following features:
- Upload and analyze CSV files
- Drop unwanted columns
- Handle missing values (replace with 0, mean, median, or drop rows)
- Transform data (normalize or standardize)
- Download cleaned dataset

### 2. CO₂ Dashboard (a4_ex2)
An interactive dashboard for analyzing global CO₂ emissions data:
- Country-specific CO₂ time series with rolling mean
- Regional grouping and analysis
- Built with Plotly visualizations
- Data sourced from Our World in Data

## Running Locally

### Prerequisites
- Python 3.8+
- Virtual environment with dependencies installed

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Ivan550071/Python-Shiny-Homework.git
cd Python-Shiny-Homework
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Run Applications

**Data Cleaner:**
```bash
python -m shiny run --reload a4_ex1/app.py
```

**CO₂ Dashboard:**
```bash
python -m shiny run --reload a4_ex2/app.py
```

## Running with Docker

See [README_DOCKER.md](README_DOCKER.md) for detailed Docker instructions.

### Quick Start

Build and run a single app:
```bash
docker build -t a4-shiny .
docker run --rm -p 8000:8000 a4-shiny
```

Run both apps with Docker Compose:
```bash
docker compose up -d --build
```

Access the apps at:
- Exercise 1: http://localhost:8001
- Exercise 2: http://localhost:8002

## Technologies Used

- **Shiny for Python**: Interactive web applications
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation and analysis
- **Docker**: Containerization and deployment

## License

This project is for educational purposes.
