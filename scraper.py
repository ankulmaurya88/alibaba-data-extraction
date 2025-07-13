
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime,timedelta
import requests
import os

# Setup Chrome options
options = Options()
options.headless = True  # Run in headless mode

driver = webdriver.Firefox(options=options)

# for i in range(0, 1):
    
# URL to fetch
url = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm?spm=a2700.8073608.1998677541.1.82be65aaoUUItC&country=AE&recently=Y&tracelog=newest"


driver.get(url)


time.sleep(5)














# Let the content load
# time.sleep(5)

# Optional: Scroll to bottom to ensure dynamic content is loaded
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# Folder to save screenshot
folder_name = "rfq_screenshots"
os.makedirs(folder_name, exist_ok=True)

# File name
file_path = os.path.join(folder_name, "rfq_page3.png")

# Full page screenshot (Firefox only)
# driver.get_screenshot_as_file(file_path)

# print(f"✅ Screenshot saved to: {file_path}")








# Get page HTML and extract rfqIds using regex
html = driver.page_source
rfq_ids = re.findall(r'rfqId:\s*"(.*?)"', html)


soup = BeautifulSoup(driver.page_source, "html.parser")


rfq_items = soup.find_all("div", class_="brh-rfq-item")

# Extract data
data = []

inquiry_time_data=[]
for i, item in enumerate(rfq_items):
    title_tag = item.find("a", class_="brh-rfq-item__subject-link")
    title = title_tag.text.strip() if title_tag else "N/A"

    desc_tag = item.find("div", class_="brh-rfq-item__detail")
    description = desc_tag.text.strip() if desc_tag else "N/A"

    qty_tag = item.find("div", class_="brh-rfq-item__quantity")
    quantity = qty_tag.find("span", class_="brh-rfq-item__quantity-num").text.strip() if qty_tag else "N/A"

    country_tag = item.find("div", class_="brh-rfq-item__country")
    country = country_tag.text.strip().replace("Posted in:", "").strip() if country_tag else "N/A"

    buyer_tag = item.find("div", class_="text")
    buyer = buyer_tag.text.strip() if buyer_tag else "N/A"

    inquiry_time_tag = item.find("div", class_="brh-rfq-item__publishtime")
    inquiry_time = inquiry_time_tag.get_text(strip=True) if inquiry_time_tag else "N/A"

    quotes_left_tag = item.find("div", class_="brh-rfq-item__quote-left")
    quotes_left = quotes_left_tag.text.replace("Quotes Left", "").strip() if quotes_left_tag else "N/A"

    date_tag = item.find("div", class_="brh-rfq-item__publishtime")
    date_posted = date_tag.text.replace("Date Posted:", "").strip() if date_tag else "N/A"

    discount_tag = item.find("span", class_="rfq-quote-consume-tip-discount")
    discount_quote = discount_tag.text.strip() if discount_tag else "N/A"

    image_tag = item.find("img", class_="user-img")
    buyer_image = "https:" + image_tag['src'] if image_tag and image_tag.get('src') else "N/A"

    # Tags logic (basic example)
    tag_check = item.find("div", class_="next-tag-body")
    yes_no = "Yes" if tag_check else "No"

    # Assign rfqId based on index if available
    rfq_id = rfq_ids[i] if i < len(rfq_ids) else "N/A"
    inquiry_url=title_tag['href'].strip() if title_tag and title_tag.has_attr('href') else "N/A"
    # print()
    
    





    if not inquiry_url.startswith("http"):
        inquiry_url = "https:" + inquiry_url

    # Visit the inquiry URL
    driver.get(inquiry_url)
    time.sleep(3)  # wait to fully load

    # Save unique screenshot
    rfq_id = rfq_ids[i] if i < len(rfq_ids) else f"no_id_{i}"
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')[:50]
    file_path = os.path.join(folder_name, f"{i+1}_{safe_title}_{rfq_id}.png")
    driver.save_screenshot(file_path)

    # print(f"✅ Screenshot saved: {file_path}")

    time.sleep(1)  # wait before next



    data.append({
        "RFQ ID": rfq_id,
        "Title": title,
        "Buyer Name": buyer,
        "Buyer Image": buyer_image,
        "Inquiry Time": inquiry_time,
        "Quotes Left": quotes_left,
        "Country": country,
        "Quantity Required": quantity,
        "Email Confirmed": yes_no,
        "Experienced Buyer": yes_no,
        "Complete Order via RFQ": yes_no,
        "Typical Replies": yes_no,
        "Interactive User": yes_no,
        "Inquiry URL": inquiry_url,  # Could be parsed if needed
        "Inquiry Date": "N/A",
        "Scraping Date": datetime.now().strftime("%d-%m-%Y")
    })


    inquiry_time_data.append({"Scraping Date": datetime.now().strftime("%d-%m-%Y"),
                                "Inquiry Time": inquiry_time,})








# print(inquiry_time_data)
# Helper function
def parse_inquiry_date_only(inquiry_time_str, scraping_date_str):
    try:
        match = re.search(r"Date Posted:(.*)", inquiry_time_str)
        if not match:
            return "N/A"
        time_str = match.group(1).strip().lower()

        base_time = datetime.strptime(scraping_date_str, "%d-%m-%Y")
        now = datetime.now()
        base_time = base_time.replace(hour=now.hour, minute=now.minute)

        if "just now" in time_str:
            inquiry_time = base_time
        elif "minute" in time_str:
            minutes = int(re.search(r"(\d+)", time_str).group(1))
            inquiry_time = base_time - timedelta(minutes=minutes)
        elif "hour" in time_str:
            hours = int(re.search(r"(\d+)", time_str).group(1))
            inquiry_time = base_time - timedelta(hours=hours)
        else:
            return "N/A"

        return inquiry_time.strftime("%d-%m-%Y")  # ✅ Only date
    except:
        return "N/A"

# Final result list
inquiry_dates_only = [
    parse_inquiry_date_only(item["Inquiry Time"], item["Scraping Date"])
    for item in inquiry_time_data
]





for i, date in enumerate(inquiry_dates_only):
    if i < len(data):
        data[i]["Inquiry Date"] = date  # ✅ Replace old "N/A" with parsed date





# print(data)
df = pd.DataFrame(data)




df.to_csv("rfq_output.csv", index=False)

print("Scraping completed. Data saved to rfq_output.csv")

