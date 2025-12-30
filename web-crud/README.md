# Jungle CRUD (FastAPI + MongoDB + Vite/React)

인증(JWT), 닉네임, 게시판(글쓰기/목록/상세), 댓글 기능까지 포함한 풀스택 예제입니다. 프론트는 React + Tailwind, 백엔드는 FastAPI + Beanie(MongoDB)로 구성되어 있습니다.

## 주요 기능

- 회원가입/로그인(JWT) 및 내 정보 조회
- 회원가입 시 닉네임 생성 → 글/댓글 작성자 표시 시 닉네임 우선 노출
- 게시판
  - 글 목록(제목 클릭 시 상세)
  - 글쓰기(별도 페이지)
  - 글 상세(작성자/작성일 표시, 본인만 수정/삭제 가능)
- 댓글(글 상세 하단)
  - 목록/작성/삭제(본인만)
- 해시 기반 라우팅: `#/`, `#/write`, `#/post/:id`

## 기술 스택

- Backend: FastAPI, Beanie, Motor, PyJWT, bcrypt, pydantic-settings
- Frontend: Vite, React 18, Tailwind CSS
- DB: MongoDB (로컬 27017 기본)

## 실행 준비물

- Python 3.11+
- Node.js 18+
- 로컬 MongoDB 6+

## 백엔드 실행 (Windows PowerShell)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- 환경설정: `backend/app/core/config.py`
  - 기본 Mongo URL: `mongodb://localhost:27017/crud`
  - CORS: 개발용 프론트(5173) 허용
- 헬스체크: http://localhost:8000/health

## 프론트엔드 실행 (Windows PowerShell)

```powershell
cd frontend
npm install
npm run dev
```

- 접속: http://localhost:5173/
- 라우팅: `#/`(목록), `#/write`(글쓰기), `#/post/:id`(상세)

## 아키텍처 개요

개발 환경에서의 전체 흐름은 다음과 같습니다.

```
┌─────────────────────────┐        ┌──────────────────────────────┐
│  Browser (React App)    │  HTTP  │  Vite Dev Server (5173)      │
│  - Hash Routing (#/...) │ <────> │  - Static Assets             │
│  - Fetch /api/v1/*      │        │  - Proxy /api -> 8000        │
└────────────┬────────────┘        └──────────────┬───────────────┘
             │                                      │
             │ /api/v1/* (proxy)                    │
             │                                      ▼
             │                         ┌──────────────────────────┐
             │                         │ FastAPI (Uvicorn, 8000)  │
             │                         │ - Routers: auth/posts/   │
             │                         │   comments                │
             │                         │ - Beanie ODM              │
             │                         └───────────┬──────────────┘
             │                                     │ Motor
             ▼                                     ▼
┌─────────────────────────┐          ┌────────────────────────────┐
│  LocalStorage           │          │ MongoDB (localhost:27017)  │
│  - token, user          │          │ - db: crud                 │
└─────────────────────────┘          │ - collections: users/posts │
                                     │   /comments                │
                                     └────────────────────────────┘
```

- 프론트는 Vite 개발 서버를 통해 정적 리소스를 제공하고, `/api/*` 요청은 `vite.config.js`의 proxy 설정으로 FastAPI(8000)로 전달됩니다.
- FastAPI는 인증/게시글/댓글 라우터를 제공하고, Beanie를 통해 MongoDB에 접근합니다.
- 인증 토큰과 사용자 정보는 LocalStorage에 저장되어, 프론트에서 인증이 필요한 요청 시 Authorization 헤더로 전송됩니다.

프로덕션 구성(권장 예)

- 프론트: `npm run build` 결과를 Nginx 등으로 정적 호스팅
- 백엔드: Uvicorn(혹은 Gunicorn+Uvicorn workers) 뒤 Nginx 리버스 프록시
- 환경 변수로 비밀 키/DB URL/CORS 원본 제어

## 프로젝트 구조(요약)

- `backend/app/main.py` FastAPI 앱, Beanie 초기화, 라우터 등록
- `backend/app/models/user.py` 사용자(User) 모델/DTO(nickname 포함)
- `backend/app/models/post.py` 게시글(Post) 모델(author_id, author_nickname, created_at)
- `backend/app/models/comment.py` 댓글(Comment) 모델(author_id, author_nickname, created_at)
- `backend/app/routers/auth.py` 인증 라우터(signup/login/me)
- `backend/app/routers/posts.py` 게시글 CRUD 라우터
- `backend/app/routers/comments.py` 댓글 라우터(게시글별 목록/작성, 댓글 삭제)
- `frontend/src/App.jsx` 해시 라우팅 진입
- `frontend/src/components/AuthForm.jsx` 로그인/회원가입(닉네임 입력)
- `frontend/src/components/PostBoard.jsx` 목록
- `frontend/src/components/PostWrite.jsx` 글쓰기
- `frontend/src/components/PostDetail.jsx` 상세(본인만 수정/삭제)
- `frontend/src/components/CommentSection.jsx` 댓글

