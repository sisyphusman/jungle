#include "rbtree.h"

#include <stdlib.h>

/*
  RB 트리 5가지 특성
  1. 모든 노드는 red or black
  2. 루트 노드는 black
  3. 모든 nil 노드는 black
  4. 노드가 red라면 자녀들은 black
  5. 각 노드에서 자손 nil 노드들까지 가는 모든 경로는 black 수와 같다

 z = new, y = par, x = cur
*/

void delete_subtree(rbtree* t, node_t* p);
void delete_rbtree(rbtree *t);
void left_rotate(rbtree* t, node_t* x);
void right_rotate(rbtree* t, node_t* x);
void insert_fixup(rbtree* t, node_t* new);
void rb_transplant(rbtree* t, node_t* u, node_t* v);
node_t* tree_minimum(const rbtree* t, node_t* x);
void rb_delete_fixup(rbtree* t, node_t* x);

rbtree *new_rbtree(void) 
{
  rbtree *p = (rbtree *)calloc(1, sizeof(rbtree));  

  // 동적할당 NULL 체크
  if (p == NULL)
  {
    return NULL;
  }

  // nil 노드 생성
  p->nil = (node_t *)calloc(1, sizeof(node_t));

  if (p->nil == NULL)
  {
    free(p);
    return NULL;
  }
  
  // color 지정
  p->nil->color = RBTREE_BLACK;
  
  // NULL을 대체하기 위한 노드
  p->nil->left = p->nil->right = p->nil->parent = p->nil;

  // 초기 루트는 nil을 가리킴
  p->root = p->nil;

  return p;
}

void delete_subtree(rbtree* t, node_t* p)
{
  // 베이스 케이스
  if (t->nil == p)
  {
    return;
  }

  delete_subtree(t, p->left);
  delete_subtree(t, p->right);
  free(p);
}

void delete_rbtree(rbtree *t) 
{
  if (t == NULL)
  {
    return;
  }

  delete_subtree(t, t->root);
  free(t->nil);
  free(t);
}

void left_rotate(rbtree* t, node_t* x)
{
  node_t* y = x->right;
  x->right = y->left;                     // y의 왼쪽 서브 트리를 x의 오른쪽 서브 트리로 회전한다
  
  if (y->left != t->nil)                  // y의 왼쪽 서브 트리가 비어 있지 않은 경우
  {
    y->left->parent = x;                  // 그러면 x는 서브 트리 루트의 부모가 된다
  }

  y->parent = x->parent;                  // x의 부모가 y의 부모가 된다

  if (x->parent == t->nil)                // x가 루트인 경우
  {
    t->root = y;
  }
  else if (x == x->parent->left)          // 그렇지 않으면, x가 왼쪽 자식인 경우
  {
    x->parent->left = y;                  // 그러면 y는 왼쪽 자식이 된다
  }
  else
  {
    x->parent->right = y;
  }
  
  y->left = x;                            // x를 y의 왼쪽 자식이 되게 한다
  x->parent = y;
}

void right_rotate(rbtree* t, node_t* y)
{
  node_t* x = y->left;                    // x는 y의 왼쪽 자식
  y->left = x->right;                     // x의 오른쪽 서브트리를 y의 왼쪽으로 이동

  if (x->right != t->nil)                 // 비어있지 않으면 부모 갱신
  {
    x->right->parent = y;
  }

  x->parent = y->parent;                  // y의 부모를 x의 부모로 교체
  if (y->parent == t->nil)                // y가 루트였다면
  {
    t->root = x;                          
  }
  else if (y == y->parent->right)         // y가 오른쪽 자식이었다면
  {
    y->parent->right = x;                 
  }
  else                                    // y가 왼쪽 자식이었다면
  {
    y->parent->left = x;            
  }

  x->right = y;                           // y를 x의 오른쪽 자식으로
  y->parent = x;
}

