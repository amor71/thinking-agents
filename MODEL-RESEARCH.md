# Thinking Agents — Model Research

> Peripheral tier: cheap background thinking ticks (~500 token prompt, ~200 token response)
> Research date: 2026-02-15

## OpenClaw Provider Support Summary

| Model | Built-in Provider | Custom Config Needed |
|-------|------------------|---------------------|
| Kimi (Moonshot) | ❌ Not built-in | ✅ Yes — `models.providers` with OpenAI-compatible baseUrl |
| GLM (Zhipu/Z.AI) | ✅ **Built-in** (`zai`) | No — just set `ZAI_API_KEY` |
| Qwen (Alibaba) | ✅ **Built-in** (`qwen-portal` plugin) | No — OAuth device flow or DashScope API key |
| DeepSeek | ✅ Via **HuggingFace** or **OpenRouter** | Custom provider also works (OpenAI-compatible) |
| Mistral | ✅ **Built-in** (`mistral`) | No — just set `MISTRAL_API_KEY` |
| Ollama (local) | ✅ **Built-in** (`ollama`) | No — auto-detected at localhost:11434 |

---

## 1. Kimi (Moonshot AI)

- **Sign up**: https://platform.moonshot.ai — email registration, $5 bonus on first $5 recharge
- **API Endpoint**: `https://api.moonshot.ai/v1` (OpenAI-compatible)
- **Auth**: Bearer token (`MOONSHOT_API_KEY`)
- **OpenAI-compatible**: ✅ Yes — chat completions format
- **Models**: `kimi-k2.5`, `kimi-k2-0905-preview`, `kimi-k2-turbo-preview`, `kimi-k2-thinking`
- **Context**: up to 131K–256K tokens

### Pricing (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| Kimi K2 | $0.50–$0.60 | $2.40–$2.50 |
| Kimi K2 (cache hit) | $0.15 | $2.50 |

### Cost per thinking tick
- Input: 500 tokens × $0.60/1M = $0.0003
- Output: 200 tokens × $2.50/1M = $0.0005
- **Total: ~$0.0008/tick** ($0.80 per 1000 ticks)

### OpenClaw Config
```json5
{
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [{ id: "kimi-k2.5", name: "Kimi K2.5" }],
      },
    },
  },
}
```

---

## 2. GLM (Zhipu AI / Z.AI)

- **Sign up**: https://open.bigmodel.cn or https://z.ai
- **API Endpoint**: `https://open.bigmodel.cn/api/paas/v4` (or Z.AI endpoint)
- **Auth**: Bearer token (`ZAI_API_KEY`)
- **OpenAI-compatible**: ✅ Yes (also supports Anthropic format)
- **Context**: up to 200K tokens (GLM-4.7)

### Pricing (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| GLM-4.7 | $0.60 | $2.20 |
| GLM-4.7-FlashX | $0.07 | $0.40 |
| GLM-4.5-Air | $0.20 | $1.10 |
| **GLM-4.7-Flash** | **FREE** | **FREE** |
| **GLM-4.5-Flash** | **FREE** | **FREE** |

### Cost per thinking tick
- **GLM-4.7-Flash: $0.00/tick** (FREE!) ← Best for thinking ticks
- GLM-4.7-FlashX: ~$0.0001/tick
- GLM-4.7: ~$0.0007/tick

### OpenClaw Config (built-in)
```json5
{
  agents: { defaults: { model: { primary: "zai/glm-4.7-flash" } } },
}
// Just set env: ZAI_API_KEY
```

**⭐ RECOMMENDED for free thinking ticks — GLM-4.7-Flash and GLM-4.5-Flash are completely free.**

---

## 3. Qwen (Alibaba Cloud / DashScope)

- **Sign up**: https://dashscope.console.aliyun.com or https://qwen.ai/apiplatform
- **API Endpoint**: `https://dashscope.aliyuncs.com/compatible-mode/v1` (OpenAI-compatible)
- **Auth**: Bearer token (`DASHSCOPE_API_KEY`)
- **OpenAI-compatible**: ✅ Yes — explicit OpenAI Chat Completion compatibility
- **Also available via**: OpenClaw `qwen-portal` plugin (OAuth, free tier)

### Pricing (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| Qwen-Max | $0.38 | ~$1.20 |
| Qwen-Plus | ~$0.15 | ~$0.60 |
| Qwen-Turbo | ~$0.05 | ~$0.20 |
| Qwen3-32B (via Groq) | $0.29 | ~$0.39 |

### Cost per thinking tick
- Qwen-Turbo: ~$0.0001/tick
- Qwen-Plus: ~$0.0002/tick
- Qwen-Max: ~$0.0004/tick

### OpenClaw Config
Option A — Built-in plugin (free OAuth tier):
```bash
openclaw plugins enable qwen-portal-auth
openclaw models auth login --provider qwen-portal --set-default
# Model: qwen-portal/coder-model
```

Option B — DashScope API key (custom provider):
```json5
{
  models: {
    mode: "merge",
    providers: {
      qwen: {
        baseUrl: "https://dashscope.aliyuncs.com/compatible-mode/v1",
        apiKey: "${DASHSCOPE_API_KEY}",
        api: "openai-completions",
        models: [{ id: "qwen-turbo", name: "Qwen Turbo" }],
      },
    },
  },
}
```

