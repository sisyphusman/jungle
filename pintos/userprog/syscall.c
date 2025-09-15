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
void
syscall_handler (struct intr_frame *f UNUSED) {
	// TODO: Your implementation goes here.
	int syscall = f->R.rax;

	switch (syscall)
	{
	case SYS_WRITE:
		//printf ("write 호출!\n");
		f->R.rax = write(f->R.rdi, f->R.rsi, f->R.rdx);
		break;
	case SYS_EXIT:
		int status = f->R.rdi;
		exit(status);
		break;
	case SYS_HALT:
		halt();
		break;
	case SYS_FORK:
		break;
	case SYS_CREATE:
		break;
	// case SYS_EXEC:
	// const char *cmd_line = (const char *)f->R.rdi;
	// 	f->R.rax = exec(cmd_line);
	// 	break;
	default:
	 	printf("Unknown syscall: %d\n", (int)f->R.rax);
		break;
	}
	//printf ("system call!\n");
	//thread_exit ();
}


int write (int fd, const void *buffer, unsigned size){
	if(fd == 1){ // STDOUT
		putbuf(buffer,size);
		return size;
	}

	return -1;
}


void exit (int status)
{	
	struct thread *cur = thread_current();
	printf("%s: exit(%d)\n", cur->name, status);
	thread_exit();
}

void halt(){
	power_off();
}

bool create (const char *file, unsigned initial_size){

}

// int exec (const char *cmd_line){
// 	char *fn_copy;
// 	tid_t tid;

// 	char command_copy[128];
// 	char *program_command;
// 	char *str_point;
	
// 	strlcpy(command_copy, cmd_line, sizeof(command_copy));
// 	program_command = strtok_r(command_copy, " ", &str_point);

// 	/* Make a copy of FILE_NAME.
// 	 * Otherwise there's a race between the caller and load(). */
// 	fn_copy = palloc_get_page (0);
// 	if (fn_copy == NULL)
// 		return TID_ERROR;
// 	strlcpy (fn_copy, cmd_line, PGSIZE);

// 	/* Create a new thread to execute FILE_NAME. */
// 	if (tid == TID_ERROR)
// 		palloc_free_page (fn_copy);


// 	return tid;
// }