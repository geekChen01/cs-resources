#include <iostream>
#include <fstream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
using namespace std;
void file_operations() {
    string filename = "test.txt";
    ofstream outfile(filename, ios::app);
    if (outfile.is_open()) 
    {
        outfile << "Hello, world!" << endl;
        outfile.close();
    } 
    else 
    {
        cout << "Unable to open file for writing." << endl;
    }
    
    ifstream infile(filename);
    if (infile.is_open()) 
    {
        string line;
        while (getline(infile, line)) 
        {
            cout << line << endl;
        }
        infile.close();
    } 
    else 
    {
        cout << "Unable to open file for reading." << endl;
    }
}

void process_operations() {
    pid_t pid = fork();
    if (pid == 0) //fork() 返回值为 0，则表示当前处于子进程中
    {
        cout << "子进程运转" << endl;
        sleep(5);
        cout << "子进程结束" << endl;
        exit(0);
    } 
    else if (pid < 0) 
    {
        cout << "Unable to create child process." << endl;
    } 
    else 
    {
        cout << "父进程运转" << endl;
        int status;
    //    waitpid(pid, &status, 0);
        cout << "子进程" << pid << " 结束" << endl;
    }
}

int main() {
    while (true) 
    {
        file_operations();
        process_operations();
        sleep(1);
    }
  
    return 0;
}
