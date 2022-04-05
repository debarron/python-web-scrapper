# jjm

Jenkins job monitor (duh), is a boring and simple script to check Jenkins jobs from command line. It's only informative.
BTW, brace yourselves for a bunch of emojis, I got carried away.
This is a lerners effort to dig into Python's type hint, it was fun.

## Under the hood
This script reciever either a URL or a text file containing URLs.

TL-DR
- Makes an http-get request to the Jenkins URL
- Goes through the response HTML using Beautifulsoup
- Prints only active sessions

## Usage
Make sure to install libraries listed in `libs` text file.
After installing the libraries, run `jjm` by:

`python jjm -u jenkins_URL`

or

`python jjm -i file_with_jenkins_urls`

Cheers 🍻 !
