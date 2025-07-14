
# 📦 Alibaba RFQ Data Extraction

This repository contains a powerful and customizable web scraping tool built with **Python, Selenium, and BeautifulSoup** to extract RFQ (Request for Quotation) data from [sourcing.alibaba.com](https://sourcing.alibaba.com). The tool captures detailed buyer inquiries, product requirements, and associated metadata — including screenshots of individual RFQ pages.

---

## 🚀 Features

- ✅ Extracts buyer and product data from Alibaba RFQ listings
- 📆 Converts relative "Date Posted" to accurate **Inquiry Date**
- 🌍 Captures metadata such as Country, Buyer Name, Quantity, Email Status, etc.
- 📸 Takes **full-page screenshots** of each RFQ detail page
- 💾 Saves data into CSV and Excel formats
- 🧠 Handles "Just now", "X minutes ago", and "X hours ago" cases
- 📂 Automatically stores screenshots in a dedicated folder

---

## 🛠️ Tech Stack

- **Python 3.12**
- **Selenium WebDriver**
- **BeautifulSoup4**
- **Pandas**
- **OpenPyXL** (for writing Excel files)

---

## 📦 Installation

```bash
git clone https://github.com/ankulmaurya88/alibaba-data-extraction.git
cd alibaba-data-extraction
python3 -m venv venv
source venv/bin/activate   # Or use venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---
📄 Usage
Run the scraper script:
---
``` bash
python scraper.py
```

---
The script will:

Navigate to Alibaba RFQ listing pages
Extract RFQ details
Visit each RFQ detail page and take a screenshot
Convert Inquiry Times into full Inquiry Dates
Save everything into rfq_output.csv and rfq_output.xlsx

---



## 🗃️ Output Files

- rfq_output.csv – Tabular data of all RFQs scraped
- rfq_output.xlsx – Excel version of the same
- /rfq_screenshots/ – Folder containing all RFQ page screenshots


## 📊 Data Columns

- Column	Description
- RFQ ID	Unique RFQ Identifier
- Title	Product or service being requested
- Buyer Name	Name of the person raising the inquiry
- Buyer Image	Profile image of buyer (if available)
- Inquiry Time	Time displayed on the site (e.g., "5 hours ago")
- Inquiry Date	Converted to full date (e.g., "13-07-2025")
- Quotes Left	Number of quotes remaining for RFQ
- Country	Buyer location
- Quantity Required	Quantity requested
- Email Confirmed	Whether buyer's email is confirmed
- Experienced Buyer	Tag status
- Complete Order via RFQ	Tag status
- Typical Replies	Tag status
- Interactive User	Tag status
- Inquiry URL	URL to the inquiry page
- Scraping Date	Date on which scraping was performed





# Chrome & ChromeDriver (version match required)


# 📬 Contact
---
Created by @ankulmaurya88
Feel free to raise issues or pull requests.
---

# 📄 License
---
This project is licensed under the MIT License.
---













