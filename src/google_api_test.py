import gspread
import os

# Load credentials from environment variable
creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
gclient = gspread.service_account(filename=creds_path)

# Open a sheet by name
gsheet = gclient.open("Pickles DB")
worksheet = gsheet.worksheet("products")

# Write a line to a row
worksheet.update(range_name="A4", values=[[3, "fusion_pickles", "Gurke, exotisch", "Single unit of fusion pickles", 0]])
