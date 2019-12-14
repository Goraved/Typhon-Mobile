# Typhon mobile tests (iOS/Android)
Automation tests for the mobile apps base on Python + Appium + BrowserStack

## IMPORTANT!
Note! It's just a template of mobile project with empty variables and test. To make it work need to specify all needed fields, tests, screen, locators and configs. 

## Setup
Brave yourself and read small instruction below.
I do not guarantee that you will understand something cause there are a lot of pitfalls with XCode and Appium versions. At first, make sure that you have a Developer provision profile and account from the app you gonna test. Then you need all the latest versions of:
* XCode;
* Android Studio;
* Appium;
* MacOS;
* iOS;
After that open `WebDriverAgent` project using XCode and add sign all WebDriverAgent in this project with your dev profile. And set the target version needed to your app.

#### Good luck!

# Instruction:
## Setup dev environment

Mobile tests project which supports iOS and Android using Appium.

This project is [Python](https://www.python.org/) based, so you will need Python to work with it.
For reports generation [Allure](http://allure.qatools.ru/) is used. Install it as well.

```
brew install python3
brew install Allure
```

In Terminal from the main project, folder do the following
1. Setup the local virtual env `python3 -m virtualenv venv`
2. Install all the requirements
```
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

Also, you can run the next script:
```bash
sh scripts/venv.sh
```

### Install Appium
```
brew install node || apt-get install nodejs # get node.js
npm install -g appium # get appium
npm install wd # get appium client
```
Or use the desktop version - http://appium.io/

## Android
[Install android sdk](https://developer.android.com/studio) 
```bash
brew tap caskroom/cask
brew cask install android-sdk
export ANDROID_HOME=/usr/local/share/android-sdk
```
[Create emulator](https://developer.android.com/studio/command-line/avdmanager)
```bash
sdkmanager "system-images;android-25;google_apis;x86"
avdmanager create avd -n test_emu -k "system-images;android-28;google_apis;x86" --device "pixel_xl"
avdmanager list avd
emulator -avd test_emu
```

## iOS
It can be automated only on Mac. 
``` bash
brew install libimobiledevice
brew install ios-deploy
```
1. Install Xcode
1. Get the dev permissions to the iOS developer group
1. Use guide to setup WebAgentRunner in the Xcode http://appium.io/docs/en/drivers/ios-xcuitest-real-devices/

### Launch Mobile tests 

Go to `scripts` dir. Execute the following script
```
execute_tests.sh
``` 

## ADVISES!
1. Try to use [Appium Desktop](https://github.com/appium/appium-desktop/releases) cause it would be faster for you and you could easily setup correct desired capabilities;

## Extra useful links:
1. [Creating a Test Automation Framework using Appium with Python](https://qaboy.com/2018/06/27/automation-framework-using-appium-python/)
2. [Appium XCUITest Driver Real Device Setup](http://appium.io/docs/en/drivers/ios-xcuitest-real-devices/)


#### kill appium nodes
`````/usr/bin/killall -KILL node`````

