# -*- coding: utf-8 -*-

# ========================
# Task 5: Repository Layer
# ========================
# Write a Repository class to handle data persistence for your app:
# [ ] Start with a JSONRepository class:
#     - Handles saving and loading data to/from a JSON file
#     - Methods: save(data: dict), load() -> dict
#     - Use utf-8 encoding
#     - Handle file not found and JSON decode errors gracefully
# [ ] Then, create a GoogleSheetsRepository class that inherits from JSONRepository:
#     - Implements saving/loading data to Google Sheets
#     - Methods: save(data: dict), load() -> dict (override as needed)
#     - Use Google Sheets API (or mock for now)
#     - Handle API errors gracefully
# [ ] (Optional) Add an abstract base class if you want to enforce method signatures
# [ ] (Optional) Add static/class methods for validation or setup
