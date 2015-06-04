Configuration
=============

Introduction
------------

When you define a :doc:`view <views>`, a :doc:`path <paths_and_linking>`,
a :doc:`setting <settings>`, a :doc:`tween <tweens>`, or if a third party
package defines that for you, Morepath needs to be told about it.

This is called the Morepath *configuration*.


How it works
------------

Morepath needs to be configured before it is run. That means that you need
to run the necessary configuration steps, before you pass a new instance
of your application to your WSGI server::

  if __name__ == '__main__':
      config = morepath.setup()
      config.scan()
      config.commit()
      morepath.run(App())

Morepath will always scan itself first, then whatever packages you whish to
scan. In the example above, it scans itself during ``morepath.setup``, handing
over the configuration object to you.

``config.scan`` will then scan whatever package it is handed. If it receives
no package, it will scan the package it is called from. That's the current
file in the example above.

Once all scanning is completed, the configuration is committed and the
application may be run.

Scanning dependencies
---------------------

Morepath aims to be a micro framework, so you probably want to use other
packages that add extra functionality to Morepath. For instance, you might use
`more.chameleon <https://github.com/morepath/more.chameleon>`_
for templating or
`more.transaction <https://github.com/morepath/more.transaction>`_
for SQLAlchemy integration.

These packages bring their own Morepath configuration to the table. Said
configuration also needs to be loaded by Morepath before Morepath is run.

Manual scan
~~~~~~~~~~~

If you like to stay away from magic as much as possible, you can use manual
scanning. Say you depend on
`more.jinja2 <https://github.com/morepath/more.jinja2>`_ and you want to
extend the example from above.

This is what you do::

  import more.jinja2

  if __name__ == '__main__':
      config = morepath.setup()
      config.scan(more.jinja2)
      config.scan()
      config.commit()
      morepath.run(App())

As you can see, you need to import your dependency and scan it using
``config.scan``. If you have more dependencies, just add them in this fashion.

Automatic scan
~~~~~~~~~~~~~~

Manual scanning can get tedious as you need to add each and every new
dependency that you rely on.

Instead, you may use the ``autoconfig`` method, which will try to scan
all packages which themselves depend on Morepath. To use this method,
the example from above has to be changed slightly. Note how we no longer
use ``morepath.setup``::

  if __name__ == '__main__':
      config = morepath.autoconfig()
      config.scan()
      config.commit()
      morepath.run(App())


As you can see, we also don't need to import any dependencies anymore. We still
need to run ``config.scan`` without parameters however, so our own file gets
scanned.

That is, unless we move all our configuration into a separate package as well.
Then the file containing the configuration code might not need scanning.

Autosetup
~~~~~~~~~

If you don't need to scan the file you are running the configuration from,
you can get away with very little code.

Combining the automatic scan from above with an automatic commit gives you
this::

  if __name__ == '__main__':
      morepath.autosetup()
      morepath.run(App())

Now that you know how to scan yourself and your dependencies, what if you want
to write your own package that can be scanned automatically?

Read the next part to find out how.

Writing scannable packages
~~~~~~~~~~~~~~~~~~~~~~~~~~

When Morepath looks for packages that it can scan, it has a few requirements
that each package has to fulfill to be considered.

1. The package must be made available using a ``setup.py`` file.

  This should go without saying. Without a ``setup.py`` file your package is
  not really a package in Morepath's eyes. So the package needs to have that
  and it needs to be installed in your current environment (be it in your
  global site-packages, in your virtualenv or in your buildout environment).

2. The package itself or a dependency of the package must include ``morepath``
   in the ``install-requires`` list of the ``setup.py`` file.

  To avoid having to scan *all* packages, Morepath filters out packages which
  in no way depend on Morepath. If your package does, you need to add
  ``morepath`` to ``install_requires``::

    setup(name='mypackage'
      ...
      install_requires=[
        'morepath'
      ])

3. The module to import must be named after the package *(Alternative A)*

  This means that the name inside ``setup.py`` is importable in Python. For
  example: if the module inside the package is named ``myapp``, the package
  must be named ``myapp`` as well (not ``my-app`` or ``MyApp``).

  Morepath tries to import the package name in this case. This is why this
  works::

    import myapp

  But this does not::

    import my-app
    import MyApp

  If you do not follow this naming convention, you don't need to rename
  everything though, you may also tell Morepath explicitly what to do with
  *Alternative* B below.

3. The module to import must be listed in the ``entry_points``
   *(Alternative B)*

  If your package has a name that Morepath cannot import, then you need to tell
  Morepath the actual module name it can. You can also do this if you want
  to be explicit, or if you want Morepath to only scan parts of your package::

    setup(name='my-package'
      ...
      entry_points={
          'morepath': [
              'autoimport = my.package'
          ]
      }

  If Morepath finds such a package, it will use the name in the
  ``entry_points``, import it and then scan it.

  Note that you still need to have ``morepath`` in the ``install_requires``
  list for this to work.

More information
----------------

Even more information and nitty gritty details can be found in the API docs.
See :doc:`api`.
