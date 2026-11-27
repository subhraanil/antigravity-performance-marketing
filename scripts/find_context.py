with open('data/storiai/chunks/App-XFfRbN91.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('hero-home.webp')
if idx != -1:
    print("Context around hero-home.webp:")
    print(text[max(0, idx - 200): min(len(text), idx + 200)])
else:
    print("Not found directly as string")

for needle in ['Where Your Child', 'Emotions', 'Personalized', 'Create Your First Story', 'How STORIAI Works']:
    pos = text.find(needle)
    if pos != -1:
        print(f"\nContext around '{needle}':")
        print(text[max(0, pos - 150): min(len(text), pos + 250)])
    else:
        print(f"'{needle}' not found in App-XFfRbN91.js")
