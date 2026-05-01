#include <cstdio> // 使用C标准库的头文件

#include <unistd.h> // 使用fork()和sleep()函数的头文件
#include <sys/types.h> // 使用pid_t的头文件
#include <sys/wait.h> // 使用waitpid()函数的头文件
#include <cstdlib> // 使用exit()函数的头文件
#include <cstring> // 使用memset()函数的头文件

// 文件操作函数
void fileOps() {
    // 定义文件名
    const char* filename = "test.txt";

    // 写入文件
    FILE* outfile;
    if ((outfile = fopen(filename, "a")) != NULL) { // 打开文件，以追加方式写入
        fprintf(outfile, "Hello, world!\n"); // 写入文本
        fclose(outfile); // 关闭文件
    } else {
        printf("Unable to open file for writing.\n"); // 打开文件失败
    }

    // 读取文件
    FILE* infile;
    if ((infile = fopen(filename, "r")) != NULL) { // 打开文件，以只读方式读取
        char line[256];
        while (fgets(line, sizeof(line), infile) != NULL) { // 逐行读取文本
            printf("%s", line); // 输出读取到的行
        }
        fclose(infile); // 关闭文件
    } else {
        printf("Unable to open file for reading.\n"); // 打开文件失败
    }
}

// 进程操作函数
void processOps() {
    pid_t pid = fork(); // 创建子进程
    if (pid == 0) {
        // 子进程
        printf("Child process start.\n");
        sleep(5); // 子进程睡眠5秒
        printf("Child process end.\n");
        exit(0); // 子进程结束
    } else if (pid < 0) {
        // 创建子进程失败
        printf("Unable to create child process.\n");
    } else {
        // 父进程
        printf("Parent process start.\n");
        int status;
        waitpid(pid, &status, 0); // 等待子进程结束
        printf("Child process %d end.\n", pid);
    }
}

int main() {
    for (;;) {
        fileOps(); // 文件操作
        processOps(); // 进程操作
        sleep(1); // 主进程睡眠1秒
        // 清空输出缓冲区
        fflush(stdout);
        memset(NULL, 0, sizeof(NULL));
    }
    return 0;
}

