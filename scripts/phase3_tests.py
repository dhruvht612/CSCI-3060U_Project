#!/usr/bin/env python3
"""Phase 3 execution/verification only; never updates application data files.

Only CRLF -> LF is normalized. No stripping, token sorting, or rounding is used.
Behavioral descriptions remain intact; reviewed event assertions live separately.
"""
import argparse
import datetime
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def normalized(path):
    return path.read_bytes().replace(b"\r\n", b"\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head():
    # A submission ZIP has no .git; provenance must not block test execution.
    try:
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                text=True, capture_output=True, timeout=5, check=False)
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def discover():
    ids = sorted(p.name.removesuffix('.inp.txt') for p in (ROOT / 'inputs').glob('TC*.inp.txt'))
    required = [f'TC{i:02}' for i in range(1, 47)]
    if ids != required:
        raise ValueError(f'Expected TC01-TC46 exactly; discovered {ids}')
    for tid in ids:
        for folder, suffixes in [('inputs', ['inp', 'user', 'game', 'collection']),
                                 ('expected', ['exptf', 'expout'])]:
            for suffix in suffixes:
                if not (ROOT / folder / f'{tid}.{suffix}.txt').is_file():
                    raise ValueError(f'Missing {folder}/{tid}.{suffix}.txt')
    return ids


def schema_errors(data):
    # Explicit Phase 1 compatibility profile; see Phase3_Format_Decisions.md.
    patterns = {
        b'01': rb'01 [ -~]{15} (AA|FS|BS|SS) [0-9]{6}\.[0-9]{2}',
        b'02': rb'02 [ -~]{15}    000000\.00',
        b'03': rb'03 [ -~]{25} [ -~]{15} [0-9]{3}\.[0-9]{2}',
        b'04': rb'04 [ -~]{25} [ -~]{15} [ -~]{15} [0-9]{3}\.[0-9]{2}',
        b'05': rb'05 [ -~]{15} [ -~]{15} [0-9]{6}\.[0-9]{2}',
        b'06': rb'06 [ -~]{15} (AA|FS|BS|SS) [0-9]{6}\.[0-9]{2}',
    }
    errors = []
    if not data.endswith(b'\n'):
        errors.append('DTF missing final newline')
    lines = data.split(b'\n')[:-1]
    if not lines or lines[-1] != b'00' or lines.count(b'00') != 1:
        errors.append('DTF must end with exactly one bare 00')
    for number, line in enumerate(lines[:-1], 1):
        if not re.fullmatch(patterns.get(line[:2], rb'(?!)'), line):
            errors.append(f'DTF record {number}: invalid code/field width/spacing/money')
    return errors


