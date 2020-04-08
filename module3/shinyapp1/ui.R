library(plotly)
library(shiny)
library(rsconnect)

df <- read.csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv',
               header= TRUE, stringsAsFactors=TRUE)

fluidPage(
  titlePanel('Data 608, Module 3, Question 1. TJenkins.'),
  sidebarPanel(
    selectInput("cod", label = "Cause of Death:",
                choices = df$ICD.Chapter)
  ),
  mainPanel(
    plotlyOutput('chart1') 
  )
)
