# PULSE DRIVE 게임 개발 실습 노트

> **작성일:** 2026년 5월 2주차  
> **개발 환경:** Python 3.12 / pygame 2.6 / VS Code / Windows  
> **이번 주 주제:** 허브 월드 구현 + 전체 코드 버그 수정 및 최적화

---

## 📋 이번 주 목표

- [ ] 허브 월드(격납고) 배경 — TMX 타일맵 적용
- [ ] 허브 시설 오브젝트 위치 맵 레이아웃 기준으로 재배치
- [ ] 전체 코드 2회 정밀 검토 및 버그 수정
- [ ] 스프라이트 애니메이션 오류 전수 점검

---

## 1. AI에게 물어본 질문

### Q1. 스프라이트 시트에서 프레임 크기가 잘못 설정되면 어떻게 되나요?

> *"보스랑 적이 사용하는 모든 총알 스프라이트 이미지 다시 자세하게 분석해서 e_kla_bb 같은 케이스 없는지 확인하고 수정해줘"*

`e_kla_bb` 스프라이트를 분석하다가 발견한 문제였다. 원래 `fsz=16, 2프레임`으로 설정되어 있었는데, 실제로는 16px 프레임 하나 안에 8px짜리 탄환 2개가 나란히 묶여 있는 구조였다. AI와 함께 픽셀 단위 시각화로 확인했다.

```
y 4: ██       (2px) ← 뾰족한 꼭대기(노즈)
y 6: ████     (4px) ← 넓은 날개(몸체)
y10: ███      (3px) ← 가는 다리(꼬리)
```

`fsz=8, 4프레임`으로 수정하자 각 프레임에 탄환 1개씩 들어와 정상적인 애니메이션이 완성됐다. 이후 같은 문제를 가진 `e_nau_rok`, `e_nai_rok`, `e_nau_b` 등도 같은 방법으로 점검했다.

---

### Q2. 유도 미사일의 유도 기능이 제대로 안 되는 것 같은데, 코드 어디가 문제인가요?

> *"일반 유도 미사일의 유도 기능이 제대로 작동하지 않는 거 같아서 유도 기능 제대로 작동하는지 확인해주고 시너지 유도 강화도 한번 확인해줘"*

두 가지 버그를 발견했다.

**버그 1 — 적 추적이 발사 순간에만 동작하는 문제**

`player.py`의 `fire_all()`에서 `eref = list(self.enemies_ref)`로 **발사 시점의 스냅샷**을 만들어 미사일에 전달하고 있었다. 화면에 적이 없을 때 발사하면 빈 리스트(`[]`)가 전달되어 미사일이 끝까지 직선으로만 날아갔다.

```python
# 수정 전 (버그)
eref = list(self.enemies_ref)   # ← 발사 순간 스냅샷
w.fire(self, ..., eref, ...)

# 수정 후
w.fire(self, ..., self.enemies_ref, ...)  # ← Group 직접 전달
```

**버그 2 — 다발 발사 시 미사일 간격이 너무 좁은 문제**

`HomingWeapon.fire()`의 오프셋이 `[-20, 20]` 픽셀로 하드코딩되어 있었다. 1920×1080 해상도에서는 `sx(20) = 48px`이어야 하는데 20px 그대로 적용되어 미사일들이 거의 한 점에서 발사됐다.

```python
# 수정 전
offsets = {1:[0], 2:[-20,20], 3:[-30,0,30], ...}

# 수정 후 (해상도 보정)
o = sx(16)
offsets = {1:[0], 2:[-o, o], 3:[-o*2, 0, o*2], ...}
```

---

### Q3. TMX 타일맵 파일을 pygame에서 어떻게 배경으로 사용하나요?

> *"격납고 배경 파일을 만들었는데 게임 코드 확인하고 파일 중 적용 가능한 걸로 적용해서 맵에 맞게 오브젝트 위치도 수정해줘"*

Tiled로 제작한 `.tmx` + `.png` 타일셋 파일을 pygame에서 직접 렌더링하는 방법을 배웠다.

**TMX 파일 파싱 흐름:**
```
TMX → CSV 레이어 데이터 → 타일 ID 추출 → 타일셋 이미지에서 잘라내기 → pygame Surface에 blit
```

**flip 플래그 처리:**  
Tiled의 수평/수직 반전 정보는 타일 ID 상위 비트에 인코딩되어 있다.
```python
flip_h = bool(raw_val & 0x80000000)
flip_v = bool(raw_val & 0x40000000)
tile_id = raw_val & 0x1FFFFFFF
```

