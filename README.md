# Buyabook

This app, when completed, will be aimed to serve as a platform where users would be able to register and sell their new or second-hand books to other registered users.
The users would be able to have a view on all books available (through the "Catalogue" menu link, they would be able to see only the books they are selling (through "My Dashboard") and also to filter only the books that they can buy (through the "Buyabook" view).

When a user adds a book in their cart, that is saved in the database so that the user could open their cart from another device to finish the purchase.
If any book remains longer in someone's cart, the seller would be able to "retrieve" the book and make it again "available" for purchase by another user or for editing or for deletion from the personal Dashboard.


Features in the pipeline:
* Completing an order:
When a user wants to complete an order, if no address is presented during registration, this user would be prompted to add that (preferably with pop up window). Then an email will be sent to the seller with the delivery details.
Consider refactoring into a session based cart - pros/cons.
If the user has chosen books from multiple sellers, individual emails would be sent.

* Create a store app:
A new app in the project / model should be introduced as an individual store area for each seller which could be useful for bigger sellers as well as for filtering purposes.

* Adding a category
Create a category input request from a user to 'staff' members so that new categories could be added to the drop down menu.
