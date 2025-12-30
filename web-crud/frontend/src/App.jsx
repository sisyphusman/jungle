import { useState, useEffect } from 'react'
import AuthForm from './components/AuthForm'
import PostBoard from './components/PostBoard'
import PostWrite from './components/PostWrite'
import PostDetail from './components/PostDetail'
import Header from './components/Header'

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [user, setUser] = useState(() => {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  })

  const handleLogin = (tokenData, userData) => {
    setToken(tokenData)
    setUser(userData)
    localStorage.setItem('token', tokenData)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const handleLogout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // 간단한 해시 라우팅 (#/, #/write, #/post/:id)
  const [route, setRoute] = useState(window.location.hash || '#/')
  useEffect(() => {
    const onHashChange = () => setRoute(window.location.hash || '#/')
    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  if (!token) {
    return (
      <div className="min-h-screen bg-gray-50">
        <AuthForm onLogin={handleLogin} />
      </div>
    )
  }

  let page = null
  if (route === '#/write') {
    page = <PostWrite token={token} />
  } else if (route.startsWith('#/post/')) {
    const postId = route.slice('#/post/'.length)
    if (!postId || postId === 'undefined' || postId === 'null') {
      window.location.hash = '#/'
      page = <PostBoard user={user} token={token} onLogout={handleLogout} />
    } else {
      page = <PostDetail postId={postId} user={user} token={token} />
    }
  } else {
    page = <PostBoard user={user} token={token} onLogout={handleLogout} />
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={user} onLogout={handleLogout} />
      <main className="mx-auto max-w-4xl px-4 sm:px-6 py-6">{page}</main>
    </div>
  )
}

export default App
