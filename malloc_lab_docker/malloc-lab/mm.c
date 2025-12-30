#define WSIZE   4                                                       // 워드 크기: 헤더/푸터의 크기(4바이트)
#define DSIZE   8                                                       // 더블 워드 크기: 최소 블록 크기(8바이트, 정렬용)
#define CHUNKSIZE (1<<12)                                               // 힙을 확장할 때 기본 크기(4096바이트 = 4KB) 2^12 = 4096
    
#define MAX(x,y) ((x) > (y) ? (x) : (y))                                // 두 값 중 더 큰 값을 반환하는 매크로
    
#define PACK(size, alloc) ((size) | (alloc))                            // or 연산으로 합침, 블록의 크기(size)와 할당 여부(alloc)를 하나의 워드에 저장. size는 항상 8의 배수이므로 하위 3비트가 비어있고, 그 중 1비트를 할당 여부 표시로 사용
                                                    
#define GET(p)      (*(unsigned int*)(p))                               // 주소 p가 가리키는 워드(4바이트)를 읽어옴
#define PUT(p, val) (*(unsigned int*)(p) = (val))                       // 주소 p가 가리키는 워드(4바이트)에 val을 저장
    
#define GET_SIZE(p) (GET(p) & ~0x7)                                     // 헤더/푸터에 저장된 값에서 하위 3비트를 제외한 블록의 크기만 추출 0x7 = 0b111, ~0x7 = 111...1000
#define GET_ALLOC(p) (GET(p) & 0x1)                                     // 헤더/푸터 값에서 할당 여부 비트(최하위 1비트)만 추출
    
#define HDRP(bp) ((char*)(bp) - WSIZE)                                  // 주어진 블록 포인터(bp, payload 시작점)에서 헤더 위치로 이동
#define FTRP(bp) ((char*)(bp) + GET_SIZE(HDRP(bp)) - DSIZE)             // 주어진 블록 포인터(bp)에서 푸터 위치로 이동, 주어진 블록 포인터(bp)에서 푸터 위치로 이동

#define NEXT_BLKP(bp) ((char*)(bp) + GET_SIZE(((char*)(bp) - WSIZE)))   // 현재 블록(bp)의 헤더를 참조해 블록 크기를 더하여 다음 블록의 payload 주소 반환
#define PREV_BLKP(bp) ((char*)(bp) - GET_SIZE(((char*)(bp) - DSIZE)))   // 현재 블록(bp)의 푸터를 참조해 블록 크기를 빼서 이전 블록의 payload 주소 반환

/*
 * mm-naive.c - The fastest, least memory-efficient malloc package.
 *
 * In this naive approach, a block is allocated by simply incrementing
 * the brk pointer.  A block is pure payload. There are no headers or
 * footers.  Blocks are never coalesced or reused. Realloc is
 * implemented directly using mm_malloc and mm_free.
 *
 * NOTE TO STUDENTS: Replace this header comment with your own header
 * comment that gives a high level description of your solution.
 */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>
#include <string.h>

#include "mm.h"
#include "memlib.h"

/*********************************************************
 * NOTE TO STUDENTS: Before you do anything else, please
 * provide your team information in the following struct.
 ********************************************************/
team_t team = {
    /* Team name */
    "ateam",
    /* First member's full name */
    "Harry Bovik",
    /* First member's email address */
    "bovik@cs.cmu.edu",
    /* Second member's full name (leave blank if none) */
    "",
    /* Second member's email address (leave blank if none) */
    ""};

/* single word (4) or double word (8) alignment */
#define ALIGNMENT 8

/* rounds up to the nearest multiple of ALIGNMENT */
#define ALIGN(size) (((size) + (ALIGNMENT - 1)) & ~0x7)                 // 주어진 크기 size를 8바이트 배수로 올려서 정렬하는 매크로입니다 메모리 블록을 항상 더블워드 경계(8바이트) 정렬
                                                                        // (size + 7) → 미리 약간 키워서 올림 효과를 유도, & ~0x7 → 하위 3비트를 날려서 8의 배수로 만든다
                                                                        // 항상 올림 정렬하기 위해서 +7 한 이후, & ~0x7 한다
#define SIZE_T_SIZE (ALIGN(sizeof(size_t)))                             // 블록의 헤더를 저장하는 데 필요한 최소 크기를, 8바이트 단위로 맞춘 값

static char* heap_listp;
static char* save_bp;

