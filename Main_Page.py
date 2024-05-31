import streamlit as st

st.set_page_config(
    page_title="Fire Emblem Dashboard",
    page_icon="🗡️"
)
# st.image("images/fire_emblem_logo.jpeg")
st.sidebar.success("Select a Page above!")
# with open("README.md") as f:
#     main_blurb = f.read()

# st.markdown(main_blurb)

st.markdown(
    """
    # Welcome to my Fire Emblem Application
    
    This project was designed to be a quick and useful reference for much of the data a player will want access to.
    The Fire Emblem franchise is one built around data, stats and probability. 
    The fandom has created hundreds of tables compiling this information across a multitude of games and that's amazing!
    However, when you're checking these tables mid-game you may end up with dozens of open tabs and no quick way
    to access what you need. 
    
    My goal here is to provide a tool that allows you to easily navigate most of that information in one place.
    
    - Simply checking character stats?
    - Comparing a couple characters bases and growths to decide who to use? 
    - Seeing where a character falls amongst the entire roster? 
    
    I want to provide that and more. 
    
    ⬅️ Use the sidebar on the left to navigate the various tools I've built out.
    
    ## The Data
    
    All of the data I'm using has been collected from the wonderful [Serenes Forest](https://serenesforest.net/).
    This application wouldn't be possible without the work of the community. Without data I can't do anything.
    
    Of course this application is very much under construction but it's one I intend to improve over time! 
    
    ## Features
    
    | Feature | Status |
    |---|---|
    | Character Comparison | ✅|
    | Full Roster Stat Analysis | ✅|
    | General Stat Tables | 🚧️|
    | True Hit Calculator | 🚧️|
    | Combat Outcome Calculator | 🚧️|
    
    This is a basic overview of what I want to include, I have so many ideas beyond this but gotta start somewhere!
    
    ## Games
    
    Note that there's a lot of tables for these games so I won't have all the games right off the bat.
    I have to scrape the data, clean it and do even more work to ensure it functions properly with these features.
    Whats more is that as the games get more complex the data changes and the math does too! So give me time to 
    slowly expand the scope of this project.
    
    Currently I only plan to get all the GBA games working. Once I develop those features in full I'll start
    to look at which games would be easiest for me to include and hopefully someday I'll be able to have all of the games!
    I'm starting with Fire Emblem 8 as it has the simplest data for me to work with.
    
    |Game|Status|
    |---|---|
    |FE6 - Binding Blade|🚧️|
    |FE7 - Blazing Sword|🚧️|
    |FE8 - Sacred Stones|✅|
    """
)