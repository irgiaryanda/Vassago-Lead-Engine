# Vassago Lead Engine

**READY TO USE (NON-DEVELOPERS):**
You don't need to install Python or use the terminal. Download the compiled Windows standalone application directly from our [Latest Release](https://github.com/irgiaryanda/Vassago-Lead-Engine/releases/latest). Extract the ZIP file and run `VassagoLeadEngine.exe`.

A robust, asynchronous web scraping engine designed for automated B2B lead generation. Built on FastAPI and Playwright, this application features dynamic search engine querying, anti-bot mitigation, and a standalone front-end dashboard for real-time monitoring and data extraction.

## System Architecture

*   **Backend:** FastAPI (Python) for high-performance, asynchronous REST API endpoints.
*   **Engine:** Playwright (Headless Chromium) for dynamic DOM rendering and JavaScript execution.
*   **Database:** SQLite with asynchronous I/O (aiosqlite) for lightweight, persistent data storage.
*   **Frontend:** Vanilla JavaScript, HTML5, and CSS3. No heavy frameworks, ensuring rapid load times.

## Key Features

*   **Asynchronous Processing:** Non-blocking architecture allows simultaneous API handling and browser automation.
*   **Anti-Bot Evasion:** Implements custom User-Agents, realistic viewport configurations, and automatic filtering of Cloudflare or CAPTCHA-protected domains.
*   **Search Engine Redundancy:** Utilizes Yahoo Search to bypass strict regional ISP SSL blocking and aggressive rate-limiting commonly found in other engines.
*   **Automated Data Normalization:** Regex-based email extraction and automatic deduplication via SQLite `INSERT OR IGNORE` constraints.
*   **Real-time Dashboard:** A clean, dark-themed UI for executing scans and visualizing captured lead data instantaneously.

## Prerequisites

Ensure the following dependencies are installed on your local machine before proceeding:

*   Python 3.10 or higher
*   Git

## Local Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/irgiaryanda/Vassago-Lead-Engine.git](https://github.com/irgiaryanda/Vassago-Lead-Engine.git)
   cd Vassago-Lead-Engine
