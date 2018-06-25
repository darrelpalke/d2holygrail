# d2holygrail
Tracker for D2 Holy Grail

This is a simple python script I wrote to try and help with my tracking of the D2 Holy Grail quest, the quest to find all the items in game.  This is by no means perfect, but it's simple enough for me.  Ideal next steps would be a GUI or a website version.  This was a bit more straightforward for me to use over the Google drive spreadsheet trackers.  The ones that existed were missing a lot of things I wanted to query.
The script will manage a .txt database called d2_items.txt.  It will create one from the blank data on first run.

I'm using D2 1.13c and PlugY 10.0.  One of the key features of the script is to tell me where to place each item in the PlugY stash. 
I've set it up in a specific way and there is a parameter at the top called 'startPage' that will tell it where to start. I like to put gems, charms, and other misc items early on in my stash, thus the 40 pages left for space.

On the placement, it loosely follow these rules:
- I leave room for both the non-eth and eth versions.  If an item has no eth version or is always eth, then I leave room for one spot.
- Misc group gets a single page per subgroup. (There aren't that many rings/amulets/etc)
- Sets are 2 sets per page. (No set is larger than this)
- New page at the start of a new subgroup otherwise.  Skip 10 pages for a new group.
- Per subgroup, I take the largest height value for an item and use that to choose how many rows of items.  This works good for armors and things where the whole group is the same size. Bad for shields, axes, etc.
- When placing items, if I don't have room for the eth/non-eth version on the same row, I skip to a new row.

Enter a 'h' character to print the help and a 'q' to quit.  

There are a number of query functions:
- Listing all the groups of items (Misc, Weapons, Armors, Sets)
- Listing all the subgroups within each group
- Listing all the items within a subgroups
- Listing all items that have been found (regular and ethereal versions)
- Listing all items within a subgroup (regular and ethereal versions)
- Print the long-form data for a particular item.

There are a number of ways to interact with the database.
- Mark items as found or unfound (regular and ethereal versions)
- Update the comment field for an item

There are a few quirks.  Mainly, when entering the names of a group or object, it must be in a single string of characters.  Omit spaces, apostrophes, dashes.  This is to allow me to be able to have additional parameters past that point (such as a comment to add or a keyword to trigger an unfound). It also uses regular expressions so you only have to type a uniquely identifying string.

