EvaluateModel <- function(y, yhat, verbose = TRUE)

# Evaluates the quality of a regression fit
# Args:  
#   y:        vector of observed outcomes (testing set)
#   yhat:     vector of predicted outcomes (testing set)
#   verbose:  does not really make any difference...
#  
# Returns:
#   pm: performance measure  
#   p1: plot 1
#   p2: plot 2  

{
  # compute performance measure
  pm <- caret::postResample(obs = y, pred = yhat)

  df <- data.frame(y,yhat)
  # Plot residuals vs. observed values
  print(ggplot2::ggplot(data = df,
                        aes(x = (yhat-y)/y*100, y = yhat)) +
    geom_point() +
    ylab("Residual = (yhat-y)/y * 100") +
    xlab("Observed value y"))
  
  # Plot predicted values vs. observed values
    print(ggplot2::ggplot(data=df,
                          aes(x = y, y = yhat)) +
    geom_point() +
    ylab("Predicted value: yhat") +
    xlab("Observed value: y") +
    geom_abline(intercept = 0, slope = 1, col = "red", linetype = 2))
  
  
  return(pm)
}


# ideas:
#   # Calculate error on testing set
#   testing.0 <- dplyr::mutate(testing.0, error = price.pred - price)
# errTest <- testing.0$error/testing.0$price*100
# summary(errTest)
# 
# mean(errTest, na.rm=TRUE)
# sd(errTest, na.rm=TRUE) 
# hist(errTest, breaks = pretty(-300:300, n=100))

