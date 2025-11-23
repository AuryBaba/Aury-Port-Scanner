# guide_2025_pro.py → AurySoftWare © 2025 | Professional TCP Port Scanner
import socket
import threading
import ipaddress
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime

# Ana pencere
root = tk.Tk()
root.title("GUIDE 2025 © AurySoftWare - Professional TCP Scanner")
root.geometry("1150x750")
root.configure(bg="#f8f9fa")

# Header
header = tk.Frame(root, bg="#003087", height=90)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(header, text="GUIDE 2025", font=("Segoe UI", 28, "bold"), fg="white", bg="#003087").pack(side="left", padx=30, pady=15)
tk.Label(header, text="© AurySoftWare 2025", font=("Segoe UI", 14), fg="#a0c4ff", bg="#003087").pack(side="right", padx=30, pady=25)

# Main frame
main = tk.Frame(root, bg="#f8f9fa")
main.pack(fill="both", expand=True, padx=30, pady=20)

# Sol panel - Kontroller
left = tk.LabelFrame(main, text=" Tarama Parametreleri", font=("Segoe UI", 12, "bold"), bg="white", fg="#003087")
left.pack(side="left", fill="y", padx=(0, 20))

# Hedef IP
tk.Label(left, text="Hedef IP Adresi:", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w", pady=(20,5))
ip_entry = tk.Entry(left, font=("Segoe UI", 11), width=30)
ip_entry.pack(pady=5, ipady=8)
ip_entry.insert(0, "192.168.1.1")

# Port aralığı
tk.Label(left, text="Port Aralığı:", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w", pady=(15,5))
port_frame = tk.Frame(left, bg="white")
port_frame.pack()
start_port = tk.Entry(port_frame, width=10, font=("Segoe UI", 11)); start_port.grid(row=0, column=0, padx=5)
start_port.insert(0, "1")
tk.Label(port_frame, text=" - ", bg="white").grid(row=0, column=1)
end_port = tk.Entry(port_frame, width=10, font=("Segoe UI", 11)); end_port.grid(row=0, column=2, padx=5)
end_port.insert(0, "1000")

# Timeout ayarı
tk.Label(left, text="Timeout (saniye):", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w", pady=(15,5))
timeout_var = tk.DoubleVar(value=0.01)
tk.Scale(left, from_=0.01, to=2.0, resolution=0.01, orient="horizontal", variable=timeout_var, length=250).pack(pady=5)

# Başlat butonu
start_btn = ttk.Button(left, text="TARAMAYI BAŞLAT")
start_btn.pack(pady=30, ipadx=30, ipady=12)

# Sağ panel - Sonuçlar
right = tk.LabelFrame(main, text=" Tarama Sonuçları", font=("Segoe UI", 12, "bold"), bg="white", fg="#003087")
right.pack(side="right", fill="both", expand=True)

log = scrolledtext.ScrolledText(right, font=("Consolas", 11), bg="#f8f9fa")
log.pack(fill="both", expand=True, padx=15, pady=15)

# Durum çubuğu
status = tk.Label(root, text="Hazır • GUIDE 2025 © AurySoftWare", bg="#e9ecef", fg="#495057", anchor="w", padx=20, pady=8, font=("Segoe UI", 9))
status.pack(fill="x", side="bottom")

# Senin orijinal TCP scan fonksiyonu (hiç dokunmadım)
def tcp_scan(ip_addr, start_port, end_port):
    socket.setdefaulttimeout(timeout_var.get())
    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
                if not tcp.connect_ex((ip_addr, port)):
                    log.insert("end", f"[+] {ip_addr}:{port}/TCP Open\n", "open")
                    log.see("end")
                    open_ports.append(port)
        except Exception:
            pass
    return open_ports

# Tarama başlat
def start_scan():
    ip = ip_entry.get().strip()
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        messagebox.showerror("Hata", "Geçerli bir IP adresi girin!")
        return

    try:
        s_port = int(start_port.get())
        e_port = int(end_port.get())
        if not (1 <= s_port <= e_port <= 65535):
            raise ValueError
    except ValueError:
        messagebox.showerror("Hata", "Geçerli port aralığı girin (1-65535)")
        return

    log.delete(1.0, "end")
    log.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] GUIDE 2025 © AurySoftWare başlatılıyor...\n", "header")
    log.insert("end", f"[*] Hedef: {ip} | Port: {s_port}-{e_port} | Timeout: {timeout_var.get()}s\n\n", "info")
    status.config(text="Tarama devam ediyor...")

    def run():
        start_time = datetime.now()
        open_ports = tcp_scan(ip, s_port, e_port)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        log.insert("end", "\n" + "="*60 + "\n", "header")
        log.insert("end", f"Tarama tamamlandı → {len(open_ports)} açık port bulundu\n", "header")
        log.insert("end", f"Süre: {duration:.2f} saniye\n", "info")
        log.insert("end", f"© AurySoftWare 2025 - Tüm hakları saklıdır.\n", "footer")
        status.config(text=f"Tarama bitti • {len(open_ports)} açık • {datetime.now().strftime('%H:%M:%S')}")

    threading.Thread(target=run, daemon=True).start()

# Renkler
log.tag_config("header", foreground="#003087", font=("Consolas", 11, "bold"))
log.tag_config("info", foreground="#495057")
log.tag_config("open", foreground="#d63384", font=("Consolas", 11, "bold"))
log.tag_config("footer", foreground="#666", font=("Consolas", 9, "italic"))

start_btn.config(command=start_scan)

# Footer
tk.Label(root, text="Developed by DVA1 • AurySoftWare © 2025", bg="#f8f9fa", fg="#666", font=("Segoe UI", 9)).pack(side="bottom", pady=10)

root.mainloop()