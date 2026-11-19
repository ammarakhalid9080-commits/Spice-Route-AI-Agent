
# Spice Route – Restaurant Guest Inquiry API

## Project Overview
Spice Route is a Python-based restaurant guest inquiry management system built using Flask.

It receives guest inquiries through a REST API, validates the submitted information, and stores valid inquiries in a CSV file.

## Technologies Used
- Python
- Flask
- CSV
- REST API
- Unittest

## Project Features
- Receive guest inquiries through POST requests.
- Validate guest name and message.
- Validate party size (1–10 guests).
- Save valid inquiries in a CSV database.
- Retrieve restaurant menu information.
- Retrieve operating hours.
- Retrieve reservation rules.
- Automated testing.

## Project Structure

```text
Spice_Route/
│
├── app.py
├── README.md
│
├── database/
│   ├── guest_inquiries.csv
│   ├── menu.csv
│   ├── operating_hours.csv
│   └── reservation_rules.csv
│
├── tests/
│   └── test_app.py
│
├── screenshots/
└── workflow/
```

## Installation

1. Clone or download the project.
2. Open the project folder in the terminal.
3. Create a virtual environment:

   `py -m venv venv`

4. Activate the environment in PowerShell:

   `.\venv\Scripts\Activate.ps1`

5. Install Flask:

   `py -m pip install flask`

## Run the Application

Run:

`py app.py`

Open:

`http://127.0.0.1:5000/`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| POST | `/api/inquiries` | Submit guest inquiry |
| GET | `/api/menu` | Retrieve restaurant menu |
| GET | `/api/operating-hours` | Retrieve operating hours |
| GET | `/api/reservation-rules` | Retrieve reservation rules |

# Spice Route – Automated Table Reservation & Guest Feedback AI Agent

## 1. Project Overview

Spice Route is a Python-based restaurant guest inquiry management system integrated with an n8n AI Agent.

The system receives guest inquiries through an n8n webhook, validates guest information, uses an AI assistant to answer restaurant-related questions, checks menu information and dietary requirements through custom Python APIs, and saves valid inquiries in a CSV database.

## 2. Technologies Used

- Python 3.14
- Flask
- n8n Workflow Automation
- Google Gemini AI
- REST APIs
- CSV Data Storage
- JSON
- Unittest

## 3. Project Features

- Receive guest inquiries through an n8n webhook.
- Validate guest name, message, and party size.
- Accept reservations for 1–10 guests.
- AI-powered restaurant guest assistance.
- Search restaurant menu items and prices.
- Check vegetarian and vegan dietary requirements.
- Retrieve menu, operating hours, and reservation rules.
- Save valid guest inquiries automatically in CSV.
- Automated Python unit tests.
- Error handling through workflow validation.

## 4. Project Structure

```text
Spice_Route/
│
├── app.py
├── menu_tool.py
├── menu_tool_api.py
├── README.md
│
├── database/
│   ├── guest_inquiries.csv
│   ├── menu.csv
│   ├── operating_hours.csv
│   └── reservation_rules.csv
│
├── tests/
│   └── test_app.py
│
├── screenshots/
│
├── workflow/
│   └── spice_route_workflow.json
│
└── venv/
```

## 5. Installation

1. Open the project folder in PowerShell.
2. Create a virtual environment:

   `py -m venv venv`

3. Activate it:

   `.\venv\Scripts\Activate.ps1`

4. Install Flask:

   `py -m pip install flask`

## 6. Run the Python Applications

### Main Guest Inquiry API

Run:

`py app.py`

Main API address:

`http://127.0.0.1:5000/`

### Menu Tool API

Open another terminal, activate the virtual environment, and run:

`py menu_tool_api.py`
├── menu_search_tool.py

Menu Tool API address:

`http://127.0.0.1:5001/`

Both applications must remain running while testing the complete workflow.

## 7. Main API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| POST | `/api/inquiries` | Submit and save guest inquiry |
| GET | `/api/menu` | Retrieve restaurant menu |
| GET | `/api/operating-hours` | Retrieve operating hours |
| GET | `/api/reservation-rules` | Retrieve reservation rules |

## 8. Menu Tool API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check Menu Tool API status |
| POST | `/menu/search` | Search for menu items |
| POST | `/menu/dietary-check` | Check dietary suitability |

## 9. n8n AI Agent Workflow

Workflow name: `Spice Route Guest Reservation Agent`

The workflow includes:

1. **Webhook Trigger:** Receives guest inquiry data.
2. **IF Validation:** Checks required fields and validates party size between 1 and 10.
3. **AI Agent:** Uses Google Gemini to understand and respond to guest questions.
4. **Menu Search Tool:** Retrieves menu item information through the Python API.
5. **Dietary Check Tool:** Checks whether menu items meet guest dietary requirements.
6. **Inquiry Logging:** Sends valid inquiries to the Flask API for CSV storage.

The exported workflow is available at:

`workflow/spice_route_workflow.json`

### Webhook Test URL

`http://localhost:5678/webhook-test/spice-route-reservation`

### Sample Inquiry JSON

```json
{
  "guest_name": "Ali",
  "guest_message": "Is Fresh Juice suitable for vegan guests?",
  "party_size": 2
}
```

### Gemini Configuration

Configure Google Gemini credentials in n8n before executing the AI Agent workflow. Keep API keys private and do not include them in the exported project files.

## 10. Automated Testing

Run:

`py -m unittest discover -s tests -v`

### Test Results

All 5 Python unit tests passed successfully.

## 11. Data Storage

Guest inquiries are automatically stored in:

`database/guest_inquiries.csv`

The database also contains sample menu items, operating hours, and reservation rules.

## 12. Important Notes

- Menu items, prices, operating hours, and reservation rules are sample demonstration data, not verified restaurant information.
- The project uses local CSV storage for automated inquiry logging.
- The Google Sheets spreadsheet is a separate sample log template; automated Google Sheets integration is not included.
- The n8n workflow requires the Python APIs to be running and their configured network addresses to be reachable.
- Update the local network IP addresses in n8n HTTP Request nodes if the computer's IP address changes.

## 13. Project Objective
## Task 2 – AI Agent Integration

### Technologies Added
- n8n Workflow Automation
- Google Gemini API
- Custom Python Tool
- JSON Schema Validation

### AI Agent Features
- Answers restaurant menu and dietary questions.
- Searches restaurant data using a custom Python tool.
- Retrieves reservation rules.
- Checks party size and restaurant operating hours.
- Returns structured JSON responses.

### Supported Python Tool Actions
- `search_menu`
- `get_reservation_rules`
- `check_reservation`

### Structured JSON Output
The AI Agent returns:
- `response` – Message for the guest.
- `follow_up` – Boolean follow-up flag.
- `action` – Action performed by the AI Agent.

### Security
Google Gemini API credentials are stored securely in n8n Credentials.

### Testing
- Vegan food search tested.
- Gluten-free food search tested.
- Reservation request for four guests on Monday at 20:00 tested.
- Structured JSON output tested.

**Note:** The system checks restaurant operating hours only. It does not confirm actual live table availability.

The objective is to demonstrate how Python REST APIs, workflow automation, and an AI Agent can work together to automate restaurant guest inquiries, menu assistance, dietary checks, and inquiry management.