static void* coalesce(void* bp)                                         // free된 블록을 인접 블록들과 합쳐서 더 큰 free 블록을 만드는 함수
{
    size_t prev_alloc = GET_ALLOC(FTRP(PREV_BLKP(bp)));                 // 현재 블록 바로 앞에 있는 블록이 할당되어 있는지 확인
    size_t next_alloc = GET_ALLOC(HDRP(NEXT_BLKP(bp)));                 // 현재 블록 바로 다음에 있는 블록이 할당되어 있는지 확인
    size_t size = GET_SIZE(HDRP(bp));                                   // 전체 크기(헤더+payload+푸터) 를 읽어옴

    if (prev_alloc && next_alloc)                                       // 이전 블록도 할당, 다음 블록도 할당 → 병합 불가
    {
        return bp;
    }
    else if (prev_alloc && !next_alloc)                                 // 이전 블록 할당, 다음 블록은 프리
    {
        size += GET_SIZE(HDRP(NEXT_BLKP(bp)));                          // 현재 블록 + 다음 블록 크기 합침
        PUT(HDRP(bp), PACK(size, 0));                                   // 합쳐진 블록의 헤더 갱신
        PUT(FTRP(bp), PACK(size, 0));                                   // 합쳐진 블록의 푸터 갱신
    }
    else if (!prev_alloc && next_alloc)                                 // 앞은 free, 뒤는 할당
    {
        size += GET_SIZE(HDRP(PREV_BLKP(bp)));                          // 현재 블록 + 이전 블록 크기 합침
        PUT(FTRP(bp), PACK(size, 0));                                   // 새 블록의 푸터 갱신
        PUT(HDRP(PREV_BLKP(bp)), PACK(size, 0));                        // 새 블록의 헤더 갱신
        bp = PREV_BLKP(bp);                                             // 블록 포인터를 "앞 블록"으로 이동
    }
    else
    {
        size += GET_SIZE(HDRP(PREV_BLKP(bp))) +                         
            GET_SIZE(FTRP(NEXT_BLKP(bp)));                              // 앞 + 현재 + 뒤 크기 합침
        PUT(HDRP(PREV_BLKP(bp)), PACK(size, 0));                        // 새로운 헤더는 이전 블록 헤더
        PUT(FTRP(NEXT_BLKP(bp)), PACK(size, 0));                        // 새로운 푸터는 다음 블록 푸터
        bp = PREV_BLKP(bp);                                             // 블록 시작을 이전 블록으로 이동
    }

    return bp;
}

static void* extend_heap(size_t words)                                  // 힙 공간이 부족할 때 새로운 블록을 힙에 확장해서 추가
 {
    char* bp;
    size_t size;

    size = ALIGN(words * WSIZE);
    
    // size = (words % 2) ? (words + 1) * WSIZE : words * WSIZE;        // words가 홀수이면 +1해서 짝수로 만들어준다 size는 8의 배수

    if ((long)(bp = mem_sbrk(size)) == -1)                              // mem_sbrk(size)로 힙을 size 바이트 확장
        return NULL;
    
    PUT(HDRP(bp), PACK(size, 0));                                       // 새로 확장한 블록을 free 블록으로 초기화
    PUT(FTRP(bp), PACK(size, 0));                                       // 헤더와 푸터에 (size, alloc=0)을 기록
    PUT(HDRP(NEXT_BLKP(bp)), PACK(0, 1));                               // 힙의 에필로그 블록(epilogue block) 생성

    return coalesce(bp);                                                // 최종적으로 병합된 free 블록의 포인터 반환
 }

/*
 * mm_init - initialize the malloc package.
 */

int mm_init(void)
{
    if ((heap_listp = mem_sbrk(4 * WSIZE)) == (void*)-1)                // 초기 힙 영역을 4워드(16바이트) 크기로 요청
        return -1;
    
    PUT(heap_listp, 0);                                                 // [워드 0] 패딩 (정렬용, 사용 안 함)
    PUT(heap_listp + (1 * WSIZE), PACK(DSIZE, 1));                      // [워드 1] 프롤로그 헤더 (크기 8, 할당됨)
    PUT(heap_listp + (2 * WSIZE), PACK(DSIZE, 1));                      // [워드 2] 프롤로그 푸터 (크기 8, 할당됨)
    PUT(heap_listp + (3 * WSIZE), PACK(0, 1));                          // [워드 3] 에필로그 헤더 (크기 0, 할당됨)
    heap_listp += (2 * WSIZE);                                          // 프롤로그 블록의 payload 시작 주소로 이동

    if (extend_heap(CHUNKSIZE/WSIZE) == NULL)
        return -1;

    save_bp = heap_listp;
    return 0;
}

char* first_fit(size_t asize)                                           // asize = 찾으려는 블록의 필요 크기
{
    void* bp;                                                           // 현재 탐색 중인 블록의 payload 포인터

    for (bp = heap_listp; GET_SIZE(HDRP(bp)) > 0; bp = NEXT_BLKP(bp))   // 첫 번째-맞춤(first fit): 힙의 처음부터 탐색
    {
        if (!GET_ALLOC(HDRP(bp)) && (asize <= GET_SIZE(HDRP(bp))))      // 블록이 비어 있고(헤더의 할당 비트가 0), 크기가 충분하다면 bp 반환
        {
            return bp;
        }
    }

    return NULL;
}

