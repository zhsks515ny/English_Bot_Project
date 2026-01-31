# Daily English Expression Bot 🌟

매일 아침 랜덤 영어 표현을 텔레그램으로 보내주는 봇입니다.

## 설정 방법

### 1. Telegram Bot 생성

1. Telegram에서 [@BotFather](https://t.me/BotFather)를 검색합니다
2. `/newbot` 명령어를 입력합니다
3. Bot 이름과 username을 설정합니다
4. **Bot Token**을 받아서 저장해둡니다 (예: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Chat ID 확인

1. 생성한 봇에게 아무 메시지나 보냅니다
2. 브라우저에서 다음 URL을 엽니다:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
3. 응답에서 `"chat":{"id":123456789}` 형태의 **Chat ID**를 찾습니다

### 3. GitHub Repository 설정

1. 이 프로젝트를 GitHub에 push합니다
2. Repository의 **Settings** → **Secrets and variables** → **Actions**로 이동합니다
3. 다음 두 개의 Secrets를 추가합니다:
   - `TELEGRAM_BOT_TOKEN`: Bot Token
   - `TELEGRAM_CHAT_ID`: Chat ID

### 4. GitHub Actions 활성화

Repository의 **Actions** 탭에서 워크플로우를 활성화합니다.

## 실행 시간

- 매일 오전 8시 (KST)에 자동 실행됩니다
- Actions 탭에서 "Run workflow" 버튼으로 수동 실행도 가능합니다

## 로컬 테스트

```bash
# 환경 변수 설정
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"

# 의존성 설치
pip install -r requirements.txt

# 실행
python send_expression.py
```

## 프로젝트 구조

```
english-daily-bot/
├── .github/
│   └── workflows/
│       └── daily-expression.yml  # GitHub Actions 워크플로우
├── data/
│   └── expressions.json          # 영어 표현 100개 DB
├── send_expression.py            # 메인 스크립트
├── requirements.txt              # Python 의존성
└── README.md
```

## 메시지 예시

```
🌟 오늘의 영어 표현 🌟

📚 Expression: Break the ice

💡 Meaning: To initiate a conversation in a social setting

🇰🇷 뜻: 어색한 분위기를 깨다

📝 Example:
He told a joke to break the ice at the meeting.

━━━━━━━━━━━━━━━
Have a great day! 좋은 하루 보내세요! 🚀
```

## 표현 추가/수정

`data/expressions.json` 파일을 수정하여 새로운 표현을 추가하거나 기존 표현을 수정할 수 있습니다.

```json
{
  "id": 101,
  "expression": "New expression",
  "meaning": "English meaning",
  "meaning_kr": "한국어 뜻",
  "example": "Example sentence."
}
```
