# Mac Installation

## Foreword
Our project requires a significant number of dependencies so this guide aims at providing some tips for where I ran into problems. I am running Mac OS 10.12.1, but I have also installed this on Mac OSX 10.10 so you shouldn't run into many problems if you're installing on recent previous versions. This installation will be similar to the linux installation, so feel free to check that out if you get stuck too. As we go along you can also look at the documentation on the individual application's wiki pages.

## Disclaimer
What I describe here is the process I went through for my installation. It may differ from your installation process but hopefully this will send you in the right direction.

I recommend that you install homebrew, a package manager for mac, as it allows you to install some of the dependencies. If you do not have homebrew already installed you, can also consider macports, an alternative package manager. Macports is supposed to support more of the packages, but this tutorial will show you how to install using homebrew.

## Homebrew
To install Homebrew, I will send you to their website, [here](http://brew.sh). Type `brew --version` to make sure your installation completed succesfully. To update, run `brew update`.

## Sumo
The transportation simulation of our project will be the first large component that we instal. In my case, I found that the only way I could get it to work well is by compiling it from source. Download version 0.25.0 from [here](https://sourceforge.net/projects/sumo/files/sumo/version%200.25.0/sumo-src-0.25.0.zip/download). You can follow the compilation instructions [here](http://sumo.dlr.de/wiki/Installing/MacOS_Build_w_Homebrew).

## Omnet++
The networking simulation of our project is the next component. We will need to compile from source, so go [here](https://omnetpp.org/component/jdownloads/download/32-release-older-versions/2290-omnet-4-6-source-ide-tgz) and download version 5.0. You will have to extract it, then export the omnet binaries folder by placing and editing the following line in your .bashrc or respective file.
`export PATH=$PATH:/Users/you/path/to/omnetpp-4.6/bin`
Then just run `./configure` followed by `make`. Both of these will take a significant amount of time.
You should now have Omnet++ compiled and installed. To run it, type `omnetpp`. Your first time, you might be prompted to install the legacy java 6 runtime. Click the "more info" button on the window and download the helper linked on the page it takes you to. You might also need to authorize omnet++ by going to Security & Privacy in system preferences and press "Open Anyway".

If you run the application and it is crashing immediately, or if it failing to compile, first make sure the PATH is set to the omnetpp folder correctly, otherwise, here are two things you can try.
1. Install the latest JDK [here](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html). Get the latest version, then in a terminal, run `java -version`. That should tell you what version of java you are running. For me, this is `java version "1.8.0_111"`. Just make sure you are running 1.8+, not the 1.6 that Apple suggests. Once you have done this, remove your whole installation folder, and repeat the steps described above.
2. If you are still having problems, it might be a permissions problem with the omnetpp.app permissions. Navigate to the root of your Omnetpp install folder. Then to the "ide" folder. There you should see a file called omnetpp.app which is what is causing the problem. Run: `xattr -rc omnetpp.app`. That should fix the permissions issues, and it should no longer crash.

## Veins
We've almost made it now, hang in there. At this point, you should be able to run `SUMO-GUI` or `omnetpp` to bring up either of the respective simulations. The last large component we have is to download Veins, the link between Omnet++ and SUMO. For this project, we had to add some functionality to Veins, so we forked their repo which can be found on github [here](https://github.com/burtonwilliamt/veins). Now let's get it installed.

Download the repo. Next, open omnetpp (by typing `omnetpp` into a terminal). Now goto File > Import then expand the "General" section, and select "Existing Projects into Workspace". Hit next, then browse to where you just downloaded our fork and select the root folder. You should see a project selected labeled "veins". Now hit finish. Almost there!

You still need to build the veins project. To do this, go to Project > Build All alternatively, use (command B). Now test the veins project! Run the sumo-launchd.py script that is included in the veins folder. Navigate to the veins folder using a terminal, then run the following command `python sumo-launchd.py -vv -c sumo-gui`. The beginning runs the sumo-launchd.py script, `-vv` specifies that we want some logging to the termianl, and `-c sumo-gui` specifies that we want to use the GUI version of sumo. If you don't need this then it's better to run with `-c sumo` to avoid the extra graphics running, but I think the GUI version makes it easier to understand what's going on.
