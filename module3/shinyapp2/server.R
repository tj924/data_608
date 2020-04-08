library(tidyverse)  
library(dplyr)    
library(tidyr)    
library(tibble)      
library(reshape2)   
library(stringr)   

library(plotly)
library(shiny)
library(rsconnect)



function(input, output) {
  
  df <- 
    read.csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv')
 

  output$chart2 <- 
    renderPlotly({ 
      pp2 <- df %>%
        group_by(Year, ICD.Chapter) %>%                                      
        filter(ICD.Chapter == input$cod) %>%                                       
        mutate(US.Crude.Rate = round(
          sum(Deaths) / sum(Population) * 100000),3) %>%                        
        group_by(Year, ICD.Chapter, State)
      
      
      chart2 <- pp2 %>%
        as_tibble()  %>% 
        filter(., State == input$state) %>% 
        select(., Year, Crude.Rate, US.Crude.Rate) %>%
        plot_ly(x = ~Year, y = ~Crude.Rate, type='bar',
                text = ~Crude.Rate, textposition = 'auto',
                marker = list(color = 'rgb(158,202,225)'), 
                name = 'State') %>%                                 
        add_trace(x = ~Year, y = ~US.Crude.Rate, type='bar',        
                  text = ~US.Crude.Rate, textposition = 'auto',
                  marker = list(color = 'rgb(58,200,225)'), name = 'US')  %>%
        layout(
          title= list(text=paste0(input$cod,"\ncause-based State and US Crude Death Rates by Year\nfor ",input$state),
                      font=list(size = 10)),
          barmode = 'group',
          xaxis = list(title = "Year"),
          yaxis = list(title = "Crude Death Rate")) 
    }
    )
  }
