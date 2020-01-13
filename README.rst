About stroller2
-------------------------

stroller2 is a Pluggable application for TurboGears2.

Installing
-------------------------------

stroller2 can be installed both from pypi or from github (still not released)::

    pip install stroller2

should just work for most of the users

Plugging stroller2
----------------------------

In your application *config/app_cfg.py* import **plug**::

    from tgext.pluggable import plug

Then at the *end of the file* call plug with stroller2::

    plug(base_config, 'stroller2')

You will be able to access the plugged application at
*http://localhost:8080/commerce*.

Available Hooks
----------------------

stroller2 makes available a some hooks which will be
called during some actions to alter the default
behavior of the appplications:

Exposed Partials
----------------------

stroller2 exposes a bunch of partials which can be used
to render pieces of the blogging system anywhere in your
application:

Exposed Templates
--------------------

The templates used by registration and that can be replaced with
*tgext.pluggable.replace_template* are:

