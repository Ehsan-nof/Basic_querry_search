import os

path = ""
STOP_WORDS = ["is",".","was","are","the","were","am","?"]

def list_transform (words:list):
    result = []
    for word in words:
        word = word.lower()
        if not word in STOP_WORDS:
            result.append(word)
    return result
        
def linguistic_transform(file_word:dict):
    for k in file_word.keys():
        file_word[k] = list_transform(file_word[k])

def read_from_files(directory:str)->dict:
    id = 0
    words = {}
    
    for path, folders, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".txt"):
                with open(os.path.join(path, file_name)) as f:
                    text = f.read()
                text = text.lower()
                text = text.replace("." , ' ')
                text = text.replace('\n' , ' ')
                text_list = text.split()
                unique_name = str(id) + " : " + file_name
                words[unique_name] = text_list
                id += 1

    return words

#-------------------------------------------------------------
def redo ():
    # some redo fancy cool stuff
    answer = input("Would you like to search another word? ")
    if answer.lower() == "yes":
        linguistic_search()
    else:
        return()
# function for updating the querry dictionary values     
def set_key(dictionary:dict, key:str, value:int):
    if key not in dictionary:
        dictionary[key] = value
    elif type(dictionary[key]) == list:
        # if it repeated more than one time in one file we would have a list of indices in that file
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]
        
def querry_print(dictionary:dict):
    count = 0
    # handling the user word and printing it in console
    for key in dictionary.keys():
        # printing keys(file names)
        print("This word was found in file: {:s}".format(key))
        if type(dictionary[key]) == list:
            # calculating the times that a word is repeated
            count = count + (len(dictionary[key]))
            # print indices of word in a file
            print("Index of the word are: ",end="")
            for index in dictionary[key]:
                print(index,end=" ")
            print("")
        else:
            # calculating the times that a word is repeated
            count = count + 1
            # print index of word in a file
            print("Index of the word is: {:d}".format(dictionary[key]))
     #--------------------------------
     # writing the amount of reputation of a single word in a specific file
    if count > 1:
        print("This word was repeated {:d} times".format(count))
        # redo the search (fancy stuff)
        redo()
    elif count == 1:
        print("This word was repeated {:d} time".format(count))
        # redo the search (fancy stuff)
        redo()
        
def make_inverse_indices(file_word:dict)->dict:
    result = {}
    
    for k in file_word.keys():
        for i in range (len(file_word[k])):
            # check if a key already exist or not
            if file_word[k][i] in result:
                # if a key is in result it would update value
                Word = {}
                Word[k] = i
                set_key(result[file_word[k][i]],k,i)                
            else:
                # if we dont have the key it would create it for the first time
                Word = {}
                Word[k] = i
                result[file_word[k][i]] = Word
    return result

def User_querry(term:str,result:dict):
    term = term.lower()
    
    # check if querry is in the files or not
    if term not in result.keys():
        print("This word is either a STOP WORD or doesn't exist")
        # guide the user through stop words
        answer = input("Do you want to see the STOP WORDS? ")
        if(answer.lower() == "yes"):
            for word in STOP_WORDS:
                print(word)
            redo()
        else:
            # redo the search (fancy stuff)
            redo()
            
    # pass the querry words to function for printing the right expressions
    else:    
        for big_key in result.keys():
            if big_key == term: 
                querry_print(result[big_key])
                   
# The game itself :)
def linguistic_search():
    # reading from files
    file_words  = read_from_files(path)
    # make the input standard and delete the useless words
    linguistic_transform(file_words)
    # re arrenging data so every index is ready to show for user
    result = make_inverse_indices(file_words)
    print(result)
    # getting the word and showing it in console
    user_word = input("Enter the word: ")
    User_querry(user_word,result)

if __name__ == "__main__":
    # start the engin
    linguistic_search()
