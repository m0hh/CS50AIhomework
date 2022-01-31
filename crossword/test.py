a = {"a": 1,"b":2,"c":3,"d":4}

if len(set(a.values())) != len(a.values()):
    print("not unique")
elif len(set(a.values())) == len(a.values()):
    print("unique")

print(a.items())