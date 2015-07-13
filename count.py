import pprint
message = 'It was a bright cold day in April, and the clocks were striking thirteen.'
count = {}

for word in message:
    count.setdefault(word, 0)
    count[word] = count[word] + 1

pprint.pprint(count)
