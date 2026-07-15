# Together AI(Flux)로 33명 캐릭터 이미지 자동 생성 — 안정적 유료 경로
"""
실행: gen-together.bat  (또는 python scripts/gen_together.py)
준비: Together 가입(가입 무료 크레딧 있음) → API 키 발급 → 아래처럼 환경변수 설정 후 실행.
      Windows:  set TOGETHER_API_KEY=여기에_키   그다음  python scripts\gen_together.py
결과: out_together/<id>.png (이미 있으면 건너뜀)
프롬프트는 scripts/char_prompts.py 에서 공유(모든 경로 동일).
"""
import os
import sys
import time
import json
import base64
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from char_prompts import CHARS, full_prompt

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("SPRITE_OUT", os.path.join(_REPO, "out_together"))
API_KEY = os.environ.get("TOGETHER_API_KEY", "")
MODEL = os.environ.get("TOGETHER_MODEL", "black-forest-labs/FLUX.1-schnell-Free")
W = int(os.environ.get("POLL_W", "1024"))
H = int(os.environ.get("POLL_H", "1024"))
RETRIES = int(os.environ.get("POLL_RETRIES", "5"))
ENDPOINT = "https://api.together.xyz/v1/images/generations"


def gen_one(prompt):
    body = {"model": MODEL, "prompt": prompt, "width": W, "height": H, "n": 1, "steps": 4}
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        res = json.loads(r.read())
    item = res["data"][0]
    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])
    url = item["url"]  # url 로 오면 내려받기
    dreq = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(dreq, timeout=180) as d:
        return d.read()


def main():
    if not API_KEY:
        print("[에러] TOGETHER_API_KEY 환경변수가 없습니다.")
        print("  Together 가입 → API 키 발급 → set TOGETHER_API_KEY=키  후 다시 실행하세요.")
        return
    os.makedirs(OUT, exist_ok=True)
    ids = list(CHARS)
    print(f"{len(ids)}명 생성 시작(Together/{MODEL}) → {OUT}")
    for i, cid in enumerate(ids, 1):
        path = os.path.join(OUT, cid + ".png")
        if os.path.exists(path):
            print(f"[{i}/{len(ids)}] 건너뜀 {cid} (이미 있음)")
            continue
        ok = False
        for attempt in range(RETRIES):
            try:
                data = gen_one(full_prompt(cid))
                if len(data) < 2000:
                    raise ValueError("응답이 너무 작음")
                with open(path, "wb") as f:
                    f.write(data)
                print(f"[{i}/{len(ids)}] {cid}.png  ({len(data)//1024} KB)")
                ok = True
                break
            except Exception as e:
                wait = min(30, 6 * (attempt + 1))
                print(f"    재시도 {attempt + 1}/{RETRIES}: {cid} — {e} (대기 {wait}s)")
                time.sleep(wait)
        if not ok:
            print(f"    [실패] {cid} — 다시 실행하면 재시도됩니다")
        time.sleep(1)
    print("완료. 결과 폴더:", OUT)


try:
    main()
except KeyboardInterrupt:
    print("\n[중단] 다시 실행하면 안 된 것만 이어서 생성합니다.")
