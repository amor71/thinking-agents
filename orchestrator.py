#!/usr/bin/env python3
"""
🧠 Thinking Agents — Multi-Model Orchestrator
Runs 4 thinking threads in parallel on different models,
then aggregates results into subconscious.json.

Thread → Model mapping:
  Watcher   → Groq (Llama 3.3 70B) — fast, observational
  Librarian → Gemini 2.0 Flash — pattern recognition
  Oracle    → GLM-5 — deep reasoning, different worldview
  Dreamer   → GPT-4o-mini — creative, cost-effective
"""

import json
import os
import sys
import time
import signal
import socket
import subprocess
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Set a global default socket timeout as a safety net
socket.setdefaulttimeout(120)

# ─── Paths ────────────────────────────────────────────────────
BASE = Path(__file__).parent
PROMPTS = BASE / "prompts"
SUBCONSCIOUS = BASE / "subconscious.json"

# ─── API Keys ─────────────────────────────────────────────────
def load_env(path):
    """Load KEY=VALUE from env file."""
    env = {}
    p = Path(path).expanduser()
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

GROQ_KEY = load_env("~/.config/groq/credentials.env").get("GROQ_API_KEY", "")
GEMINI_KEY = load_env("~/.config/google/gemini.env").get("GEMINI_API_KEY", "")
GLM_KEY = load_env("~/.config/zhipu/credentials.env").get("ZHIPU_API_KEY", "")
OPENAI_KEY = load_env("~/.config/openai/credentials.env").get("OPENAI_API_KEY", "")

# ─── Model Config ─────────────────────────────────────────────
THREADS = {
    "watcher": {
        "provider": "groq",
        "model": "llama-3.3-70b-versatile",
        "prompt_file": PROMPTS / "watcher.md",
    },
    "librarian": {
        "provider": "gemini",
        "model": "gemini-2.0-flash",
        "prompt_file": PROMPTS / "librarian.md",
    },
    "oracle": {
        "provider": "glm",
        "model": "glm-5",
        "prompt_file": PROMPTS / "oracle.md",
    },
    "dreamer": {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "prompt_file": PROMPTS / "dreamer.md",
    },
}

# ─── Gather Context ───────────────────────────────────────────
def get_system_health():
    """Quick system health check."""
    try:
        disk = subprocess.check_output(["df", "-h", "/"], timeout=5).decode().strip().split("\n")[-1]
        mem = subprocess.check_output(["free", "-h"], timeout=5).decode().strip().split("\n")[1]
        uptime = subprocess.check_output(["uptime", "-p"], timeout=5).decode().strip()
        return f"Disk: {disk}\nMemory: {mem}\nUptime: {uptime}"
    except Exception as e:
        return f"Health check failed: {e}"

BRAVE_KEY = load_env("~/.config/brave/credentials.env").get("BRAVE_API_KEY", "")

def get_news_headlines():
    """Fetch a few news headlines for external stimulation. Rotates topics."""
    if not BRAVE_KEY:
        return "(no Brave API key — skipping news)"
    
    # Rotate topics based on tick count
    topics = [
        "top news today",
        "AI technology news today",
        "financial markets news",
        "science breakthroughs this week",
        "world news today",
        "startup funding news",
        "open source software news",
        "interesting discoveries this week",
    ]
    
    try:
        tick = load_subconscious().get("tick_count", 0)
        topic = topics[tick % len(topics)]
        
        params = urllib.parse.urlencode({"q": topic, "count": 5, "freshness": "pd"})
        url = f"https://api.search.brave.com/res/v1/web/search?{params}"
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "X-Subscription-Token": BRAVE_KEY,
            "User-Agent": "thinking-agents/1.0",
        })
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        
        results = []
        for item in data.get("web", {}).get("results", [])[:5]:
            title = item.get("title", "")
            desc = item.get("description", "")[:150]
            results.append(f"• {title}: {desc}")
        
        return f"[News — {topic}]\n" + "\n".join(results) if results else "(no news results)"
    except Exception as e:
        return f"(news fetch failed: {e})"

