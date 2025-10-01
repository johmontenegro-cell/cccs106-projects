# Lab 4 Report: Contact Book Application Enhancement

**Student Name:** John Renzzo C. Montenegro\
**Student ID:** 231002278 \
**Section:** 3A\
**Date:** October 1, 2025

## Git Configuration

### Repository Setup
- **GitHub Repository:** https://github.com/johmontenegro-cell/cccs106-projects
- **Local Repository:** ✅ Initialized and connected
- **Commit History:** 14 commits with descriptive messages

## Flet GUI Applications

### 1. main.py
- **Status:** ✅ Completed
- **Features:** Search / Filter Function, Theme Switching, and Database Integration 
- **UI Components:** Text, TextField, ElevatedButtons, ListView, ThemeMode, Switch, Column, Row, Divider
- **Error Handling:** Input Validation
- **Notes:** I had a hard time searching for the right components on Flet Docs which took most of my time to develop this.

### 2. database.py
- **Status:** ✅ Completed
- **Features:** sqlite3, Contact Manipulation (Initializing, Adding, Deleting, Updating, and Returning) 
- **Error Handling:** Database Connection Error
- **Notes:** I made the week4_labs folder outside of the cccs106-projects folder by mistake, which linked a database outside when I moved the week4_labs folder. I had to unlink the database by using the relative path of the new database to fix it.

### 3. app_logic.py
- **Status:** ✅ Completed
- **Features:** flet, Contact Display, Backend Functions of the main.py
- **Error Handling:** Deletion Confirmation
- **Notes:** This was the hardest part so far. I got confused editing the script mostly because of the overcrowding parentheses and brackets.

## Technical Skills Developed

### Contact Book Application Enhancement
- Input Validation
- Preventing Accidental Data Loss
- Real-time UI Updates via Search / Filter Functionality
- Theme Switching
- Modern Flet UI Application

## Challenges and Solutions

I almost did the same mistake as I did on the previous lab activity. The week4_labs 'spawned' outside the cccs106-projects folder, just like I said above, but I managed to fix it. Another problem was the numerous amount of parentheses and brackets. Luckily, there's a Quick Fix in VSCode that helps developers adjust and align the parenthesis together automatically, which is very efficacious especially when dealing with bigger projects.

## Learning Outcomes

I learned that we should double check our directories to see if we can access our work. I learned how to use ternary expressions to make the code clean and efficient, especially in developing a complex project.

## Future Enhancements

I think I could add a Sort By Function to list the contacts either alphabetically or how recently they were added.