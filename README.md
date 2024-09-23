# SteamSkipUpdate

A lil python script to update Appmanifest with SteamCMD for Python 3.x

Tired of steam updates ruining your meticulously modded games? Give this a try!

This bad boy auto fetches the latest buildid and manifest from SteamCMD and slap it into your Appmanifest of choice!

Don't know what Appmanifest is? 

Check out [this](https://steamcommunity.com/sharedfiles/filedetails/?id=2901860378) and you will understand what this script does in no time!

## Installation

First, install wexpect with pip install wexpect.

Then, create a folder and slap both the script and SteamCMD into it and run the script.

## Requirements:
- wexpect https://github.com/raczben/wexpect/tree/master
- SteamCMD https://developer.valvesoftware.com/wiki/SteamCMD

## Known issues
- SteamCMD will output old or no data sometimes when running in automated mode.
- If autofix does not fix the no Steam data error follow the prompt to manually load Steam data.
- If you are getting outdated data delete the appcache folder and try again, these are issues with SteamCMD and I can't do anything about them.
