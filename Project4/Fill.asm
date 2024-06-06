// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(BEGIN)
	// Initialize the memory address of the keyboard to 24576
	@24576
	D=A
	@keyboard
	M=D
// Check the keyboard status
(CHECK_KEYBOARD)
	@24575
	D=A
	@current
	M=D
	@keyboard
	A=M
	D=M
	// If a key is pressed, set the fill value to -1, or black in this case lol
	@fillvalue
	M=-1
	// If the keyboard status is not equal to zero,  jump to DRAW
	@DRAW
	D;JNE
	// If no key is pressed, set the fill value to 0, or white
	@fillvalue
	M=0
// Draw on the screen
(DRAW)
	@fillvalue
	D=M
	@current
	A=M
	M=D
	// The difference between the current address and the base address
	@current
	D=M
	@16384
	D=D-A
	// If the current address is less than or equal to the base address of the screen memory, jump back to CHECK_KEYBOARD
	@CHECK_KEYBOARD
	D;JLE
	// Decrement the current address, get cycled bozo (the program, not you, person reading this!)
	@current
	M=M-1
	@DRAW
	0;JMP