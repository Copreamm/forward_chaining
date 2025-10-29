import json

# Mengambil semua rules yang ada
with open("rules.json", "r") as file:
    RULES = json.load(file)

#Mengumpulkan daftar gejala
semua_gejala = []

for rule in RULES:
    for gejala in rule["if_all"]:
        semua_gejala.append(gejala)

semua_gejala_unik = set(semua_gejala)

ALL_GEJALA = sorted(semua_gejala_unik)

# Fungsi menampilkan daftar gejala
def tampil_gejala(daftar):
    print("\nDaftar Gejala:")
    for nomor, gejala in enumerate(daftar, start=1):
        nama_gejala = gejala.replace("_", " ")
        print(f"{nomor}. {nama_gejala}")

# Fungsi untuk input gejala
def input_gejala(daftar):
    tampil_gejala(daftar)
    pilih = input("\nMasukkan nomor gejala yang terlihat (pisahkan dengan koma): ")
    try:
        data_mentah = pilih.split(",")
        
        indeks = []
        gejala_terpilih = []
        
        for x in data_mentah:
            teks_bersih = x.strip()
            angka = int(teks_bersih)
            angka_asli = angka - 1
            indeks.append(angka_asli)

        for i in indeks:
            if 0 <= i < len(daftar):
                gejala = daftar[i]
                gejala_terpilih.append(gejala)
        
        return gejala_terpilih
    
    except:
        print("Input tidak valid!")
        return []

# Fungsi menjalankan metode forward chaining
def forward_chaining(observed, mode="full"):
    hasil = []

    for rule in RULES:
        kondisi = set(rule["if_all"])

        if mode == "full":
            if kondisi.issubset(observed):
                hasil.append(rule)

        elif mode == "filter":
            if observed.issubset(kondisi):
                hasil.append(rule)
    
    return hasil

# Prompt interaktif user
def main():
    print("\nSISTEM PAKAR INTERAKTIF DIAGNOSA PENYAKIT TANAMAN PADI ")
    print("Pilih mode:")
    print("1. Mode Cepat (Pilih semua gejala yang dilampirkan dan input dengan koma)")
    print("2. Pilih gejala satu per satu")
    mode = input("Masukkan pilihan (1/2): ").strip()

    observed = set()

    if mode == "1":
        dipilih = input_gejala(ALL_GEJALA)
        observed = set(dipilih)

    else:
        kandidat = RULES[:]
        sisa_gejala = set(ALL_GEJALA)

        while True:
            print("\nKemungkinan penyakit saat ini:")
            
            kemungkinan = []
            for rule in kandidat:
                penyakit = rule["then"]["penyakit"]
                kemungkinan.append(penyakit)
            kemungkinan = set(kemungkinan)

            if kemungkinan:
                hasil = ", ".join(kemungkinan)
            else:
                hasil = "(Belum ada data)"
            print(hasil)

            if not sisa_gejala:
                print("\nTidak ada gejala tersisa untuk ditanyakan.")
                break

            tampil_gejala(sorted(list(sisa_gejala)))
            pilih = input("\nMasukkan satu nomor gejala yang kamu lihat: ").strip()
            if not pilih:
                break

            try:
                idx = int(pilih) - 1
                gejala_terpilih = sorted(list(sisa_gejala))[idx]
                observed.add(gejala_terpilih)
                print(f"Ditambahkan gejala: {gejala_terpilih.replace('_',' ')}")
            except:
                print("Input tidak valid!")
                continue

            kandidat = forward_chaining(observed, mode="filter")

            sisa_gejala.discard(gejala_terpilih)
            relevan = {g for r in kandidat for g in r["if_all"]}
            sisa_gejala = sisa_gejala.intersection(relevan)

            if len(kandidat) == 1 and observed.issuperset(set(kandidat[0]["if_all"])):
                break

    # Hasil diagnosis
    hasil = forward_chaining(observed, mode="full")

    print("\n=== HASIL DIAGNOSA ===")
    if hasil:
        for h in hasil:
            print(f"Penyakit: {h['then']['penyakit']}")
            print("Saran Penanganan:")
            for s in h["then"]["saran"]:
                print(f"  - {s}")
            print("-"*40)
    else:
        kandidat = forward_chaining(observed, mode="filter")
        if kandidat:
            print("Belum cukup gejala untuk diagnosis pasti.")
            print("Kemungkinan penyakit:")
            for k in kandidat:
                print(f" - {k['then']['penyakit']}")
        else:
            print("Tidak ditemukan penyakit yang cocok.")

    print("\nTerima kasih telah menggunakan sistem pakar ini!")

if __name__ == "__main__":
    main()
