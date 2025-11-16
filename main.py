import time
import os
from playwright.sync_api import sync_playwright
import google.generativeai as genai
from dotenv import load_dotenv

#  & "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --user-data-dir="C:\tmp\brave-dev" --no-first-run

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
BROWSER_PATH = os.getenv("BROWSER_PATH")
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)
    print("🤖 Pomyślnie połączono z Gemini.")
except Exception as e:
    print(f"❌ Błąd podczas łączenia z Gemini: {e}")
    print("Sprawdź swój klucz API i połączenie internetowe.")
    exit()


def get_correct_answer(question, answers):

    answer_list_str = "\n".join([f"{i + 1}. {ans}" for i, ans in enumerate(answers)])

    prompt = f"""
    Jesteś ekspertem w odpowiadaniu na pytania quizowe.
    Odpowiedz tylko i wyłącznie tekstem poprawnej odpowiedzi. Nie dodawaj żadnych wyjaśnień.

    Pytanie:
    {question}

    Dostępne odpowiedzi:
    {answer_list_str}

    Poprawna odpowiedź (tylko tekst):
    """

    try:
        response = model.generate_content(prompt)
        correct_text = response.text.strip()
        return correct_text
    except Exception as e:
        print(f"Błąd podczas wywołania API Gemini: {e}")
        return None

REMOTE_URL = "http://127.0.0.1:9222"

with sync_playwright() as p:
    print("Łączenie z uruchomioną przeglądarką...")
    browser = p.chromium.connect_over_cdp(REMOTE_URL)
    context = browser.contexts[0] if browser.contexts else browser.new_context()
    page = context.new_page()
    page.set_default_timeout(0)  # Nieskończony timeout

    page.goto("https://play.blooket.com/play")
    print("✅ Połączono! Przejdź do okna przeglądarki i rozpocznij grę.")
    print("Skrypt czeka na pierwsze pytanie...")

    current_question = None

    while True:
        try:

            question_element = page.wait_for_selector("div._questionText_1w7yk_73")
            new_question = question_element.text_content()

            if new_question and new_question != current_question:
                current_question = new_question
                print("\n--- Nowe pytanie! ---")
                print(f"❓ Pytanie: {current_question}")

                page.wait_for_selector("div._answerText_1rz5f_129")
                answer_elements = page.query_selector_all("div._answerText_1rz5f_129")
                answer_texts = [el.text_content().strip() for el in answer_elements]

                print(f"Odpowiedzi: {answer_texts}")

                print("🧠 Wysyłanie pytania do Gemini...")
                t0=time.time()
                correct_answer_text = get_correct_answer(current_question, answer_texts)

                if not correct_answer_text:
                    print("Nie udało się uzyskać odpowiedzi od Gemini, przechodzę dalej.")
                    continue

                print(f"🤖 Odpowiedź Gemini: {correct_answer_text}")

                clicked = False
                for el in answer_elements:
                    if el.text_content().strip() == correct_answer_text:
                        print(f"🎯 Klikam: {correct_answer_text}")
                        t1=time.time()-t0
                        print(f"♿ Zajęło mi to: {t1:.3f}")

                        parent_button = el.query_selector("xpath=..")
                        parent_button.click()
                        clicked = True
                        break

                if not clicked:
                    print(f"Nie mogłem znaleźć elementu z tekstem: '{correct_answer_text}'")

                time.sleep(1)
            time.sleep(0.05)

        except Exception as e:
            time.sleep(0.5)