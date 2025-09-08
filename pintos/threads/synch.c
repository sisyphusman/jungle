/* This file is derived from source code for the Nachos
   instructional operating system.  The Nachos copyright notice
   is reproduced in full below. */

/* Copyright (c) 1992-1996 The Regents of the University of California.
   All rights reserved.

   Permission to use, copy, modify, and distribute this software
   and its documentation for any purpose, without fee, and
   without written agreement is hereby granted, provided that the
   above copyright notice and the following two paragraphs appear
   in all copies of this software.

   IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO
   ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR
   CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF THIS SOFTWARE
   AND ITS DOCUMENTATION, EVEN IF THE UNIVERSITY OF CALIFORNIA
   HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

   THE UNIVERSITY OF CALIFORNIA SPECIFICALLY DISCLAIMS ANY
   WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
   WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
   PURPOSE.  THE SOFTWARE PROVIDED HEREUNDER IS ON AN "AS IS"
   BASIS, AND THE UNIVERSITY OF CALIFORNIA HAS NO OBLIGATION TO
   PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
   MODIFICATIONS.
   */

#include "threads/synch.h"
#include <stdio.h>
#include <string.h>
#include "threads/interrupt.h"
#include "threads/thread.h"


static list_more_func higher_priority_basic;
static list_more_func higher_priority_donate;
static bool is_contain(struct list *target_list, struct list_elem *target_elem);
static bool is_semaphore_contain(struct thread *t, struct semaphore *sema);
static bool cond_sema_more (const struct list_elem *a,
                            const struct list_elem *b,
                            void *aux UNUSED); 
/* Initializes semaphore SEMA to VALUE.  A semaphore is a
   nonnegative integer along with two atomic operators for
   manipulating it:

   - down or "P": wait for the value to become positive, then
   decrement it.

   - up or "V": increment the value (and wake up one waiting
   thread, if any). */
void sema_init (struct semaphore *sema, unsigned value) {
	ASSERT (sema != NULL);

	sema->value = value;
	list_init (&sema->waiters);
}

/* Down or "P" operation on a semaphore.  Waits for SEMA's value
   to become positive and then atomically decrements it.

   This function may sleep, so it must not be called within an
   interrupt handler.  This function may be called with
   interrupts disabled, but if it sleeps then the next scheduled
   thread will probably turn interrupts back on. This is
   sema_down function. */
void sema_down (struct semaphore *sema) {
	enum intr_level old_level;

	ASSERT (sema != NULL);
	ASSERT (!intr_context ());
	
	// 보유한 락의 sema_donw 시 종료시키기 
	struct thread *cur = thread_current();
	old_level = intr_disable ();
	while (sema->value == 0) {
		list_insert_ordered(&sema->waiters, &cur->elem, higher_priority_basic, NULL);
		thread_block ();
	}
	sema->value--;
	intr_set_level (old_level);
}

bool is_semaphore_contain(struct thread *t, struct semaphore *sema) {
	ASSERT(t != NULL);
	ASSERT(sema != NULL);

	if (list_empty(&t->held_locks)) return false;

	struct list_elem *e = list_begin(&t->held_locks);
	while (e != NULL && e != list_end(&t->held_locks))
  {
		struct lock *hold = list_entry(e, struct lock, elem);
		if (&hold->semaphore == sema){
			return true;
		}
		
		e = list_next(e);
	}
	return false;
}

static bool higher_priority_basic(const struct list_elem *a,
                             const struct list_elem *b,
                             void *aux UNUSED){
	const struct thread *thread_a = list_entry(a, struct thread, elem);
	const struct thread *thread_b = list_entry(b, struct thread, elem);
  return thread_a->eff_priority > thread_b->eff_priority;
}

static bool higher_priority_donate(const struct list_elem *a,
                             const struct list_elem *b,
                             void *aux UNUSED){
	const struct thread *thread_a = list_entry(a, struct thread, donate_elem);
	const struct thread *thread_b = list_entry(b, struct thread, donate_elem);
  return thread_a->eff_priority > thread_b->eff_priority;
}

/* Down or "P" operation on a semaphore, but only if the
   semaphore is not already 0.  Returns true if the semaphore is
   decremented, false otherwise.

   This function may be called from an interrupt handler. */
bool
sema_try_down (struct semaphore *sema) {
	enum intr_level old_level;
	bool success;

	ASSERT (sema != NULL);

	old_level = intr_disable ();
	if (sema->value > 0)
	{
		sema->value--;
		success = true;
	}
	else
		success = false;
	intr_set_level (old_level);

	return success;
}

