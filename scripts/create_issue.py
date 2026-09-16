import json
import os
import urllib.request

def main():
    token = os.environ.get('GH_TOKEN')
    repo = os.environ.get('GITHUB_REPOSITORY', 'VityazevEgor/InfoSec-pr1')
    sha = os.environ.get('GITHUB_SHA', '377e6a7')[:7]
    ref = os.environ.get('GITHUB_REF_NAME', 'test-failure')

    report_file = 'sast_results.json'
    if not os.path.exists(report_file):
        print(f'[ERROR] File {report_file} not found.')
        return

    with open(report_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = data.get('results', [])
    count = len(results)

    vuln_items = []
    for r in results[:5]:
        cid = r.get('check_id', 'unknown-rule')
        sev = r.get('extra', {}).get('severity', 'ERROR')
        path = r.get('path', '')
        line = r.get('start', {}).get('line', 1)
        vuln_items.append(f'- **{cid}** (`{sev}`) в `{path}:{line}`')

    items_text = '\n'.join(vuln_items)
    if count > 5:
        items_text += f'\n- ... и еще {count - 5} дефектов'

    title = f'[SAST] Критические уязвимости в коммите {sha} ({ref})'
    body = (
        f'### [SAST Alert] Обнаружены дефекты безопасности\n\n'
        f'В коммите `{sha}` (ветка `{ref}`) обнаружено уязвимостей: **{count}**.\n\n'
        f'### Дефекты:\n'
        f'{items_text}\n\n'
        f'> Полный отчёт сохранён в артефактах сборки (`sast-results`).'
    )

    if not token:
        print('[INFO] GH_TOKEN not set. Body preview:')
        print(body)
        return

    req = urllib.request.Request(
        f'https://api.github.com/repos/{repo}/issues',
        data=json.dumps({'title': title, 'body': body, 'labels': ['security', 'bug']}).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json',
            'User-Agent': 'Semgrep-CI'
        }
    )

    try:
        with urllib.request.urlopen(req) as resp:
            issue_url = json.loads(resp.read().decode('utf-8')).get('html_url')
            print(f'[SUCCESS] Issue создан: {issue_url}')
    except Exception as e:
        print(f'[ERROR] Ошибка создания Issue: {e}')

if __name__ == '__main__':
    main()
