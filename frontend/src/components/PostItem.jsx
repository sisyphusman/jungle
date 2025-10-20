function PostItem({ post, currentUserId }) {
  const postId = (post && (post.id || post._id || (post._id && post._id.$oid))) || null
  
  const isAuthor = post.author_id === currentUserId

  return (
    <div className="border rounded p-3">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          {postId ? (
            <a className="font-semibold text-blue-700 hover:underline" href={`#/post/${postId}`}>{post.title}</a>
          ) : (
            <span className="font-semibold">{post.title}</span>
          )}
          <div className="text-sm text-gray-600 whitespace-pre-line">{post.body}</div>
          {(post.author_nickname || post.author_id) && (
            <div className="text-xs text-gray-500 mt-1">작성자: {post.author_nickname || post.author_id}</div>
          )}
        </div>
        {/* 수정/삭제는 상세 화면에서 처리 */}
      </div>
    </div>
  )
}

export default PostItem
