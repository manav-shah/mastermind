# Mastermind
This project is an attempt to recreate the board game Mastermind using Python and pygame.

![Mastermind](https://github.com/manav-shah/mastermind/blob/master/assets/mastermind.png)

# How to play 
* The game will generate a random 4 color code from the available colors (Duplicates are allowed)
* You must try to guess the code within 10 tries. After each submitted guess, you will receive a feedback response which you can use to narrow down
 your choices
* To make a guess, click on the highest colored row to toggle their colours. There are 6 possible colors (Red,Blue,Yellow,Green,Pink,Brown). After toggling the colors, click on the green submit button.
* You will receive a response feedback of white and black dots. There can be 0-4 dots. 
* A white dot indicates that one of the colors in your guess is the correct color and in the correct position. A black dot indicates one of the colors in your guesses is correct, but in the wrong position. (Note: The order of the white/black dots is not significant)
* If a white dot was awarded for one of the colors in your guess, it can't be awarded a black dot if that color appears again in the code.
Ex: If you guess \[RED BLUE BLUE BLUE] and the code is \[RED RED GREEN GREEN], you will be given one white dot for the first red in the code. But you won't receive a black dot for the second red in the code, since your guess doesn't have a second red.

Refer to license.txt for license.
