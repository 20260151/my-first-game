# 6주차 실습 기록

## 사용한 에셋

### 이미지

| 파일명 | 출처 |
|---|---|
| Main_Ship_-_Base_-_Full_health.png | itch.io — Void Main Ship (Foozle, CC0) |
| Main_Ship_-_Engines_-_Base_Engine_-_Spritesheet.png | itch.io — Void Main Ship (Foozle, CC0) |
| Main_Ship_-_Engines_-_Supercharged_Engine_-_Spritesheet.png | itch.io — Void Main Ship (Foozle, CC0) |
| Main_Ship_-_Engines_-_Base_Engine.png (글로우) | itch.io — Void Main Ship (Foozle, CC0) |
| Main_Ship_-_Engines_-_Supercharged_Engine.png (글로우) | itch.io — Void Main Ship (Foozle, CC0) |
| Kla_ed_-_Fighter/Bomber/Battlecruiser_-_Base.png | itch.io — Void Fleet Pack 1 Kla'ed (Foozle, CC0) |
| Nairan_-_Fighter/Frigate/Dreadnought_-_Base.png | itch.io — Void Fleet Pack 2 Nairan (Foozle, CC0) |
| Nautolan_Ship_-_Frigate/Dreadnought_-_Base.png | itch.io — Void Fleet Pack 3 Nautolan (Foozle, CC0) |
| Kla_ed_-_Fighter_-_Destruction.png | OpenGameArt — Void Main Ship 시리즈 (CC0) |
| Nairan_-_Fighter_-__Destruction.png | OpenGameArt — Void Main Ship 시리즈 (CC0) |
| Kla_ed_-_Bomber_-_Destruction.png | OpenGameArt — Void Main Ship 시리즈 (CC0) |
| Nautolan_Ship_-_Frigate.png | OpenGameArt — Void Main Ship 시리즈 (CC0) |
| Nairan_-_Frigate_-__Destruction.png | OpenGameArt — Void Main Ship 시리즈 (CC0) |
| Kla_ed_-_Battlecruiser_-_Destruction.png | OpenGameArt — Void Main Ship 시리즈 (CC0) |
| Nautolan_Ship_-_Dreadnought.png | OpenGameArt — Void Main Ship 시리즈 (CC0) |
| Nairan_-_Dreadnought_-__Destruction.png | OpenGameArt — Void Main Ship 시리즈 (CC0) |
| Main_ship_weapon_-_Projectile_-_Auto_cannon_bullet.png | OpenGameArt (CC0) |
| Main_ship_weapon_-_Projectile_-_Rocket.png | OpenGameArt (CC0) |
| Main_ship_weapon_-_Projectile_-_Big_Space_Gun.png | OpenGameArt (CC0) |
| Main_ship_weapon_-_Projectile_-_Zapper.png | OpenGameArt (CC0) |
| Nautolan_-_Spinning_Bullet.png | OpenGameArt (CC0) |
| Kla_ed_-_Bullet.png / Kla_ed_-_Big_Bullet.png / Kla_ed_-_Wave.png | OpenGameArt (CC0) |
| Nairan_-_Bolt.png / Nairan_-_Torpedo.png / Nairan_-_Rocket.png | OpenGameArt (CC0) |
| Nautolan_-_Bomb.png / Nautolan_-_Spinning_Bullet.png / Nautolan_-_Rocket.png / Nautolan_-_Bullet.png | OpenGameArt (CC0) |
| Starfield_01-1024x1024.png | 별도 수집 (스타필드 배경) |
| Starry_background_Layer_*.png | 별도 수집 (레이어드 배경) |

### 사운드

| 파일명 | 출처 |
|---|---|
| bgm_normal.mp3 | Suno AI로 생성한 인게임 BGM |
| bgm_boss.mp3 | Suno AI로 생성한 보스전 BGM |
| sfx_*.wav (9종) | 미구현 (제미나이로 생성 예정) |

