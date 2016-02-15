library(ggplot2)
library(reshape2)

data = read.csv("../results.csv")
data = data[data$maxRunLength > 20,]
ggplot(data = data, aes(x=maxRunLength, y=numBits, colour=codebook)) +
  geom_line() +
  labs(x="Maximum run length (bits)", y="Size of compressed file (bits)", colour="Codebook")

subset(data, numBits == min(numBits))
