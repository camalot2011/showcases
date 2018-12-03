

library(shiny)

# Define UI for application that return picked stock symbols
shinyUI(fluidPage(
  
  # Application title
  titlePanel("Stock picking App"),
  
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel(
       
       # Input the reference date (or end date) for the calculations
       dateInput(inputId = "reference_date",
                 label = "Please choose the end date",
                 min = Sys.Date()-344,
                 max = Sys.Date(),
                 value = Sys.Date()),
       # Input the price-fluctuation range between 0 and 1 with default at 0.05
       numericInput(inputId = "price_fluctuation",
                    label = "Please set price fluctuation range (0.00-1.00):",
                    min = 0,
                    max = 1,
                    step = 0.01,
                    value = 0.05),
       # Input the price drop ratio between 0 and 1 with default at 0.1
       numericInput(inputId = "price_drop_ratio",
                    label = "Please set price drop ratio (0.00-1.00)",
                    min = 0,
                    max = 1,
                    step = 0.01, 
                    value = 0.1),
       # Input the time period (in days) to look for price drop
       numericInput(inputId = "time_span",
                    label = "Please set days to look for price drop",
                    min = 0,
                    max = 180,
                    step = 1, 
                    value = 20),
       # Put up an action button
       actionButton(inputId = "update",
                    label = "Update View"),
       # Select symbol
       textInput(inputId = "symbol",
                 label = "Please enter the symbol of interest:",
                 value = "AAME"),
       # Select data frequency
       selectInput(inputId = "data",
                   label = "Please choose data frequency:",
                   c("Daily" = "daily",
                     "Weekly" = "weekly"),
                  selected = "Daily"),
       # Select daterange
       dateRangeInput(inputId = "daterange",
                      label = "Date range:",
                      start = Sys.Date()-344,
                      end = Sys.Date(),
                      min = Sys.Date()-365,
                      max = Sys.Date(),
                      format = "yyyy-mm-dd")
       
    ),
    # Show a table with the picked stock symbols
    mainPanel(
       
       h3("Stock picked:"),
       tableOutput("view"),
       h3("Stock of interest:"),
       tableOutput("ticker"),
       plotOutput("Bplot")
    )
  )
))
