# ==========================================
# Variabel Konfigurasi
# ==========================================
DC = docker compose
PROJECT_NAME = odoo

# Nama database dan modul yang sedang dikerjakan
DB = odoo_db
MODULE = estate

.PHONY: help start stop restart logs status clean update

# Menampilkan menu bantuan
help:
	@echo "Perintah yang tersedia:"
	@echo "  make start     - Menjalankan container Odoo (background)"
	@echo "  make stop      - Menghentikan container Odoo"
	@echo "  make restart   - Restart container Odoo dan lihat log"
	@echo "  make update    - Update module Odoo dan restart server"
	@echo "  make logs      - Melihat log container secara real-time"
	@echo "  make status    - Melihat status container"
	@echo "  make clean     - Menghentikan dan menghapus container"

# Menyalakan Odoo
start:
	@echo "Menyalakan Odoo..."
	$(DC) up -d

# Menghentikan Odoo
stop:
	@echo "Menghentikan Odoo..."
	$(DC) stop

# Restart Odoo dan langsung menampilkan log
restart:
	@echo "Melakukan restart Odoo..."
	$(DC) restart
	@echo "Menampilkan log..."
	$(DC) logs -f --tail=100

# ==========================================
# PERINTAH BARU UNTUK UPDATE MODULE
# ==========================================
update:
	@echo "Memuat ulang file Python terbaru dengan melakukan restart Odoo..."
	$(DC) restart
	@echo "Melakukan update module $(MODULE) pada database $(DB)..."
	$(DC) exec odoo odoo -d $(DB) -u $(MODULE) --stop-after-init
	@echo "Update selesai. Menampilkan log..."
	$(DC) logs -f --tail=100

# Melihat Log
logs:
	$(DC) logs -f --tail=100

# Cek Status
status:
	$(DC) ps

# Hapus Container
clean:
	@echo "Menghapus container..."
	$(DC) down