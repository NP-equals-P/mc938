import nistrng
import numpy as np

N = 100000  # tamanho mínimo recomendado para testes NIST
bits = np.random.randint(0, 2, N)  # substitua pelo seu gerador!

# =========================================================
#    Opções disponíveis:
#    - monobit
#    - frequency_within_block
#    - runs
#    - longest_run_ones_in_a_block
#    - binary_matrix_rank
#    - dft
#    - non_overlapping_template_matching
#    - overlapping_template_matching
#    - maurers_universal
#    - linear_complexity
#    - serial
#    - approximate_entropy
#    - cumulative sums
#    - random_excursion
#    - random_excursion_variant
# =========================================================

test_name = "monobit"

test_result = nistrng.run_by_name_battery(test_name, bits, nistrng.SP800_22R1A_BATTERY)

print(f"\n==================== {test_name} ====================")
if test_result is not None:
    result_obj, elapsed_time = test_result
    print(f"Elapsed time: {elapsed_time:.4f}s")
    print(f"Passed: {result_obj.passed}")
    print(f"P-value (score): {result_obj.score}")
    print(f"Test name: {result_obj.name}")
else:
    print("Test not eligible or failed eligibility check")