/* Up or "V" operation on a semaphore.  Increments SEMA's value
   and wakes up one thread of those waiting for SEMA, if any.

   This function may be called from an interrupt handler. */
void sema_up (struct semaphore *sema) {
	enum intr_level old_level;

	ASSERT (sema != NULL);

	old_level = intr_disable ();
	struct thread *next = NULL;
	if (!list_empty (&sema->waiters)) {
		list_sort(&sema->waiters, higher_priority_basic, NULL);
		struct list_elem *e = list_pop_front(&sema->waiters);
		next = list_entry (e, struct thread, elem);
		thread_unblock(next);
	}
	
	sema->value++;
	intr_set_level (old_level);

	/* If the unblocked thread has higher priority, yield. */
	if (next && next->eff_priority > thread_current()->eff_priority) {
		if (intr_context()) intr_yield_on_return();
		else thread_yield();
	}
}

static void sema_test_helper (void *sema_);

/* Self-test for semaphores that makes control "ping-pong"
   between a pair of threads.  Insert calls to printf() to see
   what's going on. */
void
sema_self_test (void) {
	struct semaphore sema[2];
	int i;

	printf ("Testing semaphores...");
	sema_init (&sema[0], 0);
	sema_init (&sema[1], 0);
	thread_create ("sema-test", PRI_DEFAULT, sema_test_helper, &sema);
	for (i = 0; i < 10; i++)
	{
		sema_up (&sema[0]);
		sema_down (&sema[1]);
	}
	printf ("done.\n");
}

/* Thread function used by sema_self_test(). */
static void
sema_test_helper (void *sema_) {
	struct semaphore *sema = sema_;
	int i;

	for (i = 0; i < 10; i++)
	{
		sema_down (&sema[0]);
		sema_up (&sema[1]);
	}
}

/* Initializes LOCK.  A lock can be held by at most a single
   thread at any given time.  Our locks are not "recursive", that
   is, it is an error for the thread currently holding a lock to
   try to acquire that lock.

   A lock is a specialization of a semaphore with an initial
   value of 1.  The difference between a lock and such a
   semaphore is twofold.  First, a semaphore can have a value
   greater than 1, but a lock can only be owned by a single
   thread at a time.  Second, a semaphore does not have an owner,
   meaning that one thread can "down" the semaphore and then
   another one "up" it, but with a lock the same thread must both
   acquire and release it.  When these restrictions prove
   onerous, it's a good sign that a semaphore should be used,
   instead of a lock. */
void lock_init (struct lock *lock) {
	ASSERT (lock != NULL);

	lock->holder = NULL;
	sema_init (&lock->semaphore, 1);
}

/* Acquires LOCK, sleeping until it becomes available if
   necessary.  The lock must not already be held by the current
   thread.

   This function may sleep, so it must not be called within an 
	 interrupt handler. (중요)  This function may be called with
   interrupts disabled, but interrupts will be turned back on if
   we need to sleep. */

/**
 * 락 획득 시도 => 
 * 1. 주인이 있으면 
 * - 대기자 등록 in sema => sema_down()에서 구현되어 있음
 * - 전파하기 
 * - sema_down에서 블락당하기 
 * 2. 주인이 없으면
 * - 그냥 ㄱ  
 */
void lock_acquire (struct lock *lock) {
	ASSERT (lock != NULL);
	ASSERT (!intr_context ());
	ASSERT (!lock_held_by_current_thread (lock));

	// 고민 : 전파를 어디서 해야할까? sema_down에 맡기는게 맞을까???
	enum intr_level old = intr_disable();
	struct thread *cur = thread_current();

	if (lock->holder) { // 락 대기자 등록은 SEMA_DOWN에서 하네 
		cur->waiting_lock = lock;
		propagate_eff_priority();
	}

	// 지금 만들어야 되는 작업 : lock을 획득하고 sema_down을 하면 걍 종료해야 함 
	sema_down (&lock->semaphore);
	lock->holder = cur;
	cur->waiting_lock = NULL;
	list_push_back(&cur->held_locks, &lock->elem);

	intr_set_level(old);
}

/**
 * 전파 동안 해야할 일
 * 1. lock_donators 재정렬 : Cuz cur의 유효 우선순위가 바꼈으니 
 * 2. 새로운 유효 우선순위 계산 및 검증 
 * 3. 변경 됐고 ready상태라면 ready_list update
 */
// todo : 분기가 너무 많긴한데 나중에 고쳐보자 

