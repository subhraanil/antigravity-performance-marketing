import socket
import ssl
import json
import urllib.request

domain = "storiai.ai"

# DNS IP
try:
    ip = socket.gethostbyname(domain)
    print(f"Domain IP: {ip}")
except Exception as e:
    print(f"DNS Error: {e}")

# SSL Cert
try:
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
        s.settimeout(5.0)
        s.connect((domain, 443))
        cert = s.getpeercert()
        print("SSL Issuer:", dict(x[0] for x in cert.get('issuer', [])))
        print("SSL Subject:", dict(x[0] for x in cert.get('subject', [])))
        print("SSL Valid From:", cert.get('notBefore'))
        print("SSL Valid Until:", cert.get('notAfter'))
        print("SSL SAN:", [x[1] for x in cert.get('subjectAltName', []) if x[0] == 'DNS'])
except Exception as e:
    print(f"SSL Error: {e}")

# GeoIP / Server location check
try:
    url = f"http://ip-api.com/json/{ip}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("Server Hosting & Location:")
        print(f"  ISP / Org: {data.get('isp')} / {data.get('org')}")
        print(f"  Location: {data.get('city')}, {data.get('regionName')}, {data.get('country')}")
        print(f"  AS: {data.get('as')}")
except Exception as e:
    print(f"GeoIP Error: {e}")
