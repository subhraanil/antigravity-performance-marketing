import re

with open('data/storiai/chunks/App-XFfRbN91.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's extract the string table or definitions around Kne
start_idx = text.find('Where Your Child\'s Emotions Become Stories')
if start_idx != -1:
    snippet = text[max(0, start_idx - 1000): min(len(text), start_idx + 4000)]
    print("--- CONTENT SNIPPET ---")
    print(snippet)

# Search for FAQ content
faq_idx = text.find('Frequently Asked Questions')
if faq_idx == -1:
    faq_idx = text.find('FAQ')
if faq_idx != -1:
    print("\n--- FAQ SNIPPET ---")
    print(text[max(0, faq_idx - 200): min(len(text), faq_idx + 2000)])

# Search for Pricing content
pricing_idx = text.find('choose-plan')
if pricing_idx != -1:
    print("\n--- PRICING SNIPPET ---")
    print(text[max(0, pricing_idx - 200): min(len(text), pricing_idx + 2000)])