---

## 사용한 AI 프롬프트 (요약)

1. 플레이어 기본 함선 스프라이트 적용 — 배경 제거 후 player.png 교체
2. 엔진 스프라이트 시트 분석 및 적용 — Base Engine(평소) + Supercharged Engine(오버클럭) 조합 제안
3. 엔진 글로우 이펙트 분석 및 추가 — BLEND_ADD 오버레이 적용
4. 파괴 애니메이션 스프라이트 시트(적/보스 3진영) 분석 — 게임 유닛과 진영별로 매칭, 크기·색상·프레임 수 비교
5. 투사체 스프라이트 19종 분석 — 플레이어 무기 5종 / 적·보스 진영별 총알 매칭 추천
6. 파괴 애니메이션 코드 적용 — enemy.py에 dying 상태 추가, boss.py에 start_death_anim() 구현
7. 투사체 스프라이트 전체 적용 — weapon.py 애니메이션 헬퍼 추가, 유도탄/클러스터 미사일 방향 회전 구현
8. 레이저 무기 렌더링 버그 디버깅 — self.lasers = [...] 리스트 참조 끊김 원인 분석 및 self.lasers[:] 수정
9. 레이저가 플레이어를 관통하는 문제 — start_y 파라미터 추가로 플레이어 앞에서만 빔 렌더링
10. Kla'ed / Nairan / Nautolan 3개 진영 24종 이미지 분석 — 적 5종 + 보스 3종 배치 표 작성 및 교체
11. 배경 레이어 합성 — 13개 레이어 파일 Screen·Multiply 블렌드로 합성 후 스타필드 이미지로 최종 교체
12. 전체 코드 게임성 검토 — 버그 4종 발견, 추가 요소 12가지 우선순위 분류 및 추천
13. 버그 수정 및 신규 기능 구현 — emit_engine 이중 실행 수정, homing_triple 시너지 연결, 보스 페이즈2 전환 연출, 게임오버 화면 개선

---

## AI 답변에서 도움이 된 것

**스프라이트 시트 자동 분석**
24개 파일의 프레임 수·크기·색상을 한 번에 파악할 수 있었다. 직접 이미지를 열어 하나씩 확인하기 어려운 작업을 자동화해줬다.

**레이저 버그 원인 추적**
`self.lasers = [...]`가 리스트 참조를 끊는다는 사실을 단계별로 정확히 짚어줬다. 직접 찾기 어려웠을 원인이었다.

**emit_engine 이중 실행 버그 발견**
코드를 눈으로 보기 어려운 버그를 검토 단계에서 발견해줬다.

**파괴 애니메이션 dying 상태 도입**
dying 상태 적용 시 충돌 판정, HP바 표시, 총알 처리 등 연관된 부분을 빠짐없이 함께 수정해줬다.

**엔진 애니메이션 구조 설계**
Void Main Ship 엔진 스프라이트 시트가 row0(idle)/row1(powering) 2줄 구조임을 분석하고, 이동 여부 및 오버클럭 상태에 따라 다른 행을 재생하는 로직을 바로 코드로 구현해줬다.

**3개 진영 배치 표 작성**
Kla'ed·Nairan·Nautolan 진영의 외형과 크기를 비교해서 게임 내 역할에 맞게 배치 표를 작성해줬다. 24종을 혼자 비교하기 어려운 작업이었다.

**배경 레이어 합성**
13개 레이어 파일의 역할(Solid/Shadow/Stars)을 분석하고 Screen·Multiply 블렌드 모드를 적용해 Python PIL만으로 자연스러운 배경을 합성해줬다.

**코드 전체 점검**
Stars/Nebula 미사용 클래스, rhythm 리셋 불완전, S_OVER 배경 멈춤, _draw_world 중복 호출 등 11가지 문제를 체계적으로 정리하고 우선순위까지 제시해줬다.

---

## AI 답변을 수정하거나 버린 것

