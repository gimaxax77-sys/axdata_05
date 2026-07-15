# 33명 캐릭터 프롬프트 한 곳 관리 (모든 생성 경로가 이 파일을 공유)
"""
여기 STYLE(공통 레시피)과 CHARS(33명 개별 설명)만 고치면
Pollinations / Together / OpenAI 모든 경로에 동일하게 반영됩니다.
"""

# 모든 캐릭터에 공통으로 붙는 확정 레시피(큰머리 치비 · 무기없음 · 투구없음 · 흰배경 · 자연 자세)
STYLE = (
    "cute big head chibi, stylized 3D game character render, smooth shading, glossy, "
    "highly detailed, vibrant colors, full body standing, "
    "relaxed natural standing pose, both arms lowered down at the sides, "
    "hands relaxed and loosely closed, simple clean small hands, empty hands holding nothing, "
    "unarmed, no weapon, no sword, no dagger, no blade, no bow, no staff, no wand, no shield, no held item, "
    "no extra fingers, no deformed hands, "
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


def full_prompt(cid):
    """캐릭터 고유 설명 + 공통 STYLE 을 이어붙인 최종 프롬프트."""
    return CHARS[cid] + ", " + STYLE
