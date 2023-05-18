# OOH (Out-of-Home) Events App

Out-of-home events are events that take place outside of the home. This app can be used to see events happebning around OOH locations to give an indication of the number of people who will be seeing the advertisement on a given day.

TODO

- Source billboard locations (in the US probably).
- Select location have a few controls to filter events.
- Present top-level stats about the number of people who will be nearby in a given period.

I think largely based on the other streamlit demo apps but more geared towards OOH.

## Running the app

To run the app locally:

```
$ cd ooh-events
$ python3 -m venv .venv
$ 
$ source .venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ 
$ streamlit run main.py
```

You'll need to get an API token by following the instructions at [https://docs.predicthq.com/api/authenticating](https://docs.predicthq.com/api/authenticating) and create a [Streamlit secrets](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management) file `.streamlit/secrets.toml` with the following contents:

```
api_key = "<your API token>"
```

