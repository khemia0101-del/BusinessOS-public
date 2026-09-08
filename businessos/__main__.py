"""Run `python -m businessos --help`. No model calls or paid services required."""

import argparse
import json
import os
from pathlib import Path

from businessos.runtime import Runtime
from businessos.server import serve


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=os.environ.get("BUSINESSOS_DATA_DIR", "instance/runtime"))
    parser.add_argument("--business", default=os.environ.get("BUSINESSOS_INSTANCE_ID"))
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("snapshot")
    init = commands.add_parser("configure")
    init.add_argument("file", type=Path)
    ingest = commands.add_parser("ingest")
    ingest.add_argument("file", type=Path)
    ingest.add_argument("--document-id", required=True)
    ingest.add_argument("--origin", default="primary", choices=("primary", "seller_statement", "external", "notebook", "businessos"))
    report = commands.add_parser("report")
    report.add_argument("file", type=Path)
    memo = commands.add_parser("memo")
    memo.add_argument("report_id")
    memo.add_argument("--output", type=Path, required=True)
    server = commands.add_parser("serve")
    server.add_argument("--port", type=int, default=8790)
    migration = commands.add_parser("migrate")
    migration.add_argument("file", type=Path)
    migration.add_argument("--mapping", type=Path, required=True)
    migration.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.business:
        parser.error("--business or BUSINESSOS_INSTANCE_ID is required")
    if args.command == "serve":
        return serve(args.root, args.business, args.port)
    runtime = Runtime(args.root, args.business)
    if args.command == "migrate":
        from businessos.migrate import migrate_legacy
        migrated = migrate_legacy(json.loads(args.file.read_text(encoding="utf-8-sig")), json.loads(args.mapping.read_text(encoding="utf-8-sig")))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(migrated, indent=2), encoding="utf-8")
        result = {"written": str(args.output), "status": "requires_runtime_validation"}
    elif args.command == "configure":
        result = runtime.configure(json.loads(args.file.read_text(encoding="utf-8-sig")), "owner")
    elif args.command == "ingest":
        result = runtime.ingest(args.file.read_bytes(), args.file.name, args.document_id, args.origin, "owner")
        result = {k: v for k, v in result.items() if k != "segments"}
    elif args.command == "report":
        result = runtime.create_report(json.loads(args.file.read_text(encoding="utf-8-sig")), "owner")
    elif args.command == "memo":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(runtime.memo(args.report_id), encoding="utf-8")
        result = {"written": str(args.output)}
    else:
        result = runtime.snapshot()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
