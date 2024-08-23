import requests
from requests.exceptions import HTTPError, Timeout, RequestException


def get_weather(app, city):
    api_key = "Your API key goes here"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["cod"] == 200:
            app.display_weather(data)
    except requests.exceptions.HTTPError as http_error:
        match response.status_code:
            case 400:
                app.display_error("Bad request:\nPlease check your input")
            case 401:
                app.display_error("Unauthorized:\nInvalid API key used")
            case 403:
                app.display_error("Forbidden:\nAccess denied")
            case 404:
                app.display_error("City not found")
            case 500:
                app.display_error("Internal server error:\nPlease try again later")
            case 502:
                app.display_error("Bad gateway:\nInvalid response returned from the server")
            case 503:
                app.display_error("Service currently unavailable:\nServer is down")
            case 504:
                app.display_error("Gateway timeout:\nNo server response")
            case _:
                app.display_error(f"HTTP error occurred:\n{http_error}")
    except requests.exceptions.ConnectionError:
        app.display_error("Connection Error:\nPlease check your internet connection")
    except requests.exceptions.Timeout:
        app.display_error("Timeout Error:\nThe request has timed out")
    except requests.exceptions.TooManyRedirects:
        app.display_error("Too many redirects:\nCheck the URL")
    except requests.exceptions.RequestException as req_error:
        app.display_error(f"Request Error: {req_error}")
