## 동작 방식
1. 정해진 주기마다 GitHub Actions가 `check.py`를 실행 (기본 5분, GitHub 사정에 따라 지연될 수 있음)
2. 더판 목록 페이지를 읽어 글 ID를 `seen.json`(이미 본 글 목록)과 비교
3. 처음 보는 글이면 텔레그램으로 알림
4. 판매완료 글, 끌올된 글, 목록 아래쪽 글은 알림에서 제외

## 파일 구성
- `check.py`: 사이트 확인 + 텔레그램 발송
- `.github/workflows/check.yml`: 실행 일정
- `seen.json`: 이미 본 글 기록 (자동 생성)

## 설치 방법
1. **봇 만들기**: 텔레그램 `@BotFather` → `/newbot` → 토큰 받기
2. **내 Chat ID 확인**: 봇에게 메시지를 보낸 뒤 `https://api.telegram.org/bot<토큰>/getUpdates` 접속 → `"chat":{"id":` 뒤의 숫자
3. **GitHub 리포 만들기** 후 위 파일들 업로드
4. **Secrets 등록**: 리포 Settings → Secrets and variables → Actions
   - `TELEGRAM_BOT_TOKEN`: 봇 토큰
   - `TELEGRAM_CHAT_ID`: Chat ID
5. **권한 설정**: Settings → Actions → General → Workflow permissions → **Read and write permissions**
6. **첫 실행**: Actions → check → Run workflow
   - 첫 실행은 기존 글만 기록하고 알림은 보내지 않음

## 키워드 설정 (선택)
기본 `check.py`는 새 글을 전부 알려줍니다. 특정 매물만 받고 싶으면 **키워드 버전 `check.py`로 기존 파일을 덮어쓰면** 됩니다.

1. 리포의 `check.py` → 연필 아이콘 → 전체 삭제 후 키워드 버전 코드 붙여넣기 → Commit
2. 파일 위쪽 두 줄을 원하는 값으로 수정
   - `KEYWORDS`: 제목에 이 단어가 있는 글만 알림 (예: `["세이코", "오리스"]`, 비우면 전부)
   - `MAX_PRICE`: 이 가격(원) 이하만 알림 (`0`이면 제한 없음)
3. `seen.json`은 그대로 둠

참고: 제목에 적힌 단어만 검사하므로, 짧고 흔한 표기(`ssb479` 등)로 넣는 것이 안전합니다.

## 주의
- Private 리포는 무료 사용량(월 2,000분)이 5분 간격에서 금방 소진되므로 **Public** 리포 권장
- 사이트에 부담이 가지 않게 주기를 너무 짧게 잡지 않기. 
