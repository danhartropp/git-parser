from collections import Counter, defaultdict
import csv
import fnmatch
import subprocess
import re

# set up regexes for files/folders to ignore
IGNORE = ['*.ipynb','*.log','*.json', 'scripts/']

# set up weightings e.g. deleting a line is 'worth' half as much as adding a line
WEIGHTINGS = {'addition':1, 'deletion':0.5}

# How far back in the commit history do we want to go?
MONTHS_AGO = 12

res = subprocess.run(f'git log --since="{MONTHS_AGO} months ago" --date=iso-strict --numstat --no-merges', stdout=subprocess.PIPE)

#parse the git log into something more usable
commits = [ x for x in ('\n' + res.stdout.decode('utf-8')).split('\ncommit ') if x != '']
commits = [re.sub('{.* => (.*)}', r'\1', commit) for commit in commits] # only keep the final name of renamed files 

def get_commit(commit):
    data = {'files':[]}
    lines = [x.strip() for x in commit.split('\n') if x != '']
    if 'reversing' in lines[0]:
        return None
    data['commit'] = lines[0]
    for line in lines[1:]:
        if '\t' in line:
            data['files'].append(line.split('\t'))
        elif ': ' in line:
            data[line.split(': ')[0].strip()] = line.split(': ')[1].strip()
        else:
            data['message'] = line.strip()
    data['Author'] = re.findall('<(.*)>', data['Author'])[0]
    return data

commits = [get_commit(x) for x in commits]
commits = [x for x in commits if x != None]


folder_count = defaultdict(Counter)
for commit in commits:
    for f in commit['files']:

        if any (re.match(fnmatch.translate(i), f[2]) for i in IGNORE):
            continue
        
        additions = int(f[0].replace('-','0')) * WEIGHTINGS['addition']
        deletions = int(f[1].replace('-','0')) * WEIGHTINGS['deletion']
        
        path_parts = f[2].split('/')
        for idx in range(len(path_parts)):
            path = '/' + '/'.join(path_parts[:idx + 1])
            if '.' not in path:
                path += '/'
            folder_count[commit['Author']][path] += int(additions + deletions)

# write a simple html report
html = '''<html><body>'''
html += '''<h1>Author stats</h1>'''
html += '''<table style="text-align:left;"><tr><th>Author</th><th>Changes</th></tr>'''
for author, folder_stats in folder_count.items():
    changes = sum(item[1] for item in folder_stats.items() if not item[0].endswith('/'))
    html += f'''<tr><td>{author}</td><td>{changes}</td></tr>'''
html += '''</table>'''

html += '''<h1>Headline activity per author</h1>'''
html += '''<p>NOTE: changes for sub-paths are also included in the overall changes for the parent path(s)</p>'''
for author, folder_stats in folder_count.items():
    html += f'''<h2>{author}</h2>'''
    html += '''<table style="text-align:left;"><tr><th>Path</th><th>Changes</th></tr>'''
    for path, changes in folder_stats.most_common(10):
        html += f'''<tr><td>{path}</td><td>{changes}</td></tr>'''
    html += '''</table>'''


html += '''</html'''
with open('git_stats.html', 'w', encoding="utf-8") as f:
    f.write(html)

# write the detailed stats to csv
with open('git_stats.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Author', 'path', 'changes'])
    for author, folder_stats in folder_count.items():
        for row in folder_stats.items():
            writer.writerow([author] + list(row))

