# Atlassian Coding Challenge

---

## Description

Please write, in your preferred language, code that takes a chat message string and returns a JSON string containing information about its contents. Special content to look for includes:

1. **Mentions -** A way to mention a user. Always starts with an '@' and ends when hitting a non-word character. 
2. **Emoticons -** For this exercise, you only need to consider 'custom' emoticons which are ASCII strings, no longer than 15 characters, contained in parenthesis. You can assume that anything matching this format is an emoticon.
3. **Links -** Any URLs contained in the message, along with the page's title.

For example, calling your function with the following inputs should result in the corresponding return values.

**Input:** "@chris you around?"

**Return (string):**

    {
      "mentions": [
        "chris"
      ]
    }


**Input:** "Good morning! (megusta) (coffee)"

**Return (string):**

    {
      "emoticons": [
        "megusta",
        "coffee"
      ]
    }


**Input:** "Olympics are starting soon; http://www.nbcolympics.com"

**Return (string):**

    {
      "links": [
        {
          "url": "http://www.nbcolympics.com",
          "title": "NBC Olympics | Home of the 2016 Olympic Games in Rio"
        }
      ]
    }


**Input:** "@bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016"

**Return (string):**

    {
      "mentions": [
        "bob",
        "john"
      ],
      "emoticons": [
        "success"
      ],
      "links": [
        {
          "url": "https://twitter.com/jdorfman/status/430511497475670016",
          "title": "Justin Dorfman on Twitter..."
        }
      ]
    }

---




**Dependencies:**

* python3
* virtualenv

In the project directory:
Run the following commands inside the project directory:
```
virtualenv -p python3 venv
source venv/bin/activate 
pip install -r requirements.txt
```

**How to use:**

To start the application run the following command:
```
python run.py runserver
```

**Go to your browser**

Default server is 127.0.0.1 and port is 5000

* http://127.0.0.1:5000/api/v1/parse-message
* http://127.0.0.1:5000/api/v1/parse-message?input=@atlassian%20(smile)%20http://www.atlassian.com
* http://127.0.0.1:5000/

Displays logs of the requests and their total count
* http://127.0.0.1:5000/api/v1/stats

**To run the tests:**

```
python run.py tests
```     

**Project Structure:**

```
atlassian/
├── README.md
├── config.py
├── parser
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── route.py
│   ├── helper
│   │   ├── __init__.py
│   │   ├── emoticons.py
│   │   ├── links.py
│   │   ├── mentions.py
│   │   ├── regex.py
│   │   └── stats.py
│   └── main
│       ├── __init__.py
│       └── route.py
├── requirements.txt
├── run.py
└── tests
    ├── __init__.py
    ├── test_emoticons.py
    ├── test_links.py
    ├── test_mentions.py
    ├── test_parse_mentions_using_patch.py
    └── test_parse_message_using_mocks.py
```    

**Scaling issue:**

* Currently only one request can be handled at a time by server.
* Server cannot listen for other requests when its processing.

**Possible solutions:**

* We buffer all the request in the queue to process them later when server becomes free.
* Create one or more threads/process to serve requests
* Run the application on multiple servers and use a load balancer to distribute the requests.


**External Libraries:**

**Flask:**

Using this lightweight framework to create rest api's.

**Flask-script:**

Used flask-script to take input from the command line argument when running the project. 
Flask-script extension helps to do the tasks outside the web appication
like running the development server, a customized python shell, to set up the database, cronjobs and other command line task

**Injector:**

Using injector to do dependency injection. We use dependency injection to make class more testable. 
Flask-Injector is a dependency-injection framework that avoid using global Flask objects and make testing modular and simple and decouples your code

**Mock:**

Using mock library to mock certain functionality of classes for testing.
Python provides standard unittest.mock library also.

**Webargs:**

Used for parsing and validating HTTP request arguments.

**Virtualenv:**

Using virtualenv to create isolated Python environments.

**BeautifulSoup:**

Using it for Html Parsing, to extract title.
