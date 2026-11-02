import argparse
import os
import sys
import shutil
import textwrap

from datetime import datetime
from google import genai
from google.genai import types
from pathlib import Path
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# Fallback for globally installed CLI
load_dotenv(Path.home() / ".config" / "cli-qna" / ".env")


MODEL = "gemini-3.5-flash-lite"
TIMEOUT_MS = 60000


def local_answer(question):
    question = question.strip().lower().rstrip("?!.")

    time_questions = {
        "what is the time",
        "what's the time",
        "what time is it",
        "current time",
        "time",
    }

    date_questions = {
        "what is the date",
        "what's the date",
        "what is today's date",
        "what day is it",
        "today's date",
        "todays date",
        "date",
    }

    now = datetime.now().astimezone()

    if question in time_questions:
        return now.strftime("Current time: %I:%M:%S %p (%Z)")

    if question in date_questions:
        return now.strftime("Today: %A, %d %B %Y")

    return None


def print_wrapped(text):
    width = max(
        10,
        shutil.get_terminal_size(fallback=(80, 24)).columns - 2
    )

    for paragraph in text.strip().splitlines():
        if paragraph.strip():
            print(textwrap.fill(
                paragraph,
                width=width,
                break_long_words=False,
                break_on_hyphens=False
            ))
        else:
            print()


def main():
    parser = argparse.ArgumentParser(
        prog="qna",
        description="Ask questions directly from your terminal."
    )

    parser.add_argument(
        "question",
        nargs="+",
        help="Your question"
    )

    parser.add_argument(
        "--web",
        action="store_true",
        help="Enable Google Search grounding"
    )

    args = parser.parse_args()
    question = " ".join(args.question)

    #Answer local questions without an API request
    if not args.web:
        answer = local_answer(question)
        if answer is not None:
            print(answer)
            return

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        parser.error("GEMINI_API_KEY is not configured.")

    print("Asking Gemini...", flush=True)

    try:
        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=TIMEOUT_MS
            )
        )

        tools = (
            [types.Tool(google_search=types.GoogleSearch())]
            if args.web else None
        )

        response = client.models.generate_content(
            model=MODEL,
            contents=question,
            config=types.GenerateContentConfig(
            tools=tools,
            max_output_tokens=512,
            system_instruction=(
                "You are a concise, informative CLI assistant. "
                "Answer every question in one short paragraph using "
                "2 to 3 sentences and no more than 70 words. "
                "Provide the most relevant information directly. "
                "Avoid headings, bullet points, introductions, "
                "unnecessary examples, and Markdown formatting. "
                "Prioritise accuracy and clarity."
    )
)

        )

        print()
        print_wrapped(response.text or "No answer returned.")

        if args.web and response.candidates:
            metadata = response.candidates[0].grounding_metadata
            chunks = metadata.grounding_chunks if metadata else []

            sources = []
            for chunk in chunks or []:
                web = chunk.web
                if web and web.uri and web.uri not in sources:
                    sources.append(web.uri)

            if sources:
                print("\nSources:")
                for index, url in enumerate(sources, 1):
                    print(f"{index}. {url}")

    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        sys.exit(130)

    except Exception as error:
        print(f"\nAPI error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
