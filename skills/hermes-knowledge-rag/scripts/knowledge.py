#!/usr/bin/env python3
"""Safe daily git sync and dependency-free lexical retrieval of private text."""
import argparse
from collections import Counter
from datetime import datetime
import fcntl
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

REPO = Path('/Users/marcovinciguerra/github/hermes-knowledge')
REMOTE = 'https://github.com/VinciGit00/hermes-knowledge.git'
STATE = Path.home() / 'Library/Application Support/hermes-knowledge-rag'


def git(*args):
    result = subprocess.run(
        ['/usr/bin/git', '-c', 'core.hooksPath=/dev/null', '-C', str(REPO), *args],
        env={**os.environ, 'GIT_TERMINAL_PROMPT': '0',
             'GIT_SSH_COMMAND': 'ssh -o BatchMode=yes -o ConnectTimeout=15'},
        capture_output=True, text=True, timeout=90)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or 'git failed')
    return result.stdout.strip()


def sync(force=False):
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (STATE / 'sync.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {'ok': False, 'message': 'Another sync is running; using local copy.'}
        path = STATE / 'sync.json'
        try:
            previous = json.loads(path.read_text())
        except (OSError, ValueError):
            previous = {}
        now = datetime.now().astimezone().isoformat()
        if not force and (previous.get('last_success') or '')[:10] == now[:10]:
            return {**previous, 'cached': True}
        status = {'ok': False, 'attempted_at': now,
                  'last_success': previous.get('last_success')}
        try:
            if git('remote', 'get-url', 'origin') != REMOTE:
                raise RuntimeError('Unexpected origin remote; automatic sync skipped.')
            if git('branch', '--show-current') != 'main':
                raise RuntimeError('Checkout is not on main; automatic sync skipped.')
            if git('status', '--porcelain'):
                raise RuntimeError('Working tree has local changes; automatic sync skipped.')
            git('fetch', 'origin', 'main')
            if int(git('rev-list', '--count', 'FETCH_HEAD..HEAD')):
                raise RuntimeError('Local-only commits detected; automatic sync skipped.')
            git('-c', 'pull.rebase=false', '-c', 'merge.autoStash=false',
                'pull', '--ff-only', '--no-rebase', 'origin', 'main')
            status.update(ok=True, last_success=now, commit=git('rev-parse', 'HEAD'),
                          message='Repository synchronized.')
        except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
            status['message'] = str(exc)
        temporary = path.with_suffix('.tmp')
        temporary.write_text(json.dumps(status, indent=2) + '\n')
        temporary.replace(path)
        return status


STOP = set('the a an of to and in for is are with how what does do on as by that this it di a da in con per e il lo la i gli le un una come cosa che del della delle dei'.split())


def tokens(value):
    return [word for word in re.findall(r'\w+', unicodedata.normalize('NFKC', value).lower())
            if len(word) > 1 and word not in STOP]


def chunks(repo):
    for directory in ('documents', 'graphify-out/wiki'):
        for path in sorted((repo / directory).rglob('*.md')):
            if path.is_symlink() or not path.resolve().is_relative_to(repo.resolve()):
                continue
            lines = path.read_text(errors='replace').splitlines()
            page, section = None, []

            def emit(section, page):
                for start in range(0, len(section), 30):
                    portion = section[start:start + 40]
                    text = '\n'.join(line for _, line in portion)
                    if tokens(text):
                        yield {'path': str(path), 'line': portion[0][0],
                               'end_line': portion[-1][0], 'page': page, 'text': text}
                    if start + 40 >= len(section):
                        break

            for number, line in enumerate(lines, 1):
                match = re.match(r'^## Page (\d+)\s*$', line)
                if match:
                    yield from emit(section, page)
                    section, page = [], int(match.group(1))
                section.append((number, line))
            yield from emit(section, page)


def search(repo, query, limit):
    records = list(chunks(repo))
    counts = [Counter(tokens(record['text'])) for record in records]
    frequencies = Counter(term for count in counts for term in count)
    average = sum(sum(count.values()) for count in counts) / max(len(counts), 1)
    terms = set(tokens(query))
    ranked = []
    for record, count in zip(records, counts):
        score = 0.0
        for term in terms & count.keys():
            frequency = count[term]
            idf = math.log(1 + (len(records) - frequencies[term] + .5) / (frequencies[term] + .5))
            score += idf * frequency * 2.5 / (frequency + 1.5 * (.25 + .75 * sum(count.values()) / average))
        if score:
            ranked.append({**record, 'score': round(score, 4)})
    ranked.sort(key=lambda record: record['score'], reverse=True)
    return {'query': query, 'chunks_searched': len(records), 'results': ranked[:limit]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    update = commands.add_parser('sync')
    update.add_argument('--force', action='store_true')
    retrieve = commands.add_parser('search')
    retrieve.add_argument('query')
    retrieve.add_argument('--limit', type=int, default=6, choices=range(1, 21))
    retrieve.add_argument('--no-sync', action='store_true')
    args = parser.parse_args()
    if args.command == 'sync':
        status = sync(args.force)
        print(json.dumps(status, indent=2))
        return 0 if status['ok'] else 1
    status = None if args.no_sync else sync()
    if not REPO.is_dir():
        parser.error('Knowledge repository is missing.')
    result = search(REPO, args.query, args.limit)
    result['sync'] = status
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
