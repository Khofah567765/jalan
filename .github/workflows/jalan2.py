name: Trigger Private Vision+ Scraper

on:
  schedule:
    # Berjalan otomatis setiap 1 jam
    - cron: '0 * * * *'
  workflow_dispatch: # Tombol manual "Run workflow"

jobs:
  run-private-script:
    runs-on: ubuntu-latest

    steps:
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      # 1. Download kode dari Repo Private menggunakan PAT
      - name: Checkout Private Repository
        uses: actions/checkout@v4
        with:
          repository: 'USERNAME_GITHUB_ANDA/NAMA_REPO_PRIVATE' # Ganti dengan username & nama repo private Anda
          token: ${{ secrets.GH_PAT }}
          path: 'private_core' # Diunduh ke dalam folder khusus

      # 2. Install library yang dibutuhkan oleh vs.py
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r private_core/requirements.txt

      # 3. Jalankan vs.py langsung dari folder private
      - name: Jalankan Scraper & Push ke Firebase
        env:
          FIREBASE_SERVICE_ACCOUNT: ${{ secrets.FIREBASE_SERVICE_ACCOUNT }}
          FIREBASE_DATABASE_URL: ${{ secrets.FIREBASE_DATABASE_URL }}
        run: |
          cd private_core
          python vs.py
