function PostItem({ post, currentUserId }) {
  const postId = (post && (post.id || post._id || (post._id && post._id.$oid))) || null
  
  const isAuthor = post.author_id === currentUserId

  return (
    <div className="rounded-lg border bg-white p-4 shadow-sm">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          {postId ? (
            <a className="font-semibold text-blue-700 hover:underline text-lg" href={`#/post/${postId}`}>{post.title}</a>
          ) : (
            <span className="font-semibold text-lg">{post.title}</span>
          )}
          <div className="text-sm text-gray-700 whitespace-pre-line mt-1 line-clamp-3">{post.body}</div>
          <div className="mt-2 flex flex-wrap items-center gap-2 text-xs text-gray-500">
            {(post.author_nickname || post.author_id) && (
              <span className="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5">작성자: {post.author_nickname || post.author_id}</span>
            )}
            <span className="inline-flex items-center rounded-full bg-blue-50 text-blue-700 px-2 py-0.5">조회 {post.views ?? 0}</span>
            <span className="inline-flex items-center rounded-full bg-emerald-50 text-emerald-700 px-2 py-0.5">댓글 {post.comment_count ?? 0}</span>
          </div>
        </div>
        {/* 수정/삭제는 상세 화면에서 처리 */}
      </div>
    </div>
  )
}

export default PostItem
