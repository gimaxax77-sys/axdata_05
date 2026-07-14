# Pollinations 무료 API로 33명 캐릭터 이미지 자동 생성 (미니PC 실행, GPU 불필요)
"""
실행: gen-pollinations.bat  (또는 python scripts/gen_pollinations.py)
- 각 캐릭터를 직업·칭호별로 다르게 설계한 프롬프트로 생성.
- 결과: out_gen/<id>.png (이미 있으면 건너뜀 → 특정 캐릭터만 지우고 재실행하면 그 캐릭만 다시 뽑음)
- 마음에 안 드는 캐릭터는 아래 CHARS 의 설명만 고쳐서 그 png 지우고 재실행.
- 인터넷만 있으면 됨(생성은 Pollinations 서버가 함). Python 3 필요.
"""
import os
import time
import hashlib
import urllib.parse
import urllib.request

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("SPRITE_OUT", os.path.join(_REPO, "out_gen"))
MODEL = os.environ.get("POLL_MODEL", "flux")
W = int(os.environ.get("POLL_W", "1024"))
H = int(os.environ.get("POLL_H", "1024"))
RETRIES = int(os.environ.get("POLL_RETRIES", "6"))  # 500 잦으면 늘리기

# 모든 캐릭터에 공통으로 붙는 확정 레시피(큰머리 치비 · 무기없음 · 투구없음 · 흰배경 · T포즈)
STYLE = (
    "cute big head chibi, stylized 3D game character render, smooth shading, glossy, "
    "highly detailed, vibrant colors, full body standing, "
    "both arms outstretched to the sides in a T-pose, "
    "both hands completely empty and open, palms open and visible, holding nothing in hands, "
    "unarmed, no weapon, no sword, no dagger, no blade, no bow, no staff, no wand, no shield, no held item, "
    "face and hair fully visible, no helmet, cute rounded symmetric face, clear eyes nose mouth, "
    "pure white background, no base, centered"
)

# 33명 — 직업/칭호별로 전부 다르게(머리·복장·색·성별 다양화). 손보고 싶으면 설명만 수정.
CHARS = {
    "kael":     "a brave boy fire warrior, spiky black hair with red tips, red and gold light battle armor with ember glow",
    "luna":     "a gentle girl moonlight priestess, long silver hair, flowing white and pale blue holy robe with a glowing crescent moon halo",
    "gwen":     "a stalwart boy frost guardian in armor, short blue hair, heavy blue and silver ice plate armor with frost crystals",
    "ciel":     "a lively girl wind dancer, short teal green bob hair, light flowing green and white dancer outfit with leaf ribbons",
    "bran":     "a burly boy earth defender, brown hair, massive brown and stone grey heavy armor with rocky texture",
    "ael":      "a serene boy light oracle, medium blonde hair, elegant white and gold prophet robe with glowing runes",
    "ara":      "a fierce girl storm warrior, windswept dark violet hair, sleek black and silver light armor with crackling energy",
    "mir":      "a young rookie fighter boy, messy brown hair, simple green leather and cloth training armor",
    "pyra":     "a mighty girl crimson bulwark defender, red ponytail, huge crimson and gold heavy plate armor with flame engravings",
    "frost":    "a cool boy glacier rogue, slick pale icy blue hair, dark navy and ice tight leather armor with frost mist",
    "marina":   "a kind girl tide healer, wavy aqua blue hair, soft teal and white healer robe with seashell and pearl accents",
    "signe":    "a disciplined boy frontline soldier, short auburn hair, red and bronze military uniform with a cape",
    "aurel":    "a noble boy dawn holy knight in radiant white and gold light armor, golden hair, sunrise glow",
    "nyx":      "a mysterious girl abyss oracle, long dark purple hair, deep purple and black star patterned robe with cosmic glow",
    "kai":      "a cheeky boy rookie rogue, scruffy brown hair, simple green and brown leather outfit with a small satchel",
    "vera":     "a deadly girl shadow rogue, sleek black hair, tight black and dark purple leather with the hood down",
    "robin":    "a nimble boy forest ranger, tousled green brown hair, green leather scout armor with a leaf cloak",
    "sylas":    "a graceful boy light ranger, silver white hair, white and gold ranger outfit with glowing feather accents",
    "elara":    "a spirited girl flame mage, long fiery red hair, red and orange wizard robe and pointed hat with ember sparks",
    "oriel":    "an eerie boy chaos mage, wild dark violet hair, black and purple ornate wizard robe and hat with swirling chaos energy",
    "toren":    "a young rookie shield trainee boy, short brown hair, basic grey and green partial plate armor",
    "kordan":   "a huge boy flame rampart defender, red mohawk hair, massive red and black volcanic heavy armor with lava cracks",
    "ymir":     "a giant stocky boy glacier defender, white hair, bulky pale blue and white ice armor with huge frozen pauldrons",
    "nella":    "a sweet girl apprentice priestess, short light pink hair, simple white and cream acolyte robe with a small holy symbol",
    "jax":      "a rough boy street rogue, red spiky undercut hair, worn red and black street leather with bandages",
    "mira":     "a silent girl mist rogue, pale blue grey hair, misty grey and teal light ninja outfit with a face scarf down",
    "raven":    "a brooding boy shadow rogue, black hair with purple streaks, dark shadowy black cloak and leather with wispy shadow",
    "finn":     "a friendly boy apprentice ranger, sandy brown hair, brown and green hunter leathers with fur trim",
    "lyra":     "an elegant girl moonlight ranger, long silver lavender hair, white and silver ranger dress with crescent motifs",
    "seren":    "a proud boy sky ranger, orange red hair, red and gold ornate ranger armor with a feathered wing motif",
    "pip":      "a tiny cute boy apprentice mage, green bowl cut hair, oversized green and brown wizard robe and floppy hat",
    "thalia":   "a calm girl frost mage, long icy blue hair, blue and white wizard robe and hat with snowflake patterns",
    "nocturne": "a wise young looking boy dark sage, long black hair, black and deep purple grand mage robe with silver constellations",
}


def build_url(desc, seed):
    prompt = desc + ", " + STYLE
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
        url = build_url(CHARS[cid], seed)
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
