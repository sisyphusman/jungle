export default function Header({ user, onLogout }) {
  return (
    <header className="sticky top-0 z-30 border-b bg-white/80 backdrop-blur supports-[backdrop-filter]:bg-white/60">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 py-3 flex items-center justify-between">
        <a
          href="#/"
          onClick={(e) => {
            e.preventDefault()
            // 홈으로 이동 + 현재 목록 페이지라면 1페이지로 리셋 이벤트 발행
            window.location.hash = '#/'
            window.dispatchEvent(new CustomEvent('go-home'))
          }}
          className="font-semibold text-lg tracking-tight"
        >
          정글 자유게시판
        </a>
        <nav className="flex items-center gap-2">
          <span className="text-sm text-gray-600">{user?.nickname || user?.username}님</span>
          <a href="#/write" className="inline-flex items-center gap-1 rounded-md border px-3 py-1.5 text-sm hover:bg-gray-50">
            글쓰기
          </a>
          <button onClick={onLogout} className="inline-flex items-center gap-1 rounded-md border px-3 py-1.5 text-sm hover:bg-gray-50">
            로그아웃
          </button>
        </nav>
      </div>
    </header>
  )
}
