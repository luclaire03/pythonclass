def caesar_shift(message, num):
    '''shifts each letter of message num places in alphabet'''
    alphabet = "abcedfghijklmnopqrstuvwxyz"
    newWord = ""
    for letter in message:
        if letter in alphabet:
            index = alphabet.find(letter)
            newLetter = alphabet[(index + num) % 26]
            newWord = newWord + newLetter
        else:
            newWord = newWord + letter
    print(newWord)


caesar_shift("hello ma", 2)


def student_grades(name):
    '''reads file containing student names and test scores
    and averages score, returns average when given student name'''
    file = open(studentdata.txt)
    gradebook = {}
    for line in file:
        indiv = line.split()
        if indiv[0] not in gradebook:
            gradebook[indiv[0]] = indiv[1]
        else:
            gradebook[indiv[0]] = gradebook[indiv[0]] + indiv[1]
    name = input("Enter a student's name:")
    if name in gradebook:
        return ("The average for " + str(name) + " is " + str(gradebook[name]))
    else:
        print("no")
    '''still need to calc grade avg'''


def fibonacci(x):
    if x == 1 or x == 2:
        return 1
    return fibonacci(x - 1) + fibonacci(x - 2)

