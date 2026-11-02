# CLI-QnA

A lightweight Python command-line application powered by Google Gemini, allowing users to ask questions and receive concise, informative answers directly in the terminal.

## Features

- AI-powered question answering using Google Gemini.
- Concise, single-paragraph responses.
- Automatic text wrapping based on terminal width.
- Local time and date queries without API requests.
- Optional Google Search grounding using `--web`.
- Secure API key management using `.env`.
- Global terminal access through `pipx`.

## Requirements

- Python 3.10+
- pipx
- Google Gemini API key

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/cli-qna.git
cd cli-qna
```

**2. Install the CLI**

```bash
pipx install .
```

For local development, use `pipx install --editable .` instead.

**3. Configure your API key**

Generate a free-tier API key from [Google AI Studio](https://aistudio.google.com/api-keys).

Create the global configuration directory:

```bash
mkdir -p ~/.config/cli-qna
```

Create a `.env` file:

```bash
nano ~/.config/cli-qna/.env
```

Add your API key:

```dotenv
GEMINI_API_KEY=your_api_key_here
```

Secure the file:

```bash
chmod 600 ~/.config/cli-qna/.env
```

The application automatically loads the API key using `python-dotenv`. For local development, a `.env` file in the project root is also supported.

## Usage

Ask a question from any terminal directory:

```bash
qna "What is AWS?"
```

Ask technical questions:

```bash
qna "Explain Terraform state locking"
```

Get the current local time:

```bash
qna "What is the time?"
```

Get today's date:

```bash
qna "What is the date?"
```

Enable Google Search grounding:

```bash
qna --web "What are the latest AWS updates?"
```

Google Search grounding requires a supported Gemini API project and may incur additional charges.

## Development

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/YOUR_USERNAME/cli-qna.git
cd cli-qna
pipx install --editable .
```

Changes to the Python source code will be reflected in the installed CLI. Dependency changes may require reinstalling the package.

## Tech Stack

- **Python** — Application development
- **Google Gemini API** — AI-generated responses
- **Google GenAI SDK** — Gemini integration
- **python-dotenv** — API key configuration
- **pipx** — CLI installation and environment isolation
- **setuptools** — Python packaging

## Security

API keys are stored in `.env` files and excluded from version control through `.gitignore`. Never commit credentials or sensitive configuration files to the repository.