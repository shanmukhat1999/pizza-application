# Project 3

Web Application for Pizza Ordering

This web application is useful for ordering pizzas and updating the status of orders.

This web application is written mainly in Python (using Django web framework). Data of the items in menu and users' details are stored in SQLite database. Web pages are written using HTML and Javascript with minor styling.


User Guide :

1. When user enters the website, a welcome screen is displayed, which contains two options: Login and Register.
2. Login is to be chosen when a user is already registered. Else user needs to enter details and register before logging in.
3. After logging in, user can see the menu which contains various items and the details of each item such as name, type, price etc. User can add an item to cart by clicking on the '+' symbol beside the item. Clicking on '+' will also increase the quantity of the item in cart by 1, if it's already present in cart.
4. Cart is also displayed at the top on the same page. If user wants to remove an item from cart or reduce the quantity of an item, '-' symbol beside the item in cart can be used.
5. The total price of the item is displayed along the details of all the items in the cart. User can click on Place Order button to order the item.
6. User can go to My Orders page to view all the orders placed and the status of the orders.
7. There is also an admin page which can only be accessed by the person who accepts the orders. Using that page restaurant can view all the details of all the orders and along with the details of users who placed the orders. And the status of the orders from 'Pending' to 'Completed' or 'Could not be Completed' by the restaurant. This status will get reflected in the My Orders page of the users.
8. Users or the Admin can use the logout option to logout.


Future Improvements:

1. Integrating payment gateway in the application to accept online payments while placing orders.
2. Updating customers by an SMS to mobile or an email, whenever the status of the order is changed by the restaurant.
3. Adding delivery options and tracking delivery. 
4. Verifying users before activating account, by sending OTP to phone or email.
5. Styling the application in a more user friendly way and encrypting users' passwords.

Link for ordering - https://shan99.herokuapp.com/
Link for admin - https://shan99.herokuapp.com/admin/
