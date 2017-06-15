## PrepareData.R
## Goal: prepare the dataset kiado or elado 
##          * clean the variables
##          * recode the variables 

PrepareData <- function(mydataset) {

  # Find duplicates in listing
  dupl <- duplicated(mydataset[,1])
  mydataset = subset(mydataset,!dupl)
  
  # Set case identifier
  rownames(mydataset) <- mydataset$listing
  mydataset <- dplyr::select(mydataset,-listing)
  
  # Find duplicates against features selected simultaneously
  feat <- c(2,3,4,7,10,15,16) # price, area, rooms, district, floor, lat, long
  dupl <- duplicated(mydataset[,feat])
  mydataset = subset(mydataset,!dupl)
  
  # Remove spurious data
  mydataset <- dplyr::filter(mydataset, district=='5. ker'|district=='6. ker'|district=='7. ker')
  
  # Clean the "nincs megadva"
  mydataset <- within(mydataset, {
    condition[condition == "nincs megadva"] <- NA
    lift[lift == "nincs megadva"] <- NA
    heating[heating == "nincs megadva"] <- NA
    view[view == "nincs megadva"] <- NA
    orient[orient == "nincs megadva"] <- NA
    floor[floor == "nincs megadva"] <- NA
    storeys[storeys == "nincs megadva"] <- NA
    parking[parking == "nincs megadva"] <- NA
    aircon[aircon == "nincs megadva"] <- NA
    ceiling[ceiling == "nincs megadva"] <- NA
    utility[utility == "nincs megadva"] <- NA
    bathtoil[bathtoil == "nincs megadva"] <- NA
    garcess[garcess == "nincs megadva"] <- NA
  })
  
  # Recode the categories of the factor variable "varos":
  mydataset <- within(mydataset, {
    # using simple assignments
    varos[varos == ""] <- NA
    varos[varos == "Terézváros"] <- NA
    varos[varos == "Erzsébetváros"] <- NA
  })
  
  # Reorder factor levels
  mydataset$floor <- factor(mydataset$floor, 
                            levels = c("szuterén", "földszint", "félemelet", "1", "2", "3",
                                       "4", "5", "6", "7", "8", "9", "10 felett"))
  
  # Drop unused levels
  mydataset <- droplevels(mydataset)
}
