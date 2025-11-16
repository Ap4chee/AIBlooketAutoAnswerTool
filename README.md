# Blooket Gemini Bot 🤖

A simple bot for the game [Blooket](https://www.blooket.com/) that uses **Google Gemini AI** to automatically answer quiz questions.

The bot connects to a remotely controlled browser instance (via Playwright), monitors the game screen, and when a new question appears, it sends the question and its potential answers to the Gemini API to get the correct one. It then clicks that answer in the browser.

## ⚠️ Disclaimer

This project was created for educational purposes to demonstrate the integration of browser automation (Playwright) with a large language model (Gemini).

Using bots or scripts for automation in online games like Blooket is **likely against their Terms of Service (ToS)**. Use this tool at your own risk. The author is not responsible for any consequences, such as account suspension.

---

## 🚀 How to Run

Follow these steps in order.

### Step 1: Prerequisites

* Python 3.8+
* A Chromium-based browser (e.g., Google Chrome, Brave, MS Edge)
* A Google account and a Google Gemini API Key (available from [Google AI Studio](https://aistudio.google.com/))

### Step 2: Install Dependencies

1.  Clone or download this repository.
2.  Create a `requirements.txt` file in the project folder with the following content:

    ```
    playwright
    google-generativeai
    python-dotenv
    ```

3.  Install the packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

4.  Install the browser engines for Playwright:

    ```bash
    playwright install
    ```

### Step 3: Configure Gemini API

1.  Create a file named `.env` in the same directory as the script.
2.  Add your Gemini API key and preferred model to it:

    ```ini
    # Replace with your API key from Google AI Studio
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    
    # You can use "gemini-pro" or a newer model
    MODEL_NAME="gemini-pro"
    ```

### Step 4: Launch the Browser in Debug Mode

**This is the most important step.** The bot will not launch its own browser; it will connect to the one you launch manually.

Open a terminal (CMD or PowerShell) and paste the command, adjusting the path to your browser and profile directory.

**Example for Brave:**
```bash
& "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --user-data-dir="C:\tmp\brave-dev" --no-first-run
