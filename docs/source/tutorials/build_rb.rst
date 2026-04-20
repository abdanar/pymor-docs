Tutorial: Building a Reduced Basis
===================================

In this tutorial we will learn more about VectorArrays and how to construct a reduced basis using pyMOR.

A reduced basis spans a low dimensional subspace of a Model's :attr:`~pymor.models.interface.Model.solution_space`,
in which the :meth:`solutions <pymor.models.interface.Model.solve>` of the Model
can be well approximated for all parameter_values. In this context, time is treated as an additional parameter.

An upper bound for the possible quality of a reduced space is given by the Kolmogorov :math:`N`-width:

.. math::

    \mathcal{M} := \{u(\mu)\ |\ \mu \in \mathcal{P}\},

and

.. math::

    d_N(\mathcal{M}) :=
    \inf_{\substack{V_N \subseteq V\\ \dim(V_N) \leq N}}
    \sup_{x \in \mathcal{M}}
    \inf_{v \in V_N}
    \|x - v\|.

Here, :math:`V` denotes the solution space, and :math:`\mathcal{P}` the ParameterSpace.

---

Model setup
===========

First import:

.. code-block:: ipython3

    import numpy as np
    from pymor.basic import *

We define a thermal block problem:

.. code-block:: ipython3

    problem = thermal_block_problem((3, 2))
    fom, _ = discretize_stationary_cg(problem, diameter=1/100)

Parameter space:

.. code-block:: ipython3

    parameter_space = fom.parameters.space(0.0001, 1.0)

Inspect parameters:

.. code-block:: ipython3

    fom.parameters

---

Computing snapshot data
=======================

Training set:

.. code-block:: ipython3

    training_set = parameter_space.sample_randomly(25)
    print(training_set)

Solve full-order model:

.. code-block:: ipython3

    training_data = fom.solution_space.empty()

    for mu in training_set:
        training_data.append(fom.solve(mu))

Check size:

.. code-block:: ipython3

    len(training_data)

Visualize:

.. code-block:: ipython3

    fom.visualize(training_data)

---

Trivial reduced basis
=====================

.. code-block:: ipython3

    trivial_basis = training_data.copy()

Projection problem:

Let :math:`v_{\text{proj}}` be projection:

.. math::

    \sum_{j=1}^N \lambda_j (u_j, u_i) = (v, u_i)

Gramian and projection:

.. code-block:: ipython3

    U = fom.solve(parameter_space.sample_randomly())

    G = trivial_basis.gramian()
    R = trivial_basis.inner(U)

    lambdas = np.linalg.solve(G, R)

    U_proj = trivial_basis.lincomb(lambdas)

Visualization:

.. code-block:: ipython3

    fom.visualize((U, U_proj, U - U_proj),
                  legend=('U', 'U_proj', 'error'),
                  separate_colorbars=True)

---

Using H1 inner product
======================

.. code-block:: ipython3

    G = trivial_basis[:10].gramian(product=fom.h1_0_semi_product)
    R = trivial_basis[:10].inner(U, product=fom.h1_0_semi_product)
    lambdas = np.linalg.solve(G, R)

    U_h1_proj = trivial_basis[:10].lincomb(lambdas)

---

Projection error computation
============================

.. code-block:: ipython3

    def compute_proj_errors(basis, V, product):
        G = basis.gramian(product=product)
        R = basis.inner(V, product=product)
        errors = []

        for N in range(len(basis) + 1):
            if N > 0:
                v = np.linalg.solve(G[:N, :N], R[:N, :])
            else:
                v = np.zeros((0, len(V)))

            V_proj = basis[:N].lincomb(v)
            errors.append(np.max((V - V_proj).norm(product)))

        return errors

---

Strong greedy algorithm
=======================

.. code-block:: ipython3

    def strong_greedy(U, product, N):
        basis = U.space.empty()

        for n in range(N):
            G = basis.gramian(product)
            R = basis.inner(U, product=product)

            lambdas = np.linalg.solve(G, R)
            U_proj = basis.lincomb(lambdas)

            errors = (U - U_proj).norm(product)

            basis.append(U[np.argmax(errors)])

        return basis

.. code-block:: ipython3

    greedy_basis = strong_greedy(training_data, fom.h1_0_product, 25)

---

Orthonormalization
==================

.. code-block:: ipython3

    from pymor.algorithms.gram_schmidt import gram_schmidt

    gram_schmidt(greedy_basis, product=fom.h1_0_semi_product, copy=False)
    gram_schmidt(trivial_basis, product=fom.h1_0_semi_product, copy=False)

Condition numbers:

.. code-block:: ipython3

    np.linalg.cond(trivial_basis.gramian(fom.h1_0_semi_product))

---

Orthogonal projection errors
============================

.. code-block:: ipython3

    def compute_proj_errors_orth_basis(basis, V, product):
        errors = []

        for N in range(len(basis) + 1):
            v = basis[:N].inner(V, product=product)
            V_proj = basis[:N].lincomb(v)
            errors.append(np.max((V - V_proj).norm(product)))

        return errors

---

Proper Orthogonal Decomposition (POD)
=====================================

Snapshot matrix:

.. math::

    A =
    \begin{bmatrix}
    \vdots & \vdots & \cdots & \vdots \\
    u(\mu_1) & u(\mu_2) & \cdots & u(\mu_K) \\
    \vdots & \vdots & \cdots & \vdots
    \end{bmatrix}

SVD:

.. math::

    A = U \Sigma V^T

POD computation:

.. code-block:: ipython3

    pod_basis, pod_singular_values = pod(
        training_data,
        product=fom.h1_0_semi_product,
        modes=25
    )

Check orthogonality:

.. code-block:: ipython3

    np.linalg.cond(pod_basis.gramian(fom.h1_0_semi_product))

---

Greedy vs POD comparison
========================

.. code-block:: ipython3

    pod_errors = compute_proj_errors_orth_basis(
        pod_basis, training_data, fom.h1_0_semi_product
    )

---

Weak greedy algorithm
=====================

.. math::

    \mathcal{E}(\mu) \approx \inf_{v \in V_N} \|u(\mu) - v\|

Greedy ROM construction:

.. code-block:: ipython3

    reductor = CoerciveRBReductor(
        fom,
        product=fom.h1_0_semi_product,
        coercivity_estimator=ExpressionParameterFunctional(
            'min(diffusion)', fom.parameters
        )
    )

.. code-block:: ipython3

    greedy_data = rb_greedy(
        fom,
        reductor,
        parameter_space.sample_randomly(1000),
        max_extensions=25
    )

Extract basis:

.. code-block:: ipython3

    weak_greedy_basis = reductor.bases['RB']

---

Validation
==========

.. code-block:: ipython3

    validation_set = parameter_space.sample_randomly(100)

    validation_data = fom.solution_space.empty()
    for mu in validation_set:
        validation_data.append(fom.solve(mu))

---