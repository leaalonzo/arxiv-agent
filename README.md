# arxiv-agent

A local AI agent that runs on a Raspberry Pi, fetches the latest research papers from ArXiv every morning, summarises them with an LLM, and serves a digest on a dashboard accessible from any device on your home network.

Built as a side project to learn edge AI and agentic frameworks. Full writeup on [Substack](https://gleanai.substack.com).

---

## What it does

Every morning at 7am, the agent:

1. Hits the ArXiv API and pulls the latest papers on LLMs in financial markets, machine learning in asset pricing, and algorithmic trading
2. Summarises each abstract into plain English using Groq's LLM API
3. Writes the digest to a log file
4. Serves it on a Flask dashboard at http://<your-pi-ip>:5000

---

## Stack

- Hardware: Raspberry Pi 3 (1GB RAM)
- LLM inference: Groq API (llama-3.1-8b-instant)
- Data source: ArXiv public API
- Dashboard: Flask
- Scheduler: cron

---

## Setup

### 1. Clone the repo

git clone https://github.com/leaalonzo/arxiv-agent.git
cd arxiv-agent

### 2. Install dependencies

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 3. Add your Groq API key

cp .env.example .env

Edit .env and add your key:
GROQ_API_KEY=your_key_here

Get a free API key at console.groq.com.

### 4. Run the agent

python agent.py

### 5. Open the dashboard

Navigate to http://localhost:5000 on the Pi, or http://<your-pi-ip>:5000 from any device on the same network. Find your Pi's IP by running: hostname -I

### 6. Automate with cron

crontab -e

Add this line to run every morning at 7am:
0 7 * * * /home/pi/arxiv-agent/venv/bin/python3 /home/pi/arxiv-agent/agent.py >> /home/pi/arxiv-agent/digest.log 2>&1

---

## Hardware constraints and design decisions

This project was built on a Raspberry Pi 3 with 1GB RAM. That single constraint shaped every subsequent decision:

- Local models (Mistral 7B, phi3:mini) required more RAM than available
- TinyLlama fit in memory but had a 2,048-token context window, below the 4,000-token minimum required by OpenClaw
- OpenClaw sent ~53k tokens per turn on its free Groq tier, which caps at 6k TPM, not viable
- Solution: call Groq directly from Python, keeping orchestration local and inference remote

The result is a hybrid architecture: scheduling, fetching, and serving all run on the Pi; only LLM inference is remote.

---

## Lessons learned

- Agentic frameworks have real token overhead. For a three-step daily pipeline, a plain Python script is the right tool.
- Hardware constraints force explicit trade-offs you would never encounter on a cloud machine.
- Local AI is a spectrum. Fully local is harder than it sounds on constrained hardware; hybrid is a reasonable middle ground.

---

## What's next

- Make OpenClaw work properly as the orchestrator with a paid API tier that can handle its system prompt overhead
- Add keyword filtering (risk, portfolio, forecasting, regulation)
- Build a weekly summary across 7 days of digests
- Try a Pi 5 (8GB RAM) to revisit running the model fully locally

---

Personal project. All views my own, independent of my employer.
