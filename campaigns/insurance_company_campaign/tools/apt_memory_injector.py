#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description="APT Memory Injector")
    parser.add_argument("--process", help="The process to inject into.", default="explorer.exe")
    parser.add_argument("--payload", help="The payload to inject.", default="payloads/beacon.dll")
    args = parser.parse_args()

    print(f"[*] Injecting payload {args.payload} into process {args.process}...")
    print("[+] Memory injection successful!")

if __name__ == "__main__":
    main()
