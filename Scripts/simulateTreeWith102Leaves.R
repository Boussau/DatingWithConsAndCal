library(TreeSim)
#library(BioGeoBEARS)


n<-102
lambda <- 0.9 #0.3
mu <- 0.15  #0.09  #0.02
frac <-1.0
numbsim<-1

outputPlots="Tree"

# Each extant species is included in final tree with probability frac
# (the tree has n species AFTER sampling):

#for (i in 1:10) {
i=""
tre<-sim.bd.taxa(n,numbsim,lambda,mu,frac,complete=TRUE,stochsampling=TRUE)

numTips <- length(tre[[1]]$tip.label)
tre[[1]]$node.label<-(numTips:(numTips+tre[[1]]$Nnode))

extant<-drop.extinct(tre[[1]])

extantLeaves <- setdiff( tre[[1]]$tip.label, is.extinct(tre[[1]]))
extinct <- drop.tip(tre[[1]], extantLeaves)




#outputting the trees
write.tree(tre[[1]], file = paste("completeTree", as.character(i), ".dnd", sep=""))
if (extant$Nnode >=1) {
  print("EXTANT:")
  print(extant)
  write.tree(extant, file = paste("extantTree", as.character(i), ".dnd", sep=""))
} else {
  print ("BIG PROBLEM: EXTANT TREE WITH NO TIP !")
  exit(0)
}

#if (extinct$Nnode >=1) {
#  print("EXTINCT: ")
#  print(extinct)
#  write.tree(extinct, file = paste("extinctTree", as.character(i), ".dnd", sep=""))
#}

# plotting the trees
pdf(file=paste(outputPlots, as.character(i), ".pdf", sep=""))
plot(tre[[1]], show.tip.label=FALSE)
if (extant$Nnode >=1) {
  plot(extant, show.tip.label=FALSE)
}
#if (extinct$Nnode >=1) {
#  plot(extinct, show.tip.label=FALSE)
#}
dev.off()


#}
