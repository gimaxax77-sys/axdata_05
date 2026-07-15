<!-- 캐릭터 일괄 생성 3개 경로 사용법 -->
# 캐릭터 일괄 생성 — 3개 경로

프롬프트(33명)는 `scripts/char_prompts.py` 한 곳에서 관리합니다. 세 경로가 이 파일을 공유하므로, 캐릭터 설명을 고치면 모든 경로에 동일하게 반영됩니다.

| 경로 | 실행 파일 | 결과 폴더 | 비용 | 특징 |
|---|---|---|---|---|
| **무료 (Pollinations)** | `gen-pollinations.bat` | `out_gen/` | 0원 | 무료·flux, 다만 500 불안정 |
| **유료 flux (Together)** | `gen-together.bat` | `out_together/` | 약 130원/33장 | 안정적·flux, 가입 무료크레딧 |
| **Bing품질 (OpenAI)** | `gen-openai.bat` | `out_openai/` | 약 220원/33장 | 균형비율 DALL-E 계열 품질 |
| **DALL-E 풀 (OpenAI)** | `gen-openai-full.bat` | `out_openai_full/` | 약 1,300원/33장 | DALL-E 3 최고 품질(균형비율). `hd`로 바꾸면 $0.08 |

각 경로가 **다른 폴더**에 저장하므로, 셋을 다 돌려 **나란히 비교**할 수 있습니다.

## 준비 — API 키 (유료 경로만)

**Together**
1. https://api.together.ai 가입 (가입 시 무료 크레딧).
2. 대시보드에서 **API Key** 발급·복사.
3. `gen-together.bat` 실행 → 키 붙여넣기.

**OpenAI**
1. https://platform.openai.com 가입 → Billing에 소액 충전.
2. **API keys** 에서 키 발급·복사.
3. `gen-openai.bat` 실행 → 키 붙여넣기.

무료 경로(Pollinations)는 키가 필요 없습니다.

## 공통 사용법
- 이미 있는 png는 **건너뜁니다**. 특정 캐릭터만 다시 뽑으려면 그 png를 지우고 재실행합니다.
- 마음에 안 드는 캐릭터는 `scripts/char_prompts.py` 의 설명만 고치고 그 png를 지운 뒤 재실행합니다.
- Python 3 필요(없으면 https://www.python.org/downloads/ 에서 설치, "Add to PATH" 체크).

## 참고
- 3개 폴더의 같은 캐릭터를 비교해 **가장 좋은 경로**를 정한 뒤, 그 폴더 결과로 3D 변환·렌더로 넘어갑니다.
