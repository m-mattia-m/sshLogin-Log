import paramiko
import json


class Login():

    host = ""
    port = ""
    username = ""
    password = ""

    def __init__(self, host, port, username, password):

        Login.host = host
        Login.port = port
        Login.username = username
        Login.password = password

        self.openConnection()
        self.login()
        pass

    def openConnection(self):
        try:
            Login.ssh = paramiko.SSHClient()
            Login.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print("Open Connection")
        except:
            print("Connection could not be opened")
        pass

    def login(self):
        try:
            Login.ssh.connect(Login.host, Login.port, Login.username, Login.password)
            print("Logged in")
        except:
            print("Login failed")
        pass

    pass




class Commands():

    def __init__(self):
        pass

    def countFilesInSubfolder(self):

        # Anzahl Files
        stdin, stdout, stderr = Login.ssh.exec_command("find www -type f | wc -l")
        countFiles = stdout.readlines()
        countFiles = str(countFiles).replace("['  ", "")
        countFiles = str(countFiles).replace(r"\n']", "")
        print(countFiles)

        # Auflistund der Directories
        stdin, stdout, stderr = Login.ssh.exec_command("cd www; ls")
        listDirectory = stdout.readlines()
        print(listDirectory)

        # Anzahl der Folders
        stdin, stdout, stderr = Login.ssh.exec_command("cd www; ls | wc -l")
        countFolders = stdout.readlines()
        countFolders = str(countFolders).replace("['      ", "")
        countFolders = str(countFolders).replace(r"\n']", "")
        domains = self.nDomain(str(listDirectory), str(countFolders))
        print(countFolders)

        # Anzal Files in Subfolder

        i = 0
        subDomainWithFileCountList = ""
        while i < int(countFolders):
            subDomainWithFileCount = self.filesInFolder(domains[i], i)
            subDomainWithFileCountList += subDomainWithFileCount + "\n"
            i += 1
            pass


        # Form output
        output = ""
        output += "--------------------\n"
        output += "Anzahl Files: " + str(countFiles).replace("  ", "") + "\n"
        output += "Anzahl Folders: " + str(countFolders).replace("  ", "") + "\n"
        output += "--------------------\n"
        output += subDomainWithFileCountList

        self.writeInFile(str(output))
        print("Write in File successfully")
        pass

    def writeInFile(self, text):
        outputFile = open("output.txt", "w")
        text = text.replace(r"\n', '", "\n")
        text = text.replace("['", "")
        text = text.replace(r"\n']", "\n")
        outputFile.write(text)
        outputFile.close()
        pass

    def nDomain(self, text, countFolder):
        domains = []


        # Falls nicht funktioniert die nächsten zwei zeilen einblenden die könnten evtl noch wichtig sein
        # countFolder = countFolder.replace("['      ","")
        # countFolder = countFolder.replace(r"\n']", "")

        text = text.replace("['", r"\n', '")
        text = text.replace("]", ", '")
        # print("\n->: Edited Files")
        # print(text)

        i = 0
        while i < int(countFolder):
            textIndex = text.find(r"\n', '") + 6
            text = text[textIndex:]
            textIndexLast = text.find(r"\n', '")
            # print("textIndex: " + str(textIndex))
            tempDomain = text[0 : textIndexLast]
            # print("Domain: " + str(tempDomain))
            domains.append(tempDomain)
            i += 1
            pass

        # print("Domain-Array: ")
        # print(domains)
        return domains
        pass

    def filesInFolder(self, Domain, DomainIndex):
        command = "cd www; find " + Domain + " -type f | wc -l"
        stdin, stdout, stderr = Login.ssh.exec_command(command)
        countInSubdirectory = stdout.readlines()
        countInSubdirectory = str(countInSubdirectory).replace("['   ", "")
        countInSubdirectory = str(countInSubdirectory).replace(r"\n']", "")
        # returnValue = Domain + ": \t\t\t\t" + str(countInSubdirectory)

        # print("-->: " + str(len(Domain)))

        if len(Domain) <= 4 and len(Domain) >= 0:
            # print("#1")
            returnValue = Domain + ": \t\t\t\t\t\t\t\t\t" + str(countInSubdirectory)
            pass
        elif len(Domain) <= 8 and len(Domain) >= 4:
            # print("#2")
            returnValue = Domain + ": \t\t\t\t\t\t\t\t" + str(countInSubdirectory)
            pass
        elif len(Domain) <= 12 and len(Domain) >= 8:
            # print("#3")
            returnValue = Domain + ": \t\t\t\t\t\t\t" + str(countInSubdirectory)
            pass
        elif int(len(Domain)) <= 16 and int(len(Domain)) >= 12:
            # print("#4")
            returnValue = Domain + ": \t\t\t\t\t\t" + str(countInSubdirectory)
            pass
        elif len(Domain) <= 20 and len(Domain) >= 16:
            # print("#5")
            returnValue = Domain + ": \t\t\t\t\t" + str(countInSubdirectory)
            pass
        elif len(Domain) <= 24 and len(Domain) >= 20:
            # print("#6")
            returnValue = Domain + ": \t\t\t\t" + str(countInSubdirectory)
            pass
        elif len(Domain) <= 28 and len(Domain) >= 24:
            # print("#7")
            returnValue = Domain + ": \t\t\t\t" + str(countInSubdirectory)
            pass
        elif len(Domain) <= 32 and len(Domain) >= 28:
            # print("#8")
            returnValue = Domain + ": \t\t\t" + str(countInSubdirectory)
            pass
        elif len(Domain) <= 36 and len(Domain) >= 32:
            # print("#9")
            returnValue = Domain + ": \t" + str(countInSubdirectory)
            pass
        elif len(Domain) <= 40 and len(Domain) >= 36:
            # print("#10")
            returnValue = Domain + ": " + str(countInSubdirectory)
            pass
        else:
            print("Domain nicht zuortbar")
            pass

        # print(command)
        # print(returnValue)
        return returnValue
        pass

    pass



if __name__ == '__main__':
    with open("userdata.json") as userdata:
        userdata = json.load(userdata)
        domain = userdata["domain"]
        port = userdata["port"]
        username = userdata["username"]
        password = userdata["password"]
        print(domain + " " + port + " " + username + " " + password)
        connection = Login(domain, port, username, password)
    commands = Commands().countFilesInSubfolder()
