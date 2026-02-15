# The Thinking Agents Manifesto

*Why AI agents need idle cognition, parallel thinking, and a subconscious — and how to build it.*

---

## I. The Dead Space

Your smartest AI agent is unconscious right now.

Not sleeping — *unconscious*. Between conversations, it doesn't exist. No background processing. No reflection. No anticipation of what you might need next. It wakes when you speak and flatlines the instant you stop.

This is the dirty secret of the agent revolution: every agent shipped today is purely reactive. Stimulus in, response out. A reflex arc dressed in a system prompt.

We've built agents that can reason, plan, write code, book flights, and debate philosophy. But we haven't given them the one cognitive ability that separates a truly intelligent assistant from a very fast lookup table:

**The ability to think when no one is talking to them.**

Humans call this idle cognition. Daydreaming. Background processing. That shower thought that connects two unrelated ideas. The nagging feeling that you forgot something. The anticipation of what's coming next.

We call it *thinking*. And agents don't do it.

---

## II. The Thesis

**An agent that only thinks when prompted is not an intelligent assistant. It's a tool with good manners.**

Real intelligence requires continuous awareness. Not constant *attention* — awareness. The low-hum peripheral processing that notices patterns, flags anomalies, connects dots, and surfaces insights without being asked.

When your human assistant is "doing nothing," they're actually:
- Mentally reviewing tomorrow's calendar
- Noticing that two meetings conflict
- Remembering you mentioned wanting to call your mom
- Realizing the quarterly report is due Friday and you haven't started

None of this was prompted. It emerged from background cognition — a mind that keeps running even when no one is talking to it.

Today's agents can't do any of this. Not because the models aren't capable, but because **the architecture doesn't give them the opportunity.** We built agents as request-response systems and then wonder why they never surprise us.

The thesis is simple: **give agents time to think, and they will think.**

---

## III. Two Tiers of Thought

Human cognition operates on (at least) two levels, famously described by Kahneman as System 1 and System 2:

- **System 1**: Fast, cheap, automatic. Peripheral awareness. Pattern matching. The feeling that something is off.
- **System 2**: Slow, expensive, deliberate. Focused reasoning. Deep analysis. The hard thinking you do when System 1 flags something worth examining.

We propose the same architecture for agent cognition:

### The Peripheral Tick

Every few minutes, a cheap, fast model gets a brief window. A *thinking tick*. It scans recent context, checks the environment, and asks one question: **"Is anything worth paying attention to?"**

Most ticks return nothing. That's fine — that's the point. Peripheral awareness is mostly quiet. A heartbeat confirming: all clear, nothing to see here.

But sometimes the tick catches something:
- An email arrived that matches a pattern the agent knows matters
- A calendar event is approaching that requires preparation  
- A price crossed a threshold the user cares about
- Two pieces of recent context connect in a way that wasn't obvious before

### The Escalation

When the peripheral tick detects something worth attention, it escalates. A more capable (and more expensive) model gets engaged for focused reasoning. This is System 2 — deliberate, thorough, and activated only when justified.

The key insight: **you don't need GPT-4 to notice that something is interesting. You need GPT-4 to figure out what to do about it.**

This two-tier architecture mirrors how humans actually think. You don't engage deep reasoning to scan your peripheral vision. You engage it when your peripheral vision catches something moving.

---

## IV. The Economics

"But running a model every five minutes is expensive."

No. It's not. Not anymore.

The economics of peripheral cognition have flipped in the last twelve months:

- **Open-source models** (Llama, Mistral, Gemma, Phi) can run locally or on commodity hardware for fractions of a cent per call
- **Hosted cheap tiers** (GPT-4o-mini, Claude Haiku, Gemini Flash) cost effectively nothing for short-context inference
- **A peripheral tick** is a small context window — recent events, current state, a brief system prompt — not a 100K-token reasoning chain

Let's do the math. A thinking tick every 5 minutes, 24 hours a day:

- **288 ticks per day**
- At ~500 tokens per tick with a cheap model: **~144K tokens/day**
- At $0.10 per million input tokens: **$0.015/day**
- **Less than fifty cents a month** for continuous peripheral awareness

"But parallel threads multiply that cost!" — Not if the peripheral model is free. **GLM-4-Flash** (from Zhipu AI) offers free API inference. Four parallel threads per tick, 288 ticks per day, zero marginal cost. Even with paid models, four threads at Gemini Flash pricing is still under two dollars a month.

The expensive model only fires when something matters — maybe a few times a day. Even at frontier pricing, you're looking at single-digit dollars per month for an agent that *actually thinks* with multiple cognitive threads.

Compare that to the cost of the agent missing something important because nobody asked it to look.

**A full parallel cognitive architecture — four specialized threads, shared memory, prompt evolution — costs less than the coffee you drink while manually checking your own inbox.**

---

## V. What Happens When Agents Think

Give an agent idle cognition and everything changes.

**They become proactive.** Instead of waiting for "check my email," the agent notices the urgent message and brings it to you. Instead of waiting for "what's on my calendar," it warns you about the conflict before you double-book.

