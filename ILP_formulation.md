## ILP formulation

- *q* is an upper bound of the total quantity of MDS (*lenght/2*)
- `=` is string equivalence
- `MIC[i,j]` (`MAC[i,j]`) is the substring starting at `i` and finishing at `j` (`i`,`j` being positions) of the MIC(MAC). Can be trivially defined using string concatenation and *MIC(i,c)* (*MAC(i,c)*).
- `reverse_complement(String)` is the Watson-Crick reverse complement of `String`
- Size of the Oxytricha Input genome: MIC is fragmented into ~750 000 MDSs, MAC into 300 000.
- Variables marked with $*$ are populated during the preprocessing phase.

$\linebreak$

$\mbox{objective function:} \qquad min \mathlarger{\sum_{i,j} MDS_{MACstart}(i,j)}$

$*Eq(i,j,h,l) = \begin{cases} 0 \\ 1, & \mbox{if } \code{MIC[i:j]} = \code{MAC[h:l]} \end{cases}$

$*cwc(i,j,h,l) = \begin{cases} 0 \\ 1, & \mbox{if \code{MIC[i:j]} is the reverse complement of \code{MAC[h:l]}} \end{cases}$

$*Possible_{MDSMAC}(i,a,b) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ can start at } a \mbox{ and finish at } b \mbox{ in the MAC} \end{cases}$

$*Possible_{MDSMIC}(i,a,b) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ can start at } a \mbox{ and finish at } b \mbox{ in the MIC} \end{cases}$

$Possible_{assignment}(a,b,c,d) = Eq(a,b,c,d)$

$MDS_{MICstart}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ starts at position } j \mbox{ in the MIC} \end{cases}$

$MDS_{MICend}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ ends at position } j \mbox{ in the MIC} \end{cases}$

$MDS_{MACstart}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ starts at position } j \mbox{ in the MAC} \end{cases}$

$MDS_{MACend}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ ends at position } j \mbox{ in the MAC} \end{cases}$

$Inv(i) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ is inverted in the MAC } \end{cases}$

$*MAC(i,c) = \begin{cases} 0 \\ 1, & \mbox{if } c\mbox{ is the character at position } i \mbox{ in the MAC} \end{cases}$

$*MIC(i,c) = \begin{cases} 0 \\ 1, & \mbox{if } c\mbox{ is the character at position } i \mbox{ in the MIC} \end{cases}$

$IES(i) = \begin{cases} 0 \\ 1, & \mbox{if } i \mbox{ is part of an IES:} \mathlarger{\sum_{j\leq i \leq k ; 1 \leq a \leq q} MDS_{MICstart}(a,j) + MDS_{MICend}(a,k) = 0} \end{cases}$

$MDS_{MICstart}(i,a) + MDS_{MICend}(i,b) + MDS_{MACstart}(i,c) + MDS_{MACend}(i,d) + Inv(i) - 5 cwc(a,b,c,d) = 0$

$MDS_{MICstart}(i,a) + MDS_{MICend}(i,b) + MDS_{MACstart}(i,c) + MDS_{MACend}(i,d) - 4 Eq(a,b,c,d) = Inv(i)$

$\mathlarger{\sum_{j} MDS_{MICstart}(i,j)\leq 1}$

$\mathlarger{\sum_{j} MDS_{MICend}(i,j) = \sum_{j} MDS_{MICstart}(i,j)}$

$P_{start}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if } MDS_{MACstart}(i,j) = 1 \mbox{, Pointer } i \mbox{ starts at position } j \mbox{ in the MAC} \end{cases}$

$P_{end}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if } MDS_{MACend}(i-1,j) = 1 \mbox{, Pointer } i \mbox{ ends at position } j \mbox{ in the MAC} \end{cases}$

$Cov_{MIC}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ covers the position } j \mbox{ in the MIC} \end{cases}$

$Cov_{MAC}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ covers the position } j \mbox{ in the MAC} \end{cases}$

$Cov_{MIC}(i,j) \geq MDS_{MICstart}(i,j)$

$Cov_{MAC}(i,j) \geq MDS_{MACstart}(i,j)$

$Cov_{MIC}(i,j) = 3 - (cov_{MIC}(i,j-1) + cov_{MAC}(i,j+1) + MDS_{MICstart}(i,j) + MDS_{MICend}(i,j))$

$Cov_{MAC}(i,j) = 3 - (cov_{MAC}(i,j-1) + cov_{MAC}(i,j+1) + MDS_{MACstart}(i,j) + MDS_{MACend}(i,j))$

$\mathlarger{\sum_{l\leq j} MDS_{MICstart}(i,l) + \sum_{l\geq j}MDS_{MICend}(i,l) - Cov_{MIC}(i,j) = 2}$

$\mathlarger{\sum_{l\leq j} MDS_{MACstart}(i,l) + \sum_{l\geq j}MDS_{MACend}(i,l) - Cov_{MAC}(i,j) = 2}$

$Cov_{MIC}(i,-1) = 0$

$Cov_{MAC}(i,-1) = 0$

$Cov_{MIC}(i,j) = Cov_{MIC}(i,j-1) - MDS_{MICend}(i,j-1) + MDS_{MICstart}(i,j)$

$Cov_{MAC}(i,j) = Cov_{MAC}(i,j-1) - MDS_{MACend}(i,j-1) + MDS_{MACstart}(i,j)$