# load data wrangling libraries
library(dplyr)
library(tidyr)

# load ML libraries
library(rpart)          # implements CART (regression trees)
library(rpart.plot)
library(e1071)          # skewness
library(kernlab)        # support vector machine 
library(caret)

# load graphics libraries
library(ggplot2)
library(RColorBrewer)
library(ggthemes) 
library(plotly)
library(gridExtra)      # show several ggplot objects in a grid 
library(corrgram)

# load optimization libraries
library(ROI)
library(mlrMBO)
library(smoof)

# other libraries
#library(corrgram)
#library("vcd")
#library(tree)          # great visualization for regression trees in 2D
#library(pROC)	          # plot the ROC curves