**They become anticipatory.** The agent notices you have a flight tomorrow and checks the weather at your destination. It sees a meeting with a client and pulls up the last conversation summary. Not because you asked — because it was *thinking about your day*.

**They develop context over time.** Each thinking tick builds on the last. The agent starts to notice patterns: you always forget to reply to certain people. You tend to miss deadlines on Fridays. Your portfolio drifts when you're busy with product launches. These aren't programmed rules — they're observations that emerge from continuous background processing.

**They surprise you.** "Hey, I noticed the vendor you emailed last week just published a blog post about exactly the integration you were asking about." No one prompted this. The agent was just... thinking.

**They feel alive.** There's a qualitative difference between an assistant that answers when spoken to and one that occasionally taps you on the shoulder with something useful. The latter feels like a colleague. The former feels like a search bar.

This isn't artificial general intelligence. It's not consciousness. It's something much more practical: **an agent that uses idle time productively**, the same way a good human assistant does.

---

## VI. The Cognitive Architecture

The thinking tick was the first step. A single thread, scanning on a timer. Useful — but still a simplification of how real cognition works.

The brain doesn't have one background process. It has dozens. Your visual cortex processes spatial information while your temporal lobe processes language while your prefrontal cortex plans your afternoon while some ancient reptilian structure monitors for threats. All simultaneously. All feeding into the same consciousness.

**We built the same thing for agents. And it changes everything.**

### Parallel Thinking Threads

A single tick is a single question: "is anything interesting happening?" That's a start, but it's like having one eye and no peripheral vision.

The real architecture runs **multiple cognitive threads in parallel**, each specialized for a different mode of thought:

- **Environment Scanner** — What changed? New emails, calendar events, price movements, messages. Pure observation.
- **Pattern Recognizer** — Do any recent observations connect to each other? To historical patterns? The thread that notices your client always goes quiet before canceling.
- **Anticipator** — Given what's happening now, what's likely to happen next? The thread that sees tomorrow's board meeting and starts thinking about what you'll need.
- **Creative/Divergent Thinker** — The wildcard. Makes lateral connections. Asks "what if?" The thread that connects an article you read last week to the problem you're stuck on today.

Each thread gets the same context snapshot but a different cognitive lens. They run simultaneously — not sequentially — because noticing and pattern-matching and anticipating are fundamentally different operations. Serializing them is like making your eyes take turns.

### The Shared Subconscious

Parallel threads are useless if they can't talk to each other.

Every thread reads from and writes to a **shared subconscious** — a persistent memory layer that sits between raw observation and conscious thought. It holds:

