# Product Requirements Document

## Title

**Kids Retail Analytics Dashboard (Streamlit App)**

## Author

Vladyslav Haiduk

## Date

2025-05-03

---

## Background

A small retail business with two physical stores selling clothing for children and teenagers lacks the tools to make data-driven decisions. Currently, sales, inventory, and customer insights are tracked manually or via spreadsheets, making it hard to detect trends, optimize inventory, and plan strategically.

This app will be a lightweight, interactive dashboard using Python and Streamlit to help store owners and managers understand their performance and improve their operational decisions using visual data analysis.

---

## Problem

- The business cannot easily track which products are top sellers or underperformers.
- Inventory management is reactive and not based on historical demand patterns.
- Sales data is not visualized or explored to understand seasonal trends, top categories, or revenue breakdowns.
- Manual reporting is time-consuming, error-prone, and not actionable in real-time.
- Forecasting is either done manually or not at all, leading to understocking or overstocking.

---

## Goals

- Build a responsive, modular Streamlit dashboard for visualizing sales and inventory data.
- Provide actionable insights through KPIs, trend charts, and forecasts.
- Allow filtering by store, product category, time range, and more.
- Offer basic ML-based forecasting using Prophet or similar.
- Enable business owners to export reports or snapshots of data.
- Lay a scalable foundation that could grow with the business (e.g., more stores or channels).

---

## Non-Goals

- Real-time POS integration (assume CSV or Excel uploads).
- Full ERP or inventory automation system.
- User authentication or role management (initial MVP only).
- Mobile-optimized experience beyond basic Streamlit responsiveness.

---

## Success Metrics

- Time to first insight < 2 minutes after data load.
- At least 5 core interactive views with charts and filters.
- Visual KPI summary for daily/weekly/monthly performance.
- Forecast accuracy within 10–20% range over 3-month historical data.
- User can export key tables and charts to Excel or image format.
- Zero-code setup for end-users — just upload and explore.

---

## Assumptions

- Data is provided as structured Excel or CSV files exported from POS.
- There are consistent fields: date, store ID/name, product name/category/size, quantity sold, revenue, cost.
- The app is deployed locally or on Streamlit Community Cloud.
- Store staff will not edit Python code — they’ll interact via the UI only.

---

## Requirements

### Functional Requirements

- [x] Upload sales and inventory data from CSV/XLSX.
- [x] View summary KPIs (total sales, avg order size, top categories).
- [x] Filter by date range, store, product category, and product.
- [x] Visualize sales over time (daily/weekly/monthly).
- [x] Identify best-selling and slow-moving products.
- [x] View inventory status by product/category/store.
- [x] Provide sales forecasting (Prophet-based).
- [x] Show customer segmentation insights (e.g., frequency of purchases, age group trends).
- [x] Export reports to Excel or CSV.

### Non-Functional Requirements

- [x] Runs locally or on Streamlit Cloud without installation beyond Python dependencies.
- [x] < 5s load time on datasets < 100k rows.
- [x] Cache-heavy computations (e.g., forecasting) with `@st.cache_data`.
- [x] Clean and professional UI with accessible color schemes and mobile-responsiveness.

---

## Pages / Views

### 1. 📊 Overview Dashboard

- High-level KPIs: total sales, avg basket size, gross margin
- Sales trend (line chart)
- Sales by store (bar)
- Category distribution (pie)
- Filters: date range, store

### 2. 🧺 Sales Analysis

- Drill-down by category, product, store
- Top-selling products
- Revenue by category
- Sales calendar heatmap
- Table of sales with sort/filter options

### 3. 📦 Inventory Overview

- Current stock by product/category
- Reorder alerts for low stock
- Days of supply calculation
- Inventory turnover rate
- Bar chart comparison: stock vs. avg daily sales

### 4. 📈 Forecasting

- Time series forecast using Prophet
- Adjustable forecast window (30/60/90 days)
- Forecast by store/category
- Confidence intervals displayed

### 5. 🧠 Customer Insights

- New vs. returning customers
- Avg order frequency
- Size/gender/age group breakdowns
- Optional CLV estimation

### 6. 📄 Reports & Exports

- Download current views as Excel or CSV
- Export charts as PNG (optional)
- Summary report generator

### 7. 📁 Data Upload

- Upload interface for sales/inventory files
- Schema validation and preview
- File retained in session or cache

### 8. 📍 Market Trends

- Integration with Google Trends via pytrends
- Search term popularity over time
- Optional regional breakdown

---

## User Stories

- As a **store manager**, I want to see top-selling products this week so I can reorder efficiently.
- As a **business owner**, I want to compare performance between two stores for any time period.
- As a **buyer**, I want to view which sizes/colors/styles underperform so I can reduce waste.
- As a **data novice**, I want to upload my spreadsheet and immediately see useful insights.
- As a **strategic planner**, I want to forecast sales for the next quarter so I can plan inventory.