void propagate_eff_priority() {

	enum intr_level old = intr_disable();
	
	struct thread *cur = thread_current();
	struct lock *w_lock = cur->waiting_lock;
	
	while ((w_lock = cur->waiting_lock) && w_lock->holder)
	{
		struct thread *w_lock_holder = w_lock->holder;
		// 1. lock_donators 재정렬
		// Only remove if the element is already in a list
		bool is_donator = is_contain(&w_lock_holder->donators, &cur->donate_elem);
		if (!list_empty(&w_lock_holder->donators) && is_donator){
				list_remove(&cur->donate_elem);
		}
		list_insert_ordered(&w_lock_holder->donators, &cur->donate_elem, higher_priority_donate, NULL);

		int before_eff = w_lock_holder->eff_priority;	
		if (cur->eff_priority <= before_eff) break;
		
		// 2. 새로운 유효 우선순위 계산
		recompute_eff_priority(w_lock_holder);
		
		// 변화 없으면 기부 안한걸로 치고 그 뒤 전파도 필요 없음
		if (w_lock_holder->eff_priority == before_eff) break; 

		if (w_lock_holder->status == THREAD_READY) {
			requeue_ready_list(w_lock_holder);
		}
		
		cur = w_lock_holder;
	}

	intr_set_level(old);
}

bool is_contain(struct list *target_list, struct list_elem *target_elem) {
	struct list_elem *e;
	for (e = list_begin(target_list); e != list_end(target_list); e = list_next(e)) {
		if (e == target_elem) return true;
	}

	return false;
}

/**
 * donators가 비어있다면 new_eff = cur->eff_priority
 * donators가 비어있지 않다면 new_eff = max(기부자 중 짱, ~~);
 */
void recompute_eff_priority(struct thread *t){
		enum intr_level old = intr_disable();

		int new_eff = t->priority;  // Start with thread's base priority
		if (!list_empty(&t->donators)) {
			struct thread *top = list_entry(list_front(&t->donators), struct thread, donate_elem);
			new_eff = max(top->eff_priority, t->priority);
		}

		t->eff_priority = new_eff;
		intr_set_level(old);
}

int max(int a, int b){
	return (a >= b) ? a : b;
}

/* Tries to acquires LOCK and returns true if successful or false
   on failure.  The lock must not already be held by the current
   thread.

   This function will not sleep, so it may be called within an
   interrupt handler. */
bool lock_try_acquire (struct lock *lock) {
	bool success;

	ASSERT (lock != NULL);
	ASSERT (!lock_held_by_current_thread (lock));

	success = sema_try_down (&lock->semaphore);
	if (success)
		lock->holder = thread_current ();
	return success;
}

/* Releases LOCK, which must be owned by the current thread.
   This is lock_release function.

   An interrupt handler cannot acquire a lock, so it does not
   make sense to try to release a lock within an interrupt 
   handler. */ 

/**
 * (주의 : 인터럽트 핸들러에 의해 호출되면 안되는 메서드)
 * 락해제 시 해야할 일 
 * 1. 유효 우선순위 반납
 * - 해당 락때문에 donate된 유효 우선순위 반납 
 * - 물론, 무조건 base_priority로 되는건 아님
 * - 반납 후 donators에도 제외
 * 
 * 2. waiting하고 있는애 깨워주기만??
 * 
 */
void lock_release (struct lock *lock) {
	ASSERT (lock != NULL);
	ASSERT (lock_held_by_current_thread (lock));

	enum intr_level old = intr_disable();
	struct thread *cur = lock->holder;
	/**
	 * 1. 그 락의 우선순위에 영향 미친애들 전부 찾고 donators에서 제거 
	 * - pintos는 list의 header, tail을 센티널로 관리한다.
	 * - list_begin, list_end는 이 센티널을 가리킴 
	 * 2. eff 재계산 or 조건부 재계산
	 * 3. BLOCKED 된 애 READY 로 깨워주기 - 이건 sema_up이 알아서 함 
	 */
	// todo : donators 비었는지 확인, cur 우선순위 낮아졌다면 양보 필요, 근데 sema_up, unblock이 해주지 않나?
	int before_eff_priority = cur->eff_priority;
	struct thread *next = NULL;
	if (!list_empty(&cur->donators)){
		// 1. 
		remove_donators_related_lock(cur, lock);
		// 2. 
		recompute_eff_priority(cur);
	}

	// 더 낮아 졌고, READY상태라면 => ready_list 초기화
	if ((before_eff_priority != cur->eff_priority) &&
		cur->status == THREAD_READY) {
		requeue_ready_list(cur);
	}

	lock->holder = NULL;
	// 3. 
	sema_up (&lock->semaphore); // 여기서 어차피 unblock함



	intr_set_level(old);
}

