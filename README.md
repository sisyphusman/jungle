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
- 로컬 MongoDB 6+ (또는 Docker)

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

## MongoDB (선택: Docker)

```powershell
docker run -d --name jungle-crud-mongo -p 27017:27017 mongo:6
```

## 프론트엔드 실행 (Windows PowerShell)

```powershell
cd frontend
npm install
npm run dev
```

- 접속: http://localhost:5173/
- 라우팅: `#/`(목록), `#/write`(글쓰기), `#/post/:id`(상세)

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
  - query: `page`(기본 1), `limit`(기본 10, 최대 100)
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
  - res: `{ ok: true }`

## 권한

- 게시글/댓글 수정·삭제는 작성자만 가능(백엔드에서 토큰의 사용자 id와 문서의 author_id 비교)

## 데이터베이스 스키마

MongoDB 컬렉션과 주요 필드입니다. 타입은 일반적 사용 기준이며, ObjectId는 문자열로 직렬화되어 API로 반환됩니다.

1. users

- \_id: ObjectId (문자열로 응답 시 id)
- username: string (고유)
- email: string (고유, EmailStr)
- hashed_password: string (bcrypt 해시)
- nickname: string (표시용 이름)

2. posts

- \_id: ObjectId (문자열로 응답 시 id)
- title: string
- body: string
- author_id: string (users.\_id)
- author_nickname: string
- created_at: datetime (UTC)
- views: number (기본 0)
- comment_count: number (기본 0)
- location?: { type: "Point", coordinates: [lng, lat] }

3. comments

- \_id: ObjectId (문자열로 응답 시 id)
- post_id: string (posts.\_id)
- content: string
- author_id: string (users.\_id)
- author_nickname: string
- created_at: datetime (UTC)

인덱스/기타

- posts.location: 2dsphere (지오쿼리용)
- username, email은 고유(unique) 조건을 위해 애플리케이션 레벨에서 중복 체크

## 자주 만나는 이슈

- 상세 이동 시 `#/post/undefined`
  - 해시 라우팅/목록 정규화로 방지. 여전히 보이면 응답 JSON에 `id`/`_id.$oid` 형태 확인 필요
- 401 Unauthorized
  - 토큰 만료 또는 미첨부. 로그인 후 로컬 스토리지의 token을 확인하세요.
- MongoDB 연결 오류
  - 로컬에서 `mongod`가 실행 중인지 또는 Docker 컨테이너가 실행 중인지 확인하세요.

## 라이선스

학습용 예제. 자유롭게 수정/확장해서 사용하세요.
