import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os
import urllib.request

class ZipBruteforceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("L4F - ZIP Bruteforce Tool")
        self.root.geometry("600x570")
        self.root.configure(bg="black")  # Lebih hitam pekat

        # === Set icon dari URL ===
        try:
            ico_url = "https://raw.githubusercontent.com/HanTr15/L4F-/refs/heads/main/favicon.ico"
            ico_file = "temp_icon.ico"
            urllib.request.urlretrieve(ico_url, ico_file)
            self.root.iconbitmap(ico_file)
        except Exception as e:
            print("Gagal load icon:", e)

        self.zip_path = tk.StringVar()
        self.wordlist_path = tk.StringVar()

        # === Load Logo dari URL ===
        logo_url = "https://raw.githubusercontent.com/HanTr15/L4F-/main/%7B3A43E050-36E8-4D78-81DA-A71E9740723F%7D.gif"
        logo_file = "temp_logo.gif"
        try:
            urllib.request.urlretrieve(logo_url, logo_file)
            self.logo_img = tk.PhotoImage(file=logo_file)
            tk.Label(root, image=self.logo_img, bg="black").pack(pady=10)
        except:
            tk.Label(root, text="[Logo]", fg="red", bg="black").pack(pady=10)

        # === Frame untuk File Input ===
        file_frame = tk.Frame(root, bg="black", highlightbackground="white", highlightthickness=1)
        file_frame.pack(pady=10, padx=10, fill="x")

        self.add_file_input(file_frame, "File ZIP:", self.zip_path)
        self.add_file_input(file_frame, "Wordlist:", self.wordlist_path)

        # === Tombol Mulai ===
        self.start_button = tk.Button(root, text="🚀 Mulai Bruteforce", command=self.start_bruteforce, bg="red", fg="white", font=("Segoe UI", 12, "bold"))
        self.start_button.pack(pady=15)

        # === Footer Dipindah ke Atas Log ===
        self.footer_label = tk.Label(root, text="Created by Hamdan Trisnawan", bg="black", fg="gray", font=("Segoe UI", 9, "italic"))
        self.footer_label.pack(pady=(0, 5))

        # === Output Log ===
        tk.Label(root, text="Log Output:", bg="black", fg="red", font=("Segoe UI", 10, "bold")).pack()
        self.output = tk.Text(root, height=12, bg="black", fg="white", insertbackground="white")
        self.output.pack(padx=10, pady=5, fill="both", expand=True)

    def add_file_input(self, parent, label, variable):
        frame = tk.Frame(parent, bg="black")
        frame.pack(pady=10, padx=10, fill="x")

        tk.Label(frame, text=f" • {label}", fg="white", bg="black", font=("Segoe UI", 10, "bold")).pack(anchor="w")

        entry = tk.Entry(frame, textvariable=variable, width=50, bg="#1a1a1a", fg="white", insertbackground="white")
        entry.pack(side="left", padx=(10, 5), fill="x", expand=True)

        browse_btn = tk.Button(frame, text="Browse", command=lambda: self.browse_file(variable), bg="red", fg="white")
        browse_btn.pack(side="left", padx=(5, 10))

    def browse_file(self, var):
        file_path = filedialog.askopenfilename()
        if file_path:
            var.set(file_path)

    def start_bruteforce(self):
        self.output.delete(1.0, tk.END)
        self.start_button.config(state="disabled")
        self.root.after(100, self.bruteforce)

    def bruteforce(self):
        zip_path = self.zip_path.get()
        wordlist_path = self.wordlist_path.get()

        if not os.path.isfile(zip_path) or not os.path.isfile(wordlist_path):
            messagebox.showerror("Error", "File ZIP atau Wordlist tidak valid!")
            self.start_button.config(state="normal")
            return

        try:
            with zipfile.ZipFile(zip_path) as zf:
                namelist = zf.namelist()
                if not namelist:
                    self.output.insert(tk.END, "[!] ZIP kosong atau tidak terbaca\n")
                    self.start_button.config(state="normal")
                    return

                with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        password = line.strip()
                        try:
                            # Coba extract 1 file untuk validasi password
                            zf.extract(namelist[0], pwd=password.encode())
                            self.output.insert(tk.END, f"[✓] Password ditemukan: {password}\n")
                            messagebox.showinfo("Berhasil", f"Password ditemukan: {password}")
                            self.start_button.config(state="normal")
                            return
                        except RuntimeError as e:
                            if "Bad password" in str(e):
                                self.output.insert(tk.END, f"[-] Salah: {password}\n")
                            else:
                                self.output.insert(tk.END, f"[!] Error: {e}\n")
                        except Exception as e:
                            self.output.insert(tk.END, f"[!] Gagal dengan: {password} → {e}\n")

        except NotImplementedError:
            self.output.insert(tk.END, "[✖] ZIP menggunakan enkripsi AES yang tidak didukung oleh library zipfile Python.\n")
            self.output.insert(tk.END, "Gunakan enkripsi ZipCrypto saat membuat ZIP agar dapat dibuka.\n")
        except Exception as e:
            self.output.insert(tk.END, f"[!] Gagal membuka ZIP: {e}\n")

        self.output.insert(tk.END, "[x] Password tidak ditemukan.\n")
        self.start_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZipBruteforceApp(root)
    root.mainloop()
