#
# author:
#     @j-tesla
#
from collections import Counter

t = input()
for _t in range(int(t)):
    accounts = []
    n = input()
    a = input()
    while a:
        accounts.append(a)
        a = input()
    c = Counter(accounts)

    for acc in sorted(c):
        print(acc + ' ' + str(c[acc]))

    print()
