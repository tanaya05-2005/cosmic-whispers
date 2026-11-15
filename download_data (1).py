import os
import zipfile
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

RELEASE = "https://github.com/tanaya05-2005/cosmic-whispers/releases/download/v1.0.0/"

os.makedirs(DATA, exist_ok=True)

def download(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print("Already available:", os.path.basename(path))
        return

    print("Downloading:", os.path.basename(path))
    response = requests.get(url, stream=True, timeout=300)
    response.raise_for_status()

    with open(path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    print("Downloaded:", os.path.basename(path))

# Restore project folders from ZIP
zip_path = os.path.join(BASE, "cosmic_whispers_data.zip")

required_csv = os.path.join(BASE, "results", "candidate_regions.csv")

if not os.path.exists(required_csv):
    download(RELEASE + "cosmic_whispers_data.zip", zip_path)

    print("Extracting project data...")
    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(BASE)

    print("Project data extracted.")

# Restore the three essential FITS files
fits_files = [
    "2025W18_1B_0162_1_D1.fits",
    "aligned_observation2_complete_wcs.fits",
    "corrected_difference.fits"
]

for filename in fits_files:
    download(RELEASE + filename, os.path.join(DATA, filename))

print("Cosmic Whispers data preparation complete.")
