# Medcenter-like app, that allows users to create, delete and pay for their appointments.

## The main idea
The main idea was to create a chained drop-down list with at least 4 choices using Django, without using any JavaScript at best.

## Installation
```
Install requirements.txt
Set environment variables from .env-template
Migrate DB 
Smtp backend is enabled by default, so change it first if you don't want to send a real email
```
## Features 
```
PayPal integration
Dynamic pages without writing any JavaScript code
```
## Features review
- For the PayPal integration i'm using https://django-paypal.readthedocs.io/en/latest/overview.html library.
- For the drop-down list and another dynamic elements i'm using https://htmx.org/ library, that abstracts all the JavaScript stuff. It is easier to understand, so it was a lot faster for me to get the result using it, than learning JavaScript from scratch (i spent around 3 days to make it work). It is also getting more and more popular amongst Django community. It was mentioned multiple times at the DjangoCon 2022.

## Quick note
Some pages are not dynamic, because i didn't have direct access to their html pages (like Django auth templates), or
simply wasn't able to change them in a proper way, because htmx requires strong understanding of the front-end part, like the DOM structure, etc. But i was able to implement what i initially wanted and even more (there is also a dynamic quick search bar, self-cleaning flash messages, etc.). PayPal integration also wasn't even in my plans, i just wanted to add something more interesting than dummy user balance table.
