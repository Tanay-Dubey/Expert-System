import os
import subprocess
import pandas as pd
import re

admin = False


def errorMessage(e):
    print("Bot: The action could not be completed because following error occured")
    print(str(e))


def createDB():
    try:
        print("\nBot: Enter the name of database")
        db = input("You: ")
        if ("cancel" in db):
            return
        if (os.path.exists(f"./database/{db}.csv")):
            print(f"Bot: Database named {db} already exists")
            return
        print("Bot: Enter the number of columns in the database")
        noOfCols = input("You: Number of Columns:")
        if ("cancel" in noOfCols):
            return
        noOfCols = int(noOfCols)
        print("Bot: Enter the column names")
        cols = input("You: Column Names: ").split()
        df = pd.DataFrame([], columns=cols)
        df.to_csv(f"./database/{db}.csv", index=False)
        print(f"Bot: Database named {db} created successfully")

    except Exception as e:
        errorMessage(e)


def createFile():
    try:
        print("\nBot: Enter the name of file")
        filename = input("You: ")
        if ("cancel" in filename):
            return
        if (os.path.exists(f"./filebase/{filename}")):
            print(
                f"Bot: File named \"{filename}\"  already exists")
            return
        else:
            f = open(f"./filebase/{filename}", "w")
            f.close()
            print("Bot: File Created Successfully")

    except Exception as e:
        errorMessage(e)


def create(request):
    if (admin == False):
        print("Bot: You do not have the rights to perform this operation")
        return
    if ("database" in request):
        createDB()
    else:
        createFile()


def deleteDB():
    print("\nBot: Enter the name of database")
    dbname = input("You: ")
    if ("cancel" in dbname):
        return
    try:
        if (os.path.exists(f"./database/{dbname}.csv")):
            os.remove(f"./database/{dbname}.csv")
            print("Bot: Database deleted successfully")
        else:
            print(f"The database named {dbname} does not exists")
    except Exception as e:
        print("Bot: The following error occured")
        print(str(e))


def deleteFile():
    print("\nBot: Enter the name of file")
    filename = input("You: ")
    if ("cancel" in filename):
        return
    try:
        if (os.path.exists(f"./filebase/{filename}")):
            os.remove(f"./filebase/{filename}j")
            print("Bot: File deleted successfully")
        else:
            print(f"Bot: The file named {filename} does not exists")
    except Exception as e:
        print("Bot: The following error occured")
        print(str(e))


def delete(request):
    if (admin == False):
        print("Bot: You do not have the rights to perform this operation")
        return
    if ("database" in request):
        deleteDB()
    else:
        deleteFile()


def searchDB():
    print("\nBot: Enter the name of database")
    dbname = input("You: ")
    if ("cancel" in dbname):
        return
    try:
        if (os.path.exists(f"./database/{dbname}.csv")):
            df = pd.read_csv(f"./database/{dbname}.csv")
            print("Bot: Database Information:")
            print(os.stat(f"./database/{dbname}.csv"))
            print(df)
        else:
            print(f"Bot: The database named {dbname} does not exists")

    except Exception as e:
        print("Bot: The following error occured")
        print(str(e))


def searchFile():
    print("\nBot: Enter the name of file")
    filename = input("You: ")
    if ("cancel" in filename):
        return
    try:
        if (os.path.exists(f"./filebase/{filename}")):
            print(os.stat(f"./filebase/{filename}"))
        else:
            print(f"Bot: The file named {filename} does not exists")

    except Exception as e:
        print("Bot: The following error occured")
        print(str(e))


def search(request):
    if ("database" in request):
        searchDB()
    else:
        searchFile()

def addRecord(dbname):
    try:
        df = pd.read_csv(f"./database/{dbname}.csv")
        print("\nBot: The database has the following format")
        for i in df.columns.values:
            print(i+"\t", end="")
        print("\nBot: Enter the data according to this format")
        row = input("You: ")
        row = re.split(r'\s|,', row)
        data = {}
        index = 0
        for i in df.columns.values:
            data[i] = row[index]
            index += 1
        df = df.append(data, ignore_index=True)
        df.to_csv(f"./database/{dbname}.csv",index=False)
        print("Bot: Record added successfully")
    except Exception as e:
        errorMessage(e)


def deleteRecord(dbname):
    try:
        df = pd.read_csv(f"./database/{dbname}.csv")
        print("\nBot: Enter the index column")
        colval = input("You: Column Name:")
        print("Bot: Enter that value to be deleted")
        value = int(input("You: "))
        df = df[df[colval] != value]
        df.to_csv(f"./database/{dbname}.csv",index=False)
        print("Bot: Record deleted successfully")
    except Exception as e:
        errorMessage(e)


