library(dplyr)
library(rvest)

serenes_to_df <- function(game = "engage", char_or_class = "characters") {
    link <- paste("https://serenesforest.net/", game, "/", char_or_class, "/", "growth-rates", sep = "")
    html <- rvest::read_html(link)
    
    df <- 
        html %>%
        html_nodes("table") %>%
        html_table()

    print(df)
    
    df <-
        df[[1]] %>%
        mutate(
            across(!Name, as.numeric)
        ) 

    return(df)
}

games <- c("shadow-dragon-and-blade-of-light", "gaiden", "engage", "the-sacred-stones")

for (game in games) {
    df <- serenes_to_df(game = game)
    path <- paste("data/", game, "/", sep="")
    if (!file.exists(path)){
        dir.create(path)
    }
    write.csv(df, file = paste(path, "char_growths.csv", sep=""), row.names = FALSE)
}
# write.csv(engage_character_df, file = "data/engage/char_growths.csv", row.names = FALSE)