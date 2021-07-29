# Sanity Check

This type of challenge is quite common in CTFs, so I highly recommend sharpen your skills by reading this writeup. We will learn about how to approach a CTF challenge (can be extended th other challenges as well in a limited way) and how to solve it. Let's get started.

## The Challenge Description
There are several really important or helpful information in the description itself.

 - __The category: Misc__ The category provides a quick idea, what we are expected, and if you are specialized into some field of CTF, you will probably filter by this category. In this case, the category is *Misc*, so the challenge does not fit into any other category. *Misc* is somewhat special, and everyone should take a look at those challenges. We don't know what to expect here. It could be a simple text file with a story, custom programming languages, a game to beat or basically anything else.
 - __The Name: Sanity Check__ The name often gives a first idea, what is to be expected. Sometimes it hints to the technology used (e.g. Chicken Caesar Salad) or the inteded attack vector (e.g., stackoverflow). Normally we need a bit of guessing, because the name is a bit disguised (as in "Rock Solid Algorithm refering to RSA").  In out case: *Sanity Check*. The word *sanity* is described as *the state of having a healthy mind and not being mentally* [Cambridge Dictionary]. What does this tell us? Probably it is testing our mental abilities. I can think of two possible challenges: One is a really confusing problem, like we have to write a program being valid in three different esoteric languages at the same time, and the other checks our mental ability to solve basic tasks. We will find out soon, what this is about.
 - __The Description: Welcome to ImaginaryCTF! All flags are written in flag format `ictf{.*}` unless otherwise stated. Have fun and enjoy the challenges!__ A very important part of each challenge is the description. It normally disguises itself as a plain boring story that can be ignored. __But:__ Never fall for this. There are important hints hidden in the story that can help solving it. You just need a bit of practice to read them, similar to the name. Furthermore, when you have an idea, how to solve the challenge, you can cross check whether it matches the description to verify you are on the correct track. Like, you think about a *Blind SQL injection* and the story is something like *Help me, I cannot see ...*, keep going and get that flag. Now, in this challenge: It tells us about the flag format. An *essential* piece of information for any CTF. It allows us to identify flags, search (`grep`) for flags and it can even help us as a *known plaintext*, a feature mainly important for crypto challenges. In most CTFs, the flag format is identical for all challenges, therefor after solving the first challenge, we can guess the flag format for other more advanced challenges. In this case, the flag format is `ictf{.*}`, and it is clearly stated inside the challenge description. Not always the authors are such fools simplifying the problem. If it is not provided here, a good place to look for the flag format is the *Rules*, *FAQ*  or similar pages. Often, this information can even be found before the contest even begins, giving you an enourmous time advantage over the unprepared teams. What does the flag format tell us for ImaginaryCTF? Although not being stated, `.*` indicates it is a regex (Regular Expression) (Otherwise, we should expect that each flag *is identical to* `ictf{.*}`, which allows us to solve problems really fast). A regex specifies a *pattern* and each string matching this pattern is considered *valid*, whereas all other strings are *considered* invalid. Many programs and languages support regex and they are more or less standardized. However, every regex engine uses it's own concept, whether a special character defaults to matching this character or to the regex logic. E.g., we are given `.*`. The dot (`.`) normally matches any character, but if we want to match a literal dot, we probably have to write `\.`. The asterix (`*`) means, that the previous character or sequence is repeated zero or more times. In other regex engine, `.` could match a literal dot, and to match any character, we would have to use `\.`. So, better don't assume anything and refer to the docs whenever using regex. A good site to test the regex of different engines against some strings is [here](https://regex101.com/). Ok, back to our flag. `ictf{.*}` We assume (and there is no way to be 100% sure), that each flag starts with `ictf{` (note that the `{` is special in some regex engines, but does match  aliter `{` here), continues with a sequence of just any characters, and terminates with a `}`. This is a * bad* flag format, because it allows any length (the shortes flag could be `ictf{}`), and we are never sure whether the flag is longer than what we found (`ictf{hello}continue}` is valid. A better way would be to exclude `}` from the possible characters inside the braces, or another common approach is to specify a whitelist of characters, like only alphanumeric values. But, here we are stuck with this format.
 - __Attachments__: Here we normally find the real challenge data. It might be a link to a website, a link to downloadable file, a server/port description, a combination of the above, or as in our case, a simple string.
## Solving the Challenge
Let's look at what the challenge provided us: ```ictf{w3lc0m3_t0_1m@g1nary_c7f_2021!}```
What shall we do with this?  This is everything we have (except the Category, Name and Description). And we need some string, that matches the flag format (`ictf{.*}`).
Well, it looks a bit like a flag, even if there are a lot of those strange characters inside. So let's check it. We can verify it manually, or we use the famous language `python` to check it (and not making any mistake.
```python
import re
string = "ictf{w3lc0m3_t0_1m@g1nary_c7f_2021!}"
pattern = "ictf{.*}"
match = re.search(pattern, string)
if match:
	print("The flag `" + match.group(0) + "` is a valid flag.")
else:
	print("This is not a valid flag")
```
Let's dig into it:
```python
import re
```
We tell Python to load the module responsible for regex checking.
```python
string = "ictf{w3lc0m3_t0_1m@g1nary_c7f_2021!}"
pattern = "ictf{.*}"
```
Both, the string we found in the description and the pattern for valid flags.
```python
match = re.search(pattern, string)
```
We use `search` to search for a string matching the pattern. We could use `fullmatch` instead of `search` to check whether the string in full length matches the pattern, but we are fine if only a part of it matches as well.
```python
if match:
```
This checks whether we found a match or not
```python
	print("The flag `" + match.group(0) + "` is a valid flag.")
```
We print a message. `match.group(0)` is a string containing exactly the substring of `string`, that matches the pattern. Ok, lets' run it:
```bash
$ python sanity.py 
The flag `ictf{w3lc0m3_t0_1m@g1nary_c7f_2021!}` is a valid flag.
```
Yeah, we were not sure, but now we have proof: There is a flag hidden inside the string given by the challenge.
*Note* : We could use the link above to verify the existance as well. Also note, that if you use the pattern as given by the description and set the Mode to `Java 8`, it will fail, because Java uses a different default interpretation for the `{`. 
Let's take a final look at the flag. If you blur your eyes and start some  hallucination, you can clearly imagine the string `welcome_to_imaginary_ctf_2021!`.  Really common in CTF is, that the flag string is a short phrase, often refering to the exploit you needed to get it. Additionally, it is encoded in `leetspeak`, that replaces letters with numbers or other symbols that look more or less similar to the original letter. Here is a list with possible ([options](https://www.gamehouse.com/blog/leet-speak-cheat-sheet/)).

Now, it's finally time to get some points.
## Flag Submission
Now, after finding the flag, the last step is to submit it. Depending on the CTF there are 2 places to do this. Either open the challenge and enter the flag there or, like in ImaginaryCTF, there is a single input field for all flags. 
Again, you have multiple options to get the flag into the submission formular.
- *Just type it:* You read the flag letter by letter, go to the input field, look for the correct characters on your keyboard and type them. For some challenges, this is the only reasonable option (e.g., if you found the flag inside an image). But whenever you do this, pay good attention to similar looking letters like l and l or o O 0.
- *Copy it:* You can select the string an then right-click *copy*, go to the input field, right-click *paste* and the string magically appears there. Instead of using the right-click, you can press `Ctrl+C` resp. `Ctrl+V` (`Ctrl` is `⌘` on MacOs). This is the recommended way.
- Use e.g. Python and the Browser-Scripting module `selenium` to open a browser and automatically put the flag there.
- Use e.g., the `requests` module of python, `curl` or similar to directly send the request made be the formula. But this is beyond the scope of this writeup.

And this is how you solve Sanity Check in ImaginaryCTF. And to whoever read until the end, here is a bonus tip: Continue training this challenge over and over again until you can master it in your sleep. My oracle shows me that a really similar challenge will exists in your next CTF.

