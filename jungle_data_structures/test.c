#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 10000000

int main() {
    int *data = malloc(sizeof(int) * N);
    int *indices = malloc(sizeof(int) * N);
    long long sum = 0;

    // 데이터 채우기
    for (int i = 0; i < N; i++) {
        data[i] = i;
        indices[i] = i;
    }

    // 인덱스 셔플 (랜덤 접근용)
    for (int i = N - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        int tmp = indices[i];
        indices[i] = indices[j];
        indices[j] = tmp;
    }

    clock_t start, end;

    // (1) 정렬된 순서로 접근
    start = clock();
    for (int i = 0; i < N; i++) {
        sum += data[i]; // 연속된 메모리 접근
    }
    end = clock();
    printf("Sorted access time: %.3f sec\n", (double)(end - start) / CLOCKS_PER_SEC);

    // (2) 랜덤 순서로 접근
    start = clock();
    for (int i = 0; i < N; i++) {
        sum += data[indices[i]]; // 랜덤 메모리 접근
    }
    end = clock();
    printf("Random access time: %.3f sec\n", (double)(end - start) / CLOCKS_PER_SEC);

    printf("Sum: %lld\n", sum); // 최적화 방지용
    free(data);
    free(indices);

    return 0;
}