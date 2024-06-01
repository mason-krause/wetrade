.. _api_client:

==================================
Using ``wetrade``'s API Client
==================================

``wetrade``'s API Client manages requests sent to E-Trade's web API. In 
general, you will only want a single :class:`APIClient <wetrade.api.APIClient>`
(or :ref:`UserSession <user_session>`) active at one time. Most of the time, 
users will include their :class:`APIClient <wetrade.api.APIClient>` as a parameter
when creating a new :ref:`Quote <quote>`, :ref:`Order <order>`, or :ref:`Account
<account>` object (as detailed in :ref:`getting started <getting_started>`), but 
advanced users can also use :class:`APIClient <wetrade.api.APIClient>` to interact
with the API directly. 

.. autoclass:: wetrade.api.APIClient
  :members:
  :undoc-members:

