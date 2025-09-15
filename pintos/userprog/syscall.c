#include "string.h"
#include "lib/stdarg.h"
#include "devices/input.h"
#include "filesys/file.h"
#include "filesys/filesys.h"
#include "include/threads/init.h"
#include "lib/kernel/console.h"
#include "userprog/syscall.h"
#include <stdio.h>
#include <stdlib.h>
#include <syscall-nr.h>
#include "threads/interrupt.h"
#include "threads/thread.h"
#include "threads/loader.h"
#include "userprog/gdt.h"
#include "threads/flags.h"
#include "intrinsic.h"

void syscall_entry (void);
void syscall_handler (struct intr_frame *);
static void sys_exit (int status);
static int sys_write(int fd, const void *buf, size_t size);
static void validate_user_buffer(const void *buf, size_t size);
static void validate_fd(int fd);
static bool file_create (const char *file, unsigned initial_size);
static int open_file(const char *file);
static int read(int fd, void *buffer, unsigned size);
static struct file *find_file_by_fd(int fd);
static uint64_t get_file_length(int fd);
static pid_t fork(const char *thread_name);

typedef int pid_t;
static struct lock filesys_lock;
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

	lock_init(&filesys_lock);
}

/* The main system call interface */
void syscall_handler (struct intr_frame *f UNUSED) {
	// TODO: Your implementation goes here.

	// 왜 RAX인지??
	struct thread *cur = thread_current();
	int sys_number = f->R.rax;
	switch (sys_number){
		case SYS_HALT:{
			power_off();
			break;
		}
			
		case SYS_EXIT: {
			int status = (int) f->R.rdi;  // exit status
			// printf("SYS_EXIT 호출로 받은 exit status : %d\n", status);
			sys_exit(status);
			break;
		}
			
		case SYS_FORK:{
			const char *thread_name = (char *) f->R.rdi;
			f->R.rax = fork(thread_name, f);
			break;
		}
			

		case SYS_EXEC:

			break;

		case SYS_WAIT:
			break;

		case SYS_CREATE: {
			const char *file = (const char *) f->R.rdi;
			unsigned initial_size = (int) f->R.rsi;
			f->R.rax = file_create(file, initial_size);
			break;
		}
			

		case SYS_REMOVE:
			break;

		case SYS_OPEN:{
			const char *file = (const char *) f->R.rdi;
			int result = open_file(file);
			f->R.rax = result;
			break;
		}


		case SYS_FILESIZE:{
			int fd = (int) f->R.rdi;
			f->R.rax = get_file_length(fd);
			break;
		}
			

		case SYS_READ: {
			int fd = (int) f->R.rdi;
			void *buf = (void *) f->R.rsi;
			unsigned size = (unsigned) f->R.rdx;
			int result = read(fd, buf, size);
			f->R.rax = result;
			break;
		}

		/**
		 * Return
		 * - 실제 적힌 수 
		 * - 0 : 바이트 적을 수 없으면
		 * -
		 */

		case SYS_WRITE:{
			int fd = (int) f->R.rdi;
			const void *buf = (const void *) f->R.rsi;
			size_t size = (int) f->R.rdx;
			int result = sys_write(fd, buf, size);
			f->R.rax = result;
			break;
		}

			

		case SYS_SEEK:
			break;

		case SYS_TELL:
			break;

		case SYS_CLOSE:
			break;

		default:{
			sys_exit(-1);
		}
	}

	//printf ("system call!\n");
	//thread_exit ();
}


/** 부모가 할 일 
 * 1. 값을 복사할 구조체 전용 메모리 할당 malloc - 
 * 2. 1번 구조체에 값 채워넣기(복사할 내용만)
 * 3. sema init 0으로 
 * 4. thread_create () - 2번에서 채운 내용 args로 넘기기 
 * 5. 자식 신호 대기 
 * 6. 깬 뒤 자식 tid 값 복사 
 * 7. 자식 메모리 해제 
 */
pid_t fork(const char *thread_name, struct intr_frame *frame){ 
	struct thread *cur = thread_current();
	// 1. 보따리 전용 메모리 할당 
	struct fork_args *f_args = malloc(sizeof(struct fork_args));

	// 2. 메모리에 값 채워넣기
	memcpy(&cur->tf, frame, sizeof(struct intr_frame));

	// 3. thread_create
	tid_t child_tid = thread_create(thread_name, PRI_DEFAULT, do_fork, cur);
	
	// 4. 대기 
	sema_down(&cur->fork_sema);
	if (child_tid < 0){
		return -1;
	}

	// 5, 6 
	pid_t result = child_tid;
	free(f_args);
	return result;
}

