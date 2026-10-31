#!/usr/bin/env python3
"""Mutation checks: prove that saved-result validation catches each failure kind.

Uses temporary copies, never edits the authoritative run. Integrity hashing is
disabled only in these disposable copies so semantic checks must catch defects.
"""
import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile

from phase3_tests import ROOT, validate


def main():
    source = ROOT / 'outputs/runs' / (ROOT / 'outputs/latest.txt').read_text().strip()
    results = []
    mutations = [
        ('padding', 'transactions/TC08.atf.txt', lambda b: b.replace(b'newuser ', b'newuser', 1)),
        ('code', 'transactions/TC08.atf.txt', lambda b: b.replace(b'01 ', b'07 ', 1)),
        ('money', 'transactions/TC36.atf.txt', lambda b: b.replace(b'000100.00', b'000100.01')),
        ('ordering', 'transactions/TC41.atf.txt', lambda b: b'\n'.join([b.split(b'\n')[1],b.split(b'\n')[0],*b.split(b'\n')[2:]])),
        ('end record', 'transactions/TC01.atf.txt', lambda b: b'00 extra\n'),
        ('newline', 'transactions/TC01.atf.txt', lambda b: b.rstrip(b'\r\n')),
        ('exit status', 'terminal/TC01.status.json', lambda b: b.replace(b'"exit_status": 0', b'"exit_status": 1')),
        ('stderr', 'terminal/TC01.stderr.txt', lambda b: b'error\n'),
        ('missing event', 'terminal/TC01.stdout.txt', lambda b: b.replace(b'Logout accepted.', b'Logout skipped.')),
        ('extra success', 'terminal/TC10.stdout.txt', lambda b: b+b'Create accepted. Bad success.\n'),
        ('missing file', 'transactions/TC01.atf.txt', None),
    ]
    with tempfile.TemporaryDirectory(prefix='validator-', dir=ROOT/'build') as temp:
        folder = Path(temp)
        for sub in ['terminal','transactions','oracle']:
            shutil.copytree(source/sub,folder/sub)
        (folder/'manifest.json').write_text('{"evidence_sha256":{}}')
        with contextlib.redirect_stdout(io.StringIO()):
            assert validate(folder) == 0, 'Control run must pass'
        for name,relative,change in mutations:
            path=folder/relative; original=path.read_bytes()
            if change: path.write_bytes(change(original))
            else: path.unlink()
            with contextlib.redirect_stdout(io.StringIO()):
                detected=validate(folder)==1
            path.write_bytes(original)
            results.append({'check':name,'detected':detected})
            print(('PASS' if detected else 'FAIL')+': detects '+name)
    (ROOT/'outputs/validator_checks.json').write_text(json.dumps(results,indent=2)+'\n')
    return int(not all(r['detected'] for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
