# HealthGuard AI

HealthGuard AI ek **healthcare data quality monitoring system** hai jo patient records mein missing data, anomalies aur duplicate entries detect karta hai.  
Yeh project **Hack2skill - AI for Everywhere Hackathon 2026** ke liye banaya gaya hai.  

## Problem Statement

Hospitals mein galat ya incomplete data ki wajah se:
- Wrong diagnosis aur treatment ho sakta hai  
- Duplicate records aur outdated information rehti hai  
- Cost aur patient risk dono badh jaate hain  

## Solution

HealthGuard AI:
- Patient records ko analyze karke data quality issues detect karta hai  
- Missing fields, invalid ages, abnormal blood pressure / heart rate aur duplicate patients ko flag karta hai  
- Ek simple dashboard deta hai jisme sab metrics clearly dikhte hain  

## Features

- Missing data detection (completeness score 0–100%)  
- Rule-based checks (age, BP, heart rate, last visit date)  
- Basic statistical anomaly detection (outlier values)  
- Duplicate record detection by patient name  
- Summary table / charts for quick overview  

## Tech Stack

- Python  
- Streamlit (dashboard)  
- SQL / Snowflake (data storage & queries)  
- Pandas (data processing)  

## How to Run (Demo)

1. Repository clone/download karo  
2. Python 3.8+ install ho  
3. Dependencies install karo:
   ```bash
   pip install streamlit pandas
App run karo:

   bash
   streamlit run streamlit_app.py

Project Status

Prototype working with sample data (200 patient records)

Core quality checks implemented

Future work: real hospital integration, alerts, mobile view, advanced ML models

Author
Name: [Soham Sharma]

Email: [sohamsharmapcm@gmail.com]

Built for: Hack2skill – AI for Everywhere (AI for Good / Healthcare)
