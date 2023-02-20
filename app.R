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

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            selectInput("game",
                        "Select Game",
                        c("Engage" = "engage",
                          "Gaiden" = "gaiden",
                          "Shadow Dragon" = "shadow-dragon-and-blade-of-light",
                          "Sacred Stones" = "the-sacred-stones"
                          ))
        ),

        # Show a plot of the generated distribution
        mainPanel(
            dataTableOutput('df')
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
    make_df <- reactive({
        readr::read_csv(file = paste("data/", input$game, "/char_growths.csv", sep = "")) %>%
            as_tibble()
    }) 
    
    output$df <- renderDataTable(make_df())
}

# Run the application 
shinyApp(ui = ui, server = server)
