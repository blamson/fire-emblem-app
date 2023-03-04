#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#
renv::activate()
library(shiny)
library(rvest)
library(dplyr)

# Define UI for application that draws a histogram
ui <- fluidPage(
    # Change Theme
    theme = shinythemes::shinytheme("darkly"),

    # Application title
    titlePanel("Fire Emblem Character Growths"),
    
    fluidRow(
        column(6,
               sidebarPanel(
                   selectInput(
                       "game",
                       "Select Game",
                       c("Engage" = "engage",
                         "Gaiden" = "gaiden",
                         "Shadow Dragon" = "shadow-dragon-and-blade-of-light",
                         "Sacred Stones" = "the-sacred-stones"
                       )
                   )
               ),
               uiOutput("char_select")
        )
    ),
    
    hr(),
    
    fluidRow(
        column(6,
            tabsetPanel(
                tabPanel("Character Growths", dataTableOutput('char_df')),
                tabPanel("Class Growths", dataTableOutput('class_df'))
            )       
        ),
        column(6,
            dataTableOutput('char_class_df')
        )
    )

)

# Define server logic required to draw a histogram
server <- function(input, output) {
    
    #This creates the character growth df
    char_df <- reactive({
        readr::read_csv(file = paste("data/", input$game, "/char_growths.csv", sep = "")) %>%
            as_tibble()
    }) 
    
    output$char_df <- renderDataTable(char_df(), options = list(pageLength=15))
    
    # This creates the class growth df
    class_df <- reactive({
        readr::read_csv(file = paste("data/", input$game, "/class_growths.csv", sep = "")) %>%
            as_tibble()
    }) 
    
    output$class_df <- renderDataTable(class_df(), options = list(pageLength=15))
    
    # This generates the list of characters that can be selected
    output$char_select <- renderUI({
        selectInput("char_name", "Select a character", choices = sort(unique(char_df()$Name)))
    })
    
    # This df is a specific characters growths added w/ class growths
    char_class_df <- reactive({
        char_row <- char_df() %>%
            filter(Name == input$char_name)
        
        df <- rbind(char_row, class_df()) %>%
            mutate(
                across(
                    # ignoring the first column, add the values of the first row to every row. 
                    -1, ~ . + .[1]
                )
            )
        
        # First row gets doubled due to above so we divide it by two here.
        df[1,-1] <- df[1,-1] / 2
        
        df
    })
    
    output$char_class_df <- renderDataTable(char_class_df(), options = list(pageLength=15))
    
}


# Run the application 
shinyApp(ui = ui, server = server)
