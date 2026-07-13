# 렌더 자동화 (야간 예약 + 원격 폴링)

PC가 **켜져 있고 로그인된 상태** 에서 동작합니다. 두 가지 자동화를 제공합니다.

## 사전 준비
- Blender 4.2 설치, `scripts/render_sprites.py` 의 CONFIG 경로 설정(→ 상위 `README.md`).
- `automation/poll.py` 상단 `BLENDER` 경로를 본인 설치에 맞게 수정.
- Python 이 PATH 에 있어야 함(`python --version` 확인).

---

## 1) 야간 자동 렌더 (작업 스케줄러)

매일 밤 정해진 시각에 `render.bat`(= render_sprites.py) 자동 실행.

**설치**: `automation\setup_schedule.bat` 를 **관리자 권한으로** 더블클릭.
- `SpriteNightlyRender` : 매일 23:00 렌더 실행
- `SpritePoll` : 10분마다 폴링(아래 2번)

**확인**: `schtasks /query /tn SpriteNightlyRender`
**해제**: `schtasks /delete /tn SpriteNightlyRender /f`
**시각 변경**: setup_schedule.bat 의 `/st 23:00` 수정 후 재실행.

> 스케줄러 등록이 잘 안 되면 **작업 스케줄러(GUI)** 에서 수동 등록해도 됩니다(트리거=매일, 동작=render.bat).

---

## 2) 원격 폴링 (밖에서 명령 → PC가 실행)

**보안**: PC가 밖으로 나가 저장소를 확인하는 방식이라, 외부에서 PC로 들어오지 않습니다(안전).

### 동작 흐름
1. Gim이 폰/PC에서 저장소 `jobs/inbox/` 에 명령 파일(.txt)을 올림(커밋).
2. PC의 `poll.py`(10분마다)가 `git pull` 로 명령을 받아 **화이트리스트만** 실행.
3. 실행 로그를 `jobs/done/<이름>.log` 로 남기고 명령을 `done` 으로 이동 → **커밋·푸시**.
4. Gim은 폰에서 `jobs/done/` 의 로그로 실행 결과 확인.

### 명령 형식 (`jobs/inbox/아무이름.txt`, 한 줄)
```
render <Body> <Action[,Action2,...]>
```
예시:
```
render Knight Idle
render Knight Idle,Attack
render Barbarian Idle
```

### 폰에서 명령 보내는 법 (GitHub 앱/웹)
1. 저장소 `jobs/inbox/` 로 이동 → **Add file → Create new file**.
2. 파일명 예: `job1.txt`, 내용: `render Knight Idle`.
3. Commit. → 다음 폴링(≤10분)에 PC가 실행하고 결과를 `jobs/done/` 에 올림.

### 안전장치
- `render` 명령만 허용. Body/Action 은 영문·숫자·언더스코어·콤마만 통과.
- 그 외 명령·이상 문자는 **실행하지 않고 로그만** 남김.
- 실행은 리스트 인자(shell 미사용)로만 → 명령 주입 불가.

---

## 수동 테스트
- 폴링 1회: `automation\poll.bat` 더블클릭(또는 `python automation\poll.py`).
- 야간 렌더 즉시: 상위 `render.bat` 더블클릭.
