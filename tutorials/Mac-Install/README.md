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
The networking simulation of our project is the next component. We will need to compile from source, so go [here](https://omnetpp.org/component/jdownloads/download/32-release-older-versions/2290-omnet-4-6-source-ide-tgz) and download version 4.6. You will have to extract it, then export the omnet binaries by placing and editing the following line in your .bashrc or respective file.
`export PATH=$PATH:/Users/you/path/to/omnetpp-4.6/bin`
Then just run `./configure` and then `make`
You should now have Omnet++ compiled and installed. To run it, type `omnetpp`. Your first time, you might be prompted to install the legacy java 6 runtime. Click the "more info" button on the window and download the helper linked on the page it takes you to. You might also need to authorize omnet++ by going to Security & Privacy in system preferences and press "Open Anyway"
