# Pollinations 무료 API로 33명 캐릭터 이미지 자동 생성 (미니PC 실행, GPU 불필요)
"""
실행: gen-pollinations.bat  (또는 python scripts/gen_pollinations.py)
- 각 캐릭터를 직업·칭호별로 다르게 설계한 프롬프트로 생성.
- 결과: out_gen/<id>.png (이미 있으면 건너뜀 → 특정 캐릭터만 지우고 재실행하면 그 캐릭만 다시 뽑음)
- 마음에 안 드는 캐릭터는 아래 CHARS 의 설명만 고쳐서 그 png 지우고 재실행.
- 인터넷만 있으면 됨(생성은 Pollinations 서버가 함). Python 3 필요.
"""
import os
import sys
import time
import hashlib
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from char_prompts import CHARS, full_prompt  # 33명 프롬프트 공유

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("SPRITE_OUT", os.path.join(_REPO, "out_gen"))
MODEL = os.environ.get("POLL_MODEL", "flux")
W = int(os.environ.get("POLL_W", "1024"))
H = int(os.environ.get("POLL_H", "1024"))
RETRIES = int(os.environ.get("POLL_RETRIES", "6"))  # 500 잦으면 늘리기

def build_url(prompt, seed):
    enc = urllib.parse.quote(prompt, safe="")
    return (f"https://image.pollinations.ai/prompt/{enc}"
            f"?width={W}&height={H}&nologo=true&model={MODEL}&seed={seed}")


def main():
    os.makedirs(OUT, exist_ok=True)
    ids = list(CHARS)
    print(f"{len(ids)}명 생성 시작 → {OUT}")
    for i, cid in enumerate(ids, 1):
        path = os.path.join(OUT, cid + ".png")
        if os.path.exists(path):
            print(f"[{i}/{len(ids)}] 건너뜀 {cid} (이미 있음)")
            continue
        seed = int(hashlib.md5(cid.encode()).hexdigest()[:6], 16)
        url = build_url(full_prompt(cid), seed)
        ok = False
        for attempt in range(RETRIES):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=180) as r:
                    data = r.read()
                if len(data) < 2000:
                    raise ValueError("응답이 너무 작음(생성 실패)")
                with open(path, "wb") as f:
                    f.write(data)
                print(f"[{i}/{len(ids)}] {cid}.png  ({len(data)//1024} KB)")
                ok = True
                break
            except Exception as e:
                wait = min(40, 8 * (attempt + 1))  # 서버 500 대비 넉넉히 대기
                print(f"    재시도 {attempt + 1}/{RETRIES}: {cid} — {e} (대기 {wait}s)")
                time.sleep(wait)
        if not ok:
            print(f"    [실패] {cid} — 나중에 다시 실행하면 그 캐릭만 재시도됩니다")
        time.sleep(3)  # 서버 배려
    print("완료. 결과 폴더:", OUT)


try:
    main()
except KeyboardInterrupt:
    print("\n[중단] 사용자가 멈춤. 다시 실행하면 안 된 것만 이어서 생성합니다.")