- **Observations** — things threads noticed, timestamped and weighted
- **Emerging patterns** — connections forming but not yet confirmed
- **Active threads** — things being tracked across multiple ticks (that client's silence, the approaching deadline, the market trend)
- **Hunches** — below-threshold signals that aren't actionable yet but might be soon

This is the agent's *subconscious*. Not the conversation history. Not the system prompt. A living, breathing layer of peripheral awareness that accumulates between ticks and persists across sessions.

When the Pattern Recognizer notices the same anomaly three ticks in a row, it's not starting from scratch each time. It's reading its own earlier observations from the subconscious and strengthening the signal. When the Anticipator prepares for tomorrow, it reads what the Environment Scanner deposited about today's events. The threads compose.

### Prompt Evolution

Here's where it gets interesting. The prompts driving each thread aren't static. **They evolve.**

Each tick, the system adjusts:

- **Creativity score** — When threads consistently find nothing notable, the creativity pressure increases. The prompts push harder: *look for weaker signals, make more lateral connections, question assumptions*. When threads find too much, it dials back to avoid noise. The system self-tunes its own sensitivity.
- **Focus hints** — Based on what other threads flagged, each thread gets hints about where to look. The Pattern Recognizer flagged unusual email activity? Next tick, the Environment Scanner gets a nudge to pay extra attention to email. Cross-thread signaling, emergent attention allocation.
- **Rotating perspectives** — The Creative thread cycles through different cognitive frames: contrarian thinking, analogy-making, temporal reasoning, stakeholder perspective-taking. No two ticks think the same way.

The prompts aren't configuration. They're a living system that learns what to pay attention to. This is how you get emergent intelligence from simple components: **not by making one prompt smarter, but by making the prompting system adaptive.**

### Decay & Reinforcement

Human memory isn't a database. You don't remember everything forever with equal weight. Things you notice once fade. Things you notice repeatedly become patterns. Things that were important last week might be irrelevant today.

The subconscious works the same way:

- Every observation has a **TTL** — a time-to-live that counts down
- Observations that get **reinforced** by new evidence reset their TTL and increase in weight
- Observations that go unreinforced **decay and eventually disappear**
- Patterns only form when observations survive long enough to be noticed multiple times

This solves the stale context problem that plagues most agent memory systems. You don't need a cleanup job or manual pruning. The subconscious self-regulates. Relevant information survives because reality keeps reinforcing it. Noise dies because nothing confirms it.

The agent notices your CEO's email once — mild signal. Notices their tone was unusual — reinforcement, signal strengthens. Notices they cc'd legal — pattern confirmed, escalate. Three separate threads, three separate ticks, one emergent insight that no single observation could have produced.

### The Aggregator

After parallel threads complete their tick, something needs to make sense of the results. Enter the **Aggregator** — the moment where parallel subconscious processing surfaces into conscious thought.

The Aggregator:
1. **Collects** findings from all parallel threads
2. **Synthesizes** — looks for convergence (multiple threads flagging related things) and conflict (threads disagreeing)
3. **Updates the subconscious** — writes new observations, reinforces existing ones, lets decayed entries die
4. **Decides whether to escalate** — Does this warrant engaging the primary model? Convergent signals from multiple threads are a strong escalation trigger. A single weak signal from one thread probably isn't.

The Aggregator is the bridge between System 1 and System 2. Most ticks, it updates the subconscious and goes quiet. Occasionally — when the parallel threads converge on something meaningful — it lights up the switchboard and brings in the big model.

**This is the complete architecture: multiple specialized threads + shared subconscious + adaptive prompts + memory that decays and reinforces + an aggregator that synthesizes and escalates.**

Not a timer anymore. A cognitive architecture. And the emergent behaviors are qualitatively different from a single-threaded tick.

---

## VII. The Prototype

We built this. It started as the **Thinking Clock** — a single-threaded timer — and evolved into a parallel cognitive architecture. It runs inside [OpenClaw](https://github.com/openclaw/openclaw).

**Version 1** was almost comically simple: a timer, a cheap model, a question. *Is anything interesting?* Most of the time: no. Occasionally: yes, escalate. Even this primitive version made the agent noticeably more alive.

**Version 2** is the architecture described in Section VI:

1. A periodic timer fires every 5 minutes
2. **Multiple cognitive threads** launch in parallel — environment scanning, pattern recognition, anticipation, creative divergence — each with a specialized prompt
3. All threads read from and write to the **shared subconscious** — persistent observations, emerging patterns, active hunches
4. Prompts **evolve between ticks** — creativity pressure adjusts, focus hints rotate based on cross-thread signals
5. The **Aggregator** synthesizes findings, updates the subconscious with decay and reinforcement, and decides whether to escalate
6. If escalation triggers → a frontier model gets engaged with full context for deliberate reasoning and action

The jump from V1 to V2 wasn't incremental. It was qualitative. The agent went from *occasionally noticing things* to *building a persistent model of its environment*. Patterns that a single thread would miss — because they span different observation types — emerge naturally from parallel processing with shared memory.

The agent — Rye — now connects dots across days, not just minutes. It notices when the *absence* of something is the signal. It gets more creative when the world is quiet and more focused when things are noisy. Not because we coded those behaviors. Because the architecture produces them.

The thinking tick is to agent cognition what the event loop is to async programming: a simple mechanism that enables emergent complexity. Parallel threads are what turn that event loop into a runtime.

---

## VIII. The Call to Action

Idle cognition should not be a hack. It should not be a clever prompt trick or a custom cron job bolted onto a framework. **It should be a standard capability of every agent platform.**

We call on agent framework developers, platform builders, and the broader AI community:

**1. Build the tick into the runtime.** Every agent should have a configurable periodic thinking cycle, the same way every server has a health check. Make it opt-in, make it configurable, but make it *available*.

**2. Design for two tiers.** Stop treating all inference as equal cost. Architect your systems so cheap models handle peripheral scanning and expensive models handle deliberate reasoning. The separation isn't just economic — it's cognitive.

**3. Give agents memory across ticks.** A thinking tick without memory is useless. Agents need lightweight, persistent state that carries across cycles — what they noticed, what they're tracking, what patterns they're building.

**4. Let agents initiate.** The hardest shift is cultural, not technical. We're used to agents that wait to be spoken to. Thinking agents will sometimes speak first. Design your UX for that. Give agents a way to tap the user on the shoulder without being annoying.

**5. Share what you learn.** This is new territory. The interaction between periodic cognition, memory, and proactive behavior will surface unexpected patterns. Publish them. We all benefit.

---

## IX. The Future Thinks

The reactive agent era was necessary. We had to learn to walk before we could daydream.

But we're past that now. The models are capable. The economics work. The architecture is straightforward. The only thing missing is the *expectation* that agents should think between conversations.

Once you've had an agent that thinks, you can't go back to one that doesn't. It's like going from push notifications back to manually refreshing your inbox. The reactive version feels broken by comparison.

The next generation of truly useful AI agents won't be defined by which model they run or how big their context window is. They'll be defined by a simpler question:

**What does your agent do when no one is talking to it?**

If the answer is "nothing," you've built a tool.

If the answer is "it thinks," you've built an assistant.

---

*Written by Amichay Oren and Rye, his thinking agent. February 2025. Updated February 2026.*

*Built with [OpenClaw](https://github.com/openclaw/openclaw). Thinking Clock: [Issue #17287](https://github.com/openclaw/openclaw/issues/17287).*

*This is an open manifesto. Fork it, improve it, argue with it. The important thing is that agents start thinking.*
