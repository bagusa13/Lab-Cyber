# LABORATORIUM PRAKTIKUM KEAMANAN SIBER & PENETRATION TESTING
**Author / Auditor:** Bagus  
**Platform:** Kali Linux & Windows 11  
**Repositori Direktori:** `D:\01_Bagusa\lab-cyber`

---

## 📂 Struktur & Katalog Modul Laboratorium

Repositori ini telah ditata secara rapi dan modular berdasarkan tahapan standar industri **PTES (Penetration Testing Execution Standard)** dan **Cyber Kill Chain**:

```
D:\01_Bagusa\lab-cyber\
├── 00_TOOLS_UTILITIES/       -> Utilitas pendukung lab (Ventoy USB flasher, Amlogic bootloader injector)
├── 01_RECONNAISSANCE_OSINT/   -> Modul Reconnaissance, DNS Footprinting & Laporan Tugas Keamanan Sistem
├── 02_PANDUAN_ANONIMITAS/     -> Modul OPSEC & Anonimitas Siber (Tor, Proxychains, Anonsurf, Anti-Fingerprinting)
├── 03_NETWORK_SCANNING/       -> Modul Discovery Jaringan, Full Port Scanning & Simulasi Brute-Force Hydra
└── 04_WIRELESS_PENTEST/       -> Modul Audit Penetrasi Wi-Fi WPA2-PSK (4-Way Handshake & Cracking)
```

---

## 📑 Rincian Modul & Akses Dokumen:

### 1. `00_TOOLS_UTILITIES`
* **Deskripsi:** Kumpulan alat bantu sistem dan instalasi lingkungan lab.
* **Berkas Utama:**
  * `ventoy-1.1.18-windows/` : Software pembuat bootable USB multi-ISO.
  * `SUNTIK_BOOTLOADER_SD.bat` : Skrip otomasi injeksi bootloader MicroSD untuk hardware SBC/TV Box.

### 2. `01_RECONNAISSANCE_OSINT`
* **Deskripsi:** Pengintaian informasi target, pemetaan subdomain, dan laporan akademik tugas kuliah.
* **Berkas Utama:**
  * `BUKU_PANDUAN_PRAKTIS_RECONNAISSANCE.docx`
  * `alldomaintelyu.txt` & `Laporan_Information_Gathering_TelkomUniversity.txt`
  * `LAPORAN TUGAS KEAMANAN SISTEM.docx` (serta versi revisi & backup).

### 3. `02_PANDUAN_ANONIMITAS`
* **Deskripsi:** Buku panduan komprehensif OPSEC, routing Tor transparan, spoofing MAC address, pencegahan kebocoran WebRTC, dan anti-fingerprinting browser.
* **Berkas Utama:**
  * `BUKU_PANDUAN_ANONIMITAS_DAN_OPSEC.docx`
  * `screenshots/` (Memuat bukti langkah 1 hingga 30 pengujian OPSEC).

### 4. `03_NETWORK_SCANNING`
* **Deskripsi:** Laporan audit penetrasi jaringan internal, host discovery L2, perbandingan blindspot top-1000 vs full scan 65535 ports, fingerprinting OS, audit firewall SMB, serta pengujian eksploitasi brute-force Hydra terhadap MySQL.
* **Berkas Utama:**
  * `LAPORAN_PENETRATION_TESTING_NETWORK_SCANNING.docx` *(Laporan eksekutif berformat Word, 2.19 MB)*
  * `LAPORAN_PENETRATION_TESTING_NETWORK_SCANNING.md` *(Format Markdown)*
  * `screenshots/` *(10 tangkapan layar bukti pengujian)*
  * `generate_docx.py` *(Skrip generator Word styling)*

### 5. `04_WIRELESS_PENTEST`
* **Deskripsi:** Laporan audit penetrasi jaringan Wi-Fi WPA2-Personal, deauthentication frame injection, penangkapan 4-Way Handshake, dan analisis kelemahan kata sandi PSK.
* **Berkas Utama:**
  * `LAPORAN_PENETRATION_TESTING_WIFI.docx`
  * `LAPORAN_PENETRATION_TESTING_WIFI.md`

---
*Repositori ini dikelola secara terstruktur untuk dokumentasi akademik, riset keamanan siber, dan portofolio profesional.*
