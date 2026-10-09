# Day 3 - Data Analysis & Python for AI/ML

## Project Overview

This project focuses on analyzing facility data using Python, NumPy, Pandas and Matplotlib.

The dataset contains facility information including cleanliness, odor, waste level, water availability, footfall, complaints and inspection dates.

## Problem Statement

The objective is to inspect, clean, analyze and visualize facility data to identify useful patterns and insights.

## Features

- NumPy array operations
- Pandas DataFrame operations
- Dataset inspection
- Missing value detection and handling
- Duplicate detection and removal
- Data validation
- Statistical analysis
- Location-wise analysis
- Data visualization
- Insight generation

## Technology Stack

- Python 3
- NumPy
- Pandas
- Matplotlib
- CSV

## Project Structure

```text
day-03/
├── dataset/
│   ├── facility_data.csv
│   ├── cleaned_facility_data.csv
│   ├── 01-numpy-basics.py
│   ├── 02-pandas-basics.py
│   ├── 03-pandas-operations.py
│   └── 04-pandas-cleaning.py
│
├── data-cleaning/
│   ├── 01-inspect-data.py
│   └── 02-clean-data.py
│
├── analysis/
│   ├── 01-facility-analysis.py
│   └── 02-insights.py
│
├── visualizations/
│   ├── 01-cleanliness-by-location.py
│   ├── 02-complaints-by-location.py
│   ├── 03-cleanliness-histogram.py
│   ├── 04-footfall-vs-complaints.py
│   ├── 05-water-availability.py
│   ├── cleanliness-by-location.png
│   ├── complaints-by-location.png
│   ├── cleanliness-histogram.png
│   ├── footfall-vs-complaints.png
│   └── water-availability.png
│
└── README.md