/** 자식이 할 일 
 * 1. 부모 arg로 받기?
 * 2. process_init?
 * 3. 부모의 children 채워넣기
 * 4. 가상 주소 공간 복사 (이건 아직 vm아니니까 pass)
 * 5. FD 테이블 복사 - reopen, seek 사용?
 * 6. intre_frame 복사
 * 7. rax = 0으로 세팅팅
 */
void do_fork(void *p){
		// va_copy??? 사용해야하나 
		struct thread *parent = (struct thread *) p;
		struct thread *child = thread_current();
		memcpy((void *)&child->tf, (const void *)&parent->tf, sizeof(struct intr_frame));
		

		// file_duplicate
		
}



uint64_t get_file_length(int fd) {
	struct file *file_ptr = find_file_by_fd(fd);
	if (file_ptr == NULL){
		return -1;
	}
	
	lock_acquire(&filesys_lock);
	off_t size = file_length(file_ptr);
	lock_release(&filesys_lock);
	return (uint64_t)size;
}


// return : 실제 읽은 값  (오류 시 -1)
int read (int fd, void *buffer, unsigned size) {
	if (fd == STDIN_FILENO){
		for (int i = 0; i < size; i++){
			((uint8_t *)buffer)[i] = input_getc();
		}
		return size;
	}

	if (fd == STDOUT_FILENO) {
		return -1;
	}
	
	validate_addr(buffer);
	struct file *to_read_file = find_file_by_fd(fd);
	
	if (to_read_file == NULL) {
		return -1;
	}

	lock_acquire(&filesys_lock);
	int n = file_read(to_read_file, buffer, (off_t) size);
	lock_release(&filesys_lock);
	return n;
}

struct file *find_file_by_fd(int fd){
	const struct thread *cur = thread_current();

	for(struct list_elem *e = list_begin(&cur->fd_table);
		e != list_end(&cur->fd_table);
		e = list_next(e))
	{
		struct fd_table_entry *entry = list_entry(e, struct fd_table_entry, elem);
		if (entry->fd == fd){
			return entry->file;
		}
	}
	return NULL;
}

/**
 * Return
 * - 성공 시 : FD
 * - 실패 시 : -1
 * 각각의 프로세스는 독립적인 파일 식별자들을 갖는다.
 * 파일 식별자는 자식 프로세스들에게 상속(전달)됩니다. 
 * 하나의 프로세스에 의해서든 다른 여러개의 프로세스에 의해서든, 하나의 파일이 두 번 이상 열리면 그때마다 open 시스템콜은 새로운 식별자를 반환합니다. 
 * FD는 포인터 주소만 -> 이중 포인터
 */
int open_file(const char *file){
	
	validate_addr(file);

	// 락 걸기 
	lock_acquire(&filesys_lock);
	struct file *opened_file = filesys_open(file);
	lock_release(&filesys_lock);
	if (opened_file == NULL){
		return -1;
	}

	struct thread *cur = thread_current();
	struct fd_table_entry *entry = malloc(sizeof(struct fd_table_entry));
	entry->fd = cur->next_fd;
	cur->next_fd++;
	entry->file = opened_file;
	list_push_back(&cur->fd_table, &entry->elem);

	return entry->fd;
}

// 파일이 성공적으로 생성 시 true 반환 
// 생성만하고 open하지 않는다.
bool file_create (const char *file, unsigned initial_size) {
	validate_addr(file);
	return filesys_create(file, initial_size);
}


void sys_exit(int status){

	struct thread *cur = thread_current();
	cur->exit_status = status;
	printf("%s: exit(%d)\n", cur->name, status);

	//if (cur->)
	if (cur->parent != NULL){
		sema_up(&cur->wait_sema);  // 꺠우고 ()
		sema_down(&cur->exit_sema);
	}
	
	thread_exit();
}


// Note : arg buf는 사용자 프로세스 주소 공간에 있는 포인터 
int sys_write(int fd, const void *buf, size_t size){ 
	if (size == 0) return 0;
	if (buf == NULL || fd <= STDIN_FILENO){
		-1;
	} 	
	
	validate_user_buffer(buf, size);

	// 1 = STDOUT
	if (fd == STDOUT_FILENO) {
		putbuf(buf, size);
		return (int) size;
	}

	struct file *to_write_file = find_file_by_fd(fd);
	if (to_write_file == NULL){
		sys_exit(-1);
	}

	lock_acquire(&filesys_lock);
	int n = file_write(to_write_file, buf, size);
	lock_release(&filesys_lock);
	return n;
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
	for (uint8_t *p = pg_round_down((void *)start); p <= pg_round_down((void *)end); p += PGSIZE){
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

void validate_addr(const void *addr) {
	if (addr == NULL || !(is_user_vaddr(addr)) || pml4_get_page(thread_current()->pml4, addr) == NULL) {
		sys_exit(-1);
	}
}
