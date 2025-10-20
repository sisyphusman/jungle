import { useEffect, useState } from 'react'
import CommentSection from './CommentSection'

export default function PostDetail({ postId, token, user }) {
  const [post, setPost] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [isEditing, setIsEditing] = useState(false)
  const [editData, setEditData] = useState({ title: '', body: '' })

  useEffect(() => {
    async function load() {
      setLoading(true)
      setError('')
      try {
        if (!postId || postId === 'undefined' || postId === 'null') {
          window.location.hash = '#/'
          return
        }
        const res = await fetch(`/api/v1/posts/${postId}`)
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
    <div className="mx-auto max-w-3xl p-6">
      <a href="#/" className="text-sm text-blue-600">← 목록</a>
      {isEditing ? (
        <form
          className="mt-2 space-y-2 border rounded p-4"
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
            className="w-full border rounded px-3 py-2"
            value={editData.title}
            onChange={(e) => setEditData({ ...editData, title: e.target.value })}
            required
          />
          <textarea
            className="w-full border rounded px-3 py-2"
            rows={8}
            value={editData.body}
            onChange={(e) => setEditData({ ...editData, body: e.target.value })}
            required
          />
          <div className="flex gap-2">
            <button className="bg-green-600 text-white px-3 py-1 rounded">저장</button>
            <button type="button" className="border px-3 py-1 rounded" onClick={() => setIsEditing(false)}>취소</button>
          </div>
        </form>
      ) : (
        <>
          <h1 className="text-2xl font-bold mt-2">{post.title}</h1>
          <div className="mt-3 whitespace-pre-line">{post.body}</div>
        </>
      )}
      <div className="text-xs text-gray-500 mt-2 flex gap-3">
        {(post.author_nickname || post.author_id) && (
          <span>작성자: {post.author_nickname || post.author_id}</span>
        )}
        {post.created_at && <span>작성일: {new Date(post.created_at).toLocaleString()}</span>}
      </div>
      {user && post && String(post.author_id) === String(user.id) && (
        <div className="mt-3 flex gap-2">
          {!isEditing && (
            <button className="px-3 py-1 rounded bg-amber-500 text-white text-sm hover:bg-amber-600" onClick={() => setIsEditing(true)}>
              수정
            </button>
          )}
          <button
            className="px-3 py-1 rounded bg-red-600 text-white text-sm hover:bg-red-700"
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
      <CommentSection postId={postId} token={token} user={user} />
    </div>
  )
}
