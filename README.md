Auctions
========

Auction website that allows users to create auctions in three different auction formats: 
* [British auctions] (https://en.wikipedia.org/wiki/English_auction)
* [Vickrey auction] (http://en.wikipedia.org/wiki/Vickrey_auction) 
* [Sealed bid auction] (https://en.wikipedia.org/wiki/First-price_sealed-bid_auction)

### Installation

Firstly, you need Python 2.7 (http://python.org).

Right after you download the source from github, we recommend you to install the virtualenv and pip. Virtualenv lets you install the libraries locally, so it will not conflict with other installations. Pip is package library for python. You'll install (almost) everything with it.

For windows users, follow this very good guide:
https://zignar.net/2012/06/17/install-python-on-windows/

For unix users, try following this guide:
http://www.pip-installer.org/en/latest/installing.html

After you have installed virtualenv, create one with:

```
virtualenv venv --distribute
```

Activate it with:

```
source venv/bin/activate
```

or

```
source venv/Scripts/activate (Windows)
```

You will always need to do it when running the project, as the code must run on it.

For linux users: please install python-dev and libpq-dev before continuing. Just run:

```
sudo apt-get install python-dev libpq-dev
```

After it's finished, just continue.

Now run:

```
pip install -r requirements.txt
```

Windows users, you may have problems installing the 'psycopg2' library. Please follow these steps:

1. Install postgresql, found on -> http://www.postgresql.org/download/ . Just download the binaries and run it normally.
2. After that, download psycopg2 for windows -> http://www.stickpeople.com/projects/python/win-psycopg/ . After that run on the command line ( with virtualenv ACTIVATED!) the following:

    ```
    easy_install <path/to/psycopg2>
    ```

3. If it doesn't work, easy_install directory probably is not in your path. It is found on Python27/Scripts. Note that you'll need it for every library that can't be installed with pip on windows.

Again, Windows users, should you have problems installing Pillow, just follow the steps 2 and 3 shown above.

Now, you probably want to run the code. First, it's nice to set the DB. Follow these steps:

1. Check again if virtualenv is activated! If it is not, you probably made a mistake somewhere before. Try starting over.
2. Sync the DB (only once) with: 
    ```
    python manage.py syncdb
    ```
3. Run the DB migrations (only once):
    ```
    python manage.py migrate core
    ```
4. Run the server:
    ```
    python manage.py runserver
    ```

Now you can find the app running on the localhost. The admin page is on /admin . You can access it by logging in with the superuser you created when setting up the database.
