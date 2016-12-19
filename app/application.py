from flask import Flask, request, render_template
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/navigator', methods=['GET'])
def navigator():
    if request.method == 'GET':
        ctx = {}
        search_term = request.args.get('search_term','')
        if search_term:
            ctx['search_term'] = search_term
            ctx['results'] = []

            try:
                resp = requests.get('https://api.github.com/search/repositories?q={}'.format(search_term))
            except requests.exceptions.RequestException as err:
                return err

            found_items = resp.json()['items']
            if found_items:
                found_items = sorted(found_items, key= lambda item: item['created_at'], reverse=True)[:5]
                for item in found_items:
                    info = {}
                    info['repo_name'] = item['name']
                    info['created_at'] = datetime.strptime(item['created_at'], "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %H:%M:%S')
                    info['owner'] = item['owner']['login']
                    info['avatar_url'] = item['owner']['avatar_url']
                    last_commit_url = item['commits_url'][:-6] + '?per_page=1'

                    try:
                        commit = requests.get(last_commit_url).json()
                    except requests.exceptions.RequestException as err:
                        return err

                    if type(commit) == list:
                        commit=commit[0]
                        info['commit_sha'] = commit['sha']
                        info['commit_message'] = commit['commit']['message']
                        info['commit_author'] = commit['commit']['author']['name']
                    elif commit['message']:
                        info['api_message'] = commit['message']
                    ctx['results'].append(info)
            return render_template('nav.html', context=ctx)
        else:
            return '<h2>please enter a search_term</h2>'

if __name__ == "__main__":
        app.run()
