import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv, os

# === DATA DASAR ===
symptoms = [
    ("G1", "Bercak coklat"), ("G2", "Bercak Putih"), ("G3", "Bercak Kemerahan"), ("G4", "Bercak belah ketupat"),
    ("G5", "Daun mengering"), ("G6", "Bercak Keabuan"), ("G7", "Malai Lemah"), ("G8", "Bulir hampa"),
    ("G9", "Kerdil"), ("G10", "Daun menguning"), ("G11", "Daun lembek"), ("G12", "Anakan Sedikit"),
    ("G13", "Pelepah pendek"), ("G14", "Daun terhimpit"), ("G15", "Malai pendek"), ("G16", "Bulir tidak berisi"),
    ("G17", "Tepi daun bergerigi"), ("G18", "Daun menjadi hijau tua"), ("G19", "Malai tidak muncul"),
    ("G20", "Anakan bercabang"), ("G21", "Bercak abu-abu"), ("G22", "Bercak jamur coklat"),
    ("G23", "Bercak oval"), ("G24", "Anakan berlebihan"), ("G25", "Caun pendek & sempit"),
    ("G26", "Gabah hampa"), ("G27", "Bercak kecil jingga"), ("G28", "Bercak panjang"), 
    ("G29", "Daun menggulung"), ("G30", "Buku-buku membusuk"), ("G31", "Tunas mati"),
    ("G32", "Bercak berjamur"), ("G33", "Padi mudah rebah"), ("G34", "Daun menguning"),
    ("G35", "Daun hijau kelabu"), ("G36", "Elips berwarna coklat"), ("G37", "Bercak hitam"),
    ("G38", "Bercak sempit coklat"), ("G39", "Garis coklat"), ("G40", "Bercak panjang & lebar"),
    ("G41", "Bercak seperti noda"), ("G42", "Daun merah lalu mati"), ("G43", "Daun perunggu"),
    ("G44", "Batang atas busuk"), ("G45", "Ruas berwarna coklat"),
]

diseases = {
    "P001": "Blast", "P002": "Hawar daun", "P003": "Hawar bakteri", "P004": "Keracunan besi",
    "P005": "Daun coklat", "P006": "Kerdil hampa", "P007": "Kerdil rumput", "P008": "Busuk batang",
    "P009": "Coklat bergaris", "P010": "Bercak bergaris", "P011": "Tungro", "P012": "Busuk malai"
}

rules = [
    {"id":"R1", "if":["G1","G4","G3","G2","G5","G7","G6","G9","G8"], "then":"P001"},
    {"id":"R2", "if":["G11","G10","G12"], "then":"P002"},
    {"id":"R3", "if":["G13","G14"], "then":"P003"},
    {"id":"R4", "if":["G15","G13","G18"], "then":"P004"},
    {"id":"R5", "if":["G17","G18","G20"], "then":"P005"},
    {"id":"R6", "if":["G23","G21","G25","G26"], "then":"P006"},
    {"id":"R7", "if":["G28","G29","G26"], "then":"P007"},
    {"id":"R8", "if":["G31","G30","G32"], "then":"P008"},
    {"id":"R9", "if":["G34","G35","G33"], "then":"P009"},
    {"id":"R10","if":["G36","G37","G38"], "then":"P010"},
    {"id":"R11","if":["G39","G41","G42","G40","G43","G45"], "then":"P011"},
    {"id":"R12","if":["G19"], "then":"P012"},
]

recommendations = {
    "P001": "Blast: Gunakan varietas tahan, aplikasikan fungisida sesuai anjuran, perbaiki drainase.",
    "P002": "Hawar daun: Buang daun terinfeksi, perbaiki drainase, gunakan fungisida jika perlu.",
    "P003": "Hawar bakteri: Sanitasi, gunakan benih sehat, perbaiki irigasi.",
    "P004": "Keracunan besi: Uji tanah, perbaiki pH dan nutrisi sesuai hasil uji.",
    "P005": "Daun coklat: Evaluasi pemupukan dan manajemen air.",
    "P006": "Kerdil hampa: Periksa nutrisi dan benih; gunakan benih unggul.",
    "P007": "Kerdil rumput: Kontrol gulma, perbaiki manajemen tanah.",
    "P008": "Busuk batang: Sanitasi lahan, kurangi kelembaban, gunakan fungisida jika perlu.",
    "P009": "Coklat bergaris: Cek nutrisi dan kemungkinan jamur/virus.",
    "P010": "Bercak bergaris: Rotasi tanaman, identifikasi agen penyakit.",
    "P011": "Tungro: Kontrol vektor serangga, gunakan benih tahan.",
    "P012": "Busuk malai: Hindari kelembaban saat malai, sanitasi, aplikasikan fungisida bila perlu."
}