## API 요약

인증

- POST `/api/v1/auth/signup`
  - req: `{ username, email, password, nickname }`
  - res: `{ id, username, email, nickname }`
- POST `/api/v1/auth/login`
  - req: `{ username, password }`
  - res: `{ access_token, token_type, user: { id, username, email, nickname } }`
- GET `/api/v1/auth/me` (Bearer 토큰 필요)
  - res: `{ id, username, email, nickname }`

게시글

- POST `/api/v1/posts/` (Bearer)
  - req: `{ title, body }`
  - res: `Post` (필드: id, title, body, author_id, author_nickname, created_at, views, comment_count)
- GET `/api/v1/posts/`
  - query: `page`(기본 1), `limit`(기본 5, 최대 100)
  - res: `{ items: Post[], total: number, page: number, limit: number }`
- GET `/api/v1/posts/{id}`

  - res: `Post`

  - POST `/api/v1/posts/{id}/view`
    - res: `{ ok: true, views: number }` (조회수 +1)

- PATCH `/api/v1/posts/{id}` (Bearer, 작성자만)
  - req: `{ title?, body? }`
  - res: `Post`
- DELETE `/api/v1/posts/{id}` (Bearer, 작성자만)
  - res: `{ ok: true }`

댓글

- GET `/api/v1/comments/{post_id}`
  - res: `Comment[]`
- POST `/api/v1/comments/{post_id}` (Bearer)
  - req: `{ content }`
  - res: `Comment` (필드: id, post_id, content, author_id, author_nickname, created_at)
- DELETE `/api/v1/comments/{comment_id}` (Bearer, 작성자만)

- 게시글/댓글 수정·삭제는 작성자만 가능(백엔드에서 토큰의 사용자 id와 문서의 author_id 비교)

1. users

- \_id: ObjectId (문자열로 응답 시 id)
- username: string (고유)
- email: string (고유, EmailStr)
- hashed_password: string (bcrypt 해시)
- title: string
- body: string
- author_id: string (users.\_id)
- post_id: string (posts.\_id)
- content: string
- author_id: string (users.\_id)
- username, email은 고유(unique) 조건을 위해 애플리케이션 레벨에서 중복 체크

## 더 알아야 할 것들

- 라우팅 전략

  - 현재는 해시 라우팅(#)을 사용합니다. 브라우저 새로고침 시 404 방지를 위해 파일 서버 설정이 어려울 때 유리합니다.
  - 환경이 허용되면 react-router로 전환하고 서버 사이드에서 history fallback을 설정하세요.

- 인증/보안

  - JWT 비밀키는 환경 변수로 관리(코드 하드코딩 금지). 토큰 만료/갱신 전략(Refresh Token) 도입을 고려하세요.
  - CORS는 운영 도메인에 맞춰 최소 허용 원칙으로 설정.

- 데이터 모델/일관성

  - posts: views와 comment_count는 이벤트 기반으로 갱신됩니다(상세 진입 시 view +1, 댓글 생성/삭제 시 count ±1).
  - 대량 변경 또는 외부 경로로 댓글이 추가되는 경우 카운트 재계산 잡을 고려하십시오.

- 캐시/조회수 정확도

  - 조회수 증가를 POST /view로 분리했고, 상세 조회는 캐시를 no-store로 가져옵니다.
  - 사용자 단위 중복 방지는 쿠키/LocalStorage 표식 혹은 서버 측 제한(시간당 1회 등)으로 확장 가능합니다.

- 페이지네이션

  - 서버: page/limit 쿼리 파라미터, created_at desc 정렬, total 포함
  - 클라이언트: Prev/Next, 페이지 크기 선택. 필요 시 숫자 페이지 버튼 및 URL 쿼리 동기화 추가 권장.

- 에러 처리/관찰성

  - 백엔드에 구조적 로깅/요청 ID 부여, 프론트에는 사용자 친화적 에러 메시지와 재시도 UX가 도움이 됩니다.

- 배포 체크리스트

  - 백엔드 환경변수: SECRET_KEY, MONGODB_URL, CORS_ORIGINS
  - 프론트 환경변수: API_BASE_URL(프록시 미사용 시)
  - 헬스체크 엔드포인트(/health) 연동, 리소스 제한/타임아웃 설정

- 테스트
  - 백엔드: pytest로 auth/post/comment 해피패스 + 권한/유효성 테스트
  - 프론트: 렌더 테스트와 API 호출 목킹, 주요 경로(e2e)는 Playwright/Cypress 고려
