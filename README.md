# Restaurant Management System

## 📋 Overview  
This is a **Restaurant Management System** built with **Django**. It includes features for restaurant owners to manage their restaurants, menus, and foods, as well as for customers to interact with restaurants through comments and likes. The project also supports API endpoints and uses **django-allauth** for user authentication.

---

## 🛠️ Features  

### Users  
- User registration, login, and logout (via `django-allauth`).
- Password management (change, reset, set).
- User profile management.
  
### Restaurant Dashboard  
- CRUD operations for restaurants, menus, and foods.
- Commenting, liking, disliking, and replying to comments.
- API endpoints for restaurant and food-related features.

---

## 📂 Directory Structure  
The project is structured into several apps, each responsible for different functionalities:  

- `accounts`: Handles user registration, login, and profile management.  
- `restaurant-dashboard`: Manages restaurant, menu, and food operations.  

---

## 🚀 API Endpoints  

### Authentication (via Allauth)  
- `/accounts/login/` - User login  
- `/accounts/logout/` - User logout  
- `/accounts/signup/` - User registration  
- `/accounts/profile/` - User profile  

### Restaurant Management  
- `/restaurant-dashboard/` - List all restaurants  
- `/restaurant-dashboard/create/` - Create a new restaurant  
- `/restaurant-dashboard/update/<uuid:pk>/` - Update a restaurant  
- `/restaurant-dashboard/delete/<uuid:pk>/` - Delete a restaurant  
- `/restaurant-dashboard/detail/<uuid:pk>/` - View restaurant details  

### Menu Management  
- `/restaurant-dashboard/menus/<uuid:restaurant_id>/` - List menus for a restaurant  
- `/restaurant-dashboard/menu/create/<uuid:restaurant_id>/` - Create a menu  
- `/restaurant-dashboard/menu/update/<uuid:pk>/` - Update a menu  
- `/restaurant-dashboard/menu/delete/<uuid:pk>/` - Delete a menu  

### Food Management  
- `/restaurant-dashboard/foods/<uuid:restaurant_id>/` - List foods for a restaurant  
- `/restaurant-dashboard/food/create/<uuid:restaurant_id>/` - Create food  
- `/restaurant-dashboard/food/update/<uuid:pk>/` - Update food  
- `/restaurant-dashboard/food/delete/<uuid:pk>/` - Delete food  
- `/restaurant-dashboard/food/detail/<uuid:pk>/` - Food details  

### Comments  
- **Restaurant Comments:**  
  - `/restaurant-dashboard/<uuid:pk>/comment/create/` - Create a comment  
  - `/restaurant-dashboard/comment/<uuid:pk>/edit/` - Edit a comment  
  - `/restaurant-dashboard/comment/<uuid:pk>/delete/` - Delete a comment  
  - `/restaurant-dashboard/comment/<uuid:comment_pk>/like/` - Like a comment  
  - `/restaurant-dashboard/comment/<uuid:comment_pk>/dislike/` - Dislike a comment  

- **Food Comments:**  
  - `/restaurant-dashboard/food/<uuid:pk>/comment/create/` - Create a comment  
  - `/restaurant-dashboard/food/comment/<uuid:pk>/update/` - Edit a comment  
  - `/restaurant-dashboard/food/comment/<uuid:pk>/delete/` - Delete a comment  

---

## ⚙️ Installation  

1. Clone the repository:  
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:  
   ```bash
   python manage.py migrate
   ```
4. Run the server:  
   ```bash
   python manage.py runserver
   ```

---

## 📌 Requirements  

- Python (>=3.9)  
- Django (>=4.x)  
- django-allauth  
- djangorestframework  

---

## 📜 License  
This project is licensed under the MIT License.  

---

Does this look good? Let me know if you want any changes! 😊