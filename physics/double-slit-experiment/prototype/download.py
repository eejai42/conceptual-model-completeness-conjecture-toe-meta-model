# Python Script to Download Data for ESCC (EDE-σ₈ Cross-Consistency Criterion)

import requests

# URLs to cosmological data (examples - real data URLs need verification)
data_urls = {
    'Planck_CMB': 'https://pla.esac.esa.int/pla-sl/data-action?COSMOLOGY.FILE_ID=COM_CosmoParams_fullGrid_R3.01.zip',
    'Pantheon_H0': 'https://github.com/PantheonPlusSH0ES/DataRelease/archive/refs/heads/main.zip',
    'ACT_CMB': 'https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_DR6_lcdm_params.txt',
    'DES_sigma8': 'https://des.ncsa.illinois.edu/releases/y3a2/Y3A2_cosmology_chain.txt'
}

# Download data
for name, url in data_urls.items():
    print(f"Downloading {name}...")
    response = requests.get(url)
    with open(f"{name}.dat", 'wb') as f:
        f.write(response.content)

print("Download completed.")
