<!-- 오후 10시 PC 작업 체크리스트 -->
# 🌙 오후 10시 PC 작업 체크리스트 (2026-07-13)

> PC(GPU) 작업. 위에서 아래로 순서대로. 결과는 `research.md`에 기록.

## 0. 준비 (에셋 · 선택)
- [ ] (선택) Quaternius 몬스터 1개 — https://quaternius.itch.io/lowpoly-animated-monsters (CC0)
- [x] KayKit Adventurers + Character Animations — 이미 받음

## 1. 기사 스프라이트 렌더 검증 ⭐ (핵심)
자동 스크립트로 시도(권장):
- [ ] `scripts/render_sprites.py` 의 `KAYKIT` · `OUT_DIR` 경로 수정
- [ ] 실행: `blender --background --python scripts/render_sprites.py` (또는 `render.bat`)
- [ ] `OUT_DIR` 에 `knight_idle.png` 생성 확인
- [ ] 색·각도·크기 확인 → 필요시 `CAMERA_DIR` / `ACTIONS`(실제 액션명) 조정
- (막히면) 수동 SOP: 게임팩 `docs/SPRITE_WORKFLOW.md` 따라가기

## 2. 렌더 자동화 설정 🆕 (오늘 추가)
- [ ] `automation/poll.py` 의 `BLENDER` 경로 수정
- [ ] `automation/setup_schedule.bat` **관리자 권한**으로 실행
      → 야간 렌더(23:00) + 폴링(10분) 등록
- [ ] 등록 확인: `schtasks /query /tn SpritePoll`
- [ ] **폴링 테스트**: 폰에서 `jobs/inbox/job1.txt` 생성, 내용 `render Knight Idle` → 커밋
      → 10분 내 `jobs/done/` 에 로그 올라오는지 확인

## 3. 확장 (1·2 성공 후)
- [ ] `BODIES` / `ACTIONS` 늘려 전 캐릭터 배치 렌더
- [ ] KayKit **Skeletons**(적) 또는 Quaternius 몬스터 경로 추가해 몬스터 렌더
      (게임팩 `docs/ASSET_SOURCES.md` 링크)

## 4. 마무리
- [ ] 구운 PNG를 게임팩 규격 `assets/char/<concept>/<id>.png` 로 배치(선택)
- [ ] 오늘 진행·결과를 `research.md` 에 기록

---
### 참고 문서
- 이 저장소: `README.md` · `automation/README.md`
- 게임팩(axdata_01): `docs/SPRITE_WORKFLOW.md` · `ART_STRATEGY.md` · `ASSET_SOURCES.md`
