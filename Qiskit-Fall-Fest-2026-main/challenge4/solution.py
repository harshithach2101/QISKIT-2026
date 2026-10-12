"""Challenge 4: Quantum Correlation Switch."""

from pathlib import Path
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

SHOTS = 100
HERE = Path(__file__).resolve().parent


def make_circuit(opposite=False):
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    if opposite:
        circuit.x(1)
    circuit.measure([0, 1], [0, 1])
    return circuit


def execute(circuit):
    result = StatevectorSampler().run([circuit], shots=SHOTS).result()[0]
    return result.data.get_counts() if False else result.data.c.get_counts()


def main():
    correlated = make_circuit()
    opposite = make_circuit(opposite=True)

    print("Part A prediction: 00 and 11 should dominate.")
    print(correlated.draw(output="text"))
    counts_a = execute(correlated)
    print(f"Part A counts: {counts_a}")

    print("\nPart B prediction: 01 and 10 should dominate.")
    print(opposite.draw(output="text"))
    counts_b = execute(opposite)
    print(f"Part B counts: {counts_b}")

    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for ax, title, counts in zip(
        axes, ["Part A — correlated", "Part B — opposite"], [counts_a, counts_b]
    ):
        outcomes = ["00", "01", "10", "11"]
        ax.bar(outcomes, [counts.get(key, 0) for key in outcomes])
        ax.set_title(title)
        ax.set_xlabel("Measured bit string")
        ax.set_ylabel("Count")
    fig.suptitle(f"Challenge 4 ({SHOTS} shots per experiment)")
    fig.tight_layout()
    fig.savefig(HERE / "comparison.png", dpi=160)
    plt.show()

    print("\nComparison:")
    print("Part A uses H then CX to create (|00> + |11>)/sqrt(2).")
    print("Part B adds X to qubit 1, producing (|01> + |10>)/sqrt(2).")
    print("That single extra gate flips the second measured bit, changing equal outcomes to opposite outcomes.")
    print("Counts from the H-based circuits are sampled; small differences from 50/50 are normal.")


if __name__ == "__main__":
    main()
