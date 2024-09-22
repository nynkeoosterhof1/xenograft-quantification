# xenograft-quantification

Citation: 
References
Stringer, C., Wang, T., Michaelos, M., & Pachitariu, M. (2021). Cellpose: a generalist algorithm for cellular segmentation. Nature methods, 18(1), 100-106
Casas Gimeno, G., Dvorianinova, E., Lembke, C-S., Dijkstra ESC., Abbas, H., Liu, Y., Paridaen, JTML. (2023). A quantitative characterization of early neuron generation in the developing zebrafish telencephalon. Developmental neurobiology. 83. 10.1002/dneu.22926.

# Introduction
Zebrafish cancer xenografts, the transplantation of human cells to the zebrafish organism, have gained more and more importance in the recent years, mainly based on the organisms’ advantages including easy visualization of cancer cells in vivo. Quantification of these transplanted cells in 3D can be difficult due to the number of cells in a densely packed tissue. Manually counting cells is time-intense and can be unreliable due to the difficulty of keeping track of cells throughout an image stack. Further, the number of manually counted cells can vary, dependent on the individual counting. To make quantification of cancer cell xenografts in zebrafish more reliable and unbiased, the following python code makes use of the Cellpose algorithm which uses segmentation of nuclei in 3D images. 
The manual on how to use this python code is provided in the following publication (doi: ). In short, the code used it is based on the cell counter introduced in a previous publication (doi.org/10.1002/dneu.22926) and provides functions to preprocess images to equal image intensity throughout the stack as well as counting and segmentation of the cells using Cellpose algorithm. 
