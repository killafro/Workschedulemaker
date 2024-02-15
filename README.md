# The Work schedule maker

### Video Demo: https://youtu.be/kOisgbkrd1A

## Description:

The work schedule maker is a tool for the person in charge of scheduling. By using a CSV file to input the shifts that need to be filled and asking the user for the employees and their preferred off-days, it creates a schedule. If possible, take into account the requested time off. If not possible, there is the option to distribute shifts without taking into account the requested off-days.

## Intro

"At my current job, working as a caretaker for people with mental disabilities, I am also responsible for creating and managing the schedule. It can be tough to fairly distribute shifts, taking into account all the wishes of my colleagues. I actually looked for ways to automate the process but could only find paid sites or programs. This course gave me the opportunity to try and create a system myself. I now do realize it is a lot harder than I expected, but nonetheless, I'm happy with the result."

###  All Files
- `project.py` -> the main project file
- `README.md` -> this file, an explanation of the whole project
- `requirements.txt` -> the used downloaded libraries
- `shifts.csv` -> a CSV file with the shifts at my current job, was used to test the program.
- `shifts1.csv` -> another test file with made up shifts
- `test_project.py` -> file where different functions get tested.

## How Does It Work?
Let's go over all the steps the program takes.

**Step 1:** Through a command-line argument, we specify the input file for the program. This file should be a CSV file with the following layout: "shift, start, end, days." Here,'shift' denotes the shift name, and 'start' and 'end' represent the start and end times of the shifts, respectively. The 'days' field indicates the days of the week the shift needs to be worked. These days are represented by corresponding numbers, without any spaces or commas. For example, if the shift is scheduled for all weekdays (Monday to Friday), it should be written as '12345' in the file. If it's for Saturday and Sunday, it should be '67'.

**Step 2:** The program displays the table, highlighting shifts that need coverage with a '+' symbol.

**Step 3:** The program prompts the user to input the minimum number of required employees.

**Step 4:** The program prompts the user to enter the names of workers and the days when they are unavailable to work. The information is stored in a list of dictionaries, where each dictionary represents a worker with their name and a list of unavailable days.

**Step 5:** The program verifies whether the user has input the minimum required number of workers.

**Step 6:** Clear the terminal window.

**Step 7:** The program attempts to assign shifts to employees based on their preferences. If there are not enough workers to cover all shifts, the user is prompted to generate a schedule without considering employee preferences.

**Step 8:** If the program was not able to create a schedule with all the information provided, it shows a message. If it succeeds, the table with the newly created schedule is shown.

**Step 9:** The user gets asked if they want to save the schedule to a file they can name themselves.

### Challenges
During the creation, I ran into a couple of challenges:
- It took me a while before I found a good way to store all the inputted information. How do I store the sifts, workers and requested off-days in a way they are easily accessible and usable in all kind of different scenarios.

- The second big challenge was finding a way to create the tables in such a way that only the shifts that needed to be filled got filled. This went hand in hand with my first challenge. I needed to be able to store the data correctly before I could create the tables.

- Creating the data to fill the shifts was the third major hurdle. Randomly but evenly distributing shifts was not an easy task for me. It took a lot of googling, trial and error before I got even remotely comfortable with, what in my eyes was a complex problem.

- Keeping a bird's eye view: Since the project kept growing and changing, it got tougher and tougher to keep an eye on and remember everything that was going on. Especially after focusing a while on one problem, I started to forget the logic of the other functions. This forced me to start using notes (a lot). I looked for a way that's conventional but also easy for me. After creating notes and discovering a way to fold functions, it became a lot easier to navigate and keep track of everything that was going on.

- Checking: Perhaps the toughest challenge. I am creating randomly generated schedules. Factoring in preferred off-days by workers. But how do you check if random is actually random? I firstly added some print statements to print out the requested off-days, just for convenience. Then I tested over and over again. The same schedule and requests, checking if there are any patterns or mistakes. The different schedules, different workers, and different requests. At a certain point, I noticed the shifts were not distributed evenly, after fixing that, the off-days were not factored in anymore. It kept going like that for a while. Until I reached the point where I couldn't find any mistakes anymore.

## Conclusion

This was definitely a challenge. I started out optimistic but soon realized that I was going to need a lot more time than initially thought. I deleted more code than I kept, experienced multiple headaches, but these instances taught me how important comments are.

I kept adding steps and functions, breaking them down into smaller, more understandable units. Along the way, I introduced ideas, sometimes making things needlessly more complex. I learned to cut my losses but also to persist. Most of all, I had fun and am becoming more certain that there might be some kind of future in CS for me.