void insert_fixup(rbtree* t, node_t* new)
{
  node_t* uncle = t->nil;
  while (new->parent->color == RBTREE_RED)                     // 부모가 RED일 때만 위반이 발생
  {
    if (new->parent == new->parent->parent->left)
    {
      uncle = new->parent->parent->right;

      if (uncle->color == RBTREE_RED)                          // 케이스 1 - new의 부모와 삼촌이 모두 레드인가?
      {
        new->parent->color = RBTREE_BLACK;
        uncle->color = RBTREE_BLACK;
        new->parent->parent->color = RBTREE_RED;
        new = new->parent->parent;
      }
      else
      {
        if (new == new->parent->right)                        // 케이스 2
        {
          new = new->parent;
          left_rotate(t, new);
        }
        new->parent->color = RBTREE_BLACK;                    // 케이스 3
        new->parent->parent->color = RBTREE_RED;
        right_rotate(t, new->parent->parent);
      }
    }
    else                                                      // 위와 같지만, 오른쪽과 왼쪽이 바뀜
    {
      uncle = new->parent->parent->left;
      if (uncle->color == RBTREE_RED)
      {
        new->parent->color = RBTREE_BLACK;
        uncle->color = RBTREE_BLACK;
        new->parent->parent->color = RBTREE_RED;
        new = new->parent->parent;
      }
      else
      {
        if (new == new->parent->left)
        {
          new = new->parent;
          right_rotate(t, new);
        }
        new->parent->color = RBTREE_BLACK;
        new->parent->parent->color = RBTREE_RED;
        left_rotate(t, new->parent->parent);
      }
    }
  }
  
  t->root->color = RBTREE_BLACK;
}

node_t* rbtree_insert(rbtree* t, const key_t key) 
{
  node_t* new = (node_t*)malloc(sizeof(node_t));                // 노드 동적 할당

  if (new == NULL)
  {
    return NULL;
  }

  new->color = RBTREE_RED;                                      // 구조체 설정
  new->parent = new->left = new->right = t->nil;
  new->key = key;

  node_t* cur = t->root;                                        // 노드 위치 찾기
  node_t* par = t->nil;

  while (cur != t->nil)                                         // 대소 비교
  {
    par = cur;

    if (new->key < cur->key)
    {
      cur = cur->left;
    }
    else
    {
      cur = cur->right;
    }
  }

  new->parent = par;

  if (par == t->nil)
  {
    t->root = new;                                              // 트리 T가 비어있다
  }
  else if (new->key < par->key)
  {
    par->left = new;
  }
  else
  {
    par->right = new;
  }
  
  insert_fixup(t, new);

  return new;
}

node_t *rbtree_find(const rbtree *t, const key_t key) 
{
  node_t* x = t->root;

  while(x != t->nil)
  {
    if (key == x->key)
    {
      return x;
    }

    if (key < x->key)
    {
      x = x->left;
    }
    else
    {
      x = x->right;
    }
  }

  return NULL;
}

node_t* tree_minimum(const rbtree* t, node_t* x)
{
  while (x->left != t->nil)
  {
    x = x->left;
  }

  return x;
}

node_t *rbtree_min(const rbtree *t) 
{
  if (t->root == t->nil)
  {
    return t->nil;
  }

  return tree_minimum(t, t->root);
}

node_t* tree_maximum(const rbtree* t, node_t* x)
{
  while (x->right != t->nil)
  {
    x = x->right;
  }

  return x;
}

node_t *rbtree_max(const rbtree *t) 
{
  if (t->root == t->nil)
  {
    return t->nil;
  }
  
  return tree_maximum(t, t->root);
}

void rb_transplant(rbtree* t, node_t* u, node_t* v)
{
  if (u->parent == t->nil)
  {
    t->root = v;
  }
  else if (u == u->parent->left)
  {
    u->parent->left = v;
  }
  else 
  {
    u->parent->right = v;
  }

  v->parent = u->parent;
}

