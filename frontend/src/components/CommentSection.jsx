import { useState, useEffect } from 'react'

export default function CommentSection({ postId, token, user, onCountChange }) {
  const [comments, setComments] = useState([])
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchComments = async () => {
    setLoading(true)
    setError('')
    try {
      const res = await fetch(`/api/v1/comments/${postId}`)
      if (!res.ok) throw new Error('댓글 불러오기 실패')
      const data = await res.json()
      const normalized = (Array.isArray(data) ? data : [])
        .map((c) => ({
          ...c,
          id: c.id || (c._id && (c._id.$oid || c._id)) || '',
        }))
        .filter((c) => !!c.id)
      setComments(normalized)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchComments()
  }, [postId])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await fetch(`/api/v1/comments/${postId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ content }),
      })
      if (!res.ok) throw new Error('댓글 작성 실패')
  setContent('')
  fetchComments()
  if (typeof onCountChange === 'function') onCountChange(1)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (commentId) => {
    if (!confirm('댓글을 삭제하시겠습니까?')) return
    setLoading(true)
    setError('')
    try {
      const res = await fetch(`/api/v1/comments/${commentId}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      if (!res.ok) {
        const msg = await res.text()
        throw new Error(msg || '댓글 삭제 실패')
      }
      fetchComments()
      if (typeof onCountChange === 'function') onCountChange(-1)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mt-8 border-t pt-4">
      <h3 className="font-semibold mb-2">댓글</h3>
      {loading && <div>로딩 중...</div>}
      {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
      <form onSubmit={handleSubmit} className="mb-3 space-y-2">
        <label htmlFor="comment-textarea" className="sr-only">댓글</label>
        <textarea
          id="comment-textarea"
          className="w-full rounded border px-3 py-2 min-h-24 resize-y focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="댓글을 입력하세요"
          rows={4}
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
        />
        <div className="flex items-center justify-end">
          <button
            className="inline-flex items-center rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={loading}
          >
            작성
          </button>
        </div>
      </form>
      <ul className="space-y-2">
        {comments.map((c) => (
          <li key={c.id} className="flex items-center justify-between border-b pb-2">
            <div className="flex-1">
              <div>{c.content}</div>
              <div className="text-xs text-gray-500 flex gap-3">
                {(c.author_nickname || c.author_id) && (
                  <span>작성자: {c.author_nickname || c.author_id}</span>
                )}
                {c.created_at && <span>작성일: {new Date(c.created_at).toLocaleString()}</span>}
              </div>
            </div>
            {user && user.id === c.author_id && (
              <button
                onClick={() => handleDelete(c.id)}
                className="inline-flex items-center rounded bg-red-600 px-2.5 py-1 text-xs font-medium text-white hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={loading}
                title="댓글 삭제"
              >
                삭제
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