char* next_fit(size_t asize)
{
    void* bp;

    for (bp = save_bp; GET_SIZE(HDRP(bp)) > 0; bp = NEXT_BLKP(bp))      // 직전 위치부터 힙 끝까지 탐색
    {
        if (!GET_ALLOC(HDRP(bp)) && (asize <= GET_SIZE(HDRP(bp))))
        {
            save_bp = bp;
            return bp;
        }
    }

    for (bp = heap_listp; bp < save_bp; bp = NEXT_BLKP(bp))             // 직전 위치부터 save_bp 직전까지
    {
        if (!GET_ALLOC(HDRP(bp)) && (asize <= GET_SIZE(HDRP(bp))))
        {
            save_bp = bp;
            return bp;
        }
    }

    return NULL;                                                        // 못 찾음
}

char* best_fit(size_t asize)
{
    void* bp;
    void* best_bp = NULL;                                               // 지금까지 찾은 최적(가장 잘 맞는) 블록의 포인터
    size_t best_size = (size_t)-1;                                      // 지금까지 찾은 최적 블록의 크기 (처음엔 최대값으로 설정)

    for (bp = heap_listp; GET_SIZE(HDRP(bp)) > 0; bp = NEXT_BLKP(bp))   // 힙의 첫 블록부터 끝까지 선형 탐색
    {
        if (!GET_ALLOC(HDRP(bp)))                                       // 블록이 가용 상태라면
        {
            size_t csize = GET_SIZE(HDRP(bp));                          // 현재 블록의 전체 크기

            if (csize >= asize)                                         // 현재 블록이 asize 이상이면 후보
            {
                if (csize == asize)                                     // 딱 맞는 크기 발견 시 → Best-fit의 최적 상황
                {
                    return bp;                                          // 즉시 반환 (탐색 종료)
                }
                
                if (csize < best_size)                                  // 지금까지 본 후보 중 더 작은 블록이라면 갱신
                {
                    best_size = csize;
                    best_bp = bp;
                }
            }
        }
    }

    if (best_bp != NULL)                                                // 탐색이 끝난 뒤 최적 블록(best_bp)이 있으면 반환
    {
        return best_bp;
    }

    return NULL;
}

static void place(void* bp, size_t asize)
{
    size_t csize = GET_SIZE(HDRP(bp));                                   // 현재 가용 블록의 크기

    if ((csize - asize) >= (2 * DSIZE))                                  // 분할 후에도 최소 블록 크기(16바이트) 이상 남는 경우
    {
        PUT(HDRP(bp), PACK(asize, 1));                                   // 앞쪽 부분을 할당 블록으로 설정
        PUT(FTRP(bp), PACK(asize, 1));
        
        void* rest = NEXT_BLKP(bp);                                      // 남은 부분은 새로운 가용 블록으로 설정
        PUT(HDRP(rest), PACK(csize-asize, 0));
        PUT(FTRP(rest), PACK(csize-asize, 0));
        save_bp = rest;
    }
    else
    {
        PUT(HDRP(bp), PACK(csize, 1));                                   // 잔여분 없이 통째로 할당
        PUT(FTRP(bp), PACK(csize, 1));
        save_bp = NEXT_BLKP(bp);
    }
}

/*
 * mm_malloc - Allocate a block by incrementing the brk pointer.
 *     Always allocate a block whose size is a multiple of the alignment.
 */
