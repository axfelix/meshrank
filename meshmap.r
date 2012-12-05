meshrank <- read.csv("mcsneuro_mesh.csv", sep=",")
row.names(meshrank) <- meshrank$name
meshrank <- meshrank[1:length(row.names(meshrank)),2:length(names(meshrank))]

meshrank_ranked <- sort(colSums(meshrank), decreasing = TRUE)[4:100]
meshrank <- subset(meshrank, select = names(meshrank_ranked))

meshrank_matrix <- data.matrix(meshrank)
meshrank_heatmap <- heatmap(meshrank_matrix, Rowv=NA, Colv=NA, col=cm.colors(256), scale="column", margins=c(12,0))