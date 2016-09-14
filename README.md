# Welcome to CRIPTs

## Important! I just forked the code and updated the README. No actual work has been done on this project so far. In fact, I probably won't get around to this for a while. The reason I forked it was simply to kick myself in the butt to get around to developing this since dealing with multiple large password datasets is a pain

## What Is CRIPTs?

CRIPTs is a fork of the CRITS toolset specifically altered to keep track of password datasets. The target audience for this is security researchers along with professional penitration testers.

## What Is CRITs?

CRITs is a web-based tool which combines an analytic engine with a cyber threat database that not only serves as a repository for attack data and malware, but also provides analysts with a powerful platform for conducting malware analyses, correlating malware, and for targeting data. These analyses and correlations can also be saved and exploited within CRITs. CRITs employs a simple but very useful hierarchy to structure cyber threat information. This structure gives analysts the power to 'pivot' on metadata to discover previously unknown related content.

Visit its [website](https://crits.github.io) for more information, documentation, and links to community content such as our mailing lists and IRC channel.

# Installation

CRIPTs is designed to work on a 64-bit architecture of Ubuntu or RHEL6 using Python 2.7. 

The following instructions assume you are running Ubuntu or RHEL6 64-bit with Python 2.7. If you are on RHEL which does not come with Python 2.7, you will need to install it. If you do, ensure all python library dependencies are installed using Python 2.7. Also, make sure you install mod_wsgi against the Python 2.7 install if you are looking to use Apache. 

## Quick install using bootstrap

CRIPTs comes with a bootstrap script which will help you:

* Install all of the dependencies.
* Configure CRIPTs for database connectivity and your first admin user.
* Get MongoDB running with default settings.
* Use Django's runserver to quickly get you up and running with the CRITs interface.

Just run the following:

```bash

    sh script/bootstrap
```

Once you've run bootstrap once, do not use it again to get the runserver going, you'll be going through the install process again. Instead use the server script:

```bash

    sh script/server
```

**Thanks for using CRIPTs!**
