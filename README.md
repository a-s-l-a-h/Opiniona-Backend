# Opiniona - Product Review System API 👋

Hey there, and welcome to the backend for **Opiniona**!

This project is a complete, robust RESTful API built with **Django** and **Django REST Framework**. It provides all the necessary functionality for a product review platform, allowing admins to manage products and users to submit reviews. It's built with best practices in mind, including a secure authentication system, role-based permissions, and a clean, test-driven architecture.

So grab a coffee, and let's get you set up!

---

## ✨ Core Features

- 👤 **Full User Authentication**: Secure registration, login (token-based), and logout endpoints.
- 👮 **Role-Based Permissions**: Admins manage products, regular users write reviews.
- 📦 **Complete Product Management**: Admins can create, list, update, and delete products.
- 🖼️ **Optional Image Uploads**: Admins can upload multiple images per product.
- ⭐ **Review System**: Authenticated users can post a rating (1–5) and written feedback.
- 🛡️ **Duplicate Prevention**: A user can only review each product once.
- 📊 **Rating Aggregation**: Products display the average rating from all reviews.
- ✅ **Fully Tested**: Includes a comprehensive test suite.

---

## 🛠️ Technology Stack

- **Backend**: Python 3, Django
- **API Framework**: Django REST Framework
- **Authentication**: DRF Token Authentication
- **Database**: SQLite 3
- **Image Handling**: Pillow

---

## 🏛️ System Architecture (ER Diagram)

Here’s a simple Entity-Relationship (ER) diagram showing how the data is organized:

- A `Product` can have many `Reviews`
- A `User` can write many `Reviews`
- A `Product` can have many `ProductImages`

![ER Diagram](docs/ER_Diagram.png)

---

## 🚀 Getting Started: Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/a-s-l-a-h/Opiniona-Backend.git
cd Opiniona-Backend
2. Create and Activate a Virtual Environment
On Windows (PowerShell):
bash
Copy
Edit
python -m venv venv
.\venv\Scripts\Activate
On macOS / Linux:
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Set Up the Database
bash
Copy
Edit
python manage.py migrate
5. Create an Admin User
bash
Copy
Edit
python manage.py createsuperuser
▶️ Running the Application
bash
Copy
Edit
python manage.py runserver
Your API will be live at: http://127.0.0.1:8000/

✅ Running the Tests
bash
Copy
Edit
python manage.py test
Or test specific apps:

bash
Copy
Edit
python manage.py test products
python manage.py test reviews
📖 API Endpoints Documentation
🔐 Authentication (/api/accounts/)
1. Register
http
Copy
Edit
POST /api/accounts/register/
json
Copy
Edit
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "a-strong-password",
  "password2": "a-strong-password"
}
2. Login
http
Copy
Edit
POST /api/accounts/login/
json
Copy
Edit
{
  "username": "someuser",
  "password": "their-password"
}
Response:

json
Copy
Edit
{
  "token": "a1b2c3...",
  "user_id": 5,
  "is_staff": false
}
3. Logout
http
Copy
Edit
POST /api/accounts/logout/
Token required.

📦 Products (/api/products/)
1. List Products
http
Copy
Edit
GET /api/products/
2. Create a Product (Admin only)
http
Copy
Edit
POST /api/products/
json
Copy
Edit
{
  "name": "Cool Mechanical Keyboard",
  "description": "A keyboard with satisfyingly clicky keys.",
  "price": "149.99"
}
3. View/Update/Delete Product
http
Copy
Edit
GET /api/products/<id>/
PUT /api/products/<id>/
DELETE /api/products/<id>/
4. Upload Image
http
Copy
Edit
POST /api/products/<product_id>/upload-image/
Use multipart/form-data

Key: image

Value: image file

⭐ Reviews (/api/products/<product_id>/reviews/)
1. List Reviews
http
Copy
Edit
GET /api/products/<product_id>/reviews/
2. Submit a Review
http
Copy
Edit
POST /api/products/<product_id>/reviews/
json
Copy
Edit
{
  "rating": 5,
  "feedback": "This product was fantastic!"
}
🧪 Safe Points (Branching)
To save your current working state to a versioned branch:

bash
Copy
Edit
# Make sure all changes are committed
git add .
git commit -m "version 0.1"

# Create and switch to a new branch
git checkout -b version_0.1

# Push the new branch to GitHub
git push -u origin version_0.1

# Optional: Tag the version
git tag version_0.1
git push origin version_0.1
📁 Folder Structure Note
Project documentation, including diagrams, should be placed inside a folder named:

Copy
Edit
docs/
Example:

bash
Copy
Edit
docs/ER_Diagram.png
docs/api_reference.md
That’s it! You’re ready to build, test, and scale Opiniona.

yaml
Copy
Edit

---

Let me know if you’d like this also exported to a Markdown file or auto-linked with version badges.
