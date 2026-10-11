"""One entrypoint for the four donor-adapted studies."""
import argparse
import json
from pathlib import Path
from . import bell_chsh, damping_sweep, qaoa_maxcut, zne_landscape
from .reporting import save_report


def main():
    parser = argparse.ArgumentParser(description="Personal quantum simulation experiments")
    parser.add_argument("study", choices=["bell", "damping", "qaoa", "zne"])
    parser.add_argument("--out", type=Path)
    parser.add_argument("--binding", type=Path)
    parser.add_argument("--seed", type=int, default=137)
    parser.add_argument("--shots", type=int)
    parser.add_argument("--maxiter", type=int, default=50)
    parser.add_argument("--points", type=int, default=50)
    parser.add_argument("--noise", type=float, default=0.04)
    parser.add_argument("--graph-seed", type=int, default=137)
    parser.add_argument("--parameter-seed", type=int, default=138)
    parser.add_argument("--simulator-seed", type=int, default=139)
    args = parser.parse_args()
    if args.shots is not None and args.shots < 1:
        parser.error("--shots must be positive")
    if args.points < 2 or args.maxiter < 1:
        parser.error("--points must be at least 2 and --maxiter positive")
    if args.study == "bell":
        data = bell_chsh.run(args.shots or 4096, args.seed)
    elif args.study == "damping":
        data = damping_sweep.run(args.shots or 1024, args.seed)
    elif args.study == "qaoa":
        data = qaoa_maxcut.run(args.shots or 256, args.maxiter, args.graph_seed,
                             args.parameter_seed, args.simulator_seed)
    else:
        data = zne_landscape.run(args.points, args.noise, args.seed)
    binding = json.loads(args.binding.read_text()) if args.binding else None
    report = save_report(args.study, data, args.out or Path("results") / args.study, binding)
    summary = report.get("summary") or report.get("optimizer") or {
        k: v for k, v in report.items() if k in ["wins", "trials", "win_probability", "rows"]}
    print(json.dumps({"study": args.study, "mode": "simulation", "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
