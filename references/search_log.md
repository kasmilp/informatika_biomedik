# Search Log — Literature Review

**Tanggal pencarian:** 5 November 2026  
**Topik:** Interoperability and Standardization in Biomedical Informatics  
**Metode:** structured/exploratory literature search (belum PRISMA penuh)

---

## 1. Database dan sumber

| Sumber | Fungsi |
|---|---|
| Europe PMC (mencakup PubMed/PMC) | Pencarian utama artikel biomedis open-access |
| OpenAlex | Verifikasi metadata, DOI, dan lokasi open-access |
| Crossref | Verifikasi metadata sitasi (penulis, tahun, volume, halaman) |
| Situs penerbit: BMC, JMIR, MDPI, Frontiers, Springer, PLOS, UGM, BIO Web of Conferences | Unduh PDF resmi |

---

## 2. String pencarian yang digunakan

### Tema A — Healthcare interoperability

```
(TITLE_ABS:"health information exchange" AND TITLE_ABS:"interoperability")
  AND OPEN_ACCESS:Y AND PUB_YEAR:[2020 TO 2026]

(TITLE_ABS:"interoperability challenges" AND TITLE_ABS:"healthcare")
  AND OPEN_ACCESS:Y AND PUB_YEAR:[2020 TO 2026]

(TITLE_ABS:"health information systems" AND TITLE_ABS:"integration")
  AND OPEN_ACCESS:Y AND PUB_YEAR:[2020 TO 2026]

(TITLE_ABS:"health information exchange" OR TITLE_ABS:"healthcare interoperability")
  AND OPEN_ACCESS:Y AND PUB_YEAR:[2020 TO 2026]
```

### Tema B — Healthcare standards

```
TITLE_ABS:"HL7 FHIR" AND OPEN_ACCESS:Y AND PUB_YEAR:[2020 TO 2026]

(TITLE_ABS:"FHIR" AND TITLE_ABS:"interoperability")
  AND OPEN_ACCESS:Y AND PUB_YEAR:[2020 TO 2026]

TITLE_ABS:"HL7 CDA" AND OPEN_ACCESS:Y AND PUB_YEAR:[2020 TO 2026]

(TITLE_ABS:"DICOM" AND TITLE_ABS:"interoperability")
  AND OPEN_ACCESS:Y AND PUB_YEAR:[2020 TO 2026]
```

### Tema C — Coding & terminology systems

```
(TITLE_ABS:"SNOMED CT" AND TITLE_ABS:"interoperability")
  AND OPEN_ACCESS:Y AND PUB_YEAR:[2020 TO 2026]

TITLE_ABS:LOINC AND OPEN_ACCESS:Y AND PUB_YEAR:[2020 TO 2026]

(TITLE_ABS:"semantic interoperability" AND TITLE_ABS:"health")
  AND OPEN_ACCESS:Y AND PUB_YEAR:[2020 TO 2026]

TITLE_ABS:ICD AND TITLE_ABS:coding
  AND OPEN_ACCESS:Y AND PUB_YEAR:[2020 TO 2026]
```

### Tema D — Indonesia / SATUSEHAT

```
SATUSEHAT

(TITLE_ABS:"Indonesia" AND (TITLE_ABS:"interoperability" OR TITLE_ABS:"health information exchange"))
  AND OPEN_ACCESS:Y AND PUB_YEAR:[2020 TO 2026]

(TITLE_ABS:"Indonesia" AND (TITLE_ABS:"electronic medical record" OR TITLE_ABS:"electronic health record"))
  AND OPEN_ACCESS:Y AND PUB_YEAR:[2020 TO 2026]

(TITLE_ABS:"Indonesia" AND TITLE_ABS:"health information system")
  AND OPEN_ACCESS:Y AND PUB_YEAR:[2020 TO 2026]
```

Catatan: sintaks Europe PMC sensitif terhadap tanda kutip dan tanda hubung. Beberapa query di atas dijalankan dalam bentuk yang lebih sederhana (mis. `SATUSEHAT`, `TITLE_ABS:LOINC`) lalu disaring manual.

---

## 3. Kriteria inklusi

- Publikasi **2020–2026** (prioritas; satu artikel 2020 tetap dipakai karena relevan).
- Artikel jurnal atau conference paper **peer-reviewed**.
- Berbahasa Inggris atau Indonesia.
- Membahas minimal satu dari: interoperabilitas HIS/EHR, HL7/FHIR/CDA, DICOM, SNOMED CT, LOINC, ICD-10, SATUSEHAT, atau implementasi standardisasi di Indonesia.
- Tersedia **full text open-access**.
- Relevan dengan RQ1–RQ4.

## 4. Kriteria eksklusi

- Editorial, komentar, koreksi, erratum, dan preprint.
- Artikel tanpa full text yang dapat diakses.
- Artikel non-kesehatan (mis. pertanian, keuangan) yang hanya menyebut "interoperability" secara umum.
- Duplikasi (versi preprint dan versi jurnal dianggap satu).
- Dokumen standar resmi (HL7, WHO, Kemenkes) — dipakai sebagai sumber pendukung, **tidak** dihitung sebagai artikel.

---

## 5. Hasil seleksi

| Tahap | Jumlah |
|---|---:|
| Kandidat awal (semua tema, open-access) | ± 150 |
| Setelah screening judul/abstrak | ± 45 |
| Setelah verifikasi full text dan relevansi | **26** |
| Artikel final yang diunduh | **26** |

Sebaran final: A = 6, B = 5, C = 7, D = 8.

Angka kandidat awal adalah perkiraan dari beberapa query yang dijalankan; untuk bagian Methodology paper, **hitung ulang dan catat angka persis** dari setiap database pada tanggal akses yang akan dilaporkan.

---

## 6. Keterbatasan proses pencarian ini

1. **Belum dual screening** — seleksi dilakukan satu orang, sehingga berpotensi bias seleksi.
2. **Belum snowballing** — backward/forward citation dari artikel kunci belum dilakukan.
3. **Tidak semua database diakses langsung** — Scopus/IEEE Xplore/ScienceDirect/ACM belum di-query sistematis; artikel dari penerbit tersebut dapat ditambahkan.
4. **Tiga PDF adalah reading-copy** hasil konversi full text Europe PMC (C01, D01, D03), bukan PDF layout penerbit.
5. **Angka hit per query belum lengkap** — lengkapi saat menulis bagian Review Methodology.

---

## 7. Cara memakai log ini di bagian Methodology

Tulis dengan urutan:

1. Database dan tanggal akses.
2. String pencarian per tema (bisa diringkas dalam tabel).
3. Kriteria inklusi/eksklusi.
4. Alur seleksi (identification → screening → eligibility → included).
5. Jumlah akhir dan sebaran tema.
6. Keterbatasan proses seleksi.

Contoh kalimat:

> A structured search was conducted on 5 November 2026 using Europe PMC, OpenAlex, and Crossref, complemented by publisher websites. The search combined terms related to health information exchange, HL7 FHIR, DICOM, SNOMED CT, LOINC, ICD-10, and SATUSEHAT. After screening titles and abstracts and verifying full-text availability, 26 open-access articles published between 2020 and 2026 were included (Theme A: 6; Theme B: 5; Theme C: 7; Theme D: 8).
