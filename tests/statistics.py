import numpy as np
import math
from scipy.special import gammaincc
# ---------- Intervalo de confiança ------------

def get_conf_interval(num_spl, alpha=0.01):
    p = 1 - alpha
    # Desvio
    d = 3*math.sqrt(p*(1-p)/num_spl)
    return (p-d, p+d)

def is_in_conf_interval(distr:np.array, n_spls:np.array):
    cint_check = np.zeros_like(distr).astype(bool)
    for i in range(distr.shape[0]):
        c_int = get_conf_interval(n_spls[i])
        cint_check[i] = distr[i] > c_int[0] and distr[i] < c_int[1] \
            and n_spls[i] >= 55
    return cint_check

def chi_squared(distr:np.array, bin_size=0.1):
    num_bins = 1/bin_size
    assert num_bins == math.ceil(num_bins), \
        f"Warning: bin size of {bin_size} does \
            not generate an integer number of bins"
    num_bins = int(num_bins)
    q = distr.shape[0]/10
    freqs = np.zeros(shape=(num_bins,))
    last_count = 0
    for i in range(len(freqs)):
        freqs[i] = (distr <= i*bin_size).sum() - last_count
        last_count += freqs[i]
    chi_parcels = (freqs - q)**2
    chi_sq = chi_parcels.sum()/q
    return chi_sq

def get_uniformity_pval(distr:np.array):
    chi_sq = chi_squared(distr)
    return gammaincc(9/2, chi_sq/2)

def is_distr_uniform(distr:np.array, threshold=0.0001):
    unif_pval = get_uniformity_pval(distr)
    return unif_pval >= threshold

def scale_passed(passed:np.array, eligible:np.array):
    return passed / eligible