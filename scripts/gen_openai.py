# OpenAI gpt-image-1 mini로 33명 캐릭터 이미지 자동 생성 — Bing(DALL-E) 품질 경로
"""
실행: gen-openai.bat  (또는 python scripts/gen_openai.py)
준비: OpenAI 플랫폼 가입 → 결제수단·소액 크레딧 → API 키 발급 →
      Windows:  set OPENAI_API_KEY=여기에_키   그다음  python scripts\gen_openai.py
결과: out_openai/<id>.png (이미 있으면 건너뜀)
품질: Gim이 좋아했던 균형 잡힌(빅헤드 아닌) DALL-E 계열. 장당 약 $0.005(저품질 모드).
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
OUT = os.environ.get("SPRITE_OUT", os.path.join(_REPO, "out_openai"))
API_KEY = os.environ.get("OPENAI_API_KEY", "")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-image-1-mini")
QUALITY = os.environ.get("OPENAI_QUALITY", "low")   # low=가장 저렴, medium/high 가능
SIZE = os.environ.get("OPENAI_SIZE", "1024x1024")
RETRIES = int(os.environ.get("POLL_RETRIES", "5"))
ENDPOINT = "https://api.openai.com/v1/images/generations"


def gen_one(prompt):
    body = {"model": MODEL, "prompt": prompt, "size": SIZE, "n": 1, "quality": QUALITY}
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=240) as r:
        res = json.loads(r.read())
    item = res["data"][0]
    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])
    url = item["url"]
    dreq = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(dreq, timeout=180) as d:
        return d.read()


def main():
    if not API_KEY:
        print("[에러] OPENAI_API_KEY 환경변수가 없습니다.")
        print("  OpenAI 가입 → API 키 발급 → set OPENAI_API_KEY=키  후 다시 실행하세요.")
        return
    os.makedirs(OUT, exist_ok=True)
    ids = list(CHARS)
    print(f"{len(ids)}명 생성 시작(OpenAI/{MODEL}/{QUALITY}) → {OUT}")
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
