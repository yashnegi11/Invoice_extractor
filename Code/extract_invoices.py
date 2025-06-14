import os
import fitz  
import pandas as pd
import re

INPUT_DIR = r'C:\Users\hp\ys\InvoiceExtractor\Input'
OUTPUT_FILE = r'C:\Users\hp\ys\InvoiceExtractor\Output\extracted_invoices.xlsx'

def extract_text_from_pdf_bytes(pdf_bytes):
    text = ""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_text_from_pdf_file(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def parse_amazon_invoice_multiple_items(text):
    try:
        invoice_number = re.search(r"Invoice Number\s*:\s*(\S+)", text).group(1)
        order_number = re.search(r"Order Number\s*:\s*(\S+)", text).group(1)
        invoice_date = re.search(r"Invoice Date\s*:\s*(\d{2}\.\d{2}\.\d{4})", text).group(1)
        order_date = re.search(r"Order Date\s*:\s*(\d{2}\.\d{2}\.\d{4})", text).group(1)

        billing_match = re.search(r'Billing Address\s*:\s*(.*?)\nShipping Address', text, re.DOTALL)
        shipping_match = re.search(r'Shipping Address\s*:\s*(.*?)\n', text, re.DOTALL)
        seller_match = re.search(r'Sold By\s*:\s*(.*?)\n(?:PAN|GST)', text, re.DOTALL)
        gst_match = re.search(r'GST Registration No:\s*([A-Z0-9]+)', text)
        pan_match = re.search(r'PAN No:([A-Z0-9]+)', text)
        supply_match = re.search(r'Place of supply:(.*)', text)
        delivery_match = re.search(r'Place of delivery:(.*)', text)

        billing = billing_match.group(1).replace('\n', ', ').strip() if billing_match else ""
        shipping = shipping_match.group(1).replace('\n', ', ').strip() if shipping_match else ""
        buyer_name = billing.split(',')[0] if billing else ""
        seller = seller_match.group(1).replace('\n', ', ').strip() if seller_match else ""
        seller_gst = gst_match.group(1) if gst_match else ""
        seller_pan = pan_match.group(1) if pan_match else ""
        place_of_supply = supply_match.group(1).strip() if supply_match else ""
        place_of_delivery = delivery_match.group(1).strip() if delivery_match else ""

        product_blocks = re.findall(
            r"\b\d+\s+(.*?)\(.*?\)\s*HSN:(\d+)\s*₹([\d,.]+)\s+₹([\d,.]+)\s+(\d+)\s+₹([\d,.]+)\s+([\d%]+)\s+(\w+)\s+₹([\d,.]+)\s+₹([\d,.]+)",
            text, re.DOTALL
        )

        items = []
        for desc, hsn, unit_price, discount, qty, net_amount, tax_rate, tax_type, tax_amount, total_amount in product_blocks:
            item = {
                "Source": "Amazon",
                "Invoice Number": invoice_number,
                "Order Number": order_number,
                "Invoice Date": invoice_date,
                "Order Date": order_date,
                "Product Description": desc.replace("\n", " ").strip(),
                "HSN Code": hsn,
                "Unit Price": unit_price,
                "Discount": discount,
                "Quantity": qty,
                "Net Amount": net_amount,
                "Tax Rate": tax_rate,
                "Tax Type": tax_type,
                "Tax Amount": tax_amount,
                "Total Amount": total_amount,
                "Buyer Name": buyer_name,
                "Billing Address": billing,
                "Shipping Address": shipping,
                "Seller Name": seller,
                "Seller PAN": seller_pan,
                "Seller GST": seller_gst,
                "Place of Supply": place_of_supply,
                "Place of Delivery": place_of_delivery
            }
            items.append(item)

        if not items:
            print("⚠️ No products matched. Check pattern or invoice layout.")

        return items
    except Exception as e:
        print(f"❌ Error parsing Amazon invoice: {e}")
        return []

def process_uploaded_pdfs(uploaded_files):
    all_data = []
    for file in uploaded_files:
        text = extract_text_from_pdf_bytes(file.read())
        parsed_items = parse_amazon_invoice_multiple_items(text)
        all_data.extend(parsed_items)
    df = pd.DataFrame(all_data)
    return df

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"❌ Input folder does not exist: {INPUT_DIR}")
        return
    if not os.path.exists(os.path.dirname(OUTPUT_FILE)):
        os.makedirs(os.path.dirname(OUTPUT_FILE))

    all_data = []

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(INPUT_DIR, filename)
            print(f"📄 Processing: {filename}")
            text = extract_text_from_pdf_file(file_path)

            if "amazon" in filename.lower():
                parsed = parse_amazon_invoice_multiple_items(text)
                if not parsed:
                    print(f"⚠️ No items extracted from: {filename}")
                all_data.extend(parsed)
            else:
                print(f"⏩ Skipping non-Amazon file: {filename}")

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"✅ Extraction complete. Data saved to: {OUTPUT_FILE}")
    else:
        print("⚠️ No valid Amazon invoices found to process.")

if __name__ == "__main__":
    main()
