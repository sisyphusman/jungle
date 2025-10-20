import { useEffect, useRef, useState } from 'react'
import CommentSection from './CommentSection'

export default function PostDetail({ postId, token, user }) {
  const [post, setPost] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [isEditing, setIsEditing] = useState(false)
  const [editData, setEditData] = useState({ title: '', body: '' })
  const incrementedRef = useRef(false)

  useEffect(() => {
    async function load() {
      setLoading(true)
      setError('')
      try {
        if (!postId || postId === 'undefined' || postId === 'null') {
          window.location.hash = '#/'
          return
        }
        // 조회수 증가를 먼저 수행해, 이후 GET에서 최신 값이 보이도록 함
        if (!incrementedRef.current) {
          incrementedRef.current = true
          try {
            await fetch(`/api/v1/posts/${postId}/view`, { method: 'POST' })
          } catch {}
        }
        const res = await fetch(`/api/v1/posts/${postId}`, { cache: 'no-store' })
        if (!res.ok) throw new Error('글 불러오기 실패')
        const data = await res.json()
        setPost(data)
        setEditData({ title: data.title, body: data.body })
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    if (postId) load()
  }, [postId])

  if (loading) return <div className="p-6">로딩 중...</div>
  if (error) return <div className="p-6 text-red-600">{error}</div>
  if (!post) return <div className="p-6">글이 없습니다.</div>

  return (
    <div>
      <a href="#/" className="text-sm text-blue-600 hover:underline">← 목록</a>
      {isEditing ? (
        <form
          className="mt-2 space-y-3 rounded-lg border bg-white p-4 shadow-sm"
          onSubmit={async (e) => {
            e.preventDefault()
            try {
              const res = await fetch(`/api/v1/posts/${postId}`, {
                method: 'PATCH',
                headers: {
                  'Content-Type': 'application/json',
                  Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(editData),
              })
              if (!res.ok) throw new Error('수정 실패')
              const updated = await res.json()
              setPost(updated)
              setIsEditing(false)
            } catch (err) {
              alert(err.message)
            }
          }}
        >
          <input
            className="w-full rounded border px-3 py-2"
            value={editData.title}
            onChange={(e) => setEditData({ ...editData, title: e.target.value })}
            required
          />
          <textarea
            className="w-full rounded border px-3 py-2"
            rows={8}
            value={editData.body}
            onChange={(e) => setEditData({ ...editData, body: e.target.value })}
            required
          />
          <div className="flex gap-2">
            <button className="rounded bg-green-600 px-3 py-1 text-white hover:bg-green-700">저장</button>
            <button type="button" className="rounded border px-3 py-1 hover:bg-gray-50" onClick={() => setIsEditing(false)}>취소</button>
          </div>
        </form>
      ) : (
        <>
          <article className="mt-2 rounded-lg border bg-white p-5 shadow-sm">
            <h1 className="text-2xl font-bold">{post.title}</h1>
            <div className="mt-2 text-xs text-gray-500 flex flex-wrap gap-2">
              {(post.author_nickname || post.author_id) && (
                <span className="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5">작성자: {post.author_nickname || post.author_id}</span>
              )}
              {post.created_at && <span className="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5">작성일: {new Date(post.created_at).toLocaleString()}</span>}
              <span className="inline-flex items-center rounded-full bg-blue-50 text-blue-700 px-2 py-0.5">조회 {post.views ?? 0}</span>
              <span className="inline-flex items-center rounded-full bg-emerald-50 text-emerald-700 px-2 py-0.5">댓글 {post.comment_count ?? 0}</span>
            </div>
            <div className="mt-4 whitespace-pre-line text-gray-800 text-[17px] sm:text-lg leading-relaxed">{post.body}</div>
          </article>
        </>
      )}
      {user && post && String(post.author_id) === String(user.id) && (
        <div className="mt-3 flex gap-2">
          {!isEditing && (
            <button className="rounded bg-amber-500 px-3 py-1 text-sm text-white hover:bg-amber-600" onClick={() => setIsEditing(true)}>
              수정
            </button>
          )}
          <button
            className="rounded bg-red-600 px-3 py-1 text-sm text-white hover:bg-red-700"
            onClick={async () => {
              if (!confirm('삭제하시겠습니까?')) return
              try {
                const res = await fetch(`/api/v1/posts/${postId}`, {
                  method: 'DELETE',
                  headers: { Authorization: `Bearer ${token}` },
                })
                if (!res.ok) throw new Error('삭제 실패')
                window.location.hash = '#/'
              } catch (err) {
                alert(err.message)
              }
            }}
          >
            삭제
          </button>
        </div>
      )}
      <CommentSection
        postId={postId}
        token={token}
        user={user}
        onCountChange={(delta) =>
          setPost((prev) => (prev ? { ...prev, comment_count: Math.max(0, (prev.comment_count ?? 0) + delta) } : prev))
        }
      />
    </div>
  )
}
