# Methods

## Bell/CHSH game

The Cirq donor uses four qubits: two players and two quantum referees. H/CNOT creates a shared Bell pair; referee H gates supply x,y, and the source’s controlled X rotations select the strategy. Measurements a,b,x,y are bound by key, not qubit-order guesswork. A trial wins when `a XOR b == x AND y`.

The report uses 4096 simulated trials and seed 137. Compare the measured success probability to the classical game limit 0.75 and quantum limit `cos(pi/8)^2`. The numerical test permits an absolute difference below 0.04 at 4096 trials: the Bernoulli sampling standard deviation near the quantum limit is about 0.0055, so this is a broad regression tolerance, not a confidence interval. No statistical interval is implemented. This models the quantum strategy; it is not a physical loophole-free Bell experiment or a four-setting correlator/S estimator.

## Amplitude damping

The source sequence is `measure(initial_state) → X → measure(after_not_gate)`. `ConstantQubitNoiseModel(amplitude_damp(p))` inserts a channel after moments, including measurement moments. Noise following the initial measurement leaves the ground state unchanged; the channel following X damps the prepared excited state. Noise after the final measurement cannot alter its recorded bit. A source-defined X/channel density-matrix calculation supplies the corresponding excited-state probability.

Rates are 0,0.4,0.5,1 with 1024 shots each. Each independent rate uses seed 137, explicitly recorded. The initial histogram remains all zero; endpoints yield final one at p=0 and zero at p=1. Intermediate finite-shot values are retained without enforcing monotonicity or smoothing.

## Six-node Max-Cut QAOA

Cirq’s donor generates a 3-regular six-node graph and p=2 layers. H prepares the uniform superposition; cost gates use `rzz(-0.5 * gamma)` with `ZZPowGate(exponent=2*rads/pi, global_shift=-0.5)`, followed by `rx(2*beta)` mixers. The default is the donor’s ZZ route. The unselected BooleanHamiltonianGate alternative is omitted; this study implements only the donor’s false/default route.

`cut_values` retains the donor adjacency-matrix expression with sorted nodelist. Bit arrays are cast to signed int64 before `(-1) ** bits`, preserving the intended ±1 vectors without NumPy 2 unsigned-scalar promotion. Measurement wires are LineQubits 0..5 in that same order. Exhaustive enumeration checks all 64 bitstrings. Nelder–Mead minimizes the negative sampled mean cut with 256 shots per objective call and maxiter=50. Graph, parameter and simulator streams use seeds 137,138,139 respectively; the parameter stream preserves the donor’s preliminary example-circuit draws before x0.

The best sampled bitstring across objective calls is different from the optimizer’s mean-cut objective. Both are reported, along with evaluation trace, x0/final parameters, graph order, exact optimum, approximation ratio, status/message/nit/nfev and circuit moment/operation counts. The latter are framework cost metrics, not a hardware latency claim. Finite sampling gives a noisy objective; convergence or a ratio of 1 is not forced.

## Variational landscape / zero-noise extrapolation

The Mitiq ansatz is exactly Rx(q0), CNOT(q0,q1), Rx(q1), CNOT(q0,q1), Rx(q0), at one gamma. The executor computes `real(trace(rho @ kron(Z,Z)))` using Cirq’s density-matrix simulator. Raw execution inserts depolarizing p=0.04 after circuit moments; ideal execution omits noise.

The full landscape is a 50-point linspace from 0 to 2*pi inclusive. Mitiq’s public two-stage API constructs circuits at scales [1,3,5], executes them in the same order and combines results with `RichardsonFactory.extrapolate`. Default gate weighting and moment squashing are retained; seed 137 is passed independently to each folding call. Scale factor is the library’s folding target, not an assertion of physical noise multiplication. Intermediate circuits, operations, moments and ideal/noisy expectations make this distinction inspectable.

The plots compare complete ideal/raw/mitigated curves and absolute errors. Mean errors, worsened points and out-of-range mitigated values are reported without clipping. Richardson extrapolation can be biased or unstable; improvement at every gamma is not assumed. Tests compare noiseless folded unitaries up to global phase, no-noise expectations and the two-stage result against the donor high-level mitigated executor.