// 주어진 락을 기다리는 donators 전부 삭제 
void remove_donators_related_lock(struct thread *t, struct lock *lock){
	struct list_elem *e = list_begin(&t->donators);
	while (e != list_end(&t->donators))
	{
		struct thread *donor_thread = list_entry(e, struct thread, donate_elem);
		struct list_elem *next = list_next(e); 
		if (donor_thread->waiting_lock == lock){
			list_remove(&donor_thread->donate_elem);		
		}
		e = next;
	}	
}

/* Returns true if the current thread holds LOCK, false
   otherwise.  (Note that testing whether some other thread holds
   a lock would be racy.) */
bool
lock_held_by_current_thread (const struct lock *lock) {
	ASSERT (lock != NULL);

	return lock->holder == thread_current ();
}

/* One semaphore in a list. */
struct semaphore_elem {
	struct list_elem elem;              /* List element. */
	struct semaphore semaphore;         /* This semaphore. */
};

/* Initializes condition variable COND.  A condition variable
   allows one piece of code to signal a condition and cooperating
   code to receive the signal and act upon it. */
void
cond_init (struct condition *cond) {
	ASSERT (cond != NULL);

	list_init (&cond->waiters);
}

/* Atomically releases LOCK and waits for COND to be signaled by
   some other piece of code.  After COND is signaled, LOCK is
   reacquired before returning.  LOCK must be held before calling
   this function.

   The monitor implemented by this function is "Mesa" style, not
   "Hoare" style, that is, sending and receiving a signal are not
   an atomic operation.  Thus, typically the caller must recheck
   the condition after the wait completes and, if necessary, wait
   again.

   A given condition variable is associated with only a single
   lock, but one lock may be associated with any number of
   condition variables.  That is, there is a one-to-many mapping
   from locks to condition variables.

   This function may sleep, so it must not be called within an
   interrupt handler.  This function may be called with
   interrupts disabled, but interrupts will be turned back on if
   we need to sleep. */
void
cond_wait (struct condition *cond, struct lock *lock) {
	struct semaphore_elem waiter;

	ASSERT (cond != NULL);
	ASSERT (lock != NULL);
	ASSERT (!intr_context ());
	ASSERT (lock_held_by_current_thread (lock));

	sema_init (&waiter.semaphore, 0);
	list_insert_ordered(&cond->waiters, &waiter.elem, cond_sema_more, NULL);
	//list_push_back (&cond->waiters, &waiter.elem);
	lock_release (lock);
	sema_down (&waiter.semaphore);
	lock_acquire (lock);
}

static bool cond_sema_more (const struct list_elem *a,
                            const struct list_elem *b,
                            void *aux UNUSED) {
  const struct semaphore_elem *sa = list_entry(a, struct semaphore_elem, elem);
  const struct semaphore_elem *sb = list_entry(b, struct semaphore_elem, elem);

  // 각 세마의 웨이터들 중 가장 높은 우선순위 스레드를 비교
  struct thread *ta = list_entry(list_front(&sa->semaphore.waiters), struct thread, elem);
  struct thread *tb = list_entry(list_front(&sb->semaphore.waiters), struct thread, elem);
  return ta->eff_priority > tb->eff_priority;
}

/* If any threads are waiting on COND (protected by LOCK), then
   this function signals one of them to wake up from its wait.
   LOCK must be held before calling this function.

   An interrupt handler cannot acquire a lock, so it does not
   make sense to try to signal a condition variable within an
   interrupt handler. */
void
cond_signal (struct condition *cond, struct lock *lock UNUSED) {
	ASSERT (cond != NULL);
	ASSERT (lock != NULL);
	ASSERT (!intr_context ());
	ASSERT (lock_held_by_current_thread (lock));

	if (!list_empty (&cond->waiters))
		sema_up (&list_entry (list_pop_front (&cond->waiters),
					struct semaphore_elem, elem)->semaphore);
}

/* Wakes up all threads, if any, waiting on COND (protected by
   LOCK).  LOCK must be held before calling this function.

   An interrupt handler cannot acquire a lock, so it does not
   make sense to try to signal a condition variable within an
   interrupt handler. */
void
cond_broadcast (struct condition *cond, struct lock *lock) {
	ASSERT (cond != NULL);
	ASSERT (lock != NULL);

	while (!list_empty (&cond->waiters))
		cond_signal (cond, lock);
}
