#function to detect same charcters in a string
def substart (st):
    for i in range (0, (len(st)-3)):
        subs = st [i:i+4]
        #set only takes unique elements
        subset = set (subs)
        if len (subs) == len (subset):
            print ("First start-of-packet marker after the", i+4, "th character")
            break

def messagestart (st):
    for i in range (0, (len(st)-13)):
        message = st [i:i+14]

        mset = set (message)
        if len (message) == len (mset):
            print ("First start-of-message marker after the", i+1, "th character")
            break

#open and read the input file
with open ("input.txt","r") as inpf:
    content = inpf.read()
    substart (content)
    messagestart (content)


        
