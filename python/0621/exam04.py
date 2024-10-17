def say_myself(name, age, man=True):
    print("이름 : %s" % name)
    print("나이 : %d" % age)
    if man:
        print("남")
    else:
        print("여")
    return

say_myself("lee", 20, 1)