**시설 위치 계산:**  
타일맵(40×20)을 화면(1920×1080)에 맞게 스케일하면 타일 1개 크기가 `48×54px`가 된다. 시설 오브젝트의 위치도 타일 좌표 기준으로 계산했다.
```python
TILE_W, TILE_H = 48, 54

# 출격 게이트: col 19, row 3
launch_x = (19 * TILE_W + TILE_W//2) / WIDTH   # = 0.487
launch_y  = (3  * TILE_H + TILE_H//2) / HEIGHT  # = 0.175
```

---

## 2. 시행착오 및 해결 과정

### 시행착오 1 — 스프라이트 방향 판별 자동화의 한계

처음에는 **상단/하단 밝기 비교**로 스프라이트 방향을 자동 판별하는 스크립트를 만들었다. 결과는 다음과 같았다.

```
e_kla_bb: top=15.3  bot=20.8  → 판별 실패 (차이 너무 작음)
```

밝기 차이가 5 이하일 때 오판이 발생했다. **해결책:** 픽셀별 형태 분석(`y행 당 밝은 픽셀 수`)으로 노즈(뾰족한 꼭대기)의 실제 위치를 찾았다.

```
y 4: ██  (2px)  ← 노즈 → 원본 상단에 있음 → flip_v=True 필요
y 6: ████ (4px) ← 날개
y10: ███ (3px)  ← 꼬리
```

→ **교훈:** 자동화 스크립트도 틀릴 수 있다. 결과를 맹신하지 말고 픽셀 시각화로 직접 확인해야 한다.

---

### 시행착오 2 — `fsz=8`로 수정했다가 다시 `fsz=16`으로 되돌린 사례

`e_nau_rok` 스프라이트를 분석하다가 `fsz=16`이 잘못이라고 판단해서 `fsz=8`로 수정했는데, 오히려 더 이상해졌다.

- 수정 전: `fsz=16 → 6프레임` (16px 안에 2개 서브프레임 묶임)
- 잘못 수정: `fsz=8 → 12프레임` (로켓 몸체가 프레임 경계에서 반으로 잘림)
- 최종 수정: `fsz=16 → 6프레임` 유지, 단 `flip_v=True` 추가

**결정적 판별 방법:** 특정 y행의 밝은 픽셀 **시작 x 위치** 배열로 실제 주기를 직접 측정했다.

```python
y17 = [(arr[17,x,:].sum() > 40) for x in range(w)]
starts = [x for x in range(w) if y17[x] and (x==0 or not y17[x-1])]
# starts = [7, 23, 39, 55, 71, 87] → 주기 = 16px
```

→ **교훈:** 실제 픽셀 주기를 수치로 측정해야 한다. 눈대중이나 추측으로 결정하면 오히려 망친다.

---

### 시행착오 3 — `rhythm_storm` 시너지가 게임에서 전혀 작동하지 않던 문제

`upgrade.py`에서는 분명히 `player._synergy_rhythm_storm = True`로 플래그를 설정하는데, 실제 게임에서 PERFECT를 맞춰도 10발 발사가 일어나지 않았다.

**원인:** `SpreadWeapon.fire()`에서 이 플래그를 한 번도 체크하지 않고 있었다.

```python
# upgrade.py (설정함)
setattr(player, '_synergy_rhythm_storm', True)

# weapon.py SpreadWeapon.fire() (체크 안 함 ← 버그)
pellets = 8 if judgment == 'PERFECT' else 5  # rhythm_storm 무시!
```

```python
# 수정 후
rhythm_storm = getattr(player, '_synergy_rhythm_storm', False)
if judgment == 'PERFECT' and rhythm_storm:
    pellets = 10
elif judgment == 'PERFECT':
    pellets = 8
else:
    pellets = 5
```

→ **교훈:** 시스템 연결부(설정 코드 ↔ 적용 코드)가 분리되어 있으면 한쪽만 작성하고 반쪽을 잊기 쉽다. 기능을 추가할 때 "설정하는 곳"과 "실제로 사용하는 곳"을 동시에 작성해야 한다.

---

## 3. 배운 점

### 📌 스프라이트 시트 분석 방법

타일 애니메이션 스프라이트의 올바른 프레임 크기를 찾는 신뢰할 수 있는 방법:

1. **밝기 분석 금지** — 상단/하단 밝기 비교는 오판이 잦다
2. **픽셀 주기 측정** — 특정 y행에서 밝은 픽셀 시작 위치 배열로 간격을 직접 계산
3. **픽셀맵 시각화** — `█`, `▒`, `.` 문자로 직접 눈으로 모양을 확인

```python
# 신뢰할 수 있는 주기 측정 코드
y_row = [(arr[target_y, x, :].sum() > 40) for x in range(w)]
starts = [x for x in range(w) if y_row[x] and (x==0 or not y_row[x-1])]
period = starts[1] - starts[0]  # ← 이게 올바른 fsz
```

---

### 📌 해상도 대응 — `sx()`, `sy()` 함수의 중요성

게임 내 모든 픽셀 값에 해상도 스케일 함수를 붙여야 한다. 하드코딩하면 1920×1080에서 의도치 않은 결과가 나온다.

```python
# 잘못된 예 (800×600 기준 픽셀이 그대로 사용됨)
offsets = [-20, 0, 20]

# 올바른 예
o = sx(16)   # 800×600 기준 16px → 1920×1080에서 약 38px
offsets = [-o, 0, o]
```

---

### 📌 pygame의 Group과 list() 스냅샷 차이

`pygame.sprite.Group`은 **살아있는 스프라이트의 동적 컨테이너**다. `list(group)`으로 스냅샷을 만들면 그 이후에 추가/제거된 스프라이트가 반영되지 않는다.

```
list(enemies) → 발사 시점의 복사본 → 이후 새 적 등장해도 추적 불가
enemies (Group) → 항상 현재 살아있는 적만 포함
```

유도 미사일처럼 **발사 이후에도 계속 타깃을 갱신해야 하는 경우**는 반드시 Group 자체를 전달해야 한다.

---

### 📌 TMX 타일맵을 pygame에서 직접 렌더링하는 법

Tiled 에디터로 만든 `.tmx`를 pygame에서 전용 라이브러리 없이 직접 파싱해서 쓸 수 있다.

```python
# 핵심 파싱 로직
raw_val = int(csv_cell)
flip_h  = bool(raw_val & 0x80000000)
flip_v  = bool(raw_val & 0x40000000)
tile_id = raw_val & 0x1FFFFFFF   # 실제 타일 ID

# 타일셋에서 해당 타일 잘라내기
gid = tile_id - 1               # firstgid=1이므로 -1
col = gid % tileset_cols
row = gid // tileset_cols
tile = tileset_arr[row*32:(row+1)*32, col*32:(col+1)*32]

# 반전 처리
if flip_h: tile = tile[:, ::-1, :]
if flip_v: tile = tile[::-1, :, :]
```

---

### 📌 코드 리뷰의 중요성 — dead code와 누락된 연결부

두 차례 전체 코드 리뷰에서 발견된 주요 패턴:

| 유형 | 사례 | 영향 |
|---|---|---|
| Dead code | `pbullet_list = list(self.pbullets)` 생성 후 미사용 | 매 프레임 불필요한 리스트 복사 |
| 누락된 연결 | `rhythm_storm` 설정만 하고 적용 안 함 | 시너지 기능 완전 무효화 |
| 이중 로드 | `TorpedoBullet`이 `homing` 스프라이트 로드 후 버림 | 불필요한 파일 I/O |
| 상태 누락 | `S_UPGRADE` 상태에서 배경 업데이트 미호출 | 업그레이드 메뉴 중 배경 정지 |

**정기적인 코드 리뷰** 습관이 게임 품질에 직접 영향을 준다는 걸 실감했다.

---

## 📁 이번 주 수정 파일 목록

| 파일 | 주요 변경 내용 |
|---|---|
| `hub.py` | TMX 맵 기반 격납고 배경, 시설 위치 재배치, 플레이어 이동 경계 |
| `settings.py` | `load_proj_frames()` 배경 fill 버그 수정, 패딩 로직 제거 |
| `weapon.py` | `rhythm_storm` 시너지 적용, `TorpedoBullet` 이중 로드 제거, `list()` 복사 최적화 |
| `player.py` | 유도 미사일 Group 직접 전달, `fire_all()` 이중 루프 통합 |
| `main.py` | `pbullet_list` dead code 제거, `S_UPGRADE` 배경 업데이트 추가 |
| `enemy.py` | `fade_surf` 매 프레임 생성 → 캐시 최적화 |
| `boss.py` | `overlay Surface` 매 프레임 생성 → 캐시 최적화 |

---

## 🔜 다음 주 계획

- 허브 월드 `main.py`와의 실제 연동 (`S_HUB` 상태 추가)
- 에테르 화폐 시스템 — 런 종료 후 에테르 획득 → 저장
- 거울 강화 영구 업그레이드가 런 시작 시 실제로 적용되는지 테스트
- 추가 제안받은 시스템 검토 (포커스 샷 모드, 탄환 흡수 패시브)

---

*PULSE DRIVE 개발 실습 노트 — Game Software, Hoseo University*
