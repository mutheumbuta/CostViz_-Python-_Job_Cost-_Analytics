# CostViz_-Python-_Job_Cost-_Analytics

## Refrigerated Truck Manufacturing Cost Analysis

## Job Costing Data Pipeline using Wakulima Agro lTD Data

## Project Overview

This project demonstrates the development of a data pipeline and analytics system for manufacturing job costing analysis using supply data from Wakulima Agro Limited.

A manufacturing company producing refrigerated trucks uses raw material supply data from Wakulima Agro to analyze production costs, monitor component expenses, and generate business insights for operational efficiency.

The project implements a complete data workflow that extracts raw material cost data, transforms it into structured format, stores it in a MySQL database, and visualizes production cost insights using **Streamlit dashboards.

This portfolio project simulates a real-world manufacturing analytics environment where data is used to support strategic production and cost management decisions.

## Business Context

The manufacturing company builds refrigerated transport trucks used in cold-chain logistics. These trucks require several raw materials including:

* Aluminium structures

* Steel components
  
* Mechanical fittings
 
* Structural bars
  
* Fabrication materials

Suppliers such as Wakulima Agro Limited provide these materials which contribute to the overall job cost of building each refrigerated truck.

The goal of this project is to track, store, and analyze these material costs to understand the production cost structure.

## Project Objectives

The system was built to:

1. Analyze production costs per material

2. Identify high-cost components
 
3. Monitor total job cost of refrigerated truck manufacturing
 
4. Create data pipelines for cost monitoring

5. Enable interactive dashboards for decision making
 
6. Support data-driven manufacturing optimization

## Technologies Used
Technology	Purpose
1.  Python	Data processing & ETL pipeline
  
2.  MySQL	Production cost database
  
3.  Streamlit	Business intelligence dashboard

4.  Pandas	Data cleaning & transformation

5.  python-dotenv	Secure configuration management

6.  CSV	Raw material cost dataset

7. SQL	Production cost analysis queries

## System Architecture

Supplier Cost Data (CSV)

        │
        ▼
        
Data Cleaning & Transformation (Python + Pandas)

        │
        ▼
        
Structured Data Storage (MySQL Database)

        │
        ▼
        
SQL Queries for Production Insights

        │
        ▼
        
Streamlit Dashboard

        │
        ▼
        
Manufacturing Cost Insights

## Project Structure  

wakulima-job-costing-analysis

│

├── data

│   └── wakulimaagro_cleaned.csv

│
├── scripts

│   ├── clean_data.py
│   ├── upload_to_mysql.py
│   └── etl_pipeline.py
│
├── dashboard
│   └── streamlit_dashboard.py
│
├── sql
│   └── production_queries.sql
│
├── .env
├── requirements.txt
└── README.md

📊 Database Schema

The project stores production cost data in MySQL using the following structure:

Column	Description
id	Unique record identifier
item_code	Supplier item code
product_name	Raw material name
category	Supplier category
quantity	Quantity used
uom	Unit of measure
cost_kes	Unit material cost
production_cost	Total production cost
currency	Currency type
📈 Example Business Queries
Total Production Cost
SELECT SUM(production_cost) AS total_production_cost
FROM wakulima_job_costing;

Top 10 Most Expensive Materials
SELECT product_name, production_cost
FROM wakulima_job_costing
ORDER BY production_cost DESC
LIMIT 10;

Average Cost per Category
SELECT category, AVG(cost_kes) AS avg_cost
FROM wakulima_job_costing
GROUP BY category;

📊 Dashboard Features

The Streamlit dashboard provides real-time production insights including:

✔ Total production cost
✔ Cost breakdown by material
✔ Supplier cost contribution
✔ High-cost component analysis
✔ Interactive data filtering
✔ Production cost visualization

The dashboard allows manufacturing managers to quickly identify cost drivers in refrigerated truck production.

📷 Example Dashboard

Example dashboard views include:

Production Cost Summary
Cost Distribution by Component
Top Cost Drivers
Material Usage Insights
🚀 How to Run the Project
1️⃣ Clone Repository
git clone https://github.com/yourusername/wakulima-job-costing-analysis.git
cd wakulima-job-costing-analysis

2️⃣ Create Virtual Environment
python -m venv venv


Activate:

venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create .env

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DATABASE=wakulima_costing

5️⃣ Load Data to MySQL
python upload_to_mysql.py

6️⃣ Launch Dashboard
streamlit run streamlit_dashboard.py

📊 Key Insights Generated

The system enables manufacturers to identify:

Materials contributing most to truck production cost
Supplier cost dependencies
Opportunities for cost optimization
High-value components requiring procurement negotiation
Production cost trends

These insights support better manufacturing planning and cost control.

📚 Skills Demonstrated

This project demonstrates practical skills in:

Data Engineering
ETL Pipeline Development
SQL Data Analysis
Manufacturing Cost Analytics
Data Visualization
Dashboard Development
Data Cleaning & Transformation

