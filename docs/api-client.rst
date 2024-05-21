.. _api_client:

==================================
Using ``wetrade``'s API Client
==================================

``wetrade``'s API Client manages requests sent to E-Trade's web API. In 
general, you will only want a single **APIClient** (or :ref:`UserSession
<user_session>`) active at one time. Most of the time, users will include their
**APIClient** as a parameter when creating a new Quote, Order, or :ref:`Account
<account>` object (as detailed in :ref:`getting started <getting_started>`), but advanced users can also use 
**APIClient** to interact with the API directly. 

.. autoclass:: wetrade.api.APIClient
  :members:
  :undoc-members:

