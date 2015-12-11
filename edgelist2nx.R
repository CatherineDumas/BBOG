# run script like so:

# Rscript edgelist2nx.R edge_list_filename.txt

#filename = "edge_list_1000_bbog_change_followers.txt"
filename = tail(commandArgs(), 1)

x = readLines(filename)

y = gsub("\\(u'(.*)', u'(.*)'\\)", "\\1 \\2", x)

nodes = sapply(y, function(x) strsplit(x, split = " "))
unique_nodes = unique(unlist(nodes))
nodeIDs = setNames(0:(length(unique_nodes) - 1),
    unique_nodes)

id_mat = matrix(nodeIDs[unlist(nodes)], ncol = 2, byrow = T)

new_lines1 = apply(id_mat, 1,
    function(x) paste(x[1], x[2], "1 0", sep = " "))

new_lines2 = apply(id_mat, 1,
    function(x) paste(x[2], x[1], "1 0", sep = " "))

new_lines = c(new_lines1, new_lines2)
unew_lines = unique(new_lines)

nx_file = gsub("\\.[^.]*", ".nx", filename)
writeLines(unew_lines, nx_file)

dict_file = gsub("\\.[^.]*", ".dict", filename)
write.csv(nodeIDs, file = dict_file)
