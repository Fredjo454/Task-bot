def bb (greetings):

    def a ():
        print(greetings)
    def ccc ():
        print(f"{greetings}, you")
    if greetings == "hi":
        return a
    else:
        return ccc
@bb
def dddd():
    return("hello")
bb("hello") ()