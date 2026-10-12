"""Challenge 3: Can You Change the Correlation?"""

from pathlib import Path
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

SHOTS = 100
HERE = Path(__file__).resolve().parent


def bell_circuit(modified=False):
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    if modified:
        # One additional X gate on qubit 1 changes |00>+|11> to |01>+|10>.
        circuit.x(1)
    circuit.measure([0, 1], [0, 1])
    return circuit


def run(label, circuit):
    result = StatevectorSampler().run([circuit], shots=SHOTS).result()[0]
    counts = result.data.c.get_counts()
    print(f"\n{label}")
    print(circuit.draw(output="text"))
    print(f"Counts: {counts}")
    return counts


def main():
    print("Prediction: the original Bell circuit should give 00 and 11.")
    print("After X on qubit 1, 01 and 10 should dominate.")
    original = run("Original Bell circuit", bell_circuit())
    changed = run("Modified circuit (X on qubit 1)", bell_circuit(modified=True))

    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for ax, label, counts in zip(
        axes, ["Original Bell circuit", "Modified circuit"], [original, changed]
    ):
        keys = ["00", "01", "10", "11"]
        ax.bar(keys, [counts.get(key, 0) for key in keys])
        ax.set_title(label)
        ax.set_xlabel("Measured bit string")
        ax.set_ylabel("Count")
    fig.suptitle(f"Challenge 3 ({SHOTS} shots per circuit)")
    fig.tight_layout()
    fig.savefig(HERE / "histograms.png", dpi=160)
    plt.show()

    print("\nExplanation:")
    print("The original circuit creates the Bell state (|00> + |11>)/sqrt(2).")
    print("The X gate flips the second qubit, giving (|01> + |10>)/sqrt(2).")
    print("The qubits remain correlated in the broader sense, but their measured bits are opposite.")


if __name__ == "__main__":
    main()
