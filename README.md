# Restaurant Food Order App

This is a restaurant food order CLI application that allows users to place food orders, view past orders, view current orders, and add, modify, or remove items in an order. The backend of the application is powered by SQLAlchemy ORM, managing the database interactions.

## Features

- Place Food Orders: Users can browse the menu and place new orders.
- View Past Orders: Users can view their past orders.
- View Current Order: Users can see their current order and its details.
- Add/Modify/Remove Items in Order: Users can customize their orders by adding, modifying, or removing items.

## Installation

1. Clone the repository.

```bash
git clone https://github.com/sherylmichaela/phase-3-restaurant-food-order-app.git
cd phase-3-restaurant-food-order-app
```

2. Set up a virtual environment.

```bash
pipenv shell
```

3. Install the dependencies.

```bash
pipenv install
```

## Usage

### Running the Application

```bash
python cli.py
```

### Interacting with the Application

- Place an Order

  - Type in your Australian mobile number
  - Browse the menu and select items to add to your order
  - View details of the current order
  - Add new items from the menu to your current order
  - Modify quantities of existing items
  - Remove items from your order if necessary
  - Submit the order

- View Past Orders

  - Navigate to the 'View Past Orders' in the maain menu

## Database Schema

The application uses SQLAlchemy ORM to handle database interactions. Below are the primary models:

### Customer

Represents a customer in the system.

| Column     | Type    | Description            |
| ---------- | ------- | ---------------------- |
| id         | Integer | Primary key            |
| first_name | String  | First name of customer |
| last_name  | String  | Last name of customer  |
| mobile     | String  | Mobile number          |

### MenuItem

Represents an item on the restaurant's menu.

| Column    | Type    | Description       |
| --------- | ------- | ----------------- |
| id        | Integer | Primary key       |
| item_name | String  | Name of the item  |
| price     | DECIMAL | Price of the item |

### Order

Represents an order placed by a customer.

| Column          | Type     | Description                |
| --------------- | -------- | -------------------------- |
| id              | Integer  | Primary key                |
| order_date_time | DateTime | Date and time of the order |
| customer_id     | Integer  | Foreign key to `customers` |

### OrderDetail

Represents the details of an order, linking menu items to an order.

| Column       | Type    | Description                            |
| ------------ | ------- | -------------------------------------- |
| id           | Integer | Primary key                            |
| order_id     | Integer | Foreign key to `orders`                |
| menu_item_id | Integer | Foreign key to `menu_items`            |
| quantity     | Integer | Quantity of the menu item in the order |

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License.

## Acknowledgements

SQLAlchemy for the ORM.
