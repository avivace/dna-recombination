- *q* is the total quantity of MDS
- `=` is string equivalence
- `MIC[i,j]` (`MAC[i,j]`) is the substring starting at `i` and finishing at `j` (`i`,`j` being positions) of the MIC(MAC). Can be trivially defined using string concatenation and *MIC(i,c)* (*MAC(i,c)*).
- `Inverse(String)` is the Watson-Crick reverse complement of `String`

$MDS_{MICstart}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ starts at position } j \mbox{ in the MIC} \end{cases}$

$MDS_{MICend}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ ends at position } j \mbox{ in the MIC} \end{cases}$

$MDS_{MACstart}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ starts at position } j \mbox{ in the MAC} \end{cases}$

$MDS_{MACend}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ ends at position } j \mbox{ in the MAC} \end{cases}$

$Inv(i) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ is inverted in the MAC } \end{cases}$

$MAC(i,c) = \begin{cases} 0 \\ 1, & \mbox{if } c\mbox{ is the character at position } i \mbox{ in the MAC} \end{cases}$

$MIC(i,c) = \begin{cases} 0 \\ 1, & \mbox{if } c\mbox{ is the character at position } i \mbox{ in the MIC} \end{cases}$

$IES(i) = \begin{cases} 0 \\ 1, & \mbox{if } i \mbox{ is part of an IES:} \mathlarger{\sum_{j\leq i \leq k ; 1 \leq a \leq q} MDS_{MICstart}(a,j) + MDS_{MICend}(a,k) = 0} \end{cases}$

$MDS_{MICstart}(i,a) + MDS_{MICend}(i,b) + MDS_{MACstart}(i,c) + MDS_{MACend}(i,d) + IES(i) = 5 \Rightarrow \mbox{\code{ MIC[a,b] = Inverse(MAC[c,d])}}$

$MDS_{MICstart}(i,a) + MDS_{MICend}(i,b) + MDS_{MACstart}(i,c) + MDS_{MACend}(i,d) = 4, IES(i)=0 \Rightarrow \mbox{\code{ MIC[a,b] = MAC[c,d]}}$

$P_{start}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if } MDS_{MACstart}(i,j) = 1 \mbox{, Pointer } i \mbox{ starts at position } j \mbox{ in the MAC} \end{cases}$

$P_{end}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if } MDS_{MACend}(i-1,j) = 1 \mbox{, Pointer } i \mbox{ ends at position } j \mbox{ in the MAC} \end{cases}$

$Cov_{MIC}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ covers the position } j \mbox{ in the MIC} \end{cases}$

$Cov_{MIC}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if } \mathlarger{\sum_{l\leq i} MDS_{MICstart}(i,l) + \sum_{l\textless i}MDS_{MICend}(i,l) = 1} \end{cases}$

$Cov_{MAC}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if MDS } i\mbox{ covers the position } j \mbox{ in the MAC} \end{cases}$

$Cov_{MAC}(i,j) = \begin{cases} 0 \\ 1, & \mbox{if } \mathlarger{\sum_{l\leq i} MDS_{MACstart}(i,l) + \sum_{l\textless i}MDS_{MACend}(i,l) = 1} \end{cases}$