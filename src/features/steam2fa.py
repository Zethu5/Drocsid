import os

#Finds all files with a certin name (target) in a certain prefix (dirs like C:,D:) works recursively
def findInPref(target,prefix):
    for path, dirs, files in os.walk(prefix):
        if target in dirs:
            return os.path.join(path, target)

#Finds the Steam install dir 
def findSteam():
    PREFIXES = [ chr(x) + ":\\" for x in range(65,91) if os.path.exists(chr(x) + ":") ]
    for prefix in PREFIXES:
        output = findInPref('Steam',prefix)
        if output:
            return output
    
    
#Finds the pwd for the revelant Steam files  
def getSteamFils():
    steampwd = findSteam()
    os.chdir(steampwd)
    files = []
    for file in os.listdir():
        if file.startswith('ssfn'):
            files.append(steampwd+ '\\' + file)
    return files
