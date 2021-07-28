

# Crypto Challenges

Writeups in this file only give a brief description. 

### Flip Flop
*(not the inteded / most elegant solution I think)*
We want to find a string that contains `gimmeflag` when decrypted, but we cannot encrypt such a string. But CBC processes one block (16 Byte) at a time. So, we might be able to have one block ending with e.g. `gimme` and the next block starting with `flag`. But we slightly shift the magic value, we want the first block to end with `gimmefla` and the second block to start with `g`. 
The first block is trivial, because we can simple encrypt it beforehead. So `X = encrypt("00000000gimmefla")` and take the first block (16 byte) of the result. Now, we need to find a second block to append to `X`, such that when decrypting, the block starts with `g`. We just tried random values! There are only 256 possible values for the first byte of this second block, and assuming the encryption (AES) is good, every byte will be equally likely. So, we don't have to try that many inputs (Probablility tells us, ~256 is enough, 128 tries would be the usual case.)
So the exploit is simply to run the following command several times until we get a flag (`enc` and `dec_bin` are just wrappers to handle communicating with the remote). 

    dec_bin(enc("00000000gimmefla")[:16] + os.urandom(16))

### Rock Solid Algorithm
RSA encryption with a very small `e = 5` (usual is 0x10001). Google can help finding attacks for this scenrio. In this case, we compute the 5-th root of `c`. But because `c` was computed using modulo `n`, the *real* `c` could be `c`, `c + n`, `c + 2n`, `c + 3n`, ... We try all of them (for small input strings, this is fast enough):

    import gmpy2 
    import binascii
	n = ...
	e = 5
	c = ...
	i = 0
	while 1:
	     m, b = gmpy2.iroot(c+i*n, e)
	     if b:
	        print('[-]m is:', m)
	        print(binascii.unhexlify(hex(m)[2:]))
	        break
	     i+=1

### Lines
- `s * msg % p = msg_crypt` (given in the output)
- Find the `modular inverse` for `msg` regarding `p` (e.g. `sagemath` can do this). The `modular inverse` is the value `x`, so that `msg * x = 1 (modulo p)`.
- `s * msg * x = msg_crypt * x (modulo p)` (multiply both sides with this `x`) and because of the property of `x` as the modular inverse, this equals: `s = msg_crypt * x (modulo p)`. So, we know `s`.
- Now we have the second line `s * flag % p = flag_crypt` (flag_crypt given in the output again). Do the same step, but this time find the modular inverse for s. Plug it in and get the result.
- Convert the integer to bytes for the flag as a string

### Roll it back
The programm takes `flag`, and repeatedly shifts it one bit to the right. The free space on the left is filled with `1` or `0` depending on the current value of `flag` and `T` (where `T` is a constant value we can compute just like the program did).
When we want to undo a single operation, we shift the result one to the left and clear the leftmost bit. The only problem is that the least significant bit was dropped in the program by the right shift. But there are only two options for this bit. So we try both and check whether applying the operation gives our result or not. It is important, that __exactly__ one the two options gives our result. So we can undo one operation at a time until we are back at the initial flag value.
My code can be found [here]()