def validate(run, persist=False):
    ids = discover()
    assertions = json.loads((run / 'oracle/terminal_assertions.json').read_text(encoding='utf-8'))
    manifest = json.loads((run / 'manifest.json').read_text(encoding='utf-8'))
    results = []
    for tid in ids:
        errors = []
        try:
            meta = json.loads((run / 'terminal' / f'{tid}.status.json').read_text())
            if meta['exit_status'] != 0 or meta.get('execution_error'):
                errors.append(f"process exit={meta['exit_status']}: {meta.get('execution_error', '')}")
            if (run / 'terminal' / f'{tid}.stderr.txt').read_bytes():
                errors.append('unexpected stderr')
            actual_path = run / 'transactions' / f'{tid}.atf.txt'
            expected = normalized(run / 'oracle' / f'{tid}.exptf.txt')
            if not actual_path.is_file():
                errors.append('DTF missing')
            else:
                actual = normalized(actual_path)
                errors.extend(schema_errors(actual))
                if persist:
                    (run / 'transactions' / f'{tid}.diff.txt').write_text('', encoding='utf-8')
                if actual != expected:
                    errors.append('DTF differs from original fixture (including order/padding/amounts)')
                    if persist:
                        diff = ''.join(difflib.unified_diff(expected.decode().splitlines(True),
                                      actual.decode(errors='replace').splitlines(True),
                                      fromfile='expected', tofile='actual'))
                        (run / 'transactions' / f'{tid}.diff.txt').write_text(diff, encoding='utf-8')
            output = normalized(run / 'terminal' / f'{tid}.stdout.txt').decode('utf-8', errors='replace')
            # Exact event sequence ensures no extra success/error, skipped command,
            # or unobserved rejection. Prompt prose is deliberately not an oracle.
            events = re.findall(r'(?:Login|Logout|Create|Delete|Sell|Buy|Refund|Addcredit) accepted\.[^\n]*|Error:[^\n]*', output)
            wanted = assertions[tid]['events']
            if len(events) != len(wanted) or any(not re.fullmatch(pattern, event)
                                                     for pattern, event in zip(wanted, events)):
                errors.append(f'terminal events: expected {wanted!r}; actual {events!r}')
            if 'Enter command: ' not in output or 'Enter username: ' not in output:
                errors.append('missing command/login prompts')
        except (OSError, ValueError, KeyError) as exc:
            errors.append(f'evidence incomplete: {exc}')
        results.append({'id': tid, 'passed': not errors, 'failures': errors})
        print(f"{'PASS' if not errors else 'FAIL'} {tid}" + (': ' + '; '.join(errors) if errors else ''))
    # Saved hashes protect the source/fixtures and stdout/stderr/status/DTF evidence.
    integrity = []
    for relative, sha in manifest.get('evidence_sha256', {}).items():
        path = run / relative
        if not path.is_file() or digest(path) != sha:
            integrity.append(relative)
    passed = sum(r['passed'] for r in results)
    report = {'passed': passed, 'failed': len(ids) - passed, 'total': len(ids),
              'integrity_failures': integrity, 'results': results}
    print(f"Summary: {passed}/{len(ids)} PASS; {len(ids)-passed} FAIL; evidence integrity errors: {len(integrity)}")
    if persist:
        (run / 'validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return 0 if passed == len(ids) and not integrity else 1


def execute(args):
    ids = discover()
    binary = (ROOT / args.binary).resolve()
    if not binary.is_file() and binary.with_suffix('.exe').is_file():
        binary = binary.with_suffix('.exe')
    if not binary.is_file():
        raise ValueError(f'Build the executable first: {binary}')
    name = args.label or datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    if not re.fullmatch(r'[A-Za-z0-9_-]+', name):
        raise ValueError('Label may contain only letters, numbers, hyphens and underscores')
    run = ROOT / 'outputs/runs' / name
    run.mkdir(parents=True, exist_ok=False)  # never overwrite historical evidence
    for folder in ['terminal', 'transactions', 'oracle', 'snapshot']:
        (run / folder).mkdir()
    for folder in ['src', 'include', 'inputs', 'expected', 'scripts']:
        shutil.copytree(ROOT / folder, run / 'snapshot' / folder, ignore=shutil.ignore_patterns('__pycache__'))
    for path in (ROOT / 'expected').glob('TC*.exptf.txt'):
        shutil.copy2(path, run / 'oracle' / path.name)
    shutil.copy2(ROOT / 'tests/terminal_assertions.json', run / 'oracle/terminal_assertions.json')
    manifest = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'binary_sha256': digest(binary), 'binary': str(binary),
                'platform': sys.platform, 'python': sys.version,
                'git_head': git_head(),
                'command': [str(binary), '<test.user>', '<test.game>', '<test.collection>', '<test.atf>']}
    for tid in ids:
        command = [str(binary)] + [str(ROOT / 'inputs' / f'{tid}.{ext}.txt')
                                  for ext in ['user', 'game', 'collection']]
        command.append(str(run / 'transactions' / f'{tid}.atf.txt'))
        status = {'exit_status': None, 'execution_error': ''}
        with (ROOT / 'inputs' / f'{tid}.inp.txt').open('rb') as inp, \
             (run / 'terminal' / f'{tid}.stdout.txt').open('wb') as out, \
             (run / 'terminal' / f'{tid}.stderr.txt').open('wb') as err:
            try:
                process = subprocess.run(command, stdin=inp, stdout=out, stderr=err,
                                         cwd=ROOT, timeout=args.timeout, check=False)
                status['exit_status'] = process.returncode
            except (OSError, subprocess.TimeoutExpired) as exc:
                status['execution_error'] = str(exc)
        (run / 'terminal' / f'{tid}.status.json').write_text(json.dumps(status, indent=2) + '\n')
    manifest['evidence_sha256'] = {str(p.relative_to(run)).replace('\\', '/'): digest(p)
                                   for p in sorted(run.rglob('*')) if p.is_file()}
    (run / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    result = validate(run, persist=True)
    # Convenience copies; the immutable run is authoritative.
    for folder in ['transactions', 'terminal']:
        (ROOT / 'outputs' / folder).mkdir(exist_ok=True)
        for p in (run / folder).iterdir():
            shutil.copy2(p, ROOT / 'outputs' / folder / p.name)
    (ROOT / 'outputs/latest.txt').write_text(name + '\n')
    print(f'Evidence: {run.relative_to(ROOT)}')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='action', required=True)
    run = subs.add_parser('run')
    run.add_argument('--binary', default='build/games-distribution')
    run.add_argument('--label')
    run.add_argument('--timeout', type=float, default=10)
    check = subs.add_parser('validate')
    check.add_argument('run', nargs='?')
    args = parser.parse_args()
    try:
        if args.action == 'run':
            if args.timeout <= 0:
                raise ValueError('Timeout must be positive')
            return execute(args)
        path = ROOT / args.run if args.run else ROOT / 'outputs/runs' / (ROOT / 'outputs/latest.txt').read_text().strip()
        return validate(path)
    except (OSError, ValueError, KeyError) as exc:
        print(f'Harness error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
