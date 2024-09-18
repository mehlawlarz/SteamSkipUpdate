import wexpect
import os
import re
from pathlib import Path

NotValid1 = True
NotValid2 = True
IOdata = ['\n']*10
separator = '\n-------------------------------------\n'

# Path to file
while NotValid1:
    x = input('Use last directory? (y/n) ')
    # Load configs as list
    with open(Path(__file__).with_name('path.txt'), 'r') as fileI:
        var = fileI.readlines()
        IOdata[:len(var)] = var
    # if yes load from list
    if x in ["y", "yes"]:
        directory = IOdata[0].rstrip()
        NotValid1 = False
    # if no save input to file
    elif x in ["n", "no"]:
        directory = input('Input directory (ex. X:\SteamLibrary\steamapps): ')
        # Save data for next time
        with open(Path(__file__).with_name('path.txt'), 'w') as fileO:
            IOdata[0] = directory + '\n'
            fileO.writelines(IOdata)
            NotValid1 = False
    else:
        print('Invalid input')

# Filename
while NotValid2:
    x = input('Use last filename? (y/n) ')
    # Load configs as list
    with open(Path(__file__).with_name('path.txt'), 'r') as fileI:
        var = fileI.readlines()
        IOdata[:len(var)] = var
    # if yes load from list
    if x in ["y", "yes"]:
        filename = IOdata[1].rstrip()
        NotValid2 = False
    # if no save input to file
    elif x in ["n", "no"]:
        # Save data for next time
        filename = os.path.splitext(input('Input filename: '))[0]+'.acf'
        with open(Path(__file__).with_name('path.txt'), 'w') as fileO:
            IOdata[1] = filename + '\n'
            fileO.writelines(IOdata)
            NotValid2 = False
    else:
        print('Invalid input')

print(separator)

# Normalize and combine
filepath = os.path.normpath(directory) + "\\" + filename

# Read manifest file as list and search for manifest
with open(filepath, 'r') as file:
    content = file.readlines()
    index = [x for x in range(len(content)) if 'manifest' in content[x].lower()]

# Check if its already updated
for i in content:
    if 'StateFlags' in i:
        print(i)
        if re.findall(r'\d+',i)[0] == 4:
            print('Already up to date')
            input('\n Press Enter to exit...')
            exit()

# If not show index
print('Found manifests: \n')
for i in index:
    print(content[i-2])
    print(content[i])

print(separator)

# Spicy wexpect action
child = wexpect.spawn("cmd")
child.expect('>')
appid = filename.split("_")[1].rstrip()
print('Starting SteamCMD... \n')
arg = "steamcmd.exe +login anonymous +app_info_request {} +app_info_print {} +logoff +quit".format(appid, appid)
print('>' + arg + '... \n')
child.sendline(arg)
child.expect('>')
RawDB = child.before
child.sendline("exit")
child.wait()

print(separator)

# Split output to list
DB = RawDB.splitlines(True)

# Throw error if fail
for i in range(len(DB)):
    if 'is not recognized as an internal or external command,' in DB[i].lower():
        print("Error SteamCMD not found! \n\nPlease place SteamCMD in same directory as file \n")
        print(RawDB)
        input('\n Press Enter to exit...')
        exit()

# Cleanup the list for search
Junk = [x for x in range(len(DB)) if 'logging off current session' in DB[x].lower()]
for i in range(Junk[0]):
    DB[i] = ''
DB.pop(-1)

# Search for manifest and add to list
DBindex = [x for x in range(len(DB)) if 'manifest' in DB[x].lower()]
ManifestIndex = []
for i in DBindex:
    if '}' not in DB[i-2]:
        for x in range(10):
            if re.findall(r'\d+', DB[i-x]):
                ManifestIndex.append(DB[i-x])
                ManifestIndex.append(DB[i+4])

# Search for BuildID
for idi, i in enumerate(DB):
    if 'buildid' in i:
        if 'public' in DB[idi-2]:
            BuildID = re.findall(r'\d+', DB[idi])[0]

# Error if empty
if not ManifestIndex:
    print('Error SteamCMD gave no data please run app_info_print {} manually to load the data and try again'.format(appid))
    input('\n Press Enter to exit...')
    exit()

# Compare and replace old manifest
for xid, x in enumerate(ManifestIndex):
    for i in index:
        if int(re.findall(r'\d+', content[i-2])[0]) == int(re.findall(r'\d+', x)[0]):
            print('Found match: ' + re.findall(r'\d+', x)[0] + '!\n\nold:\n' + re.findall(r'\d+',content[i])[0] + '\nnew:\n' + re.findall(r'\d+', ManifestIndex[xid + 1])[0])
            content[i] = '			"manifest"		"{}"\n'.format(re.findall(r'\d+', ManifestIndex[xid + 1])[0])

# Update BuildId, change Flag and disable ScheduledAutoUpdate
for idi, i in enumerate(content):
    if 'StateFlags' in i:
        content[idi] = '	"StateFlags"		"4"\n'
    elif 'ScheduledAutoUpdate' in i:
        content[idi] = '	"ScheduledAutoUpdate"		"0"\n'
    elif 'buildid' in i:
        content[idi] = '	"buildid"		"{}"\n'.format(BuildID)



# Output
print(separator + '\nUpdated manifest:\n\n')
for i in content:
    print(i, end='')
with open(filepath, 'w') as file:
    file.writelines(content)

input('\n Press Enter to exit...')

# F:\SteamLibrary\steamapps\appmanifest_582660.acf

