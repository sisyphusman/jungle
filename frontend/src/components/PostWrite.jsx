import { useState } from 'react'

export default function PostWrite({ token }) {
  const [title, setTitle] = useState('')
  const [body, setBody] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await fetch('/api/v1/posts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ title, body }),
      })
      if (!res.ok) {
        const msg = await res.text()
        throw new Error(msg || '글 작성 실패')
      }
      // 작성 완료 후 목록으로 이동
      window.location.hash = '#/'
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-3xl p-6">
      <h1 className="text-2xl font-bold mb-4">글쓰기</h1>
      <form onSubmit={handleSubmit} className="space-y-3 border rounded p-4">
        <div>
          <label className="block text-sm font-medium mb-1">제목</label>
          <input
            className="w-full border rounded px-3 py-2"
            placeholder="제목"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">내용</label>
          <textarea
            className="w-full border rounded px-3 py-2"
            rows="6"
            placeholder="내용"
            value={body}
            onChange={(e) => setBody(e.target.value)}
            required
          />
        </div>
        {error && <div className="text-red-600 text-sm">{error}</div>}
        <div className="flex gap-2">
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? '작성 중...' : '등록'}
          </button>
          <a href="#/" className="px-4 py-2 border rounded hover:bg-gray-100">취소</a>
        </div>
      </form>
    </div>
  )
}
