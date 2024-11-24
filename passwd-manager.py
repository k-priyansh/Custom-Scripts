import random # the library that gives the ability to create a random output given an input
import string # this library gives more complexity when generating a password


def generate_password(length: int = 10):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(alphabet) for i in range (length))
    return password

print("1. generate password")
#print("2. see password")
#print("3. store password")
#print("0. exit")
option=input("enter your choice")

if (option == "1"): 
    password = generate_password()
    print(f"Generated password: {password}")
elif(option == "2"):
    print("invaild option")
elif(option == "3"):
    print("invaild option")
elif(option == "0"):
    print("GeneratorExit")
    exit
    
