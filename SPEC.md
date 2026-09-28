# SPEC — voice-agent-engineering-workbench

## Problem

Building voice agents for client projects requires repeatedly making the same architecture, provider, configuration, and deployment decisions. Each project restarts from scratch: which STT? which TTS? which LLM? what latency is acceptable? what does it cost? The bottleneck is not writing code — it is the repeated engineering decision-making across projects with no structured way to capture, reuse, or build on previous work.

## Users

- Solo user (you) — the only operator and consumer

## Functional requirements

- FR-001: Project Management — Create, list, view, and archive client projects. Each project captures: name, language requirements, latency targets, budget constraints, use case description, and status.
- FR-002: Component Registry — Register STT, TTS, LLM, and VAD providers with structured metadata: capabilities, performance characteristics, pricing, integration details, and constraints. Providers: Deepgram (STT), ElevenLabs (TTS), OpenAI (LLM), Silero (VAD).
- FR-003: Experiment Definitions — Define controlled comparisons between providers. Experiment types: STT comparison, TTS comparison, LLM comparison, prompt comparison, latency benchmark. Each experiment records: input dataset, configuration, provider versions, environment, and status.
- FR-004: Benchmark Results — Store summary metrics and raw evidence per benchmark: latency, quality, cost, failure rate, timestamp, and raw result location. Never store only the final score.
- FR-005: Agent Configuration — Declarative YAML-based agent configuration: language, STT provider, TTS provider, LLM provider, VAD provider, conversation settings, tools, and evaluation targets. Configuration is version-controlled.
- FR-006: Decision Records — Record architecture decisions with: requirement, candidates, constraints, experiment IDs, evidence, decision, trade-offs, rejected alternatives, and expected consequences.
- FR-007: Cost Calculator — Estimate per-conversation cost across STT + LLM + TTS + infrastructure. Calculate: cost/minute, cost/conversation, cost/successful task, cost/1000 conversations.

## Non-functional requirements

- NFR-001: CLI-Only Interface — All interaction through terminal commands. No web UI in V0.
- NFR-002: Local File-Based Storage — All data stored locally in structured files (YAML/JSON). No external database required.
- NFR-003: Python 3.11+ with uv — Project uses Python 3.11+, managed with uv for dependency resolution and virtual environments.
- NFR-004: Provider Abstraction Layer — Stable interfaces (Python Protocol classes) around provider SDKs. Business logic never depends directly on vendor SDKs. Enables provider switching, benchmarking, A/B experiments, and fallback without rewriting agent code.
- NFR-005: Version-Controlled Configurations — All agent configurations, experiment definitions, and decision records are committed to git. Reproducibility is a first-class concern.

## Constraints

- Python 3.11+ with uv for dependency management
- CLI-only interface (no web UI in V0)
- Local file-based storage (YAML/JSON, no external database)
- Provider APIs: Deepgram (STT), ElevenLabs (TTS), OpenAI (LLM), Silero (VAD)
- User must have API keys for paid providers
- Configuration and records must be version-controlled in git

## Non-goals

- NG-1: No telephony integration
- NG-2: No deployment engine
- NG-3: No multi-tenancy or SaaS features
- NG-4: No web UI
- NG-5: No conversation simulator
- NG-6: No institutional knowledge system
- NG-7: No automated provider fallback in production

## Acceptance criteria

- AC-001: Project CRUD — Can create a project with requirements, list all projects, view project details, and archive a project. Data persists across sessions.
- AC-002: Provider Registration — Can register a provider with structured metadata (capabilities, pricing, integration details). Can list providers filtered by category (STT/TTS/LLM/VAD).
- AC-003: Experiment Lifecycle — Can define an experiment (type, providers, configuration), mark it running/completed/failed, and store results. Experiments are linked to projects.
- AC-004: Benchmark Storage — Can store benchmark results with summary metrics and raw evidence path. Can retrieve benchmarks by provider, experiment, or project.
- AC-005: Agent Config Assembly — Can create a declarative agent configuration YAML file from component selections. Configuration validates against provider capabilities.
- AC-006: Decision Recording — Can record a decision with full provenance (candidates, evidence, trade-offs). Decisions link to experiments and projects.
- AC-007: Cost Estimation — Can calculate estimated cost per conversation given provider selections and usage parameters. Output includes per-component and total cost breakdown.

## Risks

- R1: Provider API rate limits may block concurrent experiments
- R2: Cost of running real benchmarks against paid providers
- R3: File-based storage may not scale beyond V0 if project grows
- R4: Provider SDKs may change APIs without notice

## Open questions

- Q1: Should V0 include a simple test dataset or rely on user-provided audio/text?
- Q2: How should experiment results be visualized in CLI (table, JSON, chart)?
- Q3: Should agent configurations be importable from existing projects?
- Q4: What is the minimum viable benchmark (latency only, or latency + quality)?
