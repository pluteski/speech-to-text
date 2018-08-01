

##### Commands for publishing
Compiles markdown pages as html and pushes to pluteski.github.io/speech-to-text.

    $ . ~/virtualenvs/pelican/bin/activate
    $ cd ~/code/speech-to-text/blog/
    $ make html ; make publish ; cp -r output/* ../docs/ ; git add ../docs/*
    $ git commit -m "commit msg"
    $ git push origin master
    $ deactivate


#### Run these 2 lines:
. ~/virtualenvs/pelican/bin/activate; cd ~/code/speech-to-text/blog/
make html ; make publish ; cp -r output/* ../docs/ ; git add ../docs/*


