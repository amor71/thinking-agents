# Thinking Agents — Implementation Plan

> How to wire the Thinking Agents system into OpenClaw, step by step.

## Architecture Decision: One Cron → Four Sub-Agents

OpenClaw's cron system runs isolated agent sessions on a schedule. The cleanest approach:

**One cron job fires every 5 minutes → runs an orchestrator agent → orchestrator spawns 4 sub-agents in parallel → waits → runs aggregation → optionally escalates.**

Why not 4 separate cron jobs?
- No way to synchronize them (aggregator needs all 4 to finish first)
- Shared state writes would race condition
- One orchestrator keeps the pipeline clean

## Step-by-Step Implementation

### Phase 1: Foundation (Day 1)

#### 1.1 Set up Z.AI API key
```bash
# Get free API key from https://open.bigmodel.cn
openclaw env set ZAI_API_KEY=<key>
```

#### 1.2 Create the orchestrator script
The orchestrator is itself an agent session (can be the cron job's agent). It:

1. Reads `subconscious.json`
2. Assembles 4 prompts from templates
3. Spawns 4 sub-agents (parallel)
4. Collects results
5. Runs aggregation
6. Writes updated `subconscious.json`
7. Handles escalation if needed

#### 1.3 Create the cron job
```bash
openclaw cron add \
  --name "thinking-tick" \
  --schedule "*/5 * * * *" \
  --model "zai/glm-4.7-flash" \
  --isolated \
  --prompt "You are the Thinking Clock orchestrator. Read /home/rye/.openclaw/workspace/thinking-agents/ORCHESTRATOR.md and execute one thinking tick."
```

### Phase 2: Orchestrator Logic (Day 1-2)

#### 2.1 Write ORCHESTRATOR.md
This is the master prompt for the cron job agent. It instructs the agent to:

```markdown
# Thinking Clock — Orchestrator

## On each tick:

1. Read `thinking-agents/subconscious.json`
2. Read all 4 prompt templates from `thinking-agents/prompts/`
3. For each thread (watcher, librarian, oracle, dreamer):
   a. Replace {{SUBCONSCIOUS}} with current state
   b. Replace {{THREAD_HISTORY}} with thread_state[name].last_findings
   c. Replace {{FOCUS_HINT}} with thread_state[name].focus_hint or "No specific focus"
   d. Replace {{NOVELTY_PRESSURE}} with thread_state[name].novelty_pressure
   e. Spawn a sub-agent with that prompt + appropriate tool access
4. Wait for all 4 to complete
5. Read aggregator prompt, feed it (subconscious + 4 outputs)
6. Run aggregation (can be done inline, no sub-agent needed)
7. Write updated subconscious.json
8. If ESCALATE: send message to main session with context
```

#### 2.2 Tool Access per Thread

| Thread | Tools Needed |
|--------|-------------|
| Watcher | `exec` (himalaya, df, uptime), `read` (workspace files), `web_fetch` |
| Librarian | `read` (memory files, workspace) |
| Oracle | `read` (memory, calendar), `web_search` |
| Dreamer | `read` (workspace), `web_search` |
| Aggregator | `read`/`write` (subconscious.json only) |

### Phase 3: Sub-Agent Spawning (Day 2-3)

#### 3.1 Parallel execution pattern
The orchestrator agent uses OpenClaw's sub-agent capability. In the cron session:

```
# Spawn all 4 as sub-agents (they run in parallel)
# Each sub-agent gets:
#   - Its assembled prompt as the task
#   - Model: zai/glm-4.7-flash
#   - Relevant tool access
#   - Label for identification
```

Since sub-agents report back to the spawning agent, the orchestrator naturally collects all results before proceeding.

**Alternative if sub-agents aren't available**: Run 4 sequential calls to the model via tool use. Slower (4x serial) but simpler. At ~2-3 seconds per call on GLM-4.7-Flash, total tick time would be ~15 seconds. Acceptable.

#### 3.2 Fallback: Sequential mode
If parallel sub-agents prove complex to implement initially:
1. Run Watcher → get output
2. Run Librarian → get output  
3. Run Oracle → get output
4. Run Dreamer → get output
5. Run Aggregator with all 4 outputs
Total: ~15-20 seconds per tick. Fine for a 5-minute cycle.

### Phase 4: Aggregation (Day 3)

#### 4.1 Aggregator runs as inline logic
The orchestrator reads the aggregator prompt and executes it directly (or as one more model call). The aggregator:
- Receives: current subconscious + 4 thread outputs (as JSON)
- Returns: updated subconscious (as JSON)
- Orchestrator writes the result to `subconscious.json`

#### 4.2 Escalation handling
If aggregator returns `{"ESCALATE": true, ...}`:
- Orchestrator sends a message to the main agent session (or directly to the user's channel)
- Includes compiled context from the escalation
- Logs in escalation_history

### Phase 5: Wiring & Testing (Day 3-4)

#### 5.1 Manual test cycle
Before enabling the cron, run manually:
```bash
# Trigger one tick manually
openclaw cron trigger thinking-tick
```

Verify:
- [ ] subconscious.json updates correctly
- [ ] Thread outputs are valid JSON
- [ ] Decay works (run 3 ticks, watch entries fade)
- [ ] Reinforcement works (create conditions where the same thing is noticed twice)
- [ ] Novelty pressure increases for empty threads
- [ ] Focus hints rotate between threads

#### 5.2 Enable the cron
```bash
openclaw cron enable thinking-tick
```

#### 5.3 Monitor for the first day
- Watch subconscious.json evolve over a few hours
- Check cron logs for errors
- Verify token usage stays within free tier
- Ensure ticks complete within ~30 seconds

### Phase 6: Tuning (Week 1-2)

#### 6.1 Tune decay rate
- If subconscious empties too fast: reduce decay to -1 every 2 ticks
- If it fills with noise: increase decay or raise importance threshold from 3 to 4

#### 6.2 Tune novelty pressure
- If threads plateau: increase pressure increment
- If threads hallucinate: cap pressure lower (5 instead of 10)

#### 6.3 Tune escalation threshold
- Track false escalations in escalation_history
- Adjust thread prompts to be more/less conservative

#### 6.4 Consider model upgrades for specific threads
- If the Dreamer produces low-quality ideas: try Qwen-Turbo ($0.0001/tick)
- If the Watcher misses things: try DeepSeek V3 ($0.0004/tick)
- Keep Librarian and Oracle on free tier (pattern matching and calendar scanning are simpler tasks)

## Cost Projection

| Component | Calls/Day | Model | Daily Cost |
|-----------|-----------|-------|------------|
| 4 Threads × 288 ticks | 1,152 | GLM-4.7-Flash | **$0.00** |
| Aggregator × 288 ticks | 288 | GLM-4.7-Flash | **$0.00** |
| Escalations | ~2-5 | Claude Opus | **~$0.10-$0.25** |
| **Total** | | | **~$0.10-$0.25/day** |

## File Structure

```
thinking-agents/
├── MANIFESTO.md           # Philosophy
├── MODEL-RESEARCH.md      # Model options & pricing
├── ARCHITECTURE.md        # System design
├── IMPLEMENTATION.md      # This file
├── ORCHESTRATOR.md        # Master prompt for cron job (to be written)
├── subconscious.json      # Shared state (live, mutated each tick)
└── prompts/
    ├── watcher.md         # Thread 1 template
    ├── librarian.md       # Thread 2 template
    ├── oracle.md          # Thread 3 template
    ├── dreamer.md         # Thread 4 template
    └── aggregator.md      # Aggregation logic
```

## Next Steps After v1

1. **Visualization**: Build a simple dashboard showing subconscious state over time
2. **Thread specialization**: Let threads develop expertise based on what they keep finding
3. **User feedback loop**: When user acknowledges an escalation as useful, boost the pattern that triggered it
4. **Multi-agent**: Let other agents (Chai, Nori) contribute to the subconscious
5. **Publish**: Write up the architecture as a blog post / paper for the OpenClaw community

## Open Questions

1. **Can OpenClaw cron jobs spawn sub-agents?** If yes: parallel. If no: sequential fallback (still works).
2. **Should the Watcher have actual tool access in cron?** Need to test if isolated cron sessions can run himalaya, check system health, etc.
3. **5-minute interval — too frequent?** Start with 5 min, can relax to 10-15 if the subconscious evolves too slowly to justify the frequency.
4. **Should escalation go to the user or to the main agent session?** Probably main agent session first, let it decide whether to bother the user.
