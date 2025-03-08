import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM

# Load Pantheon+ data
pantheon_data = pd.read_csv('PantheonPlusSH0ES.dat', delim_whitespace=True)
redshifts = pantheon_data['zHD']
observed_mags = pantheon_data['m_b_corr']

# Planck LambdaCDM parameters (example)
H0_planck = 67.4  # km/s/Mpc
Om0_planck = 0.315

# Cosmological model using Planck data
cosmo_planck = FlatLambdaCDM(H0=H0_planck, Om0=Om0_planck)

# Compute theoretical magnitudes (distance modulus)
distance_modulus_theory = cosmo_planck.distmod(redshifts).value

# Compute residuals
residuals = observed_mags - distance_modulus_theory

# Check residual pattern indicating EDE
plt.scatter(redshifts, residuals, alpha=0.5)
plt.axhline(0, color='r', linestyle='--')
plt.xlabel('Redshift (z)')
plt.ylabel('Residual (Observed - Theory)')
plt.title('Residuals of Pantheon+ vs Planck ΛCDM')
plt.grid(True)
plt.show()

# Evaluate statistically significant deviations indicating EDE
mean_residual_high_z = np.mean(residuals[redshifts > 0.5])
std_residual_high_z = np.std(residuals[redshifts > 0.5])

print('Mean residual (z > 0.5):', mean_residual_high_z)
print('Std dev of residuals (z > 0.5):', std_residual_high_z)

if abs(mean_residual_high_z) > 2 * std_residual_high_z:
    print("EDE model supported by high-z residuals.")
else:
    print("No strong evidence for EDE found in high-z residuals.")