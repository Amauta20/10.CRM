import bcrypt
from CRM_System.controllers.database_controller import DatabaseController
from CRM_System.models.user import User

class AuthController:
    def __init__(self):
        self.db_controller = DatabaseController()

    def hash_password(self, password):
        """Hashea una contraseña para almacenarla de forma segura."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password, hashed_password):
        """Verifica una contraseña contra su hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def create_user(self, username, password, full_name):
        """Crea un nuevo usuario en la base de datos."""
        # Verificar si el usuario ya existe
        existing_user = self.db_controller.execute_query("SELECT id FROM users WHERE username = ?", (username,))
        if existing_user:
            raise ValueError(f"El nombre de usuario '{username}' ya existe.")

        hashed_password = self.hash_password(password)
        query = "INSERT INTO users (username, password_hash, full_name) VALUES (?, ?, ?)"
        params = (username, hashed_password, full_name)
        user_id = self.db_controller.execute_query(query, params)
        return user_id

    def authenticate_user(self, username, password):
        """Autentica a un usuario y devuelve el objeto User si es exitoso."""
        query = "SELECT id, username, password_hash, full_name FROM users WHERE username = ?"
        params = (username,)
        result = self.db_controller.execute_query(query, params)

        if not result:
            return None  # Usuario no encontrado

        user_data = result[0]
        user_id, db_username, hashed_password, full_name = user_data

        if self.verify_password(password, hashed_password):
            return User(id=user_id, username=db_username, full_name=full_name)
        
        return None # Contraseña incorrecta