---

## 4. DeepSeek (V3 / R1)

- **Sign up**: https://platform.deepseek.com
- **API Endpoint**: `https://api.deepseek.com/v1` (OpenAI-compatible)
- **Auth**: Bearer token (`DEEPSEEK_API_KEY`)
- **OpenAI-compatible**: ✅ Yes
- **Context**: 64K tokens

### Pricing (per 1M tokens)

| Model | Input (cache miss) | Input (cache hit) | Output |
|-------|-------------------|-------------------|--------|
| deepseek-chat (V3) | $0.27 | $0.07 | $1.10 |
| deepseek-reasoner (R1) | $0.55 | $0.14 | $2.19 |

### Cost per thinking tick
- DeepSeek V3: 500×$0.27/1M + 200×$1.10/1M = **~$0.0004/tick**
- DeepSeek V3 (cached): **~$0.0003/tick**
- DeepSeek R1: ~$0.0007/tick (plus CoT tokens add cost)

### OpenClaw Config
```json5
{
  models: {
    mode: "merge",
    providers: {
      deepseek: {
        baseUrl: "https://api.deepseek.com/v1",
        apiKey: "${DEEPSEEK_API_KEY}",
        api: "openai-completions",
        models: [
          { id: "deepseek-chat", name: "DeepSeek V3" },
          { id: "deepseek-reasoner", name: "DeepSeek R1" },
        ],
      },
    },
  },
}
```
Also available via: `huggingface/deepseek-ai/DeepSeek-R1` (built-in) or OpenRouter.

---

## 5. Mistral (Small / Large)

- **Sign up**: https://console.mistral.ai
- **API Endpoint**: `https://api.mistral.ai/v1` (OpenAI-compatible)
- **Auth**: Bearer token (`MISTRAL_API_KEY`)
- **OpenAI-compatible**: ✅ Yes
- **OpenClaw built-in**: ✅ Yes (`mistral` provider)

### Pricing (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| Mistral Small | $1.00 | $3.00 |
| Mistral Large | $2.00 | $6.00 |

### Cost per thinking tick
- Mistral Small: 500×$1.00/1M + 200×$3.00/1M = **~$0.0011/tick**
- Mistral Large: ~$0.0022/tick

### OpenClaw Config (built-in)
```bash
export MISTRAL_API_KEY="your-key"
# Model: mistral/mistral-small-latest or mistral/mistral-large-latest
```

---

## 6. Ollama (Local — Llama 3 8B)

- **Install**: https://ollama.ai → `curl -fsSL https://ollama.ai/install.sh | sh`
- **API Endpoint**: `http://127.0.0.1:11434/v1` (OpenAI-compatible)
- **Auth**: None
- **OpenAI-compatible**: ✅ Yes
- **Cost**: **$0.00** (local compute only — electricity + hardware)
- **RAM needed**: ~5GB for Llama 3 8B (quantized)

### Setup
```bash
ollama pull llama3:8b
# Or for newer: ollama pull llama3.3
```

### Cost per thinking tick
- **$0.00/tick** ← Zero marginal cost

### OpenClaw Config (built-in, auto-detected)
```json5
{
  agents: { defaults: { model: { primary: "ollama/llama3:8b" } } },
}
```

### Hardware Note
Our server (2-core Xeon, 8GB RAM) can run Llama 3 8B quantized (Q4_K_M) but expect ~2-5 tokens/sec. Adequate for background thinking ticks, not for interactive use.

---

## Comparison Matrix

| Provider | Cost/Tick | OpenAI Compat | Built-in OC | Quality | Latency |
|----------|-----------|---------------|-------------|---------|---------|
| **GLM-4.7-Flash** | **$0.000** | ✅ | ✅ | Medium | Fast |
| **Ollama Llama3 8B** | **$0.000** | ✅ | ✅ | Low-Med | Slow (local) |
| Qwen-Turbo | $0.0001 | ✅ | ✅ plugin | Medium | Fast |
| DeepSeek V3 | $0.0004 | ✅ | Via proxy | High | Fast |
| Kimi K2 | $0.0008 | ✅ | Custom | High | Medium |
| Mistral Small | $0.0011 | ✅ | ✅ | Medium | Fast |
| GLM-4.7 | $0.0007 | ✅ | ✅ | High | Fast |
| DeepSeek R1 | $0.0007+ | ✅ | Via proxy | Very High | Slow (CoT) |
| Mistral Large | $0.0022 | ✅ | ✅ | High | Fast |

## Recommendation

**Tier 1 — Free thinking ticks:**
1. **GLM-4.7-Flash / GLM-4.5-Flash** (Z.AI) — Free, cloud-hosted, built-in OpenClaw support. Best option.
2. **Ollama Llama 3 8B** — Free, local, but slow on our hardware.

**Tier 2 — Near-free (<$1/1000 ticks):**
3. **Qwen-Turbo** — $0.10/1000 ticks, OpenClaw plugin available
4. **DeepSeek V3** — $0.40/1000 ticks, excellent quality/price ratio

**Tier 3 — Budget ($1-2/1000 ticks):**
5. **Kimi K2** — $0.80/1000 ticks, strong reasoning
6. **Mistral Small** — $1.10/1000 ticks, built-in support

All providers use OpenAI-compatible API format. Integration with OpenClaw is straightforward for all of them.
