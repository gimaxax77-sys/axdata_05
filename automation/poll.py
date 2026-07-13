# 저장소 폴링 실행기 — 밖에서 올린 명령을 PC가 받아 실행(안전: PC가 밖으로 나가 확인)
"""
동작:
  1) git pull 로 최신 명령 받기
  2) jobs/inbox/ 의 명령 파일을 하나씩 처리(화이트리스트만 실행)
  3) 실행 로그를 jobs/done/ 에 남기고 명령 파일을 done 으로 이동
  4) 결과를 git commit + push (폰에서 실행 여부·로그 확인 가능)

명령 파일 형식(jobs/inbox/아무이름.txt, 한 줄):
  render <Body> <Action[,Action2,...]>
  예) render Knight Idle
      render Knight Idle,Attack
      render Barbarian Idle

보안: 'render' 명령만 허용하고, Body/Action 은 영문/숫자/언더스코어/콤마만 통과.
      알 수 없는 명령·이상한 문자는 실행하지 않고 로그만 남긴다.
"""
import os
import re
import subprocess
import datetime

# ===================== CONFIG (본인 PC에 맞게 수정) =====================
BLENDER = r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
# 이 저장소 루트(자동 계산: automation/ 의 상위)
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDER_SCRIPT = os.path.join(REPO_DIR, "scripts", "render_sprites.py")
# =====================================================================

INBOX = os.path.join(REPO_DIR, "jobs", "inbox")
DONE = os.path.join(REPO_DIR, "jobs", "done")
SAFE = re.compile(r"^[A-Za-z0-9_,]+$")   # Body/Action 허용 문자


def run(cmd, env=None):
    """리스트 인자로만 실행(shell=False) → 명령 주입 방지."""
    return subprocess.run(cmd, cwd=REPO_DIR, env=env, capture_output=True, text=True)


def git(*args):
    return run(["git"] + list(args))


def process_job(path):
    name = os.path.basename(path)
    with open(path, encoding="utf-8") as f:
        line = f.read().strip()
    log = [f"# {name}", f"명령: {line}", f"시각: {datetime.datetime.now().isoformat(timespec='seconds')}"]
    parts = line.split()

    if len(parts) >= 3 and parts[0] == "render" and SAFE.match(parts[1]) and SAFE.match(parts[2]):
        body, actions = parts[1], parts[2]
        env = dict(os.environ, SPRITE_BODIES=body, SPRITE_ACTIONS=actions)
        log.append(f"실행: blender render body={body} actions={actions}")
        r = run([BLENDER, "--background", "--python", RENDER_SCRIPT], env=env)
        log.append("=== STDOUT ===")
        log.append(r.stdout[-4000:])
        if r.returncode != 0:
            log.append("=== STDERR ===")
            log.append(r.stderr[-2000:])
        log.append(f"종료코드: {r.returncode}")
    else:
        log.append("[거부] 허용되지 않은 명령 형식 — 실행 안 함. 형식: render <Body> <Action[,Action2]>")

    # 로그 저장 + 명령 파일 done 으로 이동
    os.makedirs(DONE, exist_ok=True)
    with open(os.path.join(DONE, name + ".log"), "w", encoding="utf-8") as f:
        f.write("\n".join(log) + "\n")
    os.replace(path, os.path.join(DONE, name))
    print(f"[처리] {name}")


def main():
    os.makedirs(INBOX, exist_ok=True)
    os.makedirs(DONE, exist_ok=True)
    # 1) 최신 명령 받기
    git("pull", "--rebase", "--autostash")
    # 2) inbox 처리
    jobs = [os.path.join(INBOX, f) for f in sorted(os.listdir(INBOX))
            if f.endswith(".txt")]
    if not jobs:
        print("대기 명령 없음.")
        return
    for j in jobs:
        try:
            process_job(j)
        except Exception as e:
            print(f"[에러] {j}: {e}")
    # 3) 결과 커밋·푸시
    git("add", "jobs")
    c = git("commit", "-m", "auto: 폴링 명령 처리 결과")
    if c.returncode == 0:
        for _ in range(3):
            if git("push").returncode == 0:
                print("결과 푸시 완료.")
                break
            git("pull", "--rebase", "--autostash")


if __name__ == "__main__":
    main()
