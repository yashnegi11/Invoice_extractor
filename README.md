# 🧾 Amazon Invoice Extractor

A Python and Streamlit-based tool that extracts structured data from **Amazon invoice PDFs** (supports both single and multi-item invoices) and generates an Excel file report with buyer, seller, and item-level details.

---

## 📌 Features

- Upload one or more Amazon PDF invoices.
- Automatically extracts:
  - Buyer & seller details
  - Invoice and order dates
  - Product name, quantity, tax, HSN code, and pricing
- Saves output to Excel (`.xlsx`) format.
- Simple and clean **Streamlit web interface**.

---

## 📸 Screenshots


  (https://github.com/user-attachments/assets/29d2bbf0-e4c7-48be-a8cd-b607232e3f19)  


---

## 🚀 How to Run

### 1. Clone the Repository

```
git clone https://github.com/your-username/amazon-invoice-extractor.git
cd amazon-invoice-extractor
```
### 2. Create and Activate Virtual Environment
```
Copy
Edit
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux
```
### 3. Install Dependencies
```
Copy
Edit
pip install -r requirements.txt
```
### 4. Launch the Streamlit App
```
Copy
Edit
streamlit run app.py
