Describe how the system is personally meaningful to you (at least 1 paragraph).
Explain how working on it genuinely challenged you as a computer scientist (at least 1 paragraph).
How did you push yourself outside of your comfort zone?
Why was this an important challenge for you?
What are the next steps for you going forward?
Include a discussion of whether you believe your system is creative (and why or why not).
Make sure to credit your sources, including your colleagues if you sought their advice.

Youtube videos I used for help:





_____
# Start:
How to run Markov shapes game:
In order to run it, you can run the shapes.py file on your local machine (make sure to have imported pygame I still did not make an exectubale file).
## The purpose of the game:
    The purpose of the game is to draw something, or construct something visually fun with the shapes that are generated
    There are 4 shapes that are generated after 5 seconds at the buttom of the screen and the player can move them around the screen to construct something
    The sequence of shapes is decided by a markov chain where each shape has an equal chance of being generated after each shape is generated

## How to play The game:
    To move the shape around you use the arrow base keys
    A to rotate shape to left and D to rotate shape to the right
    SpaceBar to place the current shape even if you still have time on the timer (skip to next shape)

    After shapes run out, q to exit or simply close the window(you can close the window at any time)




# How this system is meaningful to me:
This is my first serious attempt at building a game and what I believe to be my first satisfactory completion of a project, so this system is very meaningful to me. I also do believe that I built something that can be built on. More shapes that are better for visual construction can be easily added, the game can be made customizable (player chooses the shape, the number of shapes, the duration etc). There are a lot of things that I could add onto this if I wanted to which is very exciting. What is most important is I believe I can add those things if I take my time with them

# Explain how it genuinely challenged me as Computer Scientist:

I had to do a lot of looking up, asking questions, thinking about the system, Looking at different resources. But most importantly, the biggest challenge was breaking it step by step and not trying to over-do it all at once. The git log should show a nice progression of what has been built from a rectangle moving around a white screen, to new rectangle spawning every 5 seconds while retaining the position of old ones, to generating new shapes and to including the new shape generation in the main() method

# How did I push myself out of my comfort zone:

This whole project was a push out of a comfort zone. I decided to take a shot at making a game within a limited time frame and with other responsibilities as a student(although the game is simple and I got a lot of help from online resources). But the most important thing was not panicking and setting short term goals for each work session. I am really happy I took it step by step and took my time and still finished with good time!

# Why was this important to me:

I switched to CS last fall and I really want to get a job for next year in tech so I can stay here for the 3 years I am allowed to as an international student. Since I started late, I feel like I am lagging behind in terms of where I should be in CS in terms of progess and demonstrable projects. This feels like a proof of my progress over the past year. Not necessary tech skills, but how do I tackle the uncertainty of a new challenge and go on it. Game development is fun and the feedback is very quick so it makes sense that the project feels smooth as a firs personal completed project. I feel a bit proud of myself for doing this!

# What are the next steps going forward:

We looked at Genetic algorithms today, and the shapes could be generated like that by genetic algorithms. Also the game can benefit from a menu, some sort of music, sound for each shape and stuff like that. a lot of stuff can be added. perhaps even make it available and playable online which could be its own fun challenge figuring out how. Also if I went more in depth maybe re-writing it in some other language or library that are more suited to games, perhaps introduce more modes such as a physics enable modes where the shapes will have their own rules for movement!

# Is the system creative?

For me yes, the system is creative as it relies on user input (movement) for it to create something yet the user is not free to do what they want. So both the system and the user are constrained with each other and push each other to be creative. Ultimately the user is the one who makes the system creative because without the user there wont be an art, but that is my interpretation of a creative system : No system is creative without a user feeling its creativity.


# Help I got building this (my sources):

I first checked this youtube video by Tech with Tim
https://www.youtube.com/watch?v=waY3LfJhQLY&t=1420s

It was realy helpful so I checked up his repisotiry as a reference for the building blocks of the game:
his repo: https://github.com/techwithtim/Python-Game-Dev-Intro

I also checked this video to draw different shapes (video by coding with Russ):
https://www.youtube.com/watch?v=YDP1Hk7uZFA

I checked this stack overflow to help with drawing text:
https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame

But most importantly I used a lot of CHATGPT to help me get going in the beginning, explain some concepts and debug certain things,
I also used Claude in the end to debug an issue as it is more powerful that CHATGPT
I did not ask the models to generate all the codes, but built my code, tested, fed it in for debugging, changed what they gave me back and ultimately built this

Special thanks to my roommates for testing it as well