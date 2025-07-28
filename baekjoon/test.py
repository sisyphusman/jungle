class TrieNode:
    def __init__(self):
        self.children = {}  # 자식 노드들
        self.is_end = False  # 단어의 끝을 나타내는 플래그

class Trie:
    def __init__(self):
        self.root = TrieNode()

    # 문자열 삽입
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:  # 자식 노드 없으면 새로 생성
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    # 문자열 존재 여부 확인 (Fetch)
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    # 문자열 삭제 (Delete)
    def delete(self, word):
        def _delete(node, word, depth):
            if depth == len(word):
                if not node.is_end:
                    return False  # 존재하지 않는 단어
                node.is_end = False
                return len(node.children) == 0  # 자식 없으면 삭제 가능

            char = word[depth]
            if char not in node.children:
                return False

            should_delete = _delete(node.children[char], word, depth + 1)

            if should_delete:
                del node.children[char]
                return not node.is_end and len(node.children) == 0
            return False

        _delete(self.root, word, 0)

# 트라이 사용해보기
trie = Trie()

# 단어 삽입
trie.insert("apple")
trie.insert("app")
trie.insert("bat")

# 검색 테스트
print(trie.search("app"))     # True
print(trie.search("apple"))   # True
print(trie.search("bat"))     # True
print(trie.search("batman"))  # False

# 삭제 후 검색
trie.delete("app")
print(trie.search("app"))     # False
print(trie.search("apple"))   # True (apple은 남아있음)

trie.delete("apple")
print(trie.search("apple"))   # False