# overcast-scrobbler-python

A basic Python script that allows automatic scrobbling your Overcast listening history.

## Requirements

 * Python (well, duh)
 * [requests](https://pypi.org/project/requests/), [opml](https://pypi.org/project/opml/)
 * The login data for your [overcast.fm](https://overcast.fm) account
 * Your Lastcast.fm API token (found in account settings)

## Usage

Simply call the script with your login data for overcast.fm and the Lastcast.fm API token as parameters:

```bash
python scrobble_overcast.py overcastuser overcastpassword lastcastapitoken
```

## Caveats

The script will create two cache files in the current directory to perform more efficiently on subsequent runs. I wish there was a way to do this without using the actual login credentials, but as far as I know Overcast does not have an API or access tokens or something similar.  
I'm only a Python hobbyist – happily will accept PRs to make the code more pythonic (or improve it in any other way – this thing has been doing its job quite well for months, but it's still more of a POC than a polished scrobbler).