**배경 제거 방법 교체**
파괴 애니메이션 적용 시 remove.bg 투명화 방법을 권장했지만, 미리보기 파일이 JPEG로 저장된다는 걸 미리 설명하지 않아 헛수고가 생겼다. 결국 `set_colorkey(0,0,0)` 방식으로 교체했다.

**numpy 오류 대응**
numpy를 사용한 배경 제거 코드가 `No module named 'numpy'` 오류를 발생시켜서 `set_colorkey` 방식으로 교체했다.

**배경 화려함 조절**
AI가 합성한 배경에 블랙홀·회전별·큰별이 포함돼 있었는데 "너무 화려한 거 같아"라고 직접 판단해서 특수 오브젝트 레이어를 제거하도록 요청했다. 최종적으로는 별도 스타필드 이미지로 교체했다.

**Stars 클래스 삭제 직접 제안**
배경 이미지 적용 후 코드로 그리는 Stars 클래스가 이중으로 겹친다는 점을 스스로 발견해서 삭제를 제안했다. AI가 먼저 제안한 것이 아니라 직접 판단한 것이다.

**적 크기 두 차례 수정 요청**
AI 제안 크기(drone 34px)가 작다고 판단해서 한 번 수정 요청한 뒤, 다시 "아직도 너무 작은 거 같아"라며 플레이어 기준 0.9배(43px)로 직접 수치를 지정했다.

**게임오버 화면 폰트 확인 필요**
게임오버 화면 초안에서 서버 환경에서는 한글이 깨져 보임 → 실제 게임 실행 환경에서 별도 확인 필요.

---

## 적용 결과

### 잘 된 것
- 플레이어 엔진 애니메이션이 오버클럭/이동 상태에 따라 자연스럽게 전환됨
- Void 시리즈 3개 진영 스프라이트로 적·보스 비주얼이 통일된 느낌
- 적 5종 + 보스 3종에 진영별 파괴 애니메이션이 각각 적용되어 처치 연출이 풍성해짐
- 플레이어 총알·적 총알 모두 스프라이트로 교체되어 시각적 완성도 향상
- 유도탄·클러스터 미사일이 진행 방향에 따라 자동 회전하여 자연스러운 추적 연출 구현
- 보스 페이즈2 전환 시 슬로우모션 + 슬라이드인 배너로 극적인 연출 추가
- 게임오버 화면이 이번 런 스탯 / 역대 기록 / 무기 구성 / 시너지를 한 화면에 보여주는 요약 화면으로 개선됨
- 스타필드 배경이 게임 분위기와 잘 어울리고 스크롤도 자연스러움
- 코드 점검으로 미사용 코드 100줄 삭제, 성능 문제 개선

### 어려웠던 것
- 레이저 버그가 두 단계(리스트 참조 끊김 → sy=0 Surface 오류)로 나뉘어서 한 번에 해결이 안 됨
- 스프라이트 배경 제거 방법(remove.bg / colorkey / numpy)마다 환경 제약이 달라서 선택이 어려웠음
- 파괴 애니메이션 dying 상태 중 충돌/EXP/레벨업 처리 순서를 잘못 짜면 버그가 생길 수 있어서 흐름 파악에 시간이 걸림
- 엔진 스프라이트 위치 조정이 숫자로만 조절해야 해서 실행해보기 전까지 결과를 예측하기 어려웠음

### 다음에 시도할 것
- 효과음(sfx) 9종 추가 — 발사음, PERFECT 판정음, 피격음 등 (제미나이로 생성 예정)
- BPM 박자에 맞춰 플레이어 주변에 펄스 링 표시 (리듬 아이덴티티 강화)
- 히트스탑 구현 (적 명중 시 1~2프레임 멈춤으로 타격감 향상)
- 보스 HP 바에 페이즈 전환 구분선 표시
- FAST/SLOW 판정 시 화면 색조 피드백 추가