def forward_chain(selected_codes):
    results = []
    for r in rules:
        rule_syms = list(dict.fromkeys(r["if"]))
        matched = [s for s in rule_syms if s in selected_codes]
        if not matched:
            continue
        conf = len(matched)/len(rule_syms)*100
        results.append({
            "rule_id": r["id"],
            "disease_code": r["then"],
            "disease_name": diseases.get(r["then"], r["then"]),
            "matched": matched,
            "rule_sym_count": len(rule_syms),
            "matched_count": len(matched),
            "confidence": round(conf,2),
            "recommendation": recommendations.get(r["then"], "")
        })
    results.sort(key=lambda x: (x["confidence"], x["matched_count"]), reverse=True)
    return results

# === GUI ===
class ExpertGUI:
    def __init__(self, root):
        self.root = root
        root.title("Diagnosa Penyakit Pada Tanaman Padi")
        root.geometry("1100x650")

        # Header
        header = tk.Frame(root, bg="#222", height=36)
        header.pack(fill=tk.X)
        tk.Label(header, text="Diagnosa Penyakit Pada Tanaman Padi", bg="#222", fg="white",
                 font=("Helvetica",12,"bold")).pack(pady=5)

        # Main layout
        main = tk.Frame(root)
        main.pack(fill=tk.BOTH, expand=True)

        # Left: Pilih Gejala
        left = tk.Frame(main, bd=1, relief="solid")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(left, text="Pilih Gejala", font=("Arial",11,"bold")).pack(anchor="w", padx=8, pady=6)
        canvas = tk.Canvas(left)
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8,0), pady=4)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y, padx=(0,8), pady=4)
        self.var_map = {}
        for code, txt in symptoms:
            v = tk.BooleanVar()
            ttk.Checkbutton(scroll_frame, text=f"{code} - {txt}", variable=v).pack(anchor="w", padx=4)
            self.var_map[code] = v

        # Right: tombol (sejajar) + hasil
        right = tk.Frame(main, bd=1, relief="solid")
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Top strip with two buttons side by side
        top_strip = tk.Frame(right, height=60)
        top_strip.pack(fill=tk.X, pady=(5,2))
        btn_diag = ttk.Button(top_strip, text="Mulai Diagnosis", command=self.on_diagnose)
        btn_diag.pack(side=tk.LEFT, padx=(30,10), pady=10)
        btn_save = ttk.Button(top_strip, text="Simpan Hasil (CSV)", command=self.save_csv)
        btn_save.pack(side=tk.LEFT, pady=10)

        # Separator line
        tk.Frame(right, height=2, bg="#222").pack(fill=tk.X)

        # Output
        tk.Label(right, text="Hasil Diagnosis", font=("Arial",11,"bold")).pack(anchor="w", padx=8, pady=4)
        self.result_text = tk.Text(right, wrap="word", state="normal")
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))
        self.last_results = None

    def on_diagnose(self):
        sel = [c for c, v in self.var_map.items() if v.get()]
        self.result_text.delete("1.0", tk.END)
        if not sel:
            self.result_text.insert(tk.END, "Tidak ada gejala dipilih.\n")
            self.last_results = None
            return
        self.result_text.insert(tk.END, f"Gejala terpilih ({len(sel)}): {', '.join(sel)}\n\n")
        results = forward_chain(sel)
        if not results:
            self.result_text.insert(tk.END, "Tidak ada aturan yang cocok.\n")
            self.last_results = None
            return
        top = results[0]
        self.result_text.insert(tk.END, "=== Diagnosis Teratas ===\n")
        self.result_text.insert(tk.END, f"{top['disease_name']} ({top['disease_code']})\n")
        self.result_text.insert(tk.END, f"Confidence: {top['confidence']}%\n")
        self.result_text.insert(tk.END, f"Rekomendasi: {top['recommendation']}\n\n")

        self.result_text.insert(tk.END, "=== Semua Aturan yang Cocok ===\n")
        for r in results:
            self.result_text.insert(tk.END, f"{r['rule_id']}: {r['disease_name']} | matched {r['matched_count']}/{r['rule_sym_count']} ({r['confidence']}%)\n")
            self.result_text.insert(tk.END, f"   Matched: {', '.join(r['matched'])}\n")
            self.result_text.insert(tk.END, f"   Rekomendasi: {r['recommendation']}\n\n")
        self.last_results = results

    def save_csv(self):
        if not self.last_results:
            messagebox.showinfo("Info", "Belum ada hasil untuk disimpan.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not path:
            return
        try:
            with open(path, "w", newline='', encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["rule_id","disease_code","disease_name","matched_symptoms","rule_sym_count","matched_count","confidence","recommendation"])
                for r in self.last_results:
                    w.writerow([r['rule_id'], r['disease_code'], r['disease_name'], ";".join(r['matched']), r['rule_sym_count'], r['matched_count'], r['confidence'], r['recommendation']])
            messagebox.showinfo("Sukses", f"Hasil tersimpan: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan CSV: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpertGUI(root)
    root.mainloop()