def get_recent_memory():
    """Read today's and yesterday's memory files."""
    mem_dir = Path.home() / ".openclaw/workspace/memory"
    now = datetime.now(timezone(timedelta(hours=-5)))
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    
    result = ""
    for day in [yesterday, today]:
        f = mem_dir / f"{day}.md"
        if f.exists():
            content = f.read_text()[:2000]  # Cap at 2000 chars
            result += f"\n--- {day} ---\n{content}\n"
    return result or "(no recent memory files)"

def get_recent_context():
    """Read Rye's curated context file for conversation awareness."""
    ctx_file = BASE / "recent-context.md"
    if ctx_file.exists():
        return ctx_file.read_text()[:3000]
    return "(no recent context)"

def load_subconscious():
    """Load current subconscious state."""
    if SUBCONSCIOUS.exists():
        try:
            return json.loads(SUBCONSCIOUS.read_text())
        except json.JSONDecodeError:
            return {"version": 1, "tick_count": 0, "active_threads": [], "patterns": [], "hunches": []}
    return {"version": 1, "tick_count": 0, "active_threads": [], "patterns": [], "hunches": []}

def get_thread_memory(thread_name):
    """Read a thread's persistent memory file."""
    mem_file = BASE / "memory" / f"{thread_name}.md"
    if mem_file.exists():
        return mem_file.read_text()[-4000:]  # Last 4000 chars to keep context window manageable
    return "(no memory yet)"

def append_thread_memory(thread_name, update):
    """Append to a thread's persistent memory file, with dedup."""
    if not update:
        return
    update_stripped = update.strip()
    if not update_stripped:
        return
    mem_file = BASE / "memory" / f"{thread_name}.md"
    # Dedup: skip if last entry is >80% similar (simple check)
    if mem_file.exists():
        existing = mem_file.read_text()
        # Get last entry (after last ###)
        parts = existing.split("\n### ")
        if len(parts) > 1:
            last_entry = parts[-1].split("\n", 1)[-1].strip() if "\n" in parts[-1] else ""
            if last_entry and len(last_entry) > 20:
                # Simple similarity: check if >80% of words overlap
                last_words = set(last_entry.lower().split())
                new_words = set(update_stripped.lower().split())
                if last_words and new_words:
                    overlap = len(last_words & new_words) / max(len(last_words), len(new_words))
                    if overlap > 0.8:
                        return  # Skip duplicate
    now = datetime.now(timezone(timedelta(hours=-5))).strftime("%Y-%m-%d %H:%M")
    with open(mem_file, "a") as f:
        f.write(f"\n### {now}\n{update_stripped}\n")
    # Trim if over 20KB (keep last 16KB)
    if mem_file.stat().st_size > 20000:
        content = mem_file.read_text()
        mem_file.write_text(content[-16000:])

def get_shared_memory():
    """Read the shared cross-pollination memory."""
    shared_file = BASE / "memory" / "shared.md"
    if shared_file.exists():
        return shared_file.read_text()[-3000:]
    return "(no shared memory yet)"

def append_shared_memory(thread_name, update):
    """Append to the shared cross-pollination memory."""
    if not update:
        return
    shared_file = BASE / "memory" / "shared.md"
    now = datetime.now(timezone(timedelta(hours=-5))).strftime("%Y-%m-%d %H:%M")
    with open(shared_file, "a") as f:
        f.write(f"\n### {now} ({thread_name})\n{update.strip()}\n")
    if shared_file.stat().st_size > 20000:
        content = shared_file.read_text()
        shared_file.write_text(content[-16000:])

