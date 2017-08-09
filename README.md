# ILP approaches on the DNA recombination problem

## Timeline

#### May, 22
Preliminary explanations.

#### July, 3
Formal stage start. Problem definition.

#### July, 6
ILP: first constraints and properties.

#### July, 27
Review of the ILP formulation: corrections, objective function (min MDSs quantity), functions definitions (equivalence, inverse, MIC/MAC substring notation). LP solver: *GUROBI*.

Preprocessing script:

- Generate all possibile MDSs annotations
- Compute values of some variables
- Python or Ruby

## Resources

- *DNA recombination through assembly graphs* - Angela Angeleska, Nataša Jonoska, Masahico Saito
- `mds ies db`: *a database of ciliate genome rearrangements* - Jonathan Burns, Denys Kukushkin, Kelsi Lindblad, Xiao Chen, Natasa Jonoska and Laura F. Landweber
- [MDS and IES annotation algorithm (Python) used in `mds ies db`](http://knot.math.usf.edu/midas/algorithm.html)
    - [BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi) - *Basic Local Alignment Search Tool*

- *Programmed genome rearrangements in the ciliate Oxytricha* - V.Talya Yerlici, Laura F. Landweber
- *RNA-guided DNA assembly* - Angela Angeleska, Natasa Jonoska
- [Gusfield ILP tutorial](http://csiflabs.cs.ucdavis.edu/~gusfield/tutorial.pdf)