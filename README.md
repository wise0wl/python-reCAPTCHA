# python-reCAPTCHA - 0.1.0

reCAPTCHA is a free CAPTCHA service that protects your site against spam,
malicious registrations and other forms of attacks where computers try to
disguise themselves as a human.

**python-reCAPTCHA** is a Python **3.x** module, that provides an easy
way to interact with the [reCAPTCHA API](http://www.google.com/recaptcha).

## Installation

    $ git clone https://github.com/rbika/python-reCAPTCHA.git
    $ cd python-reCAPTCHA
    $ python setup.py install
    $ cd .. && rm -rf python-reCAPTCHA

## Usage
To use reCAPTCHA, you need to [sign up for API
keys](http://www.google.com/recaptcha/whyrecaptcha) for your site.

Once you've signed up for API keys, adding reCAPTCHA to your site consists of
two steps.

### 1. Displaying the reCAPTCHA Widget
Generate the widget HTML by calling the `generate_html` function.

    >>> from recaptcha.captcha import generate_html
    >>>
    >>> public_key = "your_public_key"
    >>> recaptcha_html = generate_html(public_key)
    >>>
    >>> print(recaptcha_html)
    <script type="text/javascript" src="http://www.google.com/recaptcha/api/challenge?k=your_public_key"></script><noscript><iframe src="http://www.google.com/recaptcha/api/api/noscript?k=your_public_key"height="300" width="500" frameborder="0"></iframe><br><textarea name="recaptcha_challenge_field"rows="3" cols="40"></textarea><input type="hidden" name="recaptcha_response_field"value="manual_challenge"></noscript>

Place the generated HTML inside your form. If you are working with Django por
example, your form will looks like this:

    <form action="">
        {% autoscape on %}recaptcha_html{% endautoescape %}
        <input type="submit" value="Submit">
    </form>

### 2. Verifying user's anwser
After the user submit the anwser, you should get the required paramenters and
call the `verify` function. Again, a Django's example.

    >>> from recaptcha.captcha import verify
    >>>
    >>> private_key = "your_private_key"
    >>> remote_ip = request.META['REMOTE_ADDR']
    >>> challenge = request.POST.get('recaptcha_challenge_field', '')
    >>> response = request.POST.get('recaptcha_response_field', '')
    >>>
    >>> result = verify(private_key, remote_ip, challenge, response)
    >>>
    >>> print(result)
    {'success': False, 'error': 'incorrect-captcha-sol'}

## Documentation
Documentation will be available soon.
