import requests

for port in [5174, 5175]:
    url = f"http://localhost:{port}/"
    r = requests.get(url)
    print(f"Port {port} HTML: Status {r.status_code}, Length {len(r.text)}")
    print(f"  Snippet: {r.text[:300]}")
    css_url = f"http://localhost:{port}/assets/index-B7hGLdXo.css"
    r_css = requests.get(css_url)
    print(f"Port {port} CSS: Status {r_css.status_code}, Content-Type: {r_css.headers.get('Content-Type')}, Size: {len(r_css.text)} bytes")
