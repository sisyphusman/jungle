import { useState } from 'react'

const authBase = '/api/v1/auth'

function AuthForm({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState('error')
  
  const [loginData, setLoginData] = useState({ username: '', password: '' })
  const [signupData, setSignupData] = useState({ username: '', email: '', password: '', nickname: '' })

  const handleLoginSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch(`${authBase}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData),
      })
      
      if (!res.ok) {
        const error = await res.text()
        throw new Error(error || '로그인 실패')
      }
      
      const result = await res.json()
      onLogin(result.access_token, result.user)
    } catch (err) {
      setMessage(err.message)
      setMessageType('error')
    }
  }

  const handleSignupSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch(`${authBase}/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(signupData),
      })
      
      if (!res.ok) {
        const error = await res.text()
        throw new Error(error || '회원가입 실패')
      }
      
  setMessage('회원가입 성공! 로그인해주세요.')
  setMessageType('success')
  setSignupData({ username: '', email: '', password: '', nickname: '' })
      setIsLogin(true)
    } catch (err) {
      setMessage(err.message)
      setMessageType('error')
    }
  }

  return (
    <div className="mx-auto flex min-h-screen max-w-md items-center justify-center px-4">
      <div className="w-full rounded-xl border bg-white p-6 shadow-sm">
        <h1 className="mb-6 text-center text-2xl font-bold">정글 자유게시판</h1>
        <div className="mb-6 grid grid-cols-2 gap-2">
          <button
            onClick={() => { setIsLogin(true); setMessage('') }}
            className={`rounded-md px-4 py-2 text-sm ${isLogin ? 'bg-blue-600 text-white' : 'border hover:bg-gray-50'}`}
          >로그인</button>
          <button
            onClick={() => { setIsLogin(false); setMessage('') }}
            className={`rounded-md px-4 py-2 text-sm ${!isLogin ? 'bg-blue-600 text-white' : 'border hover:bg-gray-50'}`}
          >회원가입</button>
        </div>

        {isLogin ? (
          <form onSubmit={handleLoginSubmit} className="space-y-3">
            <div>
              <label className="mb-1 block text-xs text-gray-600">아이디</label>
              <input type="text" className="w-full rounded border px-3 py-2" value={loginData.username} onChange={(e) => setLoginData({ ...loginData, username: e.target.value })} required />
            </div>
            <div>
              <label className="mb-1 block text-xs text-gray-600">비밀번호</label>
              <input type="password" className="w-full rounded border px-3 py-2" value={loginData.password} onChange={(e) => setLoginData({ ...loginData, password: e.target.value })} required />
            </div>
            <button type="submit" className="w-full rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">로그인</button>
          </form>
        ) : (
          <form onSubmit={handleSignupSubmit} className="space-y-3">
            <div>
              <label className="mb-1 block text-xs text-gray-600">아이디</label>
              <input type="text" className="w-full rounded border px-3 py-2" value={signupData.username} onChange={(e) => setSignupData({ ...signupData, username: e.target.value })} required />
            </div>
            <div>
              <label className="mb-1 block text-xs text-gray-600">닉네임</label>
              <input type="text" className="w-full rounded border px-3 py-2" value={signupData.nickname} onChange={(e) => setSignupData({ ...signupData, nickname: e.target.value })} required />
            </div>
            <div>
              <label className="mb-1 block text-xs text-gray-600">이메일</label>
              <input type="email" className="w-full rounded border px-3 py-2" value={signupData.email} onChange={(e) => setSignupData({ ...signupData, email: e.target.value })} required />
            </div>
            <div>
              <label className="mb-1 block text-xs text-gray-600">비밀번호</label>
              <input type="password" className="w-full rounded border px-3 py-2" value={signupData.password} onChange={(e) => setSignupData({ ...signupData, password: e.target.value })} required />
            </div>
            <button type="submit" className="w-full rounded bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-700">회원가입</button>
          </form>
        )}

        {message && (
          <div className={`mt-4 text-center text-sm ${messageType === 'error' ? 'text-red-600' : 'text-green-600'}`}>
            {message}
          </div>
        )}
      </div>
    </div>
  )
}

export default AuthForm
