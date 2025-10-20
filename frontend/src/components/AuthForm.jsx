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
    <div className="mx-auto max-w-md p-6">
      <h1 className="text-2xl font-bold mb-6 text-center">Posts CRUD</h1>
      
      <div className="mb-6">
        <div className="flex gap-2 mb-4">
          <button
            onClick={() => {
              setIsLogin(true)
              setMessage('')
            }}
            className={`flex-1 px-4 py-2 rounded ${
              isLogin ? 'bg-blue-600 text-white' : 'border'
            }`}
          >
            로그인
          </button>
          <button
            onClick={() => {
              setIsLogin(false)
              setMessage('')
            }}
            className={`flex-1 px-4 py-2 rounded ${
              !isLogin ? 'bg-blue-600 text-white' : 'border'
            }`}
          >
            회원가입
          </button>
        </div>
        
        {isLogin ? (
          <form onSubmit={handleLoginSubmit} className="space-y-3 border rounded p-4">
            <h2 className="font-semibold">로그인</h2>
            <input
              type="text"
              className="w-full border rounded px-3 py-2"
              placeholder="아이디"
              value={loginData.username}
              onChange={(e) => setLoginData({ ...loginData, username: e.target.value })}
              required
            />
            <input
              type="password"
              className="w-full border rounded px-3 py-2"
              placeholder="비밀번호"
              value={loginData.password}
              onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
              required
            />
            <button
              type="submit"
              className="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              로그인
            </button>
          </form>
        ) : (
          <form onSubmit={handleSignupSubmit} className="space-y-3 border rounded p-4">
            <h2 className="font-semibold">회원가입</h2>
            <input
              type="text"
              className="w-full border rounded px-3 py-2"
              placeholder="아이디"
              value={signupData.username}
              onChange={(e) => setSignupData({ ...signupData, username: e.target.value })}
              required
            />
            <input
              type="text"
              className="w-full border rounded px-3 py-2"
              placeholder="닉네임"
              value={signupData.nickname}
              onChange={(e) => setSignupData({ ...signupData, nickname: e.target.value })}
              required
            />
            <input
              type="email"
              className="w-full border rounded px-3 py-2"
              placeholder="이메일"
              value={signupData.email}
              onChange={(e) => setSignupData({ ...signupData, email: e.target.value })}
              required
            />
            <input
              type="password"
              className="w-full border rounded px-3 py-2"
              placeholder="비밀번호"
              value={signupData.password}
              onChange={(e) => setSignupData({ ...signupData, password: e.target.value })}
              required
            />
            <button
              type="submit"
              className="w-full bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
            >
              회원가입
            </button>
          </form>
        )}
      </div>
      
      {message && (
        <div className={`text-sm ${messageType === 'error' ? 'text-red-600' : 'text-green-600'}`}>
          {message}
        </div>
      )}
    </div>
  )
}

export default AuthForm
