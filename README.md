# Forward Chaining Method

Forward Chaining adalah salah satu metode dalam sistem pakar yang digunakan untuk mengambil keputusan berdasarkan data atau fakta yang tersedia. Pada metode ini, sistem mulai dengan mengidentifikasi gejala (facts) yang telah diketahui dan menggunakan aturan yang ada untuk menyimpulkan penyakit yang mungkin terjadi.

Pada program ini, Forward Chaining diterapkan untuk mendiagnosa penyakit tanaman padi berdasarkan gejala yang dipilih oleh pengguna. Proses dimulai dengan pengguna memilih gejala yang terlihat pada tanaman padi. Sistem kemudian mencocokkan gejala yang dipilih dengan aturan produksi (production rules) yang ada di dalam basis pengetahuan. Setiap aturan memiliki kondisi yang harus dipenuhi untuk menghasilkan diagnosis.

Cara Kerja:

1. Pengguna memilih gejala yang terlihat pada tanaman padi.
2. Sistem mencocokkan gejala tersebut dengan aturan yang ada dalam basis pengetahuan.
3. Jika gejala yang dipilih cocok dengan premis (kondisi) dari aturan, sistem kemudian mengambil kesimpulan tentang penyakit yang kemungkinan terjadi.
4. Sistem menghitung confidence atau tingkat kepercayaan untuk setiap penyakit yang didiagnosa berdasarkan jumlah gejala yang cocok.

Program ini menggunakan data gejala, penyakit, dan aturan yang telah ditentukan sebelumnya untuk melakukan proses inferensi dan memberikan rekomendasi penanganan kepada petani.

Output:

1. Diagnosis penyakit berdasarkan gejala yang dipilih.
2. Rekomendasi penanganan yang sesuai dengan penyakit yang terdeteksi.

Metode ini memberikan cara cepat dan efisien bagi petani untuk mendapatkan diagnosa penyakit pada tanaman padi mereka.
