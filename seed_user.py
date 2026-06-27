from app.db.compat import users_db

# نضع مستخدم تجريبي داخل الذاكرة
def seed():
    users = users_db()

    users["user1"] = {
        "email": "test@test.com",
        "password": "123",
        "role": "user"
    }

    return users

if __name__ == "__main__":
    data = seed()
    print("Seeded users:", data)
