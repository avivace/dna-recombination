# Scripts

### `preprocess.py`

Compute `Eq`, `cwc`, `MAC` and `MIC`.

### `problem.py`

The actual problem definition and solution using the GUROBI python wrapper.
Not included in `preprocess.py` because gurobipy isn't available for Python 3.5 on linux.

---

### `sparray.py`

Proof of concept and performance tests on 4-d arrays using the *sparray* dictionary-like implementation.

### `segment.py`

Compute the list of all the possibile segmentations (using all the given parts) of a string with the specified lenght.

Every segmentation is a list of segments.

Every segment is an array containing the start and end indexes
