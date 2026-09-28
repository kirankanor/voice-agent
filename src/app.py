"""FastAPI backend for Voice Agent Workbench."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel

from src.projects import ProjectManager
from src.registry import ComponentRegistry, register_defaults
from src.experiments import ExperimentManager
from src.benchmarks import BenchmarkStore
from src.agent_config import AgentConfig
from src.decisions import DecisionManager
from src.costs import CostCalculator
from src.codegen import generate_project
from src.models.types import ProviderCategory

app = FastAPI(title="Voice Agent Workbench")
DATA_DIR = Path("data")


def get_managers():
    return {
        "projects": ProjectManager(DATA_DIR),
        "registry": ComponentRegistry(DATA_DIR),
        "experiments": ExperimentManager(DATA_DIR),
        "benchmarks": BenchmarkStore(DATA_DIR),
        "agents": AgentConfig(DATA_DIR),
        "decisions": DecisionManager(DATA_DIR),
        "costs": CostCalculator(DATA_DIR),
    }


class ProjectCreate(BaseModel):
    id: str
    name: str
    languages: list[str] = []
    latency_target_ms: int | None = None
    budget: str | None = None
    use_case: str = ""


class ExperimentCreate(BaseModel):
    id: str
    project_id: str
    experiment_type: str
    providers: list[str] = []


class AgentConfigCreate(BaseModel):
    id: str
    name: str
    languages: list[str] = ["en"]
    stt_provider: str | None = None
    tts_provider: str | None = None
    llm_provider: str | None = None
    vad_provider: str | None = None


class DecisionCreate(BaseModel):
    id: str
    project_id: str
    requirement: str
    candidates: list[str] = []
    decision: str = ""
    evidence: str = ""
    trade_offs: str = ""


class CostEstimate(BaseModel):
    stt_cost_per_min: float = 0.0043
    tts_cost_per_char: float = 0.00003
    llm_cost_per_1k_tokens: float = 0.002
    conversation_duration_min: float = 5.0
    avg_turns: int = 10
    avg_chars_per_response: int = 800
    avg_response_tokens: int = 200


class PlaygroundConfig(BaseModel):
    name: str = "voice-agent"
    languages: list[str] = ["en"]
    stt: str = "deepgram"
    tts: str = "elevenlabs"
    llm: str = "openai"
    vad: str = "silero"
    use_case: str = ""
    latency_target_ms: int = 800
    budget_per_min: float = 0.10


@app.get("/")
async def index():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/api/dashboard")
async def dashboard():
    m = get_managers()
    return {
        "projects": len(m["projects"].list_all()),
        "providers": len(m["registry"].list_all()),
        "experiments": len(m["experiments"].list_all()),
        "benchmarks": len(m["benchmarks"].list_all()),
        "agents": len(m["agents"].list_all()),
        "decisions": len(m["decisions"].list_all()),
    }


@app.get("/api/projects")
async def list_projects():
    m = get_managers()
    return [{"id": p.id, "name": p.name, "languages": p.languages,
             "status": p.status, "use_case": p.use_case} for p in m["projects"].list_all()]


@app.post("/api/projects")
async def create_project(data: ProjectCreate):
    m = get_managers()
    p = m["projects"].create(data.id, data.name, data.languages,
                             data.latency_target_ms, data.budget, data.use_case)
    return {"id": p.id, "name": p.name}


@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    m = get_managers()
    if m["projects"].delete(project_id):
        return {"ok": True}
    raise HTTPException(404, "Project not found")


@app.get("/api/providers")
async def list_providers():
    m = get_managers()
    return [{"id": p.id, "name": p.name, "category": p.category.value,
             "capabilities": p.capabilities, "economics": p.economics,
             "performance": p.performance} for p in m["registry"].list_all()]


@app.post("/api/providers/init")
async def init_providers():
    m = get_managers()
    register_defaults(m["registry"])
    return {"ok": True, "count": 4}


@app.get("/api/experiments")
async def list_experiments():
    m = get_managers()
    return [{"id": e.id, "project_id": e.project_id, "type": e.experiment_type,
             "providers": e.providers, "status": e.status} for e in m["experiments"].list_all()]


@app.post("/api/experiments")
async def create_experiment(data: ExperimentCreate):
    m = get_managers()
    e = m["experiments"].create(data.id, data.project_id, data.experiment_type, data.providers)
    return {"id": e.id}


@app.get("/api/benchmarks")
async def list_benchmarks():
    m = get_managers()
    return [{"id": b.id, "provider": b.provider, "component": b.component,
             "latency_ms": b.latency_ms, "quality": b.quality,
             "cost": b.cost} for b in m["benchmarks"].list_all()]


@app.get("/api/agents")
async def list_agents():
    m = get_managers()
    return m["agents"].list_all()


@app.post("/api/agents")
async def create_agent(data: AgentConfigCreate):
    m = get_managers()
    m["agents"].create(data.id, data.name, data.languages,
                       data.stt_provider, data.tts_provider,
                       data.llm_provider, data.vad_provider)
    return {"id": data.id}


@app.get("/api/decisions")
async def list_decisions():
    m = get_managers()
    return [{"id": d.id, "project_id": d.project_id, "requirement": d.requirement,
             "decision": d.decision, "candidates": d.candidates,
             "trade_offs": d.trade_offs} for d in m["decisions"].list_all()]


@app.post("/api/decisions")
async def create_decision(data: DecisionCreate):
    m = get_managers()
    m["decisions"].create(data.id, data.project_id, data.requirement,
                          data.candidates, decision=data.decision,
                          evidence=data.evidence, trade_offs=data.trade_offs)
    return {"id": data.id}


@app.post("/api/costs/estimate")
async def estimate_costs(data: CostEstimate):
    m = get_managers()
    return m["costs"].estimate(
        data.stt_cost_per_min, data.tts_cost_per_char,
        data.llm_cost_per_1k_tokens, data.avg_response_tokens,
        data.avg_chars_per_response, data.conversation_duration_min,
        data.avg_turns,
    )


# ── Playground ──────────────────────────────────────────────

@app.get("/playground")
async def playground():
    return FileResponse(Path(__file__).parent / "static" / "playground.html")


@app.get("/api/playground/providers")
async def playground_providers():
    """Provider comparison matrix for playground."""
    return {
        "stt": [
            {"id": "deepgram", "name": "Deepgram", "latency_ms": 320, "cost_per_min": 0.0043,
             "languages": ["en", "hi", "es", "fr", "de", "ja", "ko", "zh"], "streaming": True},
            {"id": "whisper", "name": "Whisper (local)", "latency_ms": 800, "cost_per_min": 0,
             "languages": ["en", "hi", "es", "fr", "de", "ja", "ko", "zh"], "streaming": False},
            {"id": "assemblyai", "name": "AssemblyAI", "latency_ms": 400, "cost_per_min": 0.0057,
             "languages": ["en", "hi", "es", "fr"], "streaming": True},
        ],
        "tts": [
            {"id": "edge-tts", "name": "Edge TTS (Free)", "latency_ms": 250, "cost_per_char": 0,
             "voices": ["en-US-Neural", "hi-IN-Neural", "es-ES-Neural"], "streaming": True, "free": True},
            {"id": "elevenlabs", "name": "ElevenLabs", "latency_ms": 200, "cost_per_char": 0.00003,
             "voices": ["Rachel", "Drew", "Clyde"], "streaming": True},
            {"id": "cartesia", "name": "Cartesia", "latency_ms": 150, "cost_per_char": 0.00001,
             "voices": ["default"], "streaming": True},
            {"id": "deepgram", "name": "Deepgram Aura", "latency_ms": 180, "cost_per_char": 0.000015,
             "voices": ["asteria", "luna"], "streaming": True},
        ],
        "llm": [
            {"id": "groq", "name": "Groq (Free Tier)", "model": "llama-3.1-8b-instant",
             "latency_ms": 80, "cost_per_1k": 0, "free": True,
             "context_window": 128000, "max_output": 8192},
            {"id": "openai", "name": "GPT-4o Mini", "latency_ms": 500, "cost_per_1k": 0.002,
             "function_calling": True},
            {"id": "anthropic", "name": "Claude 3 Haiku", "latency_ms": 400, "cost_per_1k": 0.00125,
             "function_calling": True},
        ],
        "vad": [
            {"id": "silero", "name": "Silero VAD", "latency_ms": 10, "cost": 0, "local": True},
            {"id": "webrtc", "name": "WebRTC VAD", "latency_ms": 5, "cost": 0, "local": True},
        ],
    }


@app.post("/api/playground/benchmark")
async def run_benchmark(data: PlaygroundConfig):
    """Simulate a benchmark for the selected provider combination."""
    providers = await playground_providers()
    stt = next((p for p in providers["stt"] if p["id"] == data.stt), providers["stt"][0])
    tts = next((p for p in providers["tts"] if p["id"] == data.tts), providers["tts"][0])
    llm = next((p for p in providers["llm"] if p["id"] == data.llm), providers["llm"][0])
    vad = next((p for p in providers["vad"] if p["id"] == data.vad), providers["vad"][0])

    # Simulated end-to-end latency
    e2e_latency = stt["latency_ms"] + llm["latency_ms"] + tts["latency_ms"]
    cost_per_min = stt.get("cost_per_min", 0) + tts.get("cost_per_char", 0) * 4000 + llm.get("cost_per_1k", 0) * 2

    meets_latency = e2e_latency <= data.latency_target_ms
    meets_budget = cost_per_min <= data.budget_per_min

    # Language support check
    langs_needed = set(data.languages)
    stt_langs = set(stt.get("languages", []))
    tts_ok = True  # Most TTS support en + a few others
    stt_supports = langs_needed.issubset(stt_langs)

    issues = []
    if not meets_latency:
        issues.append(f"Latency {e2e_latency}ms exceeds target {data.latency_target_ms}ms")
    if not meets_budget:
        issues.append(f"Cost ${cost_per_min:.4f}/min exceeds budget ${data.budget_per_min}/min")
    if not stt_supports:
        missing = langs_needed - stt_langs
        issues.append(f"STT missing languages: {', '.join(missing)}")

    return {
        "providers": {"stt": stt["name"], "tts": tts["name"], "llm": llm["name"], "vad": vad["name"]},
        "latency": {
            "stt_ms": stt["latency_ms"],
            "llm_ms": llm["latency_ms"],
            "tts_ms": tts["latency_ms"],
            "total_ms": e2e_latency,
            "target_ms": data.latency_target_ms,
            "meets_target": meets_latency,
        },
        "cost": {
            "stt": round(stt.get("cost_per_min", 0), 4),
            "tts": round(tts.get("cost_per_char", 0) * 4000, 4),
            "llm": round(llm.get("cost_per_1k", 0) * 2, 4),
            "total_per_min": round(cost_per_min, 4),
            "budget_per_min": data.budget_per_min,
            "meets_budget": meets_budget,
        },
        "languages": {
            "needed": list(data.languages),
            "stt_supported": stt.get("languages", []),
            "all_supported": stt_supports,
        },
        "issues": issues,
        "verdict": "PASS" if not issues else "FAIL",
    }


@app.post("/api/playground/download")
async def download_project(data: PlaygroundConfig):
    """Generate and download the voice agent project."""
    config = {
        "name": data.name,
        "stt": data.stt,
        "tts": data.tts,
        "llm": data.llm,
        "vad": data.vad,
        "languages": data.languages,
    }
    zip_bytes = generate_project(config, data.name)
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={data.name}.zip"},
    )
