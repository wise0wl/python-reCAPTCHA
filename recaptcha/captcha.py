# -*- coding: utf-8 -*-

'''
recaptcha.captcha
-----------------

Python interface for the reCAPTCHA service.

:copyright: (c) 2014 Rafael Bicalho.
:license: MIT, see LICENSE for more details.
'''

from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# Globals {{{
_API_URL = 'http://www.google.com/recaptcha/api'
_API_SECURE_URL = 'https://www.google.com/recaptcha/api'

_WIDGET_HTML = '''
<script type="text/javascript" src="%s/challenge?k=%s"></script>
<noscript>
<iframe src="%s/api/noscript?k=%s" height="300" width="500" frameborder="0">
</iframe><br>
<textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
<input type="hidden" name="recaptcha_response_field" value="manual_challenge">
</noscript>
'''  # }}}


def generate_html(public_key, ssl=False):
    '''Generate the code snippet needed to display the reCAPTCHA widget.

    **Args**: your reCAPTCHA's public key and a boolean that defines if SSL
    should be used or not.

    **Returns**: a HTML formatted string. It should be placed inside a web form
    to display the reCAPTCHA widget.
    '''

    public_key = public_key.strip()
    html = ''

    if public_key:
        url = _API_SECURE_URL if ssl else _API_URL
        html = _WIDGET_HTML % (url, public_key, url, public_key)

    return html


def verify(private_key, remote_ip, challenge, response, ssl=False):
    '''Verify if the awnser entered by the user is correct.

    **Args**: your reCAPTCHA's private key, the IP address of the user who
    solved the CAPTCHA, the value of "recaptcha_challenge_field" sent via the
    form, the value of "recaptcha_response_field" sent via form and a boolean
    that defines if SSL should be used or not.

    **Returns**: A dict containing the keys "success" and "error". "success" is
    either True or False, and "error" contains a string with an error code. For
    example: ``{'success': False, 'error': 'invalid-site-private-key'}``

    If "success" is True the error key is an empty string.

    **Error Code Reference**:

    - invalid-site-private-key: Not able to verify the private key.
    - invalid-request-cookie: The challenge parameter of the verify script was
      incorrect.
    - incorrect-captcha-sol: The CAPTCHA solution was incorrect.
    - captcha-timeout: The solution was received after the CAPTCHA timed out.
    - recaptcha-not-reachable: Unable to contact the reCAPTCHA verify server.
    '''

    private_key = private_key.strip()
    remote_ip = remote_ip.strip()
    challenge = challenge.strip()
    response = response.strip()
    result = {}

    if private_key and remote_ip and challenge and response:
        data = {
            'privatekey': private_key,
            'remoteip': remote_ip,
            'challenge': challenge,
            'response': response
        }

        header = {
            'Content-type': 'application/x-www-form-urlencoded',
            'User-agent': 'python-reCAPTCHA'
        }

        url = _API_URL + '/verify' if not ssl else _API_SECURE_URL + '/verify'
        enc_data = urlencode(data).encode('UTF-8')
        api_request = Request(url, enc_data, header)

        try:
            socket = urlopen(api_request)

            api_response = socket.read().decode('UTF-8').splitlines()

            if api_response[0] == 'true':
                result['success'] = True
                result['error'] = ''

            else:
                result['success'] = False
                result['error'] = api_response[1]

        except IOError:
            result['success'] = False
            result['error'] = 'recaptcha-not-reachable'

        except URLError as err:
            result['success'] = False
            result['error'] = 'urllib error: %s' % err

        finally:
            socket.close()

    else:
        result['success'] = False

        if not private_key:
            result['error'] = 'invalid-site-private-key'

        elif not remote_ip:
            result['error'] = 'invalid-remote-ip'

        elif not challenge:
            result['error'] = 'invalid-request-cookie'

        elif not response:
            result['error'] = 'incorrect-captcha-sol'

    return result

# vim:foldmethod=marker
