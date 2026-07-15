# Reviewer 1 Comments - Revision R1

## Overall assessment

Reviewer 1 finds that the revision makes **substantial structural changes** that address most concerns from the first review round. The reviewer specifically recognizes the following engineering revisions:

- Reformulation from CoBRE.
- Removal of the bilinear state-input term.
- Relocation of non-negativity enforcement from a target transformation to a deployment-time linear program (LP).
- Introduction of a deterministic recursive coupled-QP estimator.
- Explicit inclusion of hydraulic retention time (HRT) as an operating input.
- Expansion of the Optuna tuning budget to 100 trials per model.
- Clarification of the ANN architecture.

The reviewer judges that these changes eliminate the mathematical contradiction in the original Equation 5 and make the staged deployment rule explicit:

`raw prediction -> affine projection -> LP`.

Accordingly, the reviewer considers the majority of the earlier concerns resolved. Before recommending publication, the reviewer requests attention to two major technical points and one minor framing point. Conditional on both major comments being addressed, the reviewer considers the manuscript suitable for acceptance.

## Major comment 1 - Demonstrate enforcement of symmetry in $\Theta_{cc}$ and $\Theta_{uu}$

### Concern

In the response to the original comment R1.33, the manuscript states that the influent-influent block $\Theta_{cc}$ and the operational-operational block $\Theta_{uu}$ are symmetric "by construction," and consequently that averaging with $(\Theta + \Theta^\mathsf{T})/2$ is unnecessary before interpreting the Figure 4 heatmaps and supplementary atlases cell by cell.

The reviewer considers this claim consequential because Section 4.4 assigns physical meaning to individual reported entries, including:

- SO-SO: $-2.3899 \times 10^{-2}$
- SO-SN$_2$: $-2.1845 \times 10^{-2}$
- SO-SNO$_2$: $-1.4691 \times 10^{-2}$

### Technical rationale

The Nomenclature presently defines the blocks in the general vectorized second-order form:

$$
\Theta_{cc} \in \mathbb{R}^{F \times F^2},
\qquad
\Theta_{uu} \in \mathbb{R}^{F \times M_{op}^2}.
$$

This parameterization is not intrinsically symmetric. Because $c_{in} \otimes c_{in}$ includes both $c_i c_j$ and $c_j c_i$ as distinct, numerically identical feature entries, the contribution to each output target is determined by the sum $\theta_{k,ij} + \theta_{k,ji}$. Unless symmetry is explicitly constrained during fitting, this decomposition is non-unique: infinitely many pairs $(\theta_{k,ij}, \theta_{k,ji})$ yield the same prediction.

Thus, the model fit may remain valid, but individual off-diagonal heatmap cells do not have a unique physical interpretation without an explicit symmetry mechanism.

### What is missing

The manuscript says that the partitioned feature map and driver coefficients are organized so that the fitted $\Theta$ blocks satisfy commutativity-induced symmetry exactly. However, it does not state the mechanism by which the estimator produces that result. The reviewer cannot determine whether the method:

1. parameterizes only upper-triangular indices and reconstructs lower-triangular entries by mirroring;
2. imposes $\theta_{k,ij} = \theta_{k,ji}$ as equality constraints within the QP; or
3. projects onto the symmetric subspace after each block-coordinate update.

Any of these approaches would resolve the identifiability issue, but none is currently described.

### Requested revision

Add an explicit technical sentence in Section 2.3, or the corresponding subsection of Section 2.6, that states exactly how symmetry is enforced. Include a one-line justification for why the enforcement preserves the optimum of the coupled QP.

If the implementation does not enforce symmetry, the reviewer asks the authors to do one of the following before retaining cell-level physical interpretation in Section 4.4:

- add a symmetry-enforcing layer to the estimator; or
- plot the symmetric average $(\Theta + \Theta^\mathsf{T})/2$.

## Major comment 2 - Reframe feasibility as a hard deployment guarantee, not a regression outcome

### Concern

Section 4.3 transparently reports that no raw coupled prediction is simultaneously invariant-consistent and non-negative:

- Raw conservation compliance: 0.0%.
- Raw non-negativity: 21.7%.

The reviewer emphasizes that the reported final 0% violation rate is not a property of the learned regression alone. The regression head violates conservation for 100% of test samples. Feasibility is obtained at deployment through the staged correction:

- The affine projection resolves 21.8% of cases.
- The LP resolves the remaining 78.2% of cases.

The invariant penalty $\lambda_{inv}$ in Equation 7 is a soft training regularizer. The hard guarantee is supplied by Equation 12, i.e., by the deployment-time correction.

### Requested revision

Reframe the Abstract, Graphical Abstract, and Conclusion so that ICSOR is described as a **constrained-deployment surrogate**. Its regression head should be presented as structured to remain compatible with hard conservation correction, rather than as inherently guaranteeing the final zero-violation outcome.

Also add one sentence to Section 2.4 explicitly stating that the hard feasibility guarantee is produced by the deployment correction, not by the training objective.

## Minor comment - Align the Abstract's accuracy framing with the reported results

The reported aggregate test RMSE values are:

| Model | Aggregate test RMSE |
| --- | ---: |
| ICSOR | 5.98 |
| MLP | 4.38 |
| LightGBM | 5.30 |

ICSOR's aggregate test RMSE is 36% higher than the MLP's and 13% higher than LightGBM's. The reviewer considers the Abstract's description of "competitive aggregate accuracy" overly generous in light of this gap.

The Conclusion already characterizes this result more carefully as a "moderate predictive tradeoff." The reviewer recommends aligning the Abstract with that more cautious framing so readers are not surprised by the accuracy gap in Section 4.1.

## Acceptance condition

Reviewer 1 states that, once Major comments 1 and 2 are addressed, the manuscript should be in shape for acceptance.
