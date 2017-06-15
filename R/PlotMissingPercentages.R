PlotMissingPercentages <- function(frame, color, cutoff_condition)
  
  # Plot a bar chart of the percentage of missing value for each variable, with threshold for color
  # Args:  
  #   frame:
  #   color:
  #   cutoff_condition
  # Returns:
  #     
  # Reference: https://www.quora.com/What-are-some-R-hacks-that-not-many-people-know-about/answer/Sean-McClure-3?srid=HHsE

{
  pMiss <- function(x){sum(is.na(x))/length(x)*100}
  
  res <- apply(frame,2,pMiss)
  par(mar=c(2,3,5,2))
  mp <- barplot(res, main='missing data by percentage\n', ylab='percentage missing (%)', col=ifelse(res >= cutoff_condition, color,'steelblue'), xaxt='n')
  text(mp, par("usr")[3], labels = names(res), srt = 45, adj = c(1.1,1.1), xpd = TRUE, cex=.7)
}