import urllib.request

html = urllib.request.urlopen('http://127.0.0.1:5174/').read().decode()
new_html = html.replace('.js"', '.js?v=2"').replace('.css"', '.css?v=2"')
with open(r'C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\dist\index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print('Successfully written cache-busted index.html')
