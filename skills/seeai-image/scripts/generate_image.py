#!/usr/bin/env python3
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse
from pathlib import Path


API_URL = "https://api.ai.let5see.xyz/v1/images/generations"
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def load_env(path):
    if not path:
        return
    env_path = Path(path)
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def output_path(base, index, total):
    path = Path(base)
    if total == 1:
        return path
    return path.with_name(f"{path.stem}-{index + 1}{path.suffix}")


def decode_images(body, out):
    payload = json.loads(body)
    items = payload.get("data") or []
    if not items:
        raise RuntimeError("response missing data[]")

    written = []
    for i, item in enumerate(items):
        b64 = item.get("b64_json")
        if not b64:
            raise RuntimeError(f"data[{i}] missing b64_json")
        raw = base64.b64decode(b64)
        path = output_path(out, i, len(items))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        written.append(path)
    return written


def request_image(args):
    load_env(args.env)
    api_key = os.environ.get(args.api_key_env) or os.environ.get("SEEAI_API_KEY")
    if not api_key:
        raise RuntimeError(f"missing {args.api_key_env}; set it in the environment or .env")

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
        "quality": args.quality,
        "output_format": args.format,
        "response_format": "b64_json",
        "n": args.n,
    }
    req = urllib.request.Request(
        args.api_url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Accept": "*/*",
            "Host": urlparse(args.api_url).netloc,
            "Connection": "keep-alive",
            "User-Agent": "curl/8.7.1",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as response:
            return decode_images(response.read(), args.out)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:1000]
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc


def self_test():
    assert output_path("image.png", 0, 1) == Path("image.png")
    assert output_path("image.png", 1, 3) == Path("image-2.png")
    sample = {"data": [{"b64_json": base64.b64encode(PNG_SIG + b"x").decode()}]}
    tmp = Path(os.environ.get("TEMP") or os.environ.get("TMPDIR") or ".") / "seeai-image-self-test.png"
    written = decode_images(json.dumps(sample).encode(), tmp)
    assert written == [tmp]
    assert tmp.read_bytes().startswith(PNG_SIG)
    tmp.unlink(missing_ok=True)
    env_tmp = tmp.with_suffix(".env")
    old = os.environ.pop("GEN_IMAGE_API_KEY", None)
    try:
        env_tmp.write_text('GEN_IMAGE_API_KEY="test-key"\n', encoding="utf-8")
        load_env(env_tmp)
        assert os.environ["GEN_IMAGE_API_KEY"] == "test-key"
    finally:
        env_tmp.unlink(missing_ok=True)
        if old is not None:
            os.environ["GEN_IMAGE_API_KEY"] = old
    print("self-test ok")


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Generate an image through the SeeAI image API.")
    parser.add_argument("--prompt", help="Image prompt text.")
    parser.add_argument("--out", default="image.png", help="Output image path.")
    parser.add_argument("--env", default=".env", help="Optional .env path containing GEN_IMAGE_API_KEY.")
    parser.add_argument("--api-key-env", default="GEN_IMAGE_API_KEY", help="Environment variable name for the API key.")
    parser.add_argument("--api-url", default=API_URL)
    parser.add_argument("--model", default="gpt-image-2")
    parser.add_argument("--size", default="3840x2160")
    parser.add_argument("--quality", default="high")
    parser.add_argument("--format", default="png")
    parser.add_argument("--n", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return args
    if not args.prompt:
        parser.error("--prompt is required unless --self-test is used")
    if args.n < 1:
        parser.error("--n must be >= 1")
    return args


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    if args.self_test:
        self_test()
        return 0
    try:
        for path in request_image(args):
            print(path)
        return 0
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
