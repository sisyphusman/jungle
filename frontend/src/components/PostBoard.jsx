import { useState, useEffect } from 'react'
import PostItem from './PostItem'

const apiBase = '/api/v1/posts'

function PostBoard({ user, token, onLogout }) {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [page, setPage] = useState(1)
  const [limit, setLimit] = useState(5)
  const [total, setTotal] = useState(0)

  const loadPosts = async () => {
    try {
      setLoading(true)
      setError('')
      const res = await fetch(`${apiBase}/?page=${page}&limit=${limit}`)
      if (!res.ok) {
        throw new Error(`목록 불러오기 실패 (HTTP ${res.status})`)
      }
      const data = await res.json()
      const list = Array.isArray(data.items) ? data.items : []
      const normalized = list
        .map(p => ({
          ...p,
          id: p.id || (p._id && (p._id.$oid || p._id)) || '',
        }))
        .filter(p => !!p.id)
      setPosts(normalized)
      setTotal(typeof data.total === 'number' ? data.total : normalized.length)
    } catch (err) {
      setError(err.message || '목록 불러오기 실패')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadPosts()
  }, [page, limit])

  return (
    <div className="space-y-4">
      {/* 글쓰기 폼 제거: 글쓰기는 별도 페이지(#/write)에서 처리 */}

      <div className="space-y-3">
        {loading && <div className="text-gray-500">Loading...</div>}
        {error && <div className="text-red-600">{error}</div>}
        {!loading && !error && posts.length === 0 && (
          <div className="text-gray-500">게시글이 없습니다</div>
        )}
        {posts.map((post) => (
          <PostItem
            key={post.id}
            post={post}
            currentUserId={user.id}
          />
        ))}
        <div className="flex items-center justify-between pt-4">
          <div className="text-sm text-gray-600">
            총 {total}건 · 페이지 {page} / {Math.max(1, Math.ceil(total / limit))}
          </div>
          <div className="flex items-center gap-2">
            <button
              className="px-3 py-1 border rounded disabled:opacity-50"
              disabled={page <= 1}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
            >
              이전
            </button>
            <button
              className="px-3 py-1 border rounded disabled:opacity-50"
              disabled={page >= Math.ceil(total / limit) || total === 0}
              onClick={() => setPage((p) => p + 1)}
            >
              다음
            </button>
            <select
              className="ml-2 border rounded px-2 py-1 text-sm"
              value={limit}
              onChange={(e) => { setPage(1); setLimit(Number(e.target.value) || 10) }}
            >
              <option value={5}>5개</option>
              <option value={10}>10개</option>
              <option value={20}>20개</option>
              <option value={50}>50개</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PostBoard
