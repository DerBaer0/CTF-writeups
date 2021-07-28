
# Pwn Challenges

Writeups in this file only give a brief description. 
### stackoverflow
`scanf("%s")` does not limit input length. We write `ftci\x00\x00\x00\x00` 10 times into the buffer to overwrite the variable (Because everything here is a multiple of 8 Bytes in sizes, we repeat the 8-byte value and it will be perfectly align, no need to compute the correct offset)

### fake_canary
We first run `checksec --file=fake_canary` that tells us, there are __no__ canaries, so probably some self implemented canary. And indeed, the canary is manually compared with a hardcoded value. So our exploit (`gets` does not limit input length, so we can simply overwrite everything) can overwrite the canary with the known value.
Running `strings fake_canary` tells us, there is a `/bin/sh` and looking in the binary, we can find the function `win` that already does `system("/bin/sh");"`for us. So overwrite canary and after this, we overwrite the saved `rbp` with a reasonable value and the `return instruction pointer` with `0x400726` which is inside the `win` function. __Note__ Ubuntu 18.04 libc needs a 16-byte aligned stack, however stack is only 8-byte aligned normally. In this case, we skip the `push %rbp` instruction to get the required alignment.
:w

# The First Fit
We have a simple program giving us access to `malloc` and `free`. Also, it executes the content of `b` on option `4`.
This is my python code (where the functions simply handle the connection with the server)

	free(A)
	malloc(B)
	fill("/bin/sh")
	system()

1. We free `a` and malloc `b`. The free in libc will put the memory region into a local datastructure. The next malloc of the same size will return exactly this pointer again. (The libc heap implementation is quite complex, but there are really good explanations out there. Basically, it is mostly predictable, what happends to your buffers, but in this challenge we only need a very small part of it.)
2. Now we write to `a`. We never clear `a`, so we still have the pointer to the memory chunk. And it is the same chunk currently allocated and assigned to `b` as well.
3. We execute `b` and have a remote shell
