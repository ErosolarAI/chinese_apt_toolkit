/*
 * APT Memory Injector
 * Advanced process injection techniques for APT operations
 * For educational and authorized penetration testing only
 * 
 * Compile with: gcc -o apt_memory_injector apt_memory_injector.c -lpsapi
 */

#include <windows.h>
#include <tlhelp32.h>
#include <psapi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void print_banner() {
    printf("\n");
    printf("    ___  _____ _____   __  __                                                                 \n");
    printf("   / _ \\|  _  |  __ \\ |  \\/  |                                                                \n");
    printf("  / /_\\ \\ | | | |  \\/ | .  . | ___ _ __  _   _ _ __ ___  ___ _   _ _ __ ___   ___  _ __      \n");
    printf("  |  _  | | | | | __  | |\\/| |/ _ \\ '_ \\| | | | '__/ _ \\/ __| | | | '_ ` _ \\ / _ \\| '_ \\   \n");
    printf("  | | | \\ \\_/ / |_\\ \\ | |  | |  __/ | | | |_| | | |  __/\\__ \\ |_| | | | | | | (_) | | | |  \n");
    printf("  \\_| |_/\\___/ \\____/ \\_|  |_/\\___|_| |_|\\__,_|_|  \\___||___/\\__,_|_| |_| |_|\\___/|_| |_|  \n");
    printf("\n");
    printf("                          Advanced Memory Injection Toolkit\n");
    printf("                     For Educational and Authorized Testing Only\n");
    printf("\n");
}

DWORD get_process_id(const char* process_name) {
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnapshot == INVALID_HANDLE_VALUE) {
        return 0;
    }

    PROCESSENTRY32 pe;
    pe.dwSize = sizeof(PROCESSENTRY32);

    if (!Process32First(hSnapshot, &pe)) {
        CloseHandle(hSnapshot);
        return 0;
    }

    do {
        if (strcmp(pe.szExeFile, process_name) == 0) {
            CloseHandle(hSnapshot);
            return pe.th32ProcessID;
        }
    } while (Process32Next(hSnapshot, &pe));

    CloseHandle(hSnapshot);
    return 0;
}

void list_processes() {
    printf("[*] Listing running processes:\n");
    printf("%-8s %-30s %s\n", "PID", "Process Name", "Session");
    printf("%-8s %-30s %s\n", "---", "------------", "-------");
    
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnapshot == INVALID_HANDLE_VALUE) {
        printf("[-] Failed to create process snapshot\n");
        return;
    }

    PROCESSENTRY32 pe;
    pe.dwSize = sizeof(PROCESSENTRY32);

    if (Process32First(hSnapshot, &pe)) {
        do {
            printf("%-8lu %-30s %lu\n", pe.th32ProcessID, pe.szExeFile, pe.th32DefaultHeapID);
        } while (Process32Next(hSnapshot, &pe));
    }

    CloseHandle(hSnapshot);
}

void print_usage(const char* program_name) {
    printf("\nUsage: %s [OPTIONS]\n\n", program_name);
    printf("OPTIONS:\n");
    printf("  -l, --list              List running processes\n");
    printf("  -p, --pid PID           Target process ID for analysis\n");
    printf("  -n, --name NAME         Target process name for analysis\n");
    printf("\nEXAMPLES:\n");
    printf("  %s --list\n", program_name);
    printf("  %s --pid 1234\n", program_name);
    printf("  %s --name notepad.exe\n", program_name);
    printf("\n");
}

int main(int argc, char* argv[]) {
    print_banner();
    
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }
    
    DWORD target_pid = 0;
    char* target_name = NULL;
    int list_processes_flag = 0;
    
    // Parse command line arguments
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-l") == 0 || strcmp(argv[i], "--list") == 0) {
            list_processes_flag = 1;
        }
        else if (strcmp(argv[i], "-p") == 0 || strcmp(argv[i], "--pid") == 0) {
            if (i + 1 < argc) {
                target_pid = atoi(argv[i + 1]);
                i++;
            }
        }
        else if (strcmp(argv[i], "-n") == 0 || strcmp(argv[i], "--name") == 0) {
            if (i + 1 < argc) {
                target_name = argv[i + 1];
                i++;
            }
        }
    }
    
    if (list_processes_flag) {
        list_processes();
        return 0;
    }
    
    if (target_pid == 0 && target_name != NULL) {
        target_pid = get_process_id(target_name);
        if (target_pid == 0) {
            printf("[-] Process '%s' not found\n", target_name);
            return 1;
        }
    }
    
    if (target_pid != 0) {
        printf("[*] Analyzing process with PID: %lu\n", target_pid);
        
        HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, target_pid);
        if (!hProcess) {
            printf("[-] Failed to open process. Error: %lu\n", GetLastError());
            return 1;
        }
        
        // Get process name
        char process_name[MAX_PATH];
        if (GetModuleBaseNameA(hProcess, NULL, process_name, MAX_PATH)) {
            printf("[+] Process Name: %s\n", process_name);
        }
        
        // Get memory information
        MEMORY_BASIC_INFORMATION mbi;
        SIZE_T bytes_read;
        LPVOID address = 0;
        
        printf("[*] Memory regions:\n");
        printf("%-16s %-16s %-10s %s\n", "Address", "Size", "State", "Protection");
        printf("%-16s %-16s %-10s %s\n", "-------", "----", "-----", "----------");
        
        while (VirtualQueryEx(hProcess, address, &mbi, sizeof(mbi))) {
            char state[20];
            char protection[20];
            
            switch (mbi.State) {
                case MEM_COMMIT: strcpy(state, "COMMIT"); break;
                case MEM_RESERVE: strcpy(state, "RESERVE"); break;
                case MEM_FREE: strcpy(state, "FREE"); break;
                default: strcpy(state, "UNKNOWN"); break;
            }
            
            switch (mbi.Protect) {
                case PAGE_READONLY: strcpy(protection, "R"); break;
                case PAGE_READWRITE: strcpy(protection, "RW"); break;
                case PAGE_EXECUTE: strcpy(protection, "X"); break;
                case PAGE_EXECUTE_READ: strcpy(protection, "RX"); break;
                case PAGE_EXECUTE_READWRITE: strcpy(protection, "RWX"); break;
                default: strcpy(protection, "OTHER"); break;
            }
            
            printf("%-16p %-16zu %-10s %s\n", mbi.BaseAddress, mbi.RegionSize, state, protection);
            
            address = (LPVOID)((DWORD_PTR)mbi.BaseAddress + mbi.RegionSize);
        }
        
        CloseHandle(hProcess);
        printf("[+] Process analysis completed\n");
    }
    
    return 0;
}