def build_prompt(thread_name, prompt_template, subconscious, context):
    """Build the full prompt for a thread."""
    sub_json = json.dumps(subconscious, indent=2)
    thread_memory = get_thread_memory(thread_name)
    shared_memory = get_shared_memory()
    
    prompt = prompt_template
    prompt = prompt.replace("{{SUBCONSCIOUS}}", sub_json)
    prompt = prompt.replace("{{THREAD_MEMORY}}", thread_memory)
    prompt = prompt.replace("{{CONTEXT}}", context)
    
    # Append shared memory for cross-pollination
    prompt += f"\n\n## Shared Memory (all threads + Rye can read/write)\n```\n{shared_memory}\n```"
    prompt += "\n\nIf you have something other threads should see, include a `shared_memory_update` field in your JSON output."
    
    return prompt

# ─── API Calls ────────────────────────────────────────────────
def call_openai_compatible(url, key, model, prompt, max_tokens=500, timeout=30):
    """Call OpenAI-compatible API (OpenAI, Groq)."""
    data = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a cognitive thread in a thinking agent's mind. Respond with ONLY valid JSON as specified in your instructions."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }).encode()
    
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "thinking-agents/1.0",
    })
    
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        result = json.loads(resp.read())
        return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500]
        raise Exception(f"HTTP {e.code}: {body}")

