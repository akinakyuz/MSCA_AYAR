# two simple ensemble methods: 
# 1. a majority rule based on predicted categories (majority)
# 2. a "soft vote" majority, based on (weighted) average of the different models predicted probabilites  


# predicts an observation class using a simple majority rule
#
# inputs: 
# row - array of models predictions for an observation
# output:
# majority rule prediction for observation
# note: in case of ties, a random decision will be made

majority <- function(row){
    
  unique_categories <- unique(row)
  print("unique")
  print(unique_categories)
  counts <- tabulate(match(row, unique_categories))
  print("counts")
  print(counts)
  majorities <- unique_categories[counts == max(counts)]
  print("majorities")
  print(majorities)
  num_m_labels <- length(majorities)
  if (num_m_labels == 1){
    return(majorities)
  } 
  else{
    random_num <- runif(1, max = num_m_labels)
    index <- round(random_num)
    return(majorities[index])
  }
}


# Predict an observation class using weights of the predicted probabilites (soft-vote majority rule)
#
# inputs 
# probs: matrix of class probabilites predictions for an observation. Rows are models, columns are categories
# weights: the importance given to each model. if not given by user, defualt is equal weights
# classes_labels: name of each category. if not given, use the col names of probs
# output:
# name of the majority rule prediction for the observation
# note: in case of ties, a random decision will be made

soft.majority <- function(probs , classes_labels, weights){
  
  if(missing(classes_labels)){
    classes_labels <- colnames(probs)
    if (is.null(colnames(row.as.matrix))){
      classes_labels <- paste("C", 1:dim(probs)[1], sep="")
    }
  } 
  if(missing(weights)){
    weights <- rep(1/dim(probs)[1] , dim(probs)[1])
  } 
  # calculate weighted probability for class 
  model_weighted <- probs * weights
  weigthed.prob <- apply(model_weighted , 2, sum)
  # finding labels with highest predicted probability
  soft.majorities.labels <- classes_labels[weigthed.prob == max(weigthed.prob)]
  num_m_labels <- length(soft.majorities.labels)
  if(num_m_labels == 1){ # if one category with highest probability, return it:
    return(soft.majorities.labels)
  }
  else{ # if multiple arg.max - choose between them in random:
    random_num <- runif(1, max = num_m_labels)
    index <- round(random_num)
    return(soft.majorities.labels[index])
  }
}


# Helper function to transform a row with probabilities of models to matrix and feed to soft.majority
#
# inputs:
# row: row of predicted probabilites of models for observation
# labels: names of predicted categories
# weights: optional, defualt is unifrom weights
# output:
# soft.majority prediction
process_row <- function(row, labels, weights){
  if(missing(weights)){
    weights <- rep(1/length(labels) , length(labels))
  } 
  probs <- matrix(row , ncol = length(labels), byrow = TRUE)
  return(soft.majority(probs , classes_labels = labels, weights = weights))
}


####################################
# some initial testing of both functions:


# testing majority:
obs1 <- c("red","red","red","red","blue","blue","blue","blue","green")
obs1
majority(obs1) # returns blue or red
obs2 <- c("red","red","red","red","blue","blue","blue","green","green")
obs2
majority(obs2) #  red



# testing soft majority:
row <- c(0.2,0.4,0.4,
         0.25,0.25,0.5,
         0.9,0.1,0)
labels <- c("c1", "c2", "c3")
process_row(row , labels)
# same prediction when calculating by hand
w <- rep(1/3, 3)
row.as.matrix <- matrix(row , nrow = 3, byrow = TRUE)
#row.as.matrix * w
apply(row.as.matrix * w , 2, sum)
# same prediction when using soft.majority with the matrix as input
soft.majority(row.as.matrix, classes_labels = labels)

# example of use with multiple predictions of 3 models:
model1.prob <- as.data.frame(matrix(c(0.2,0.3,0.5,
                                      0.25,0.25,0.5,
                                      0.9,0.1,0) , nrow = 3,, byrow = TRUE))

model2.prob <- as.data.frame(matrix(c(0.2,0.7,0.1,
                                      0.4,0.1,0.5,
                                      0.3,0.3,0.4) , nrow = 3,, byrow = TRUE))

model3.prob <- as.data.frame(matrix(c(0.1,0.5,0.4,
                                      0.25,0.35,0.4,
                                      0.2,0.6,0.2) , nrow = 3,, byrow = TRUE))

categories <- c("C1", "C2", "C3")
model.probs <- cbind(model1.prob , model2.prob , model3.prob)
# soft.majority for 3 models predictions:
apply(model.probs , 1, function(x)  process_row(x , categories))

# checking that same as prediction for each row:
process_row(as.matrix(model.probs[1,]), categories)
process_row(as.matrix(model.probs[2,]), categories)
process_row(as.matrix(model.probs[3,]), categories)

