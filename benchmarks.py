from charm.toolbox.pairinggroup import PairingGroup, G1, G2, ZR, pair
import time

# Initialize pairing group (symmetric or asymmetric)
group = PairingGroup('SS512')  # Use 'MNT224' or 'BN254' for asymmetric

# Elements
g1_1 = group.random(G1)
g1_2 = group.random(G1)
g2_1 = group.random(G2)
g2_2 = group.random(G2)
z = group.random(ZR)

# Benchmark utility
def benchmark(op, trials=100):
    total = 0
    for _ in range(trials):
        start = time.time()
        op()
        total += (time.time() - start)
    return (total / trials) * 1000  # ms

# Benchmark each operation
results = {
    "G1 Mul": benchmark(lambda: g1_1 * g1_2),
    "G2 Mul": benchmark(lambda: g2_1 * g2_2),
    "G1 Exp": benchmark(lambda: g1_1 ** z),
    "G2 Exp": benchmark(lambda: g2_1 ** z),
    "Pairing": benchmark(lambda: pair(g1_1, g2_1))
}

# Print results
print("\n🔬 Benchmark Results (average over 100 trials):")
for k, v in results.items():
    print(f"{k:10s} : {v:.4f} ms")


