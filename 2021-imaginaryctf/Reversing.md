# Reversing Challenges

Writeups in this file only give a brief description. 
### Hidden
We are given a PhotoShop Image. I tried opening it with `gimp` and `krita` both without success. I don't know why. But apparently `convert` can read it, so convert it to native krita format:
```convert file.psd file.kra```  (other files supporting layers would probably work as well)
Now we can open it in krita an see there is an Image Layer with a flag name.


### Stings
The program does some computation to build the flag inside memory. You can use `gdb` to stop at the position where the flag is compared and examin the memory there. Just notice that all letters are off-by-one, so it starts with `jdug` instead of `ictf` (but still looks quite like a flag already)

### Normal
This is a Verilog file, so basically a description how to wire up some gates. I have no idea about Verilog, but with some intuition, I could guess, how to understand the syntax (otherwise, google will probably help). So we have some input wires (`flag`), a wire plan for some `nor` gates, and in the end, the output wires (`wrong`) shall all be zero. We can use the powerful SMT-solver `z3` to do simply solve the task for us. 
```python
	from z3 import *

	inp = BitVec('in', 256)

	c1 = 0x44940e8301e14fb33ba0da63cd5d2739ad079d571d9f5b987a1c3db2b60c92a3
	c2 = 0xd208851a855f817d9b3744bd03fdacae61a70c9b953fca57f78e9d2379814c21

	w1 = ~ (inp | c1)
	w2 = ~ (inp | w1)
	w3 = ~ (c1 | w1)
	w4 = ~ (w2 | w3)
	w5 = ~ (w4 | w4)
	w6 = ~ (w5 | c2)
	w7 = ~ (w5 | w6)
	w8 = ~ (c2 | w6)
	out = ~ (w7 | w8)

	m = solve(out == 0)
	print(m)
```

That's it. We declare `inp` to be a bitvector of size 256 (this is the flag). Later, we want `z3` to find out which bit needs to be 1 in flag.
The two constants are taken from the code and represent wires with fixed values.
The next lines are directly translated from the code. `nor n1 [255:0] (w1, in, c1);` means:
*connect each wire (= bit) from `in`, with the corresponding wire (bit) in `c1` using a `nor` gate inbetween and the result is the write (bit) in `w1`. This is exactly what we did in Python: Bitwise `OR` followed by `NOT`. Not that we use `inp` here, which is treated as a placeholder with yet unknown value. So `out` does not contain a value, but more a description on how to compute it, if `flag` would be given.
`solve(out == 0)` tells `z3`: Please find us some valid inputs (for the yet unknown `flag`), such that `out` will be zero. And `z3` will do exactly this.
The good thing is: I still don't have any idea what the verilog code really does or how it is working. Never tried to understand it, never needed to.

### No thoughts Head empty
A brainfuck program. (DO NOT RUN IT, unless you know what you are doing).
We can solve this using simulation or reversing the code. I will discuss both ways in a more detailed writeup (using the 'Fewer Toughts, Head emptier' challenge, but they are mostly the same).
But if you just want a quick idea:
- Run it in an emulator and look at the tape while running
- Each letter's ascii value is computed as `a * b - c * d`, where all 4 variables can be obtained from the source with a bit of parsing.

### Fewer thoughs, Head emptier
I'll write a seperate, more detailed writeup to this soon. For a quick idea see `No thoughts Head empty` above.

### Off the races
I'll write a seperate, more detailed writeup soon. Quick Idea: Loose money on the bet, race condition with logging in caused by a complex regex.

### Roolang
We are given an interpreter for the language `roolang` that contains of small images.
1. Roolang reads the image file ("source code"), and constructs a string of letters `binor`.
2. It splits the string in chunks of 5 letters, those chunks are the commands evaluated by the interpreter
3. -- roolang does everything up to now for us. We don't need to parse the images ourself etc.
4. If we look at the various command handlers, we can guess what they do (`POP`, `ADD`, ...). roolang is a stack machine. I added a mapping from roolang-opcode to common names and printed the code. The code can be found [here](https://github.com/DerBaer0/CTF-writeups/blob/main/2021-imaginaryctf/roolang.code).
5. Analyzing the code, we can see, that it calls `robin` with some loop variable and uses the result to xor it with one of the constants pushed in the beginning. Afterwards, it increments the loop variable, calls `robin` again, xor, output. etc. The problem is, that the call to `robin` is slower and slower every time.
6. What does `robin` do? It is the recursive implementation of fibonacci. And there is only one function existing in this program. This leads to the following solution:
7. I change the handler for `call` to not call the function, but apply the effect on the stack, that is: Pop the argument, compute the corresponding fibonacci number (in a much faster way), push the result back to the stack, continue execution after the call. So, here is the original call handler:
```python
    def roiin():
        global insn_pointer
        arg = stack.pop()
        stack.push(insn_pointer+1)
        stack.push(arg)
        rioon()
```
And here is mine:
```python
    def roiin():
        global insn_pointer
        arg = stack.pop()
        stack.push(fibs[arg])
        insn_pointer+=1
```
And now it is blazingly fast. Fun challenge.
(Other solutions would include looking at the stack and guessing what is happening, rewriting the roocode to be more effizient or rewrite it in python) 

