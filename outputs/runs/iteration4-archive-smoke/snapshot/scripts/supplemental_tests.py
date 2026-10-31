#!/usr/bin/env python3
"""Focused black-box regressions for gaps in the original 46 cases.

Expected records/balances are calculated here from requirements, never harvested
from the executable. Python is used only for testing, not for a Back End.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def account(code, name, kind, cents):
    return f'{code} {name:<15} {kind:2} {cents // 100:06}.{cents % 100:02}'


def sale(name, seller, cents):
    return f'03 {name:<25} {seller:<15} {cents // 100:03}.{cents % 100:02}'


def purchase(name, seller, buyer, cents):
    return f'04 {name:<25} {seller:<15} {buyer:<15} {cents // 100:03}.{cents % 100:02}'


def cases():
    return [
        dict(id='S01', purpose='Huge money must reject and continue to logout', user='buyer1',
             commands='addcredit\n99999999999999999999999999999999999999.00\n', records=[], errors=1),
        dict(id='S02', purpose='Integer cents multiplication must not overflow', user='buyer1',
             commands='addcredit\n92233720368547759.00\n', records=[], errors=1),
        dict(id='S03', purpose='Duplicate purchase and buyer/seller balance changes', user='admin',
             commands='buy\nExistingGame\nseller1\nbuy\nExistingGame\nseller1\nlist\n',
             records=[purchase('ExistingGame','seller1','admin',1500)], errors=1,
             balances={'admin':'4985.00','seller1':'515.00'}),
        dict(id='S04', purpose='Refund transfers credit to buyer and from seller', user='admin',
             commands='refund\nbuyer1\nseller1\n10.00\nlist\n',
             records=[f'05 {"buyer1":<15} {"seller1":<15} 000010.00'], errors=0,
             balances={'buyer1':'510.00','seller1':'490.00'}),
        dict(id='S05', purpose='Deleted seller inventory and account cannot be used', user='admin',
             commands='delete\nseller1\nbuy\nExistingGame\nseller1\naddcredit\n1.00\nseller1\nlist\n',
             records=[account('02','seller1','',0)], errors=2, absent_account='seller1'),
        dict(id='S06', purpose='New listing unavailable to a buy-capable account; duplicate listing rejected', user='admin',
             commands='sell\nFresh Game\n10.00\nbuy\nFresh Game\nadmin\nsell\nFresh Game\n10.00\n',
             records=[sale('Fresh Game','admin',1000)], errors=2),
        dict(id='S07', purpose='Per-account credit limits independent within session', user='admin',
             commands='addcredit\n1000.00\nbuyer1\naddcredit\n1000.00\nseller1\naddcredit\n0.01\nbuyer1\nlist\n',
             records=[account('06','buyer1','BS',100000),account('06','seller1','SS',100000)], errors=1,
             balances={'buyer1':'1500.00','seller1':'1500.00'}),
        dict(id='S08', purpose='New accounts, duplicate names, all valid type words', user='admin',
             commands='create\nnewadmin\nadmin\ncreate\nnewbuyer\nbuy-standard\ncreate\nnewseller\nsell-standard\ncreate\nnewbuyer\nfull-standard\nlist\n',
             records=[account('01','newadmin','AA',0),account('01','newbuyer','BS',0),account('01','newseller','SS',0)], errors=1,
             balances={'newadmin':'0.00','newbuyer':'0.00','newseller':'0.00'}),
        dict(id='S09', purpose='Blank, reserved, padded names and invalid account types', user='admin',
             commands='create\n\nadmin\ncreate\nEND\nadmin\ncreate\nname \nadmin\ncreate\nvalid\ninvalid\n', records=[], errors=4),
        dict(id='S10', purpose='Seller identity must match listing', user='buyer1',
             commands='buy\nExistingGame\nseller2\n', records=[], errors=1),
        dict(id='S11', purpose='Insufficient seller refund funds leave both balances unchanged', user='admin',
             commands='refund\nbuyer1\nseller1\n500.01\nlist\n', records=[], errors=1,
             balances={'buyer1':'500.00','seller1':'500.00'}),
        dict(id='S12', purpose='Missing games file rejects login politely', user='admin', commands='',
             records=None, errors=2, missing='game'),
        dict(id='S13', purpose='Malformed collection file rejects login politely', user='admin', commands='',
             records=None, errors=2, corrupt='collection'),
        dict(id='S14', purpose='Missing END in games file rejects login', user='admin', commands='',
             records=None, errors=2, no_end='game'),
        dict(id='S15', purpose='49/42 character handout input compatibility', user='buyer1',
             commands='buy\nExistingGame\nseller1\n', records=[purchase('ExistingGame','seller1','buyer1',1500)],
             errors=0, wide=True),
        dict(id='S16', purpose='EOF in a command is recoverable and creates no DTF', user='admin',
             commands='refund\nbuyer1\n', records=None, errors=1, eof=True),
        dict(id='S17', purpose='Credit limit resets and input files reload at next login', user='buyer1',
             commands='addcredit\n1000.00\nlogout\nlogin\nbuyer1\naddcredit\n1000.00\n',
             records=[account('06','buyer1','BS',100000)], errors=0),
        dict(id='S18', purpose='Buy uses credit added earlier in same session', user='lowcredit',
             commands='addcredit\n10.00\nbuy\nExistingGame\nseller1\n',
             records=[account('06','lowcredit','BS',1000),purchase('ExistingGame','seller1','lowcredit',1500)], errors=0),
        dict(id='S19', purpose='Maximum balance guard preserves account', user='admin',
             commands='addcredit\n0.01\nbuyer1\nlist\n', records=[], errors=1,
             max_balance=True, balances={'buyer1':'999999.00'}),
        dict(id='S20', purpose='Failed output write retains session and reports failure', user='admin',
             commands='', records=None, errors=1, bad_output=True),
        dict(id='S21', purpose='Printable names with embedded spaces and maximum field lengths', user='admin',
             commands='create\nJane Doe\nfull-standard\nsell\nABCDEFGHIJKLMNOPQRSTUVWXY\n999.99\n',
             records=[account('01','Jane Doe','FS',0),sale('ABCDEFGHIJKLMNOPQRSTUVWXY','admin',99999)], errors=0),
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--binary', default='build/games-distribution')
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.label):
        parser.error('Invalid label')
    binary = (ROOT / args.binary).resolve()
    if not binary.exists(): binary = binary.with_suffix('.exe')
    run = ROOT / 'outputs/supplemental' / args.label
    run.mkdir(parents=True, exist_ok=False)
    results = []
    for case in cases():
        folder = run / case['id']; folder.mkdir()
        for ext in ['user','game','collection']:
            data = (ROOT / 'inputs' / f'TC01.{ext}.txt').read_text()
            if case.get('missing') == ext: continue
            if case.get('corrupt') == ext: data = 'bad record\nEND\n'
            if case.get('no_end') == ext: data = '\n'.join(data.splitlines()[:-1]) + '\n'
            if case.get('wide') and ext in ['game','collection']:
                data = '\n'.join(line[:25]+' '+line[25:] for line in data.splitlines())+'\n'
            if case.get('max_balance') and ext == 'user':
                data = data.replace('buyer1          BS 000500.00','buyer1          BS 999999.00')
            (folder / f'{ext}.txt').write_text(data)
        commands = f"login\n{case['user']}\n" + case['commands'] + ('' if case.get('eof') else 'logout\n')
        (folder / 'input.txt').write_text(commands)
        expected = None if case['records'] is None else '\n'.join(case['records'] + ['00'])+'\n'
        if expected is not None: (folder / 'expected.atf.txt').write_text(expected)
        output = folder if case.get('bad_output') else folder / 'actual.atf.txt'
        failures=[]
        try:
            result = subprocess.run([str(binary),*[str(folder/f'{x}.txt') for x in ['user','game','collection']],str(output)],
                                    input=commands, text=True, capture_output=True, timeout=10)
            (folder/'stdout.txt').write_text(result.stdout)
            (folder/'stderr.txt').write_text(result.stderr)
            (folder/'exit_status.txt').write_text(str(result.returncode)+'\n')
            if result.returncode != 0 or result.stderr: failures.append('nonzero exit or stderr')
            actual = output.read_text() if output.is_file() else None
            if actual != expected: failures.append('DTF mismatch')
            if result.stdout.count('Error:') != case['errors']: failures.append('unexpected error count')
            for name,balance in case.get('balances',{}).items():
                if not re.search(r'^'+re.escape(name)+r' +[A-Z]{2} +'+re.escape(balance)+r'$',result.stdout,re.M):
                    failures.append(f'wrong/missing balance: {name}={balance}')
            if case.get('absent_account') and re.search(r'^'+case['absent_account']+r' +[A-Z]{2} ',result.stdout,re.M):
                failures.append('deleted account still listed')
            if not case.get('eof') and not case.get('missing') and not case.get('corrupt') and not case.get('no_end') and not case.get('bad_output'):
                if 'Logout accepted.' not in result.stdout: failures.append('did not recover to logout')
            if case.get('bad_output') and 'is still logged in.' not in result.stdout:
                failures.append('write failure did not preserve session')
        except (OSError,subprocess.TimeoutExpired) as exc:
            failures.append(str(exc))
        results.append(dict(id=case['id'],purpose=case['purpose'],passed=not failures,failures=failures))
        print(('FAIL' if failures else 'PASS')+' '+case['id']+': '+case['purpose']+ ('; '+', '.join(failures) if failures else ''))
    (run/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    (run/'test_definition.py').write_bytes(Path(__file__).read_bytes())
    print(f"Supplemental: {sum(r['passed'] for r in results)}/{len(results)} PASS")
    return int(any(not r['passed'] for r in results))


if __name__ == '__main__':
    sys.exit(main())
