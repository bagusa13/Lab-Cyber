import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_report(output_paths, media_dir):
    doc = docx.Document()

    # Set page margins (0.85 inch for clean professional aesthetic)
    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(19)
        run.font.name = 'Arial'
        run.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(11)
        run.font.name = 'Arial'
        run.font.color.rgb = RGBColor(0x0D, 0x6E, 0xFD)

    def add_meta_box(items):
        tbl = doc.add_table(rows=len(items), cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        for idx, (label, val) in enumerate(items):
            row = tbl.rows[idx]
            c0, c1 = row.cells[0], row.cells[1]
            c0.width = Inches(2.3)
            c1.width = Inches(4.5)
            set_cell_background(c0, "0A2540")
            set_cell_background(c1, "F1F5F9")
            set_cell_margins(c0, 50, 50, 90, 90)
            set_cell_margins(c1, 50, 50, 90, 90)
            
            p0 = c0.paragraphs[0]
            r0 = p0.add_run(label)
            r0.bold = True
            r0.font.size = Pt(9)
            r0.font.name = 'Arial'
            r0.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            
            p1 = c1.paragraphs[0]
            r1 = p1.add_run(val)
            r1.font.size = Pt(9)
            r1.font.name = 'Segoe UI'
            r1.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
            p0.paragraph_format.space_before = Pt(0)
            p0.paragraph_format.space_after = Pt(0)
            p1.paragraph_format.space_before = Pt(0)
            p1.paragraph_format.space_after = Pt(0)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(13)
        run.font.name = 'Arial'
        run.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(10.5)
        run.font.name = 'Arial'
        run.font.color.rgb = RGBColor(0x0D, 0x6E, 0xFD)

    def add_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.size = Pt(9.5)
            r_pre.font.name = 'Segoe UI'
            r_pre.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        r = p.add_run(text)
        r.font.size = Pt(9.5)
        r.font.name = 'Segoe UI'
        r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        return p

    def add_cmd_box(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl.rows[0].cells[0]
        c.width = Inches(6.8)
        set_cell_background(c, "0F172A")
        set_cell_margins(c, top=70, bottom=70, left=110, right=110)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(code_text)
        r.font.name = 'Consolas'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0x38, 0xBD, 0xF8)
        doc.add_paragraph().paragraph_format.space_after = Pt(3)

    def add_img(filename, caption_text):
        full_path = os.path.join(media_dir, filename)
        if os.path.exists(full_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(5)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run()
            run.add_picture(full_path, width=Inches(6.2))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(6)
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.size = Pt(8.5)
            r_cap.font.italic = True
            r_cap.font.name = 'Segoe UI'
            r_cap.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    def add_alert(title, text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl.rows[0].cells[0]
        c.width = Inches(6.8)
        set_cell_background(c, "FEF3C7")
        set_cell_margins(c, top=70, bottom=70, left=110, right=110)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r_tit = p.add_run(f"[!] {title}: ")
        r_tit.bold = True
        r_tit.font.name = 'Arial'
        r_tit.font.size = Pt(9)
        r_tit.font.color.rgb = RGBColor(0x92, 0x40, 0x0E)
        r_txt = p.add_run(text)
        r_txt.font.name = 'Segoe UI'
        r_txt.font.size = Pt(9)
        r_txt.font.color.rgb = RGBColor(0x78, 0x35, 0x0F)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # --- COVER / HEADER ---
    add_title("LAPORAN RESMI AUDIT PENETRASI KEAMANAN JARINGAN")
    add_subtitle("INTERNAL NETWORK DISCOVERY, PORT SCANNING & EXPLOITATION TESTING")

    meta = [
        ("Target Evaluasi", "Infrastruktur Subnet Internal Jaringan Lokal (192.168.1.0/24)"),
        ("Penilai Keamanan", "Tim Praktisi Keamanan Siber / Red Team"),
        ("Tanggal Pelaksanaan", "23 Oktober 2026"),
        ("Tingkat Risiko", "MEDIUM - HIGH (Sedang ke Tinggi)"),
        ("Standar Metodologi", "PTES (Penetration Testing Execution Standard) & NIST SP 800-115"),
        ("Taktik MITRE ATT&CK", "TA0007 - Discovery (T1046, T1018) | TA0006 - Credential Access (T1110 Brute Force)"),
        ("Platform Penguji", "Kali Linux (Rolling) - Hostname: DESKTOP-WV8RX5H (IP: 192.168.1.25)"),
    ]
    add_meta_box(meta)

    # --- 1. RINGKASAN EKSEKUTIF ---
    add_h1("1. RINGKASAN EKSEKUTIF (EXECUTIVE SUMMARY)")
    add_p("Pada tanggal 23 Oktober 2026, telah dilaksanakan kegiatan audit keamanan penetrasi jaringan internal (authorized internal network penetration testing) secara menyeluruh pada subnet lokal 192.168.1.0/24. Pengujian ini mencakup pemetaan topologi aset (host discovery), identifikasi port terbuka (port scanning), evaluasi visibilitas layanan basis data (service enumeration), efektivitas kontrol firewall, hingga simulasi uji penetrasi langsung (exploitation testing) menggunakan serangan credential brute-force terhadap layanan MySQL.")
    
    add_p("Berdasarkan rangkaian 10 tahapan pengujian yang dilaksanakan, penguji mencatat kesimpulan eksekutif berikut:", "Temuan Utama Audit: ")
    add_p("1. Penemuan 8 Host Aktif via Layer 2 ARP: Mekanisme ARP Sweep berhasil memetakan seluruh host aktif termasuk Gateway Fiberhome (192.168.1.1) dan Workstation Intel (192.168.1.10) tanpa terhalang kontrol filter ICMP/Ping.")
    add_p("2. Keterpaparan Layanan Basis Data Kritis: Host 192.168.1.10 membuka port 3306/tcp (MySQL) dan 33060/tcp (MySQL X Protocol) secara terbuka ke seluruh subnet.")
    add_p("3. Simulasi Eksploitasi Brute-Force (Hydra Testing): Serangan penebakan kata sandi terhadap user root MySQL berhasil ditahan di gerbang jabat tangan awal oleh mekanisme Host-Based Access Control bawaan MySQL (Error 1130: Host '192.168.1.25' is not allowed).")
    add_p("4. Bukti Blindspot Pemindaian Top-1000 Ports: Pemindaian default top-1000 gagal mendeteksi port 33060 dan port dinamis 62497. Port tersebut hanya terungkap saat dilakukan Full 65535 Port Scan.")
    add_p("5. Isolasi Firewall Efektif pada SMB: Port 445/tcp (SMB) pada host target berstatus filtered, membuktikan Windows Defender Firewall secara aktif me-drop koneksi SMB dari LAN publik, melindungi host dari exploit seperti EternalBlue.")
    add_p("6. Hardening Layanan Gateway: Router Fiberhome membuka port UDP 53 (DNS) dan 67 (DHCP), namun port 161 (SNMP) tertutup, mencegah kebocoran informasi topologi melalui SNMP.")

    # --- 2. RUANG LINGKUP & SPESIFIKASI LABORATORIUM ---
    add_h1("2. RUANG LINGKUP & SPESIFIKASI LABORATORIUM")
    add_h2("2.1. Rig Penguji / Mesin Penyerang (Attacker Rig)")
    add_p("Distribusi Sistem Operasi: Kali Linux Rolling Release\nHostname: DESKTOP-WV8RX5H (Akun: root@DESKTOP-WV8RX5H:/home/kali)\nAlamat IP Penguji: 192.168.1.25\nVersi Perangkat Lunak: Nmap Version 7.99 | THC Hydra v9.7\nWordlist Pengujian: /usr/share/wordlists/rockyou.txt (14.344.399 kata sandi)\nMetode Operasional: Stealth SYN Scan (-sS), ARP Ping (-PR), UDP Scan (-sU), NSE Scripting, Password Brute-Force")

    add_h2("2.2. Profil Target Jaringan (Target Profile)")
    add_p("Subnet Ruang Lingkup: 192.168.1.0/24 (Total 256 Alamat IP, Netmask 255.255.255.0)\nTarget Utama 1 (Server/Workstation): 192.168.1.10 (MAC: 74:3A:F4:21:8D:0B - Intel Corporate, OS: Windows 11 Build 24H2/21H2)\nTarget Utama 2 (Default Gateway Router): 192.168.1.1 (MAC: 90:55:DE:F6:66:58 - Fiberhome Telecommunication Technologies Co.,LTD)")

    # --- 3. METODOLOGI & BUKTI PELAKSANAAN ---
    add_h1("3. METODOLOGI & BUKTI PELAKSANAAN TEKNIS (EVIDENCE & FINDINGS)")

    # Step 1
    add_h2("3.1. Fase 1: Host Discovery L2 Menggunakan ARP Sweep (netdiscover)")
    add_p("Auditor memulai pengujian dengan menjalankan utilitas netdiscover untuk memetakan seluruh perangkat aktif di segmen Layer 2 melalui injeksi paket ARP Request:")
    add_cmd_box("netdiscover -r 192.168.1.0/24")
    add_img("step1_netdiscover_arp_sweep.png", "Screenshot 1: netdiscover menangkap 257 paket ARP dari 8 host aktif unik pada subnet 192.168.1.0/24")
    add_p("Hasil Pemindaian ARP: Terdeteksi 8 host aktif. Gateway Fiberhome (192.168.1.1) mendominasi lalu lintas dengan 210 paket ARP. Host target terdeteksi pada 192.168.1.10 dan 192.168.1.11 (keduanya ber-NIC Intel Corporate).", "  Analisis Hasil: ")

    # Step 2
    add_h2("3.2. Fase 2: Validasi Host Discovery L2 Menggunakan Nmap (-sn -PR)")
    add_p("Auditor memvalidasi temuan netdiscover menggunakan Nmap Host Discovery dengan flag ARP Ping (-PR) tanpa melakukan port scanning (-sn):")
    add_cmd_box("sudo nmap -sn -PR 192.168.1.0/24")
    add_img("step2_nmap_sn_pr_host_discovery.png", "Screenshot 2: Nmap ARP Host Discovery mengonfirmasi 8 host up dalam waktu 16.83 detik")
    add_p("Pemindaian selesai dalam 16.83 detik. Seluruh 8 host terverifikasi aktif dengan latensi rendah (0.0025s pada gateway dan 0.13s pada target 192.168.1.10). Penggunaan flag -PR memastikan paket tidak terhambat oleh firewall lokal.", "  Analisis Hasil: ")

    # Step 3
    add_h2("3.3. Fase 3: Full TCP Port Scanning 65535 Ports pada Target (192.168.1.10)")
    add_p("Auditor mengeksekusi Stealth SYN Scan komprehensif mencakup seluruh port TCP (1-65535) dengan laju minimum 1000 paket/detik:")
    add_cmd_box("nmap -sS -p- --min-rate 1000 -T4 192.168.1.10 -oN scan_allports.txt")
    add_img("step3_nmap_full_port_scan.png", "Screenshot 3: Full 65535 Port Scan mendeteksi 3 port terbuka (3306, 33060, 62497) pada host 192.168.1.10")
    add_p("Sebanyak 65.532 port berstatus filtered (diblokir firewall). Ditemukan 3 port terbuka (OPEN): 3306/tcp (mysql), 33060/tcp (mysqlx), dan 62497/tcp (unknown high RPC service). Total durasi scan: 87.10 detik.", "  Analisis Hasil: ")

    # Step 4
    add_h2("3.4. Fase 4: Analisis Blindspot Scanning (Top-1000 Ports Scan)")
    add_p("Auditor membandingkan hasil di atas dengan pemindaian cepat yang hanya memeriksa 1000 port standar:")
    add_cmd_box("nmap -sS --top-ports 1000 192.168.1.10")
    add_img("step4_nmap_top_ports_scan.png", "Screenshot 4: Pemindaian Top-1000 hanya menemukan port 3306 dan melewatkan port 33060 serta 62497")
    add_alert("Temuan Kritis Blindspot", "Pemindaian Top-1000 selesai lebih cepat (19.26 detik) tetapi gagal total mendeteksi port 33060/tcp dan 62497/tcp. Dalam audit penetrasi siber, Full Port Scan (-p-) wajib dijalankan pada target bernilai tinggi.")

    # Step 5
    add_h2("3.5. Fase 5: Pemindaian Layanan UDP pada Gateway Router (192.168.1.1)")
    add_p("Auditor menguji port UDP penting pada default gateway Fiberhome untuk mendeteksi layanan kritis:")
    add_cmd_box("nmap -sU -p 53,67,68,161 192.168.1.1")
    add_img("step5_nmap_udp_gateway_scan.png", "Screenshot 5: Pemindaian port UDP pada Router Fiberhome 192.168.1.1")
    add_p("Port 53/udp OPEN (Domain / DNS server aktif). Port 67/udp OPEN|FILTERED (DHCP Server aktif). Port 161/udp CLOSED (SNMP tertutup, mencegah SNMP enumeration).", "  Analisis Hasil: ")

    # Step 6
    add_h2("3.6. Fase 6: Deteksi Versi Layanan & Fingerprinting OS (-sV -O)")
    add_p("Auditor melakukan banner grabbing tingkat lanjut dan identifikasi stack TCP/IP untuk menentukan sistem operasi target:")
    add_cmd_box("nmap -sV --version-intensity 5 -O 192.168.1.10 -oN scan_service.txt")
    add_img("step6_nmap_service_version_os.png", "Screenshot 6: Service version banner grabbing dan fingerprinting sistem operasi Windows 11")
    add_p("Layanan 3306/tcp teridentifikasi sebagai 'MySQL (unauthorized)', menandakan daemon MySQL menolak koneksi langsung tanpa kredensial terdaftar untuk host IP penguji. Sistem operasi teridentifikasi sebagai Microsoft Windows 11 (24H2/21H2) dengan akurasi 92%.", "  Analisis Hasil: ")

    # Step 7
    add_h2("3.7. Fase 7: Otomasi Skrip Default Nmap Scripting Engine (-sC)")
    add_p("Auditor mengeksekusi kumpulan skrip default Lua Nmap untuk menguji kemampuan ekstraksi informasi otomatis:")
    add_cmd_box("nmap -sC 192.168.1.10")
    add_img("step7_nmap_default_nse_scripts.png", "Screenshot 7: Eksekusi nmap -sC pada host 192.168.1.10")
    add_p("Skrip default mengonfirmasi stabilitas port 3306 dan membuktikan bahwa server tidak merespons query banner anonim secara sembarangan.", "  Analisis Hasil: ")

    # Step 8
    add_h2("3.8. Fase 8: Pemindaian Kerentanan CVE Otomatis (--script vuln)")
    add_p("Auditor menguji potensi kerentanan CVE pada layanan database menggunakan suite vuln non-DoS:")
    add_cmd_box("nmap -sV --script \"vuln and not dos\" 192.168.1.10 -oN scan_vuln.txt")
    add_img("step8_nmap_vuln_scripts.png", "Screenshot 8: Hasil pengujian suite vuln membuktikan tidak ada RCE pre-auth yang dapat dieksploitasi instan")
    add_p("Tidak ditemukan exploit pre-authentication instan yang terbuka. Server database telah diperbarui dengan patch keamanan standar, meskipun port tetap terekspos ke subnet publik.", "  Analisis Hasil: ")

    # Step 9
    add_h2("3.9. Fase 9: Audit Port SMB / File Sharing (Port 445)")
    add_p("Auditor memeriksa potensi eksploitasi protokol file-sharing SMB yang sering menjadi target lateral movement malware:")
    add_cmd_box("nmap -p 445 --script smb-enum-shares,smb-vuln* 192.168.1.10")
    add_img("step9_nmap_smb_audit.png", "Screenshot 9: Port 445 berstatus filtered membuktikan perlindungan firewall host aktif")
    add_p("Port 445 berstatus 'filtered', mengonfirmasi bahwa Windows Defender Firewall aktif memblokir akses SMB dari subnet Wi-Fi/LAN, meniadakan ancaman eksploitasi SMB seperti EternalBlue (MS17-010) atau SMB Relay.", "  Analisis Hasil: ")

    # Step 10
    add_h2("3.10. Fase 10: Simulasi Eksploitasi Langsung (THC Hydra MySQL Brute-Force)")
    add_p("Sebagai pembuktian empiris terhadap risiko port MySQL terbuka, auditor mengeksekusi simulasi serangan brute-force terhadap user root target:")
    add_cmd_box("hydra -l root -P /usr/share/wordlists/rockyou.txt 192.168.1.10 mysql")
    add_img("step10_hydra_mysql_bruteforce.png", "Screenshot 10: Eksekusi serangan Hydra menghasilkan penolakan [ERROR] Host '192.168.1.25' is not allowed to connect")
    add_p("Hasil Eksploitasi: Serangan terhenti di awal jabat tangan jaringan. MySQL secara bawaan mengikat otentikasi pada pasangan 'user'@'host' (secara default hanya 'root'@'localhost'). Karena IP penyerang 192.168.1.25 tidak ada di tabel izin MySQL, server langsung memutuskan koneksi (MySQL Error 1130). Target terlindungi dari serangan jarak jauh langsung terhadap user root.", "  Analisis Hasil: ")

    # --- BAB 4: ADVERSARY TRADECRAFT ---
    add_h1("4. ADVERSARY TRADECRAFT: STRATEGI & JALUR PENETRASI LANJUTAN PENYERANG")
    add_p("Mentalitas seorang penyerang (adversary mindset) tidak pernah menyerah hanya karena satu gerbang tertutup. Ketika penyerang menghadapi pesan 'Host is not allowed' pada port database, mereka akan memutar arah (pivoting & lateral movement) melalui 4 jalur eksploitasi alternatif:")

    add_h2("4.1. Jalur 1: Menyerang Lewat Aplikasi Web Lokal (Bypass via SQL Injection)")
    add_p("Logika Penyerang: MySQL menolak IP penyerang (192.168.1.25), tetapi MySQL selalu mengizinkan koneksi dari localhost (127.0.0.1). Penyerang mencari aplikasi web lokal (PHP/Node.js) yang terhubung ke database. Jika aplikasi web memiliki celah SQL Injection (SQLi), penyerang menyuntikkan kueri SQL lewat input web. Kueri dijalankan oleh web server lokal, dan proteksi 'Host is not allowed' dilewati secara total.")

    add_h2("4.2. Jalur 2: Penetrasi Port Tersembunyi 62497/tcp (High Port Debug/RPC)")
    add_p("Port dinamis 62497/tcp berstatus unknown pada hasil full port scan. Port tinggi sering digunakan oleh utilitas pengembangan (seperti debugger Node.js, Python microservices, atau agent RPC internal) yang kerap lupa diberi proteksi autentikasi. Penyerang akan mengujinya dengan:")
    add_cmd_box("nc -v 192.168.1.10 62497\ncurl -v http://192.168.1.10:62497")
    add_p("Jika port ini rentan terhadap eksekusi perintah (RCE), penyerang masuk ke Windows terlebih dahulu, lalu membuka database MySQL dari dalam secara lokal.")

    add_h2("4.3. Jalur 3: Penyadapan Lalu Lintas (MITM via ARP Spoofing)")
    add_p("Hasil scan netdiscover membuktikan bahwa router tidak mengisolasi klien Wi-Fi. Penyerang dapat melancarkan serangan ARP Poisoning:")
    add_cmd_box("arpspoof -i wlan0 -t 192.168.1.10 192.168.1.1")
    add_p("Dengan membelokkan lalu lintas laptop target melewati mesin penyerang, penyerang dapat menyadap kredensial unencrypted, kueri DNS, dan memanipulasi sesi browsing.")

    add_h2("4.4. Jalur 4: Rekayasa Sosial (Social Engineering & Client-Side Phishing)")
    add_p("Ketika pertahanan sistem (firewall dan permission) sulit ditembus dari luar, penyerang akan menargetkan faktor manusia. Mengirimkan file dokumen atau installer palsu (misalnya fake browser update). Begitu korban mengeksekusi file, malware langsung menghubungi penyerang dari dalam (reverse shell) melewati firewall dan izin host MySQL.")

    add_h2("4.5. Pelajaran Fundamental: Konsep Defense-in-Depth (Pertahanan Berlapis)")
    add_p("Pengujian empiris ini membuktikan teori pertahanan siber terpenting:\n- Lapis 1 (Firewall Windows): Berhasil melindungi SMB (Port 445 aman).\n- Lapis 2 (MySQL Host Permission): Berhasil menggagalkan brute-force Hydra langsung.\n- Lapis 3 (Port Exposure): Lemah, karena port 3306 tetap terlihat dari jaringan luar, memicu penyerang mencari celah sekunder.")

    # --- 5. MATRIKS RISIKO & CVSS ---
    add_h1("5. MATRIKS RISIKO & PENILAIAN KERENTANAN (VULNERABILITY MATRIX)")
    
    vuln_data = [
        ("VULN-NET-01", "Exposed Database Service to LAN Subnet (MySQL 3306 & 33060)", "3306/tcp, 33060/tcp", "6.5 (Medium)\nCVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N", "MEDIUM"),
        ("VULN-NET-02", "Blindspot in Default Top-1000 Port Scanning", "33060/tcp, 62497/tcp", "4.3 (Medium)\nCVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N", "LOW - MED"),
        ("VULN-NET-03", "Unrestricted Layer 2 ARP Topology Reconnaissance", "Subnet 192.168.1.0/24", "3.5 (Low)\nCVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N", "LOW"),
    ]

    tbl_v = doc.add_table(rows=1, cols=5)
    tbl_v.alignment = WD_TABLE_ALIGNMENT.CENTER
    hv = tbl_v.rows[0].cells
    headers = ["ID Temuan", "Deskripsi Kerentanan", "Port Terdampak", "Skor CVSS v3.1", "Tingkat Risiko"]
    for i, h in enumerate(hv):
        h.text = headers[i]
        set_cell_background(h, "0A2540")
        set_cell_margins(h, 60, 60, 80, 80)
        p = h.paragraphs[0]
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.runs[0].bold = True
        p.runs[0].font.size = Pt(9)

    for item in vuln_data:
        row = tbl_v.add_row().cells
        for idx, text in enumerate(item):
            row[idx].text = text
            set_cell_background(row[idx], "FFFFFF" if "MEDIUM" not in text else "FFFBEB")
            set_cell_margins(row[idx], 50, 50, 80, 80)
            p = row[idx].paragraphs[0]
            p.runs[0].font.size = Pt(8.5)
            p.runs[0].font.name = 'Segoe UI'
            if idx == 4:
                p.runs[0].bold = True
                p.runs[0].font.color.rgb = RGBColor(0xD9, 0x77, 0x06) if "MEDIUM" in text else RGBColor(0x16, 0xA3, 0x4A)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # --- 6. REKOMENDASI PERBAIKAN ---
    add_h1("6. REKOMENDASI PERBAIKAN & REMEDIASI (BLUE TEAM DEFENSE)")
    add_p("1. Solusi Cepat 1 Menit: Batasi Binding Address MySQL ke Localhost (Solusi Utama):\nBuka file konfigurasi my.ini (atau my.cnf), ubah baris bind-address menjadi bind-address = 127.0.0.1, lalu restart MySQL. Port 3306 akan langsung hilang dari pandangan pemindai di jaringan Wi-Fi.", "Rekomendasi 1: ")
    add_cmd_box("[mysqld]\nbind-address = 127.0.0.1\nmysqlx_bind_address = 127.0.0.1")
    add_p("2. Pengetatan Aturan Windows Defender Firewall: Buat aturan Inbound Rule spesifik pada Windows Firewall untuk port 3306 dengan membatasi Scope Remote IP Address hanya ke IP aplikasi tepercaya, bukan seluruh subnet /24.", "Rekomendasi 2: ")
    add_p("3. Pengaktifan AP Isolation / Client Isolation pada Gateway: Aktifkan fitur Client Isolation pada router Fiberhome (192.168.1.1). Fitur ini mengisolasi komunikasi Layer 2 antar sesama klien nirkabel sehingga serangan ARP Sweep dan MITM tidak dapat dilakukan.", "Rekomendasi 3: ")
    add_p("4. Penerapan Signature Deteksi Port Scan pada NIDS (Snort/Suricata): Terapkan signature deteksi SYN sweep untuk memantau aktivitas pemindaian agresif di jaringan internal secara otomatis.", "Rekomendasi 4: ")

    # --- 7. KESIMPULAN ---
    add_h1("7. KESIMPULAN")
    add_p("Kegiatan audit penetrasi jaringan internal, enumerasi layanan, dan simulasi eksploitasi berhasil diselesaikan secara metodologis. Seluruh 10 bukti pemindaian dan pengujian teknis berhasil mendokumentasikan postur keamanan jaringan lokal: host memiliki perlindungan firewall yang baik pada port SMB (445), host menolak upaya brute-force langsung lewat hak izin host MySQL bawaan, namun keterbukaan port database tetap menjadi celah yang harus ditutup menggunakan isolasi bind-address localhost. Rekomendasi perbaikan instan telah diserahkan untuk segera diterapkan.")

    for path in output_paths:
        doc.save(path)
        print("Report successfully generated at:", path)

if __name__ == "__main__":
    out_paths = [
        r"d:\01_Bagusa\lab-cyber\03_NETWORK_SCANNING\LAPORAN_PENETRATION_TESTING_NETWORK_SCANNING.docx",
        r"d:\01_Bagusa\lab-cyber\LAPORAN_PENETRATION_TESTING_NETWORK_SCANNING.docx"
    ]
    media = r"d:\01_Bagusa\lab-cyber\03_NETWORK_SCANNING\screenshots"
    create_report(out_paths, media)
