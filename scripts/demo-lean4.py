from lean_dojo import *
from pathlib import Path

repo = LeanGitRepo(
    "https://github.com/leanprover-community/mathlib4",
    "29dcec074de168ac2bf835a77ef68bbe069194c5",
)

traced_repo = trace(repo)

# Manually set the back-reference from each TracedFile to the TracedRepo.
# This is needed because TracedFile.traced_repo is not serialized, and the
# loading process in this version of the library doesn't restore it,
# causing an AssertionError in check_sanity.
for tf in traced_repo.traced_files:
    tf.traced_repo = traced_repo

traced_file = traced_repo.get_traced_file("Mathlib/Algebra/BigOperators/Pi.lean")

traced_theorems = traced_file.get_traced_theorems()

print(len(traced_theorems))

thm = traced_file.get_traced_theorem("pi_eq_sum_univ")

if thm is None:
    raise ValueError("Theorem not found")

proof_node = thm.get_proof_node()
proof = proof_node.lean_file[proof_node.start : proof_node.end]
print(proof)

traced_tactics = thm.get_traced_tactics()

tac = traced_tactics[1]

theorem = Theorem(repo, Path("Mathlib/Algebra/BigOperators/Pi.lean"), "pi_eq_sum_univ")

# For some theorems, it might take a few minutes.
dojo, state_0 = Dojo(theorem).__enter__()

print(state_0.pp)

state_1 = dojo.run_tac(state_0, "revert x")

print(state_1.pp)

state_2 = dojo.run_tac(state_0, "hello world!")

print(state_2.pp)
