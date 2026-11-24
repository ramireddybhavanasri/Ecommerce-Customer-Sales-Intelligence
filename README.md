# 🛒 E-Commerce Customer & Sales Intelligence

An interactive e-commerce analytics dashboard built using Python, Pandas, and Streamlit to explore customer behaviour, order trends, product performance, delivery efficiency, and payment patterns.

## 📌 Project Overview

This project analyzes the Brazilian Olist e-commerce dataset to understand business performance through data analysis and interactive visualizations.

## ✨ Features

- **Business Overview:** Total orders, delivered orders, canceled orders, and order status distribution.
- **Order Analytics:** Monthly order trends and delivery performance.
- **Customer Analytics:** Unique customers, repeat customers, and customer order distribution.
- **Product Analytics:** Product category performance and top 10 categories.
- **Payment Analytics:** Payment transactions, total payment value, and popular payment methods.
- **Interactive Filters:** Filter orders by status and date range.
- **CSV Export:** Download filtered order data.

## 🛠️ Technologies Used

- Python
- Pandas
- Streamlit
- Jupyter Notebook
- Matplotlib

## 📂 Project Structure

```text
Ecommerce-Intelligence/
│
├── app.py
├── 01_data_exploration.ipynb
├── requirements.txt
├── .gitignore
│
├── monthly_order_trends.png
├── order_status_analysis.png
├── payment_type_distribution.png
└── top_10_product_categories.png
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project folder

```bash
cd Ecommerce-Intelligence
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows:

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Add the dataset

Download the Olist Brazilian E-Commerce dataset and place the required CSV files inside a folder named `datasets`.

Required files:

- olist_orders_dataset.csv
- olist_customers_dataset.csv
- olist_order_items_dataset.csv
- olist_products_dataset.csv
- olist_order_payments_dataset.csv

### 7. Run the dashboard

```bash
streamlit run app.py
```

## 📊 Dataset

The project uses the Olist Brazilian E-Commerce Public Dataset.

The dataset contains information about orders, customers, products, and payments.

## 🎯 Project Objective

The objective is to transform raw e-commerce data into meaningful business insights using data analysis and interactive visualization.

## 👩‍💻 Author

**Bhavana Sri**

AI & Data Science Student

---

*Developed as a practical data analytics project using Python and Streamlit.*
