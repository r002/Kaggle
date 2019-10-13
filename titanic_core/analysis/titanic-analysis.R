## Perform analysis to figure out if families tended to survive entirely intact.
## How many family members died on average per family?

## Extract all of the name of surnames who had family members onboard (sibsp>0 | parch>0)

## Do analysis to see how many passengers who shared the same ticket # shared the same fate?  How many didn't?

share_fate <- function()
{
    # Build a df with ticket numbers that appear more than once
    df_train <- read.csv("train.csv")
    
    tt <-table(df$Ticket)
    
    # Get all ticket numbers representing three or more passengers
    names(tt[tt>2])
    
    df2 <- subset(data_train, Ticket %in% names(tt[tt > 2]))
}