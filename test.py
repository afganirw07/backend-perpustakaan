import bcrypt
hashed = bcrypt.hashpw("test123".encode('utf-8'), bcrypt.gensalt())
print(hashed)
