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

더미 데이터 테스트

```
// Studio 3T: use(...) 없이 DB 선택
const crud = db.getSiblingDB('crud');
const posts = crud.getCollection('posts');

// (옵션) 기존 문서 전체 삭제 후 삽입하려면 주석 해제
// posts.deleteMany({});

// 테스트 데이터 (author_id는 문자열로 저장: 백엔드 스키마와 일치)
const docs = [
  {
    _id: ObjectId("4e496cbd85329a587a11c478"),
    title: "첫 번째 더미 글",
    body: "이것은 예제 본문입니다. 실제 서비스에서는 여기에 글 내용이 들어갑니다.",
    author_id: "78c20286b64edddc0ad33361",
    author_nickname: "도훈",
    created_at: ISODate("2025-10-15T08:10:31+09:00"),
    views: 173,
    comment_count: 9
  },
  {
    _id: ObjectId("7f91dedc10190730e3395949"),
    title: "두 번째 테스트 글",
    body: "더미 데이터입니다. 본문은 길어도 짧아도 상관없습니다.",
    author_id: "d158c3d8482969e956b7a28d",
    author_nickname: "민수",
    created_at: ISODate("2025-10-12T23:33:31+09:00"),
    views: 112,
    comment_count: 6
  },
  {
    _id: ObjectId("7a60fdea5642cde9a8b43f8e"),
    title: "React + FastAPI 메모",
    body: "샘플 텍스트: JWT, 댓글, 조회수 로직을 테스트합니다.",
    author_id: "9a68d51f105c85b6ad3a129e",
    author_nickname: "지연",
    created_at: ISODate("2025-10-20T18:17:31+09:00"),
    views: 25,
    comment_count: 5
  },
  {
    _id: ObjectId("cd78a16f47f90fd1f389cf14"),
    title: "게임 엔진 일지",
    body: "테스트 포스트입니다. 프론트엔드와 백엔드 연동 테스트용.",
    author_id: "39c5ee02f720b7a5bad22b28",
    author_nickname: "서준",
    created_at: ISODate("2025-10-08T12:04:31+09:00"),
    views: 9,
    comment_count: 0
  },
  {
    _id: ObjectId("97ca796dee0ccea5c17dcb5c"),
    title: "MongoDB 학습 노트",
    body: "MongoDB + Beanie로 문서 저장과 조회를 실험합니다.",
    author_id: "5ebeeabf9eda116b5225899d",
    author_nickname: "하린",
    created_at: ISODate("2025-10-08T03:12:31+09:00"),
    views: 8,
    comment_count: 10
  },
  {
    _id: ObjectId("d322cdd47933430d6b411310"),
    title: "운동 루틴 기록",
    body: "오늘의 운동: 유산소와 어깨 운동. 로그 작성.",
    author_id: "45cbc8ac3d7b91ab36e1d1eb",
    author_nickname: "지호",
    created_at: ISODate("2025-10-12T20:39:31+09:00"),
    views: 19,
    comment_count: 1
  },
  {
    _id: ObjectId("5dc3b1775f683abd87bd60d7"),
    title: "알고리즘 문제 풀이",
    body: "DFS/BFS, 투 포인터, 그리디 요약 메모.",
    author_id: "c7250593eb33e8a83787c0ec",
    author_nickname: "윤서",
    created_at: ISODate("2025-10-18T16:03:31+09:00"),
    views: 287,
    comment_count: 6
  },
  {
    _id: ObjectId("791a97b77b6ae2e588a1082f"),
    title: "유니티 2D 멀티 노트",
    body: "Unity Netcode, WebGL 빌드 체크리스트.",
    author_id: "cc2705d18f3a85768b850732",
    author_nickname: "현우",
    created_at: ISODate("2025-09-30T11:12:31+09:00"),
    views: 213,
    comment_count: 7
  },
  {
    _id: ObjectId("36efe884ed4b5fbf58602f49"),
    title: "네트워크 기초 정리",
    body: "TCP/UDP, 소켓, HTTP 요약 정리.",
    author_id: "995a7e0f48e75e284db13745",
    author_nickname: "민지",
    created_at: ISODate("2025-10-08T15:00:31+09:00"),
    views: 299,
    comment_count: 9
  },
  {
    _id: ObjectId("d837b20f2cd2612d84b1104b"),
    title: "일일 회고",
    body: "하루를 돌아보며 개선점을 적습니다.",
    author_id: "a5e13cfc1d0ad810ccb24aa4",
    author_nickname: "서연",
    created_at: ISODate("2025-10-06T01:00:31+09:00"),
    views: 270,
    comment_count: 6
  }
];

// 삽입(중복 _id가 있어도 나머지 계속 진행)
const result = posts.insertMany(docs, { ordered: false });
printjson({ insertedCount: result.insertedIds ? Object.keys(result.insertedIds).length : 0 });

// (옵션) 확인용
print('total posts:', posts.countDocuments());
posts.find({}, { title: 1, created_at: 1 }).sort({ created_at: -1 }).limit(20).forEach(printjson);
```