void *mm_malloc(size_t size)
{
    // int newsize = ALIGN(size + SIZE_T_SIZE);                        // 요청한 size에 추가 메타데이터 공간(SIZE_T_SIZE)를 더하고, 블록 크기를 ALIGN 매크로로 정렬한다
    // void *p = mem_sbrk(newsize);                                    // mem_sbrk로 힙을 newsize만큼 확장한다
    // if (p == (void *)-1)                                            // mem_sbrk가 실패하면, (void *)-1를 반환하므로 NULL을 리턴한다
    //     return NULL;   
    // else   
    // {   
    //     *(size_t *)p = size;                                        // 블록 맨 앞에 payLoad의 크기를 기록한다
    //     return (void *)((char *)p + SIZE_T_SIZE);                   // 사용자에게는 그 다음 주소(payLoad 시작점)을 반환한다
    // }   
   
    size_t asize;                                                      // 실제 할당할 블록의 크기 (헤더/푸터, 정렬 포함)
    size_t extendsize;                                                 // 힙에 새로 확장할 크기                            
    char* bp;                                                          // 블록 포인터 (payload 시작점)

    if (size == 0)                                              
        return NULL;
    

    asize = MAX(2 * DSIZE, ALIGN(size + DSIZE));                       // 최소 블록 크기(16B) 보장 + 헤더/푸터 8B 포함해 정렬
    
    // if (size <= DSIZE)
    //     asize = 2 * DSIZE;                                          // 요청 크기가 너무 작으면, 최소 블록 크기(16바이트)로 맞춤
    // else
    //     asize = DSIZE * ((size + (DSIZE) + (DSIZE - 1)) / DSIZE);   // 요청 크기가 클 경우: 헤더/푸터 등 오버헤드와 정렬을 포함해 8바이트(DSIZE) 배수로 올림 처리
    
    if ((bp = best_fit(asize)) != NULL)                                // 가용 리스트에서 asize 크기 이상 맞는 블록을 탐색
    {   
        place(bp, asize);                                              // 찾았다면 그 블록에 asize 크기만큼 배치 (필요시 분할)
        return bp;                                                     // 블록의 payload 포인터 반환
    }   
   
    extendsize = MAX(asize, CHUNKSIZE);                                // 못 찾으면, 최소 4KB(CHUNKSIZE) 또는 asize 중 큰 값만큼 확장
    if ((bp = extend_heap(extendsize / WSIZE)) == NULL)                // 힙 확장 시도 (워드 단위 환산)
        return NULL;   
   
    place(bp, asize);                                                  // 확장된 블록에 asize 크기만큼 배치
    return bp;                                                         // 최종 블록의 payload 포인터 반환
}

/*
 * mm_free - Freeing a block does nothing.
 */
void mm_free(void *bp)
{
    size_t size = GET_SIZE(HDRP(bp));
    
    // 1) 내가 free임을 먼저 표기
    PUT(HDRP(bp), PACK(size, 0));
    PUT(FTRP(bp), PACK(size, 0));

    // 2) 그 다음 병합해서 새 시작 포인터 받기
    bp = coalesce(bp);

    // 3) next-fit의 시작점 업데이트
    save_bp = bp;
}

/*
 * mm_realloc - Implemented simply in terms of mm_malloc and mm_free
 */
void *mm_realloc(void *ptr, size_t size)
{
    // void *oldptr = ptr;
    // void *newptr;
    // size_t copySize;

    // newptr = mm_malloc(size);
    // if (newptr == NULL)
    //     return NULL;
    // copySize = *(size_t *)((char *)oldptr - SIZE_T_SIZE);
    // if (size < copySize)
    //     copySize = size;
    // memcpy(newptr, oldptr, copySize);
    // mm_free(oldptr);
    // return newptr;

    if (ptr == NULL)                            // ptr이 NULL이면 그냥 malloc과 동일하게 동작
    {
        return mm_malloc(size);
    }
    
    if (size == 0)                              // 요청 크기가 0이면 free와 동일하게 동작
    {
        mm_free(ptr);
        return NULL;
    }

    size_t old_block = GET_SIZE(HDRP(ptr));     // 헤더에 있는 블록 전체 크기
    size_t old_payload = old_block - DSIZE;     // payLoad 크기(헤더 + 푸터 제외)

    size_t asize = MAX(2*DSIZE, ALIGN(size + DSIZE));
    // size_t asize = (size <= DSIZE) ? 2 * DSIZE : DSIZE * ((size + DSIZE + (DSIZE - 1)) / DSIZE);

    if (asize <= old_block)                     // 기존 블록이 충분히 커서 그대로 사용 가능
    {
        place(ptr, asize);                      // 필요하다면 블록을 분할
        return ptr;                             // 그대로 반환
    }

    void* next = NEXT_BLKP(ptr);
    
    if (!GET_ALLOC(HDRP(next)) && old_block + GET_SIZE(HDRP(next)) >= asize)  // 바로 뒤 블록이 free 상태이고, 합치면 asize 이상이 되는 경우 → in-place 확장
    {
        size_t total = old_block + GET_SIZE(HDRP(next));
        PUT(HDRP(ptr), PACK(total, 1));                                       // 헤더/푸터 갱신해서 현재 블록을 크게 만든다
        PUT(FTRP(ptr), PACK(total, 1));
        place(ptr, asize);                                                    // 필요하다면 다시 분할
        return ptr;                                                           // 포인터 그대로 반환 (복사 불필요)
    }

    void* newp = mm_malloc(size);                                             // 새 블록을 따로 할당해야 하는 경우
    
    if (!newp)
    {
        return NULL;
    }

    size_t copy = (old_payload < size) ? old_payload : size;                  // 기존 payload 데이터를 새 블록으로 복사, 크기는 기존 payload와 새 요청 중 작은 값
    memcpy(newp, ptr, copy);
    mm_free(ptr);                                                             // 기존 블록 반환
    return newp;
}