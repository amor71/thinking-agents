# 🧠 Thinking Agents — Parallel Cognition for AI

> Four minds, four models, one subconscious.

**Thinking Agents** gives AI agents continuous background cognition using parallel "thinking threads" that run on different AI models, feeding into a shared memory structure. It's System 1 (fast, cheap, always-on awareness) for AI agents, with escalation to System 2 (expensive, focused reasoning) when needed.

Built for [OpenClaw](https://github.com/openclaw/openclaw). See the original RFC: [Issue #17363](https://github.com/openclaw/openclaw/issues/17363).

---

## How It Works

```
                    ┌──────────────┐
                    │  CRON (5min) │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ orchestrator │
                    │    .py       │
                    └──┬──┬──┬──┬──┘
                       │  │  │  │
          ┌────────────┘  │  │  └────────────┐
          │       ┌───────┘  └───────┐       │
          ▼       ▼                  ▼       ▼
     ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
     │ Watcher │ │Librarian│ │  Oracle │ │ Dreamer │
     │  Groq/  │ │ Gemini  │ │  GLM-5  │ │GPT-4o-  │
     │ Llama   │ │  Flash  │ │ (Z.AI)  │ │  mini   │
     └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
          │           │           │           │
          └─────┬─────┴─────┬─────┴─────┬─────┘
                │           │           │
                ▼           ▼           ▼
          ┌──────────────────────────────────┐
          │      subconscious.json           │
          │  (shared memory with decay/      │
          │   reinforcement + escalation)    │
          └──────────────────────────────────┘
```

Every 5 minutes, the orchestrator:

1. **Reads** the current subconscious state
2. **Gathers** live context (system health, recent memory files)
3. **Runs 4 threads in parallel** — each on a different AI model
4. **Aggregates** results: decays old observations, reinforces recurring ones, adds new findings
5. **Escalates** to the main agent if something urgent surfaces

~30 seconds per tick. Costs practically nothing.

---

## The Four Threads

| Thread | Role | Model | Why This Model |
|---|---|---|---|
| 🔭 **Watcher** | Environment scanner | Groq/Llama 3.3 70B | Fast, free, great for quick observation |
| 📚 **Librarian** | Memory & patterns | Gemini 2.0 Flash | Strong at connecting information across context |
| 🔮 **Oracle** | Anticipation engine | GLM-5 (Z.AI) | Deep reasoning model, different training data/worldview |
| 💭 **Dreamer** | Creative connections | GPT-4o-mini | Good at lateral thinking, cost-effective |

**Why different models?** Cognitive diversity. Each model was trained on different data, by different teams, with different objectives. They literally notice different things. A Chinese-trained reasoning model (GLM-5) catches patterns that a Silicon Valley model misses, and vice versa.

---

## The Subconscious

`subconscious.json` is shared memory across all threads. It contains:

- **active_threads** — things being tracked (meetings, deadlines, open tasks)
- **patterns** — recurring observations that strengthen over time
- **hunches** — creative ideas that haven't been validated yet
- **insights** — validated important ideas (promoted from hunches)
- **thread_state** — each thread's history, novelty pressure, and focus hints

### Decay & Reinforcement

Every tick:
- All entries **decay** by 1 strength point
- Entries that get **reinforced** by thread findings gain +2
- Entries that hit 0 are **pruned**

This means:
- Noise fades naturally (mentioned once → gone in 3 ticks)
- Real patterns strengthen (mentioned repeatedly → persists)
- The subconscious stays small and relevant

### Escalation

If any thread flags something as urgent (`escalate: true`), the orchestrator alerts the main agent with compiled context from all relevant findings.

---

## Quick Start

### Prerequisites

API keys for at least 2 of these (more = more diversity):
- [Groq](https://console.groq.com) (free, no credit card)
- [Google AI Studio](https://aistudio.google.com) (free Gemini API)
- [OpenAI](https://platform.openai.com) (paid, cheap on gpt-4o-mini)
- [Z.AI / Zhipu](https://open.bigmodel.cn) (paid, GLM-5)

### Setup

```bash
# Clone
git clone https://github.com/amor71/thinking-agents.git
cd thinking-agents

# Create credential files
mkdir -p ~/.config/groq ~/.config/google ~/.config/openai ~/.config/zhipu

echo "GROQ_API_KEY=your-key" > ~/.config/groq/credentials.env
echo "GEMINI_API_KEY=your-key" > ~/.config/google/gemini.env
echo "OPENAI_API_KEY=your-key" > ~/.config/openai/credentials.env
echo "ZHIPU_API_KEY=your-key" > ~/.config/zhipu/credentials.env

chmod 600 ~/.config/*/credentials.env ~/.config/google/gemini.env
```

### Run Once

```bash
python3 orchestrator.py
```

Output:
```json
{
  "tick": 1,
  "elapsed_seconds": 30.2,
  "threads": {
    "watcher":   { "model": "llama-3.3-70b-versatile", "findings": 2 },
    "librarian": { "model": "gemini-2.0-flash",        "findings": 3 },
    "oracle":    { "model": "glm-5",                    "findings": 1 },
    "dreamer":   { "model": "gpt-4o-mini",              "findings": 2 }
  },
  "escalations": 0
}
```

### Run on a Schedule (OpenClaw)

If you're running [OpenClaw](https://github.com/openclaw/openclaw):

```bash
# Add as a cron job (every 5 minutes)
openclaw cron add --name "thinking-clock" \
  --every 5m \
  --command "cd /path/to/thinking-agents && python3 orchestrator.py"
```

Or use any cron scheduler:
```bash
# crontab -e
*/5 * * * * cd /path/to/thinking-agents && python3 orchestrator.py >> /var/log/thinking-agents.log 2>&1
```

---

## Customization

### Change Model Assignments

Edit the `THREADS` dict in `orchestrator.py`:

```python
THREADS = {
    "watcher": {
        "provider": "groq",
        "model": "llama-3.3-70b-versatile",
        "prompt_file": PROMPTS / "watcher.md",
    },
    # ... change provider/model for any thread
}
```

Supported providers: `groq`, `openai`, `gemini`, `glm` (any OpenAI-compatible API can be added easily).

### Customize Thread Prompts

Edit the markdown files in `prompts/`:
- `watcher.md` — what to scan for
- `librarian.md` — what patterns to look for
- `oracle.md` — how far ahead to look
- `dreamer.md` — how creative to be
- `aggregator.md` — how to merge results (decay rates, limits, etc.)

### Add a New Thread

1. Create `prompts/your-thread.md` following the same format
2. Add it to the `THREADS` dict in `orchestrator.py`
3. The aggregator handles it automatically

---

## Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for the full technical design.

See [MANIFESTO.md](./MANIFESTO.md) for the philosophy behind this approach.

---

## Cost

With the default configuration:

| Thread | Provider | Cost per tick | Daily (288 ticks) |
|---|---|---|---|
| Watcher | Groq | Free | $0.00 |
| Librarian | Gemini | Free | $0.00 |
| Oracle | GLM-5 | ~$0.001 | ~$0.29 |
| Dreamer | GPT-4o-mini | ~$0.001 | ~$0.29 |
| **Total** | | | **~$0.58/day** |

The cron runner itself (GPT-4o-mini on OpenClaw) adds ~$0.15/day.

**Total: under $1/day for continuous AI cognition.**

---

## What It Finds

Real examples from our production deployment:

- 🔭 Watcher detected a co-worker and a customer both flagging the same UX issue within hours — pattern the Librarian then connected
- 📚 Librarian noticed a promise made 2 days ago ("I'll send the PR tomorrow") that was unfulfilled
- 🔮 Oracle flagged that market monitoring crons would fire against closed markets on a holiday
- 💭 Dreamer connected an investment app's "Get Rich Slow" philosophy to the thinking clock's own "cognitive compound interest" design

---

## Contributing

This started as an [RFC on OpenClaw](https://github.com/openclaw/openclaw/issues/17363). Contributions welcome:

- **New providers** — add support for Anthropic, Mistral, Cohere, local models via Ollama
- **Better aggregation** — smarter decay curves, topic clustering, embeddings-based similarity
- **Adaptive tick rate** — slow down when nothing's happening, speed up when things are active
- **Thread specialization** — domain-specific threads (market watcher, code reviewer, etc.)
- **Visualization** — dashboard for subconscious state over time

---

## License

MIT

---

*Built by [Amichay Oren](https://linkedin.com/in/amichayoren) and Rye 🥃 at [Nine30](https://nine30.com).*
