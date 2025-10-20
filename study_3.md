구현 완료 내용
백엔드 (FastAPI + MongoDB)
User 모델 (user.py)

bcrypt를 사용한 비밀번호 해싱
username, email, hashed_password 필드
인증 라우터 (auth.py)

POST /api/v1/auth/signup - 회원가입
POST /api/v1/auth/login - 로그인 (JWT 토큰 발급)
GET /api/v1/auth/me - 현재 사용자 정보
게시글 라우터 수정 (posts.py)

글 작성 시 자동으로 작성자 ID 저장
수정/삭제는 작성자만 가능 (권한 체크)
의존성 추가 (requirements.txt)

bcrypt - 비밀번호 해싱
PyJWT - JWT 토큰 생성/검증
프론트엔드 (Vite + Vanilla JS)
로그인/회원가입 UI (index.js)

회원가입 폼 (아이디, 이메일, 비밀번호)
로그인 폼 (아이디, 비밀번호)
탭 전환 기능
게시판 UI 개선

로그인한 사용자 이름 표시
로그아웃 버튼
본인이 작성한 글만 수정/삭제 버튼 표시
토큰 관리

LocalStorage에 JWT 토큰 저장
모든 API 요청에 Authorization 헤더 자동 추가
토큰 만료 시 자동 로그아웃

실행 방법

1. MongoDB 실행
2. 백엔드 실행
3. 프론트엔드 실행
4. 접속
   http://localhost:5173/

사용 흐름
회원가입: 아이디, 이메일, 비밀번호 입력
로그인: 회원가입한 계정으로 로그인
글쓰기: 제목, 내용 입력 후 "글쓰기" 버튼
게시글 보기: 목록에 모든 글이 표시됨
수정/삭제: 본인이 작성한 글만 수정/삭제 버튼이 표시됨
로그아웃: 우측 상단 로그아웃 버튼

보안 기능
비밀번호는 bcrypt로 해싱하여 저장
JWT 토큰 기반 인증 (24시간 유효)
작성자만 본인 게시글 수정/삭제 가능
토큰 만료 시 자동 로그아웃

# 명령어

### db

post 삭제 - db.posts.deleteMany({})
댓글 삭제 - db.comments.deleteMany({})
유저 삭제 - db.users.deleteMany({})

post 검색 - db.getCollection("posts").find({})