void rb_delete_fixup(rbtree* t, node_t* x)
{
  node_t* w = t->nil;

  while ((x != t->root) && (x->color == RBTREE_BLACK))
  {
    if (x == x->parent->left)
    {
      w = x->parent->right;

      if (w->color == RBTREE_RED)                                                 // 케이스 1
      {
        w->color = RBTREE_BLACK;
        w->parent->color = RBTREE_RED;
        left_rotate(t, x->parent);
        w = x->parent->right;
      }
      
      if ((w->left->color == RBTREE_BLACK) && (w->right->color == RBTREE_BLACK))  // 케이스 2
      {
        w->color = RBTREE_RED;
        x = x->parent;
      }
      else                                                                        // 케이스 3
      {
        if (w->right->color == RBTREE_BLACK)
        {
          w->left->color = RBTREE_BLACK;
          w->color = RBTREE_RED;
          right_rotate(t, w);
          w = x->parent->right;
        }

        w->color = x->parent->color;                                              // 케이스 4
        x->parent->color = RBTREE_BLACK;
        w->right->color = RBTREE_BLACK;
        left_rotate(t, x->parent);
        x = t->root;
      }
    }
    else                                                                          // 위와 동일하지만, 오른쪽과 왼쪽이 바뀜
    {
      w = x->parent->left;

      if (w->color == RBTREE_RED)
      {
        w->color = RBTREE_BLACK;
        x->parent->color = RBTREE_RED;
        right_rotate(t, x->parent);
        w = x->parent->left;
       }

      if ((w->left->color == RBTREE_BLACK) && (w->right->color == RBTREE_BLACK))
      {
        w->color = RBTREE_RED;
        x = x->parent;
      }
      else
      {
        if (w->left->color == RBTREE_BLACK)
        {
          w->right->color = RBTREE_BLACK;
          w->color = RBTREE_RED;
          left_rotate(t, w);
          w = x->parent->left;
        }

        w->color = x->parent->color;
        x->parent->color = RBTREE_BLACK;
        w->left->color = RBTREE_BLACK;
        right_rotate(t, x->parent);
        x = t->root;
      }
    }
  }

  x->color = RBTREE_BLACK;
}

int rbtree_erase(rbtree *t, node_t *z) 
{
  node_t* y = z;
  node_t* x = t->nil;
  color_t y_origin_color = y->color;

  if (z->left == t->nil)
  {
    x = z->right;
    rb_transplant(t, z, z->right);                              // z를 오른쪽 자식으로 바꾼다
  }
  else if (z->right == t->nil)
  {
    x = z->left;
    rb_transplant(t, z, z->left);                               // z를 왼쪽 자식으로 바꾼다
  }
  else
  {
    y = tree_minimum(t, z->right);                              // y는 z의 후손이다
    y_origin_color = y->color;
    x = y->right;
    
    if (y->parent == z)                                         // y가 트리에서 더 아래쪽인가?
    {
      x->parent = y;      
    }
    else                                                        
    {                                                           // x가 T.nil인 경우                                        
      rb_transplant(t, y, y->right);                            // y를 오른쪽 자식으로 바꾼다
      y->right = z->right;                                      // z의 오른쪽 자식
      y->right->parent = y;                                     // y의 오른쪽 자식
    }

    rb_transplant(t, z, y);                                     // z를 그 후손인 y로 바꾼다    
    y->left = z->left;                                          // z의 왼쪽 자식을 y에 부여한다
    y->left->parent = y;                                        // 왼쪽 자식이 없는 y
    y->color = z->color;
  }

  if (y_origin_color == RBTREE_BLACK)                         // 레드 블랙 위반이 발생한 경우
  {
    rb_delete_fixup(t, x);                                    // 수정함
  }

  free(z);
  return 0;
}

void inorder(const rbtree* t, node_t* x, key_t *arr, const size_t n, size_t* i)
{
  if (x == t->nil || *i >= n)
  {
    return;
  }

  inorder(t, x->left, arr, n, i);

  if (*i < n)
  {
    arr[(*i)++] = x->key;
  }

  inorder(t, x->right, arr, n, i);
}

//  rbtree_to_array(t, res, n);
int rbtree_to_array(const rbtree *t, key_t *arr, const size_t n) 
{
  size_t i = 0;
  inorder(t, t->root, arr, n, &i);

  return (int)i;
}
