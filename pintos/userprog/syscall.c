#include "userprog/syscall.h"
#include <stdio.h>
#include <syscall-nr.h>
#include "threads/interrupt.h"
#include "threads/thread.h"
#include "threads/loader.h"
#include "userprog/gdt.h"
#include "threads/flags.h"
#include "intrinsic.h"

void syscall_entry (void);
void syscall_handler (struct intr_frame *);

/* System call.
 *
 * Previously system call services was handled by the interrupt handler
 * (e.g. int 0x80 in linux). However, in x86-64, the manufacturer supplies
 * efficient path for requesting the system call, the `syscall` instruction.
 *
 * The syscall instruction works by reading the values from the the Model
 * Specific Register (MSR). For the details, see the manual. */

#define MSR_STAR 0xc0000081         /* Segment selector msr */
#define MSR_LSTAR 0xc0000082        /* Long mode SYSCALL target */
#define MSR_SYSCALL_MASK 0xc0000084 /* Mask for the eflags */
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2

void
syscall_init (void) {
	write_msr(MSR_STAR, ((uint64_t)SEL_UCSEG - 0x10) << 48  |
			((uint64_t)SEL_KCSEG) << 32);
	write_msr(MSR_LSTAR, (uint64_t) syscall_entry);

	/* The interrupt service rountine should not serve any interrupts
	 * until the syscall_entry swaps the userland stack to the kernel
	 * mode stack. Therefore, we masked the FLAG_FL. */
	write_msr(MSR_SYSCALL_MASK,
			FLAG_IF | FLAG_TF | FLAG_DF | FLAG_IOPL | FLAG_AC | FLAG_NT);
}

/* The main system call interface */
void syscall_handler (struct intr_frame *f UNUSED) {
	// TODO: Your implementation goes here.

	// 왜 RAX인지??
	int sys_number = f->R.rax;
	switch (sys_number){
		case SYS_HALT:
			break;

		case SYS_EXIT: {
			int status = (int) f->R.rdi;  // exit status
			sys_exit(status);
			break;
		}
			
		case SYS_FORK:
			break;

		case SYS_EXEC:

			break;

		case SYS_WAIT:
			break;

		case SYS_CREATE:
			break;

		case SYS_REMOVE:
			break;

		case SYS_OPEN:
			break;

		case SYS_FILESIZE:
			break;

		case SYS_READ:
			break;

		case SYS_WRITE:
			break;

		case SYS_SEEK:
			break;

		case SYS_TELL:
			break;

		case SYS_CLOSE:
			break;

		default:
			break;
	}

	printf ("system call!\n");
	thread_exit ();
}

void sys_exit(int status){

	struct thread *cur = thread_current();
	cur->exit_status = status;

	struct thread *parent = cur->parent;
	if (parent != NULL) {
		sema_up(&cur->wait_sema);  // 꺠우고 ()
		sema_down(&cur->exit_sema);
	}

	thread_exit();
}


void sys_exit(int status){

	struct thread *cur = thread_current();
	cur->exit_status = status;

	struct thread *parent = cur->parent;
	if (parent != NULL) {
		sema_up(&cur->wait_sema);  // 꺠우고 ()
		sema_down(&cur->exit_sema);
	}

	thread_exit();
}



// Note : arg buf는 사용자 프로세스 주소 공간에 있는 포인터 
int sys_write(int fd, const void *buf, size_t size){ 
	if (size == 0) return 0;
	if (buf == NULL || fd <= STDIN_FILENO){
		sys_exit(-1);
	} 	
	
	validate_user_buffer(buf, size);

	// 1 = STDOUT
	if (fd == STDOUT_FILENO) {
		putbuf(buf, size);
		return (int) size;
	}

	/**
	 * todo : 나중에 심화로 파일 쓰기 하기 
	 * - fd로 파일 객체 찾기
	 * - 락 걸고 파일 쓰기 
	 * 
	 */ 
}

/**
 * 검증할 것 
 * - buf가 실제로 매핑된 메모리가 있는지
 * - buf가 user영역에 속하는지
 */ 
void validate_user_buffer(const void *buf, size_t size) {
	// TODO: Your implementation goes here.
	const uint8_t *start = (uint8_t *)buf;
	const uint8_t *end = (uint8_t *)buf + size - 1;
	
	// 유효한 주소 인지 
	if (!is_user_vaddr((void *)start) || !is_user_vaddr((void *)end)) {
		sys_exit(-1);
	}

	// pg_round_down(va) : 이 va주소가 속한 페이지의 시작 주소를 구하는 메크로 
	// 페이지가 걸칠 수 있기 때문에 페이지 단위로 loop돌면서 pml4_get_page()로 매핑 여부 확인 
	for (uint8_t *p = pg_round_down(start); p < pg_round_down(end); p += PGSIZE){
		if (pml4_get_page(thread_current()->pml4, p) == NULL) {
			sys_exit(-1);
		}
	}
}

void validate_fd(int fd) {
	// TODO: Your implementation goes here.
	const struct thread *cur = thread_current();	
	if (fd < 0) {
		sys_exit(-1);
	}
	// if (cur->fd_table[fd] == NULL) {
	// 	sys_exit(-1);
	// }
}

void sys_exit(int staus){
	// 임시 
	struct thread *cur = thread_current();
	cur->status = staus;

	thread_exit();
}