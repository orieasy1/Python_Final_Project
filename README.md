# One-Key Endless Runner (Python / Pygame)

스페이스바 하나로 조작하는 무한 러닝 게임입니다. 캐릭터는 자동으로 앞으로 달리고, 점프만으로 장애물을 피합니다. 시간이 지날수록 속도가 올라가며, 충돌하면 게임이 종료되고 점수가 기록됩니다.

## 실행 방법

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## 조작법
- `Space`: 점프 (시작/재시작도 Space)

## 룰
- 오른쪽에서 무작위 간격으로 생성되는 장애물을 점프로 회피
- 시간이 지날수록 이동 속도와 생성 빈도 증가
- 충돌 시 게임 종료, 현재 점수 표시
- 최고 점수는 `highscore.txt`에 저장되어 다음 플레이와 비교

## 파일 구조
- `main.py`: 게임 루프, 플레이어/장애물 로직, 점수·난이도 관리
- `requirements.txt`: 필요한 패키지
- `highscore.txt`: 플레이 중 생성·업데이트되는 최고 점수 파일

## 포인트
- **이벤트 기반 입력**: 스페이스바 하나로 점프/시작/재시작
- **물리 기반 점프**: 중력·속도 적용, 공중에서 추가 점프 제한
- **난이도 스케일링**: 시간 경과에 따른 속도 증가, 스폰 주기 단축
- **충돌/점수 처리**: 충돌 즉시 종료, 생존 시간 기반 점수, 최고 기록 저장

### 플레이 사진
<img width="806" height="432" alt="image" src="https://github.com/user-attachments/assets/c32c2743-df9f-4243-8dc5-7d64bb857aae" />

<img width="794" height="428" alt="image" src="https://github.com/user-attachments/assets/b93ac9e7-ef8b-4931-91b1-56779b5332e6" />

<img width="803" height="421" alt="image" src="https://github.com/user-attachments/assets/52602f32-dc1c-4c48-98ea-6d1b533cae50" />
