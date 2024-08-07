.. _pdf:

=======================================
You can deeplink to a specific PDF page
=======================================

2024 Jul 11

Just append ``#page=X`` to your URL, where ``X`` is a placeholder for
the page you want to link to. For example, the following link should
jump you to page 70 of the Raspberry Pi Pico getting started guide. You should
see a section titled ``Debug with a second Pico``:
https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf#page=70

------------------------
Browser/OS compatibility
------------------------
.. _PDF navigation features: https://pdfa.org/pdf-fragment-identifiers/#Browser_support_for_basic_PDF_navigation_features

`evilpie <https://lobste.rs/s/arffew/you_can_deeplink_specific_pdf_page#c_36prye>`_
linked me to a comprehensive report on the state of `PDF navigation features`_.

.. raw:: html

   <style>
     table {
       border-collapse: collapse;
     }
     td, th {
       border: 1px solid black;
       padding: 1em;
     }
   </style>

.. csv-table::
   :header: "Browser", "OS", "Works?", "Source"

   "Firefox", "Android", "Yes", "`crmsnbleyd <https://lobste.rs/s/arffew/you_can_deeplink_specific_pdf_page#c_ntwysl>`_"
   "Chrome 126", "gLinux", "Yes", "Me"
   "Firefox 115", "gLinux", "Yes", "Me"
   "Safari", "iOS", "No", "`rodaine <https://lobste.rs/s/arffew/you_can_deeplink_specific_pdf_page#c_ipxulb>`_"
   "Safari", "macOS 14.5", "Yes", "`hoistbypetard <https://lobste.rs/s/arffew/you_can_deeplink_specific_pdf_page#c_3zs0tn>`_"
   "Edge 103", "Windows 10", "Yes", "`ine <https://lobste.rs/s/arffew/you_can_deeplink_specific_pdf_page#c_jk0wl7>`_\*\*"

\*\* update yer machine :P
