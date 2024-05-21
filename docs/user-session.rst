.. _user_session:

==================================
Managing Auth with **UserSession**
==================================

``wetrade``'s :ref:`API Client <api_client>` uses a **UserSession** to login to
your E-Trade account and manage handling for timeouts, expired sessions, and
server errors. By default, a **UserSession** will use the configuration specified
in your :ref:`settings.py <settings>`. You can also bypass **UserSession**'s 
error handling using **SimpleUserSession** which is a drop-in replacement. Most
users should let :ref:`API Client <api_client>` create a **UserSession** for them,
but this section may be helpful for development testing and those interested 
in using **SimpleUserSession**.

.. py:class:: wetrade.user_session.UserSession(config=None)

The **UserSession** manages authentication and handling for most expected server
issues. Using **UserSession** directly is not recommended and is generally only
needed for development testing and when using **SimpleUserSession** (below).

.. py:class:: wetrade.user_session.SimpleUserSession(config=None)

This is a simplified version of **UserSession** that bypasses all error and 
exception handling.

