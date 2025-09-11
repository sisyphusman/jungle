# [WEEK10~11] Pintos User Programs

#### 커밋 컨벤션
<img width="400" height="1026" alt="image" src="https://github.com/user-attachments/assets/1a1cb7c8-41c2-4fff-ad00-9f5bdafbdb66" />   

[커밋 컨벤션 참고 자료](https://www.conventionalcommits.org/ko/v1.0.0/)

&nbsp;

#### Guide

* KAIST Guide : https://casys-kaist.github.io/pintos-kaist/
* PKU Guide : https://pkuflyingpig.gitbook.io/pintos

&nbsp;

#### 작업환경 및 설정

전체 테스트

```
    cd pintos
    source ./activate
    cd threads
    make check
    ...
    20 of 27 tests failed.
```

&nbsp;

부분 테스트

```
/threads/build/ pintos -- -q run alarm-multiple

/threads/build/ make tests/threads/priority-sema.result

```

&nbsp;

***
1. PROJECT 1 - THREADS

   ✅ Alarm Clock  
   ✅ Priority Scheduling  
   ✅ Priority Scheduling and Synchronization     
   ✅ Priority Donation   
   ❓ Multi-Level Feedback Queue Scheduler  

&nbsp;

2. PROJECT 2 - USER PROGRAMS  

   ❓ Project 2 : Argument Passing  
   ❓ Project 2 : System Call  
   ❓ Project 2 : File Descriptor   
   ❓ Project 2 : Hierarchical Process Structure   
