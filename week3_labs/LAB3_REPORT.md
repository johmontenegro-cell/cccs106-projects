# Lab 2 Report: Git Version Control and Flet GUI Development

**Student Name:** John Renzzo C. Montenegro
**Student ID:** 231002278 \
**Section:** 3A\
**Date:** September 3, 2025

## Git Configuration

### Repository Setup
- **GitHub Repository:** https://github.com/johmontenegro-cell/cccs106-projects
- **Local Repository:** ✅ Initialized and connected
- **Commit History:** 4 commits with descriptive messages

### Git Skills Demonstrated
- ✅ Repository initialization and configuration
- ✅ Adding, committing, and pushing changes
- ✅ Branch creation and merging
- ✅ Remote repository management

## Flet GUI Applications

### 1. hello_flet.py
- **Status:** ✅ Completed
- **Features:** Interactive greeting, student info display, dialog boxes
- **UI Components:** Text, TextField, Buttons, Dialog, Containers
- **Notes:** Some parts of the code resulted in an error because of Pyright, which made me quick fix it with pyright: ignore[reportAttributeAccessIssue].

### 2. personal_info_gui.py
- **Status:** ✅ Completed
- **Features:** Form inputs, dropdowns, radio buttons, profile generation
- **UI Components:** TextField, Dropdown, RadioGroup, Containers, Scrolling
- **Error Handling:** Input validation and user feedback
- **Notes:** The colors of the flet GUI depends on the desktops theme, which I find very unsettling since some themes make it hard to read the texts in the GUI.

## Technical Skills Developed

### Git Version Control
- Understanding of repository concepts
- Basic Git workflow (add, commit, push)
- Branch management and merging
- Remote repository collaboration

### Flet GUI Development
- Flet 0.28.3 syntax and components
- Page configuration and layout management
- Event handling and user interaction
- Modern UI design principles

## Challenges and Solutions

I encountered errors when I was setting up .gitignore which resulted into the whole virtual environment and my previous lab1 zip to be pushed and committed to the repository. I managed to fix it by deleting it on the repository and adding cccs106_env_montenegro/ and .zip to the .gitignore file.

## Learning Outcomes

I learned that in managing version control, we should always be careful of the files we are trying to access or modify before committing. This help us avoid problems that might affect future complex systems.

## Screenshots
### Git Repository
**Github Commit**
![github commit](lab2_screenshots\github_commit.jpg)

**Local Commit**
![local commit](lab2_screenshots\local_commit.jpg)

### GUI Applications
**Hello Flet GUI**
![hello flet](lab2_screenshots\hello_flet_gui.jpg)

**Personal Info GUI**
![personal info](lab2_screenshots\personal_info_gui.jpg)

## Future Enhancements

I have a few more ideas for the UI / UX. I think the colors should be edited and make it not based on the device's theme.