def searchRecord(dbname):
    try:
        df = pd.read_csv(f"./database/{dbname}.csv")
        print("\nBot: Enter the index column")
        colval = input("You: Column Name:")
        print("Bot: Enter the value to be searched")
        value = input("You: ")
        print("Bot: ")
        print(df.loc[df[colval]==value])
    except Exception as e:
        errorMessage(e)


def editDB():
    commands = {"add": addRecord, "append": addRecord,
                "delete": deleteRecord, "drop": deleteRecord, "search": searchRecord}
    print("\nBot: Enter the name of database")
    dbname = input("You: ")
    if ("cancel" in dbname):
        return
    if(os.path.exists(f"./database/{dbname}.csv")==False):
        print(f"Bot: Database named {dbname} does not exists")
        return
    print(f"\nBot: What operation would you like to perform in the {dbname}")
    request = input("You: ")
    if ("cancel" in request):
        return
    for i in commands.keys():
        if (i in request):
            commands[i](dbname)
            return


def writeData(filename):
    try:
        print("\nBot: Enter the data to be overwritten")
        data = input("You: ")
        with open(f"./filebase/{filename}", "w") as file:
            file.write(data)
        print("Bot: File edited successfully")

    except Exception as e:
        errorMessage(e)


def addData(filename):
    try:
        print("\nBot: Enter the data to be appended")
        data = input("You: ")
        with open(f"./filebase/{filename}", "a") as file:
            file.write(data)
        print("Bot: File edited successfully")

    except Exception as e:
        errorMessage(e)


def editFile():
    commands = {"add": addData, "append": addData, "write": writeData}
    print("\nBot: Enter the name of file")
    filename = input("You: ")
    if ("cancel" in filename):
        return
    if (os.path.exists(f"./filebase/{filename}") == False):
        print(f"\nBot: The file named {filename} does not exist")
        return

    print(f"Bot: What operation would you like to perform on the {filename}")
    request = input("You: ")
    if ("cancel" in request):
        return
    for i in commands.keys():
        if (i in request):
            commands[i](filename)
            return


def edit(request):
    if (admin == False):
        print("Bot: You do not have the rights to perform this operation")
        return

    if ("database" in request):
        editDB()
    else:
        editFile()


def viewDB():
    try:
        print("\nBot: Enter the name of database")
        dbname = input("You: ")
        if ("cancel" in dbname):
            return
        if (os.path.exists(f"./database/{dbname}.csv")):
            df = pd.read_csv(f"./database/{dbname}.csv")
            print("Bot: ")
            print(df)
        else:
            print(f"Bot: The database named {dbname} does not exists")

    except Exception as e:
        errorMessage(e)


def viewFile():
    try:
        print("\nBot: Enter the name of the file")
        filename = input("You: ")
        if ("cancel" in filename):
            return
        if (os.path.exists(f"./filebase/{filename}")):
            with open(f"./filebase/{filename}") as file:
                content = file.read()
            print("Bot: ")
            print(content)
        else:
            print(f"Bot: The file named {filename} does not exists")

    except Exception as e:
        errorMessage(e)


def view(request):
    if ("database" in request):
        viewDB()
    else:
        viewFile()


def viewBySoftware():
    try:
        print("\nBot: Enter the name of file")
        filename=input("You: ")
        if("cancel" in filename):
            return
        if(os.path.exists(f"./filebase/{filename}")==False):
            print(f"Bot: The file named {filename} does not exists")
            return
        print("Bot: Opening the file...")
        filepath=f"./filebase/{filename}"
        subprocess.Popen(["start",filepath],shell=True)
    except Exception as e:
        errorMessage(e)


def processRequest(request):
    request = request.lower()
    swcommands = {"software": viewBySoftware,
                  "editor": viewBySoftware, "viewer": viewBySoftware}
    commands = {"create": create, "edit": edit, "append": edit, "delete": delete, "search": search,
                "info": search, "information": search, "read": view, "view": view, "open": view, "see": view, "login": start}
    for i in swcommands.keys():
        if(i in request):
            swcommands[i]()
            return

    for i in commands.keys():
        if (i in request):
            commands[i](request)
            return
    print("Bot: We do not have sufficient knowledge to process this request")
    return


def interact():
    print("\nBot: Welcome. How can I help you?")
    request = input("You: ")
    if ("exit" in request):
        print("Bot: See you next time")
        exit(0)
    processRequest(request)
    while (True):
        print("\nBot: Is there else you want me to do?")
        request = input("You: ")
        if ("exit" in request):
            print("Bot: See you next time")
            exit(0)
        processRequest(request)


def start(request=None):
    print("Bot: Please Login to access the system")
    username = input("Username: ")
    password = input("Password: ")
    df = pd.read_csv("./userData/login.csv")
    found = False
    for _, row in df.iterrows():
        if (row["Username"] == username and row["Password"] == password):
            found = True
            global admin 
            admin= bool(row["Admin"])
            break
    if (found):
        interact()
    else:
        print("Bot: No matching credentials found")


start()