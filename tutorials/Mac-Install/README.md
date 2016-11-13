# Mac Installation

## Foreword
Our project requires a significant number of dependencies so this guide aims at providing some tips for where I ran into problems. I am running Mac OS 10.12.1, but I have also installed this on Mac OSX 10.10 so you shouldn't run into many problems if you're installing on recent previous versions. This installation will be similar to the linux installation, so feel free to check that out if you get stuck too. As we go along you can also look at the documentation on the individual application's wiki pages.

## Disclaimer
What I describe here is the process I went through for my installation. It may differ from your installation process but hopefully this will send you in the right direction.

I recommend that you install homebrew, a package manager for mac, as it allows you to install some of the dependencies. If you do not have homebrew already installed you, can also consider macports, an alternative package manager. Macports is supposed to support more of the packages, but this tutorial will show you how to install using homebrew.

## Homebrew
To install Homebrew, I will send you to their website, [here](http://brew.sh). Type `brew --version` to make sure your installation completed succesfully.

## Sumo
The transportation simulation of our project will be the first large component that we instal. In my case, I found that the only way I could get it to work well is by compiling it from source.
