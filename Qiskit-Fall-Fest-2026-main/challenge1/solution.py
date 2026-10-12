"""Challenge 1: Predict the Output."""

from pathlib import Path
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

SHOTS = 100
HERE = Path(__file__).resolve().parent


def run_circuit(name, gates):
    circuit = QuantumCircuit(1, 1)
    for gate in gates:
        getattr(circuit, gate)(0)
    circuit.measure(0, 0)

    sampler = StatevectorSampler()
    result = sampler.run([circuit], shots=SHOTS).result()[0]
    counts = result.data.c.get_counts()
    print(f"\n{name}")
    print(circuit.draw(output="text"))
    print(f"Counts: {counts}")
    return counts


def plot_counts(all_counts):
    labels = ["Circuit A", "Circuit B", "Circuit C"]
    outcomes = ["0", "1"]
    values = [[counts.get(bit, 0) for bit in outcomes] for counts in all_counts]
    x = range(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar([i - width / 2 for i in x], [v[0] for v in values],
           width, label="0")
    ax.bar([i + width / 2 for i in x], [v[1] for v in values],
           width, label="1")
    ax.set_xticks(list(x), labels)
    ax.set_ylabel("Measurements")
    ax.set_title(f"Challenge 1 results ({SHOTS} shots per circuit)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(HERE / "histogram.png", dpi=160)
    plt.show()


def main():
    print("Predictions before running:")
    print("A: X changes |0> to |1>, so 1 should appear in all 100 shots.")
    print("B: two X gates return the qubit to |0>, so 0 should appear in all 100 shots.")
    print("C: H creates an equal superposition, so 0 and 1 should each appear about 50 times.")

    counts_a = run_circuit("Circuit A — one X gate", ["x"])
    counts_b = run_circuit("Circuit B — two X gates", ["x", "x"])
    counts_c = run_circuit("Circuit C — one H gate", ["h"])
    plot_counts([counts_a, counts_b, counts_c])

    print("\nComparison:")
    print("The X gate flips the computational-basis state. Applying it twice restores |0>.")
    print("The H gate creates a superposition, so measurement outcomes are probabilistic.")


if __name__ == "__main__":
    main()
