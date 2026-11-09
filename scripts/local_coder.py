#!/usr/bin/env python3
"""
Local AI Coder Assistant using Qwen 2.5 Coder 1.5B via Ollama.
Designed for 8 GB RAM machines — lightweight, offline, and fast.
"""
import argparse
import json
import sys
import urllib.error
import urllib.request

OLLAMA_ENDPOINT = "http://127.0.0.1:11434/v1/chat/completions"
DEFAULT_MODEL = "qwen2.5-coder:1.5b"

def query_local_coder(prompt, system_prompt=None, model=DEFAULT_MODEL, temperature=0.2, max_tokens=1024, stream=True):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    else:
        messages.append({
            "role": "system",
            "content": "You are Qwen 2.5 Coder, an expert programming assistant. Provide clean, concise, production-ready code with minimal conversational filler."
        })
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json", "Authorization": "Bearer ollama"}
    )

    try:
        with urllib.request.urlopen(req) as resp:
            if stream:
                for line in resp:
                    line = line.decode("utf-8").strip()
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_str)
                            delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if delta:
                                sys.stdout.write(delta)
                                sys.stdout.flush()
                        except json.JSONDecodeError:
                            continue
                print()
            else:
                body = json.loads(resp.read().decode("utf-8"))
                content = body["choices"][0]["message"]["content"]
                print(content)
                return content
    except urllib.error.URLError as e:
        print(f"[Error] Failed to connect to Ollama at {OLLAMA_ENDPOINT}.", file=sys.stderr)
        print("Please ensure Ollama is running ('ollama serve').", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Ensure UTF-8 output on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Query local Qwen 2.5 Coder via Ollama")
    parser.add_argument("prompt", nargs="?", help="Prompt to send to the model")
    parser.add_argument("--file", "-f", help="Read input code or prompt from a file")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help=f"Model tag (default: {DEFAULT_MODEL})")
    parser.add_argument("--max-tokens", type=int, default=1024, help="Maximum generation tokens (default: 1024)")
    parser.add_argument("--no-stream", action="store_true", help="Disable streaming output")

    args = parser.parse_args()

    input_text = ""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as fp:
            input_text = fp.read()
    elif args.prompt:
        input_text = args.prompt
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(0)

    query_local_coder(
        prompt=input_text,
        model=args.model,
        max_tokens=args.max_tokens,
        stream=not args.no_stream
    )
