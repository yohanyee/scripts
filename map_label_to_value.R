#!/usr/bin/Rscript
library(RMINC)

args <- commandArgs(trailingOnly = TRUE)
in_labels <- args[1]  # Label volume
in_defs <- args[2]    # Label definitions file
in_mapping <- args[3] # File consisting of two columns containing label name and value
outfile <- args[4]    # Output volume

# Read input files
labels <- output <- mincGetVolume(in_labels)
defs <- read.csv(in_defs)
mapping <- read.csv(in_mapping)


# write.csv writes a csv file with row numbers by default. Remove this if this is the case
if (dim(mapping)[2]==3 & colnames(mapping)[1]=="X") {
  mapping <- mapping[,2:3]
}
colnames(mapping) <- c("label", "mapping")

# Set output volume to zero
output[] <- 0

# Loop over mapping labels
for (i in 1:dim(mapping)[1]) {
  mlabel <- toString(mapping$label[i])
  cat(paste("Working on label: ", mlabel, " ... ", sep=""))
  
  # Get labels IDs associated with mapping label name
  if (startsWith(mlabel, "right ")) {
    ml <- gsub("right ", "", mlabel)
    ml_id <- defs$right.label[which(defs$Structure==ml)]
  } else if (startsWith(mlabel, "left ")) {
    ml <- gsub("left ", "", mlabel)
    ml_id <- defs$left.label[which(defs$Structure==ml)]
  } else {
    ml_id <- c(defs$right.label[which(defs$Structure==mlabel)], defs$left.label[which(defs$Structure==mlabel)])
  }
  
  # Replace mapping labels with mapping value
  voxels_to_replace <- which(labels[] %in% ml_id)
  output[voxels_to_replace] <- mapping$mapping[i]
  cat(paste("Replaced ", length(voxels_to_replace), " voxels.\n", sep=""))
}

# Write volume
mincWriteVolume(output, output.filename = outfile)