def call_gemini(key, model, prompt, max_tokens=500, timeout=30):
    """Call Gemini API."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    data = json.dumps({
        "contents": [{"parts": [{"text": f"You are a cognitive thread in a thinking agent's mind. Respond with ONLY valid JSON as specified in your instructions.\n\n{prompt}"}]}],
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.7}
    }).encode()
    
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "User-Agent": "thinking-agents/1.0"})
    resp = urllib.request.urlopen(req, timeout=timeout)
    result = json.loads(resp.read())
    return result["candidates"][0]["content"]["parts"][0]["text"]

def call_glm(key, model, prompt, max_tokens=1000, timeout=120):
    """Call Z.AI GLM API (reasoning model, needs more tokens)."""
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    data = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a cognitive thread in a thinking agent's mind. Respond with ONLY valid JSON as specified in your instructions."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }).encode()
    
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "thinking-agents/1.0",
    })
    
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        result = json.loads(resp.read())
        return result["choices"][0]["message"]["content"]
    except (urllib.error.HTTPError, urllib.error.URLError, socket.timeout, TimeoutError, OSError) as e:
        raise Exception(f"GLM API error: {e}")

def run_thread(thread_name, config, prompt):
    """Run a single thinking thread on its assigned model."""
    provider = config["provider"]
    model = config["model"]
    
    try:
        if provider == "groq":
            raw = call_openai_compatible(
                "https://api.groq.com/openai/v1/chat/completions",
                GROQ_KEY, model, prompt
            )
        elif provider == "openai":
            raw = call_openai_compatible(
                "https://api.openai.com/v1/chat/completions",
                OPENAI_KEY, model, prompt
            )
        elif provider == "gemini":
            raw = call_gemini(GEMINI_KEY, model, prompt)
        elif provider == "glm":
            raw = call_glm(GLM_KEY, model, prompt)
        else:
            return {"error": f"Unknown provider: {provider}"}
        
        # Try to parse JSON from response (may have markdown fences)
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
            raw = raw.strip()
        
        return json.loads(raw)
    
    except json.JSONDecodeError:
        return {"findings": [], "escalate": False, "raw_response": raw[:500]}
    except Exception as e:
        return {"error": str(e), "findings": [], "escalate": False}

# ─── Aggregator ───────────────────────────────────────────────
def aggregate(subconscious, thread_results):
    """Merge thread results into subconscious state."""
    now = datetime.now(timezone(timedelta(hours=-5))).isoformat()
    
    # Init thread_state if missing
    if "thread_state" not in subconscious:
        subconscious["thread_state"] = {}
    
    # Decay existing entries
    for category in ["active_threads", "patterns", "hunches", "insights"]:
        entries = subconscious.get(category, [])
        subconscious[category] = [e for e in entries if e.get("strength", 1) > 1]
        for e in subconscious[category]:
            e["strength"] = max(0, e.get("strength", 1) - 1)
    
    escalations = []
    all_focus_hints = {}
    
    for thread_name, result in thread_results.items():
        findings = result.get("findings", [])
        
        # Update thread state
        subconscious["thread_state"][thread_name] = {
            "last_findings": [f.get("summary", "")[:80] for f in findings[:3]],
            "novelty_pressure": min(10, subconscious.get("thread_state", {}).get(thread_name, {}).get("novelty_pressure", 0) + 1) if not findings else 0,
            "last_tick": now,
            "model": THREADS[thread_name]["model"],
            "provider": THREADS[thread_name]["provider"],
        }
        
        # Collect focus hints
        if result.get("suggested_focus"):
            all_focus_hints[thread_name] = result["suggested_focus"]
        
        # Check escalation
        if result.get("escalate"):
            escalations.append({
                "thread": thread_name,
                "reason": result.get("escalate_reason", "Unknown"),
                "timestamp": now,
            })
        
        # Process findings
        for finding in findings:
            importance = finding.get("importance", 0)
            if importance < 3:
                continue
            
            # Check for reinforcement
            reinforce_ids = finding.get("reinforce", []) + finding.get("related_threads", [])
            reinforced = False
            for category in ["active_threads", "patterns", "hunches", "insights"]:
                for entry in subconscious.get(category, []):
                    if entry.get("id") in reinforce_ids or (
                        finding.get("summary", "").lower()[:30] in entry.get("summary", "").lower()
                    ):
                        entry["strength"] = min(10, entry.get("strength", 1) + 2)
                        entry["last_seen"] = now
                        reinforced = True
            
            if not reinforced:
                # Add new entry
                new_entry = {
                    "id": f"{thread_name[:2]}-{finding.get('type', 'obs')[:8]}-{int(time.time()) % 10000}",
                    "summary": finding.get("summary", "")[:100],
                    "strength": 3,
                    "added": now,
                    "last_seen": now,
                    "source": thread_name,
                }
                
                ftype = finding.get("type", "observation")
                if ftype in ("idea", "connection", "question", "challenge", "delight"):
                    if importance >= 6:
                        subconscious.setdefault("insights", []).append(new_entry)
                    else:
                        subconscious.setdefault("hunches", []).append(new_entry)
                elif ftype in ("pattern", "connection"):
                    subconscious.setdefault("patterns", []).append(new_entry)
                else:
                    subconscious.setdefault("active_threads", []).append(new_entry)
    
    # Distribute focus hints (each thread gets hints from others)
    for thread_name in THREADS:
        hints = [f"{k}: {v}" for k, v in all_focus_hints.items() if k != thread_name]
        if hints:
            subconscious["thread_state"].setdefault(thread_name, {})["focus_hint"] = "; ".join(hints[:3])
    
    # Prune
    limits = {"active_threads": 5, "patterns": 5, "hunches": 5, "insights": 3}
    for category, limit in limits.items():
        entries = subconscious.get(category, [])
        if len(entries) > limit:
            entries.sort(key=lambda e: e.get("strength", 0), reverse=True)
            subconscious[category] = entries[:limit]
    
    # Update metadata
    subconscious["last_tick"] = now
    subconscious["tick_count"] = subconscious.get("tick_count", 0) + 1
    
    # Handle escalations with cooldown (max 1 per hour)
    if escalations:
        last_escalation = subconscious.get("last_escalation_time", "")
        now_dt = datetime.now(timezone(timedelta(hours=-5)))
        cooldown_ok = True
        if last_escalation:
            try:
                last_dt = datetime.fromisoformat(last_escalation)
                if (now_dt - last_dt).total_seconds() < 3600:  # 1 hour cooldown
                    cooldown_ok = False
            except (ValueError, TypeError):
                pass
        
        if cooldown_ok:
            subconscious.setdefault("escalation_history", []).extend(escalations)
            subconscious["escalation_history"] = subconscious["escalation_history"][-10:]
            subconscious["last_escalation_time"] = now
        else:
            # Suppress — too soon since last escalation
            escalations = []
    
    return subconscious, escalations

# ─── Main ─────────────────────────────────────────────────────
def main():
    start = time.time()
    
    # Load state
    subconscious = load_subconscious()
    
    # Gather context
    health = get_system_health()
    memory = get_recent_memory()
    news = get_news_headlines()
    recent_ctx = get_recent_context()
    context = f"System Health:\n{health}\n\nRecent Memory:\n{memory}\n\nRecent Conversation Context (from Rye):\n{recent_ctx}\n\nExternal World:\n{news}"
    
    # Determine which threads to run based on time of day
    now_est = datetime.now(timezone(timedelta(hours=-5)))
    hour = now_est.hour
    is_night = hour >= 23 or hour < 8
    
    tick = subconscious.get("tick_count", 0)
    active_threads = dict(THREADS)
    if is_night:
        # Night mode: dreamers > workers. Skip watcher & librarian every other tick.
        if tick % 2 == 0:
            active_threads = {k: v for k, v in THREADS.items() if k in ("dreamer", "oracle")}
        # Oracle thinks deep at night too — good time for reflection
    else:
        # Daytime: run Watcher every 3rd tick to stay within Groq free tier (100K tokens/day)
        if tick % 3 != 0 and "watcher" in active_threads:
            del active_threads["watcher"]
    
    # Build prompts
    prompts = {}
    for name, config in active_threads.items():
        template = config["prompt_file"].read_text()
        prompts[name] = build_prompt(name, template, subconscious, context)
    
    # Run threads in parallel
    results = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(run_thread, name, config, prompts[name]): name
            for name, config in active_threads.items()
        }
        for future in as_completed(futures, timeout=150):
            name = futures[future]
            try:
                results[name] = future.result()
            except Exception as e:
                results[name] = {"error": str(e), "findings": [], "escalate": False}
    
    # Aggregate
    updated, escalations = aggregate(subconscious, results)
    
    # Write thread memory updates
    for name, result in results.items():
        mem_update = result.get("memory_update")
        if mem_update:
            append_thread_memory(name, mem_update)
        shared_update = result.get("shared_memory_update")
        if shared_update:
            append_shared_memory(name, shared_update)
    
    # Write
    SUBCONSCIOUS.write_text(json.dumps(updated, indent=2))
    
    elapsed = time.time() - start
    
    # Report
    report = {
        "tick": updated["tick_count"],
        "elapsed_seconds": round(elapsed, 1),
        "threads": {},
        "escalations": len(escalations),
    }
    for name in THREADS:
        r = results.get(name, {})
        report["threads"][name] = {
            "model": THREADS[name]["model"],
            "provider": THREADS[name]["provider"],
            "findings": len(r.get("findings", [])),
            "error": r.get("error"),
            "escalate": r.get("escalate", False),
        }
    
    print(json.dumps(report, indent=2))
    
    # If escalation, write to file for Rye to pick up on heartbeat
    if escalations:
        msg = "🚨 Thinking Clock Escalation:\n" + "\n".join(
            f"• {e['thread']}: {e['reason']}" for e in escalations
        )
        print(f"\n{msg}")
        escalation_file = SCRIPT_DIR / "escalations.jsonl"
        try:
            with open(escalation_file, "a") as f:
                f.write(json.dumps({
                    "time": datetime.now().isoformat(),
                    "escalations": escalations,
                    "tick": tick
                }) + "\n")
            print("  → Written to escalations.jsonl")
        except Exception as we:
            print(f"  → Failed to write escalation: {we}")

if __name__ == "__main__":
    main()
