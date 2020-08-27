from functools import wraps
from flask import g, request, redirect, url_for, render_template
from app import types as t

def verified_user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print('####')
        # We assume the user is logged in
        if g.user is None:
            return redirect(url_for('auth.login'))

        if g.user.email_verified:
            print('email verified')
            if not(g.user.developer \
                    and g.user.developer.verification_status == \
                        t.VerificationStatus.accepted):
                # Return the landing page
                return render_template('profile/landing_page.html')
            return f(*args, **kwargs)
        return f(*args, **kwargs)
    return decorated_function
