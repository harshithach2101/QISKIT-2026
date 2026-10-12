"""Challenge 2: Make the Quantum Coin Biased."""

from pathlib import Path
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

SHOTS = 100
HERE = Path(__file__).resolve().parent


def make_circuit(gate_sequence):
    circuit = QuantumCircuit(1, 1)
    for gate in gate_sequence:
        if gate == "h":
            circuit.h(0)
        elif gate == "x":
            circuit.x(0)
        elif gate == "ry":
            # A 60-degree rotation gives P(1) = sin(30 degrees)^2 = 0.25.
            circuit.ry(3.141592653589793 / 3, 0)
        else:
            raise ValueError(f"Unknown gate: {gate}")
    circuit.measure(0, 0)
    return circuit


def run(label, gates):
    circuit = make_circuit(gates)
    result = StatevectorSampler().run([circuit], shots=SHOTS).result()[0]
    counts = result.data.c.get_counts()
    print(f"\n{label}")
    print(circuit.draw(output="text"))
    print("Predicted probabilities: P(0) = 75%, P(1) = 25%" if gates == ["ry"] else
          "Predicted probabilities: P(0) = 25%, P(1) = 75%")
    print(f"Measured counts: {counts}")
    return counts


def main():
    print("The RY rotation controls the measurement probabilities.")
    print("A pi/3 rotation from |0> predicts about 75% zeros and 25% ones.")
    print("Applying X after that rotation reverses the probabilities.")

    zero_favored = run("Circuit A — 0 is more likely", ["ry"])
    one_favored = run("Circuit B — 1 is more likely", ["ry", "x"])

    fig, ax = plt.subplots()
    labels = ["0 favored", "1 favored"]
    x = range(2)
    width = 0.35
    for index, outcome in enumerate(["0", "1"]):
        values = [counts.get(outcome, 0) for counts in
                  [zero_favored, one_favored]]
        ax.bar([i + (index - 0.5) * width for i in x], values,
               width, label=f"Outcome {outcome}")
    ax.set_xticks(list(x), labels)
    ax.set_ylabel("Measurements")
    ax.set_title(f"Biased quantum coin ({SHOTS} shots per circuit)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(HERE / "histogram.png", dpi=160)
    plt.show()

    print("\nChallenge question:")
    print("Quantum gates change the amplitudes of the |0> and |1> components.")
    print("Measurement probabilities are the squared magnitudes of those amplitudes.")
    print("An RY rotation sets a bias, and X swaps the probabilities of 0 and 1.")


if __name__ == "__main__":
    main()
