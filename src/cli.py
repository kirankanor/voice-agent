"""CLI interface for the Voice Agent Engineering Workbench."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.projects import ProjectManager
from src.registry import ComponentRegistry, register_defaults
from src.experiments import ExperimentManager
from src.benchmarks import BenchmarkStore
from src.agent_config import AgentConfig
from src.decisions import DecisionManager
from src.costs import CostCalculator
from src.models.types import ProviderCategory


DATA_DIR = Path("data")


def get_managers():
    """Initialize all managers."""
    return {
        "projects": ProjectManager(DATA_DIR),
        "registry": ComponentRegistry(DATA_DIR),
        "experiments": ExperimentManager(DATA_DIR),
        "benchmarks": BenchmarkStore(DATA_DIR),
        "agents": AgentConfig(DATA_DIR),
        "decisions": DecisionManager(DATA_DIR),
        "costs": CostCalculator(DATA_DIR),
    }


def cmd_project(args, managers):
    """Handle project commands."""
    pm = managers["projects"]
    if args.project_action == "create":
        p = pm.create(args.id, args.name, languages=args.languages.split(",") if args.languages else None)
        print(f"Created project: {p.id}")
    elif args.project_action == "list":
        for p in pm.list_all():
            print(f"  {p.id}: {p.name} [{p.status}]")
    elif args.project_action == "get":
        p = pm.get(args.id)
        if p:
            print(f"  {p.id}: {p.name}")
            print(f"  Languages: {p.languages}")
            print(f"  Status: {p.status}")
        else:
            print(f"Project {args.id} not found")
    elif args.project_action == "archive":
        if pm.archive(args.id):
            print(f"Archived {args.id}")
        else:
            print(f"Project {args.id} not found")


def cmd_registry(args, managers):
    """Handle registry commands."""
    reg = managers["registry"]
    if args.registry_action == "init":
        register_defaults(reg)
        print("Registered default providers: deepgram, elevenlabs, openai, silero")
    elif args.registry_action == "list":
        category = ProviderCategory(args.category) if args.category else None
        for p in reg.list_all(category):
            print(f"  {p.id}: {p.name} [{p.category.value}]")
    elif args.registry_action == "get":
        p = reg.get(args.id)
        if p:
            print(f"  {p.id}: {p.name}")
            print(f"  Category: {p.category.value}")
            print(f"  Capabilities: {p.capabilities}")
        else:
            print(f"Provider {args.id} not found")


def cmd_experiment(args, managers):
    """Handle experiment commands."""
    em = managers["experiments"]
    if args.experiment_action == "create":
        exp = em.create(args.id, args.project, args.type)
        print(f"Created experiment: {exp.id}")
    elif args.experiment_action == "list":
        for e in em.list_all():
            print(f"  {e.id}: {e.experiment_type} [{e.status}]")
    elif args.experiment_action == "status":
        exp = em.update_status(args.id, args.status)
        if exp:
            print(f"Updated {args.id} to {args.status}")
        else:
            print(f"Experiment {args.id} not found")


def cmd_benchmark(args, managers):
    """Handle benchmark commands."""
    bs = managers["benchmarks"]
    if args.benchmark_action == "list":
        for b in bs.list_all():
            print(f"  {b.id}: {b.provider} {b.component} latency={b.latency_ms}ms")
    elif args.benchmark_action == "get":
        b = bs.get(args.id)
        if b:
            print(f"  {b.id}: {b.provider} {b.component}")
            print(f"  Latency: {b.latency_ms}ms")
            print(f"  Quality: {b.quality}")
            print(f"  Cost: {b.cost}")
        else:
            print(f"Benchmark {args.id} not found")


def cmd_agent(args, managers):
    """Handle agent config commands."""
    ac = managers["agents"]
    if args.agent_action == "create":
        config = ac.create(args.id, args.name)
        print(f"Created agent config: {args.id}")
    elif args.agent_action == "list":
        for c in ac.list_all():
            print(f"  {c['id']}: {c['agent']['name']}")
    elif args.agent_action == "validate":
        config = ac.get(args.id)
        if config:
            errors = ac.validate(config)
            if errors:
                for e in errors:
                    print(f"  ERROR: {e}")
            else:
                print("  Config is valid")
        else:
            print(f"Agent {args.id} not found")


def cmd_decision(args, managers):
    """Handle decision commands."""
    dm = managers["decisions"]
    if args.decision_action == "create":
        dec = dm.create(args.id, args.project, args.requirement)
        print(f"Created decision: {args.id}")
    elif args.decision_action == "list":
        for d in dm.list_all():
            print(f"  {d.id}: {d.requirement} -> {d.decision or 'pending'}")


def cmd_cost(args, managers):
    """Handle cost commands."""
    cc = managers["costs"]
    if args.cost_action == "estimate":
        result = cc.estimate(args.stt_cost, args.tts_cost, args.llm_cost)
        print(f"  STT: ${result['stt']}")
        print(f"  TTS: ${result['tts']}")
        print(f"  LLM: ${result['llm']}")
        print(f"  Total: ${result['total']}")
        print(f"  Per minute: ${result['per_minute']}")
        print(f"  Per 1k conversations: ${result['per_1k_conversations']}")
    elif args.cost_action == "list":
        for c in cc.list_all():
            print(f"  {c['id']}: ${c['estimate']['total']}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Voice Agent Engineering Workbench")
    subparsers = parser.add_subparsers(dest="command")

    # Project commands
    project_parser = subparsers.add_parser("project", help="Manage projects")
    project_parser.add_argument("project_action", choices=["create", "list", "get", "archive"])
    project_parser.add_argument("--id", help="Project ID")
    project_parser.add_argument("--name", help="Project name")
    project_parser.add_argument("--languages", help="Comma-separated languages")

    # Registry commands
    registry_parser = subparsers.add_parser("registry", help="Manage providers")
    registry_parser.add_argument("registry_action", choices=["init", "list", "get"])
    registry_parser.add_argument("--id", help="Provider ID")
    registry_parser.add_argument("--category", help="Filter by category")

    # Experiment commands
    experiment_parser = subparsers.add_parser("experiment", help="Manage experiments")
    experiment_parser.add_argument("experiment_action", choices=["create", "list", "status"])
    experiment_parser.add_argument("--id", help="Experiment ID")
    experiment_parser.add_argument("--project", help="Project ID")
    experiment_parser.add_argument("--type", help="Experiment type")
    experiment_parser.add_argument("--status", help="New status")

    # Benchmark commands
    benchmark_parser = subparsers.add_parser("benchmark", help="View benchmarks")
    benchmark_parser.add_argument("benchmark_action", choices=["list", "get"])
    benchmark_parser.add_argument("--id", help="Benchmark ID")

    # Agent commands
    agent_parser = subparsers.add_parser("agent", help="Manage agent configs")
    agent_parser.add_argument("agent_action", choices=["create", "list", "validate"])
    agent_parser.add_argument("--id", help="Agent ID")
    agent_parser.add_argument("--name", help="Agent name")

    # Decision commands
    decision_parser = subparsers.add_parser("decision", help="Manage decisions")
    decision_parser.add_argument("decision_action", choices=["create", "list"])
    decision_parser.add_argument("--id", help="Decision ID")
    decision_parser.add_argument("--project", help="Project ID")
    decision_parser.add_argument("--requirement", help="Requirement text")

    # Cost commands
    cost_parser = subparsers.add_parser("cost", help="Cost estimation")
    cost_parser.add_argument("cost_action", choices=["estimate", "list"])
    cost_parser.add_argument("--stt-cost", type=float, default=0.0043, help="STT cost per minute")
    cost_parser.add_argument("--tts-cost", type=float, default=0.00003, help="TTS cost per character")
    cost_parser.add_argument("--llm-cost", type=float, default=0.002, help="LLM cost per 1k tokens")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    managers = get_managers()
    handlers = {
        "project": cmd_project,
        "registry": cmd_registry,
        "experiment": cmd_experiment,
        "benchmark": cmd_benchmark,
        "agent": cmd_agent,
        "decision": cmd_decision,
        "cost": cmd_cost,
    }
    handlers[args.command](args, managers)


if __name__ == "__main__":
    main()
