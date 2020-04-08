library(tidyverse)  
library(dplyr)    
library(tidyr)    
library(tibble)      
library(reshape2)   
library(stringr)   

library(plotly)
library(shiny)
library(rsconnect)

df <- read.csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv',
               header= TRUE, stringsAsFactors=TRUE)
 

function(input, output) {
  
  output$chart1 <- 
    renderPlotly({
      cod = input$cod
      pp1 <- df %>%
        filter(., Year == "2010" & ICD.Chapter == cod) %>%  
        arrange(desc(State), Crude.Rate)                    
      
      
      chart1 <- pp1 %>%
        plot_ly(x = ~pp1$Crude.Rate, y = pp1$State, type="bar", orientation="h") %>%
        layout(
          title= list(text=paste0(input$cod,"\ncause-based 2010 State Crude Mortality Rates"),
                      font=list(size = 10)),
          xaxis=list(title="Crude Rate"),
          yaxis=list(title="States",
                     categoryorder = "array",
                     categoryarray = rev(~State))       
        )
    })
}
 
