# Spice Route – Automated Table Reservation & Guest Feedback AI Agent

## 1. Project Overview

Spice Route is an AI-powered restaurant guest inquiry and reservation assistance system built using Python, Flask, n8n, and Google Gemini.

The system receives guest messages through an n8n webhook, processes inquiries using an AI Agent, accesses restaurant information through custom Python APIs, and stores guest inquiries and workflow execution logs in CSV files.

## 2. Technologies Used

- Python 3.14
- Flask
- n8n Workflow Automation
- Google Gemini API
- REST APIs
- JSON
- CSV Data Storage
- Python Unittest

## 3. Features

- Guest inquiry handling through an n8n webhook.
- AI-powered restaurant guest assistance.
- Menu search and dietary checks.
- Retrieval of restaurant operating hours and reservation rules.
- Party-size and reservation-time validation.
- Structured AI responses using JSON.
- Guest inquiry storage in CSV.
- Workflow success and failure logging in CSV.
- Error handling for invalid requests and failed workflow steps.

**Important:** The reservation check validates restaurant rules and operating hours. It does not confirm actual live table availability.

## 4. Project Structure

```text
Spice_Route/
├── app.py
├── menu_tool.py
├── menu_tool_api.py
├── menu_search_tool.py
├── README.md
├── database/
│   ├── guest_inquiries.csv
│   ├── menu.csv
│   ├── operating_hours.csv
│   ├── reservation_rules.csv
│   └── workflow_logs.csv
├── tests/
├── screenshots/
└── workflow/
    └── spice_route_workflow.json
```

## 5. Installation

Open PowerShell in the project directory:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
py -m pip install flask
```

## 6. Run the Python APIs

### Main Guest Inquiry API

```powershell
py app.py
```

Runs on port 5000.

### Menu Tool API

Open a second PowerShell terminal, activate the virtual environment, and run:

```powershell
py menu_tool_api.py
```

Runs on port 5001.

Keep both APIs running while testing the n8n workflow.

## 7. Main API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API health check |
| POST | `/api/inquiries` | Save guest inquiry |
| GET | `/api/menu` | Retrieve menu |
| GET | `/api/operating-hours` | Retrieve operating hours |
| GET | `/api/reservation-rules` | Retrieve reservation rules |
| POST | `/api/workflow-logs` | Record workflow execution logs |

## 8. n8n AI Agent Workflow

Workflow name: Spice Route Guest Reservation Agent

Main workflow components:

1. Webhook receives guest inquiry.
2. IF node validates incoming information.
3. HTTP Request nodes communicate with Python APIs.
4. Google Gemini Chat Model powers the AI Agent.
5. AI Agent processes guest requests and uses relevant tools.
6. Structured Output Parser validates the AI response.
7. Flask API stores guest inquiries.
8. Success and error branches send workflow logs to the local CSV endpoint.

### Webhook Test URL

```text
http://localhost:5678/webhook-test/spice-route-reservation
```

### Sample Test Request

```json
{
  "guest_name": "Test Guest",
  "guest_message": "I want to book a table",
  "party_size": 4
}
```

### Gemini Setup

Configure a valid Google Gemini API credential in n8n and select an available model.

Never publish API keys or credentials in the repository.

## 9. Workflow Logging

All workflow outcomes are stored in:

```text
database/workflow_logs.csv
```

The CSV contains:

- timestamp
- execution_status
- workflow_step
- action
- http_status
- message

Both successful and failed workflow executions are intended to be recorded through:

```text
POST /api/workflow-logs
```

The CSV can be checked using:

```powershell
Get-Content .\database\workflow_logs.csv
```

## 10. Automated Testing

Run Python unit tests using:

```powershell
py -m unittest discover -s tests -v
```

## 11. Configuration and Security

- Flask API ports are configured in the Python application files.
- n8n HTTP Request nodes must use reachable addresses for the local Flask APIs.
- Update local network IP addresses in n8n if the computer's IP changes.
- Gemini credentials are managed through n8n Credentials.
- Do not commit API keys, passwords, or private credentials.

## 12. Important Notes and Limitations

- Restaurant menu, prices, operating hours, and reservation rules are demonstration data.
- Reservation validation does not connect to a live restaurant table inventory.
- Workflow execution depends on Google Gemini service availability.
- Temporary Gemini API 503 errors may occur during periods of high demand.
- Local CSV files are used for inquiry storage and workflow logging instead of automated Google Sheets integration.

## 13. Submission and Demonstration

GitHub Repository:

https://github.com/ammarakhalid9080-commits/Spice-Route-AI-Agent

A screen recording demonstrating the Python APIs, n8n workflow, and CSV logging should be added to the project submission when available.

## 14. Project Objective

The objective is to demonstrate the integration of Python REST APIs, n8n workflow automation, and an AI Agent to assist with restaurant guest inquiries, menu searches, dietary questions, reservation-rule validation, and workflow logging.