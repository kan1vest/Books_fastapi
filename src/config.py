from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings): 
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    PSW_ADMIN: str
    SECURITY_USER_JWT_SECRET_KEY: str
    SECURITY_USER_JWT_ACCESS_COOKIE_NAME: str
    SECURITY_USER_JWT_TOKEN_LOCATION: str
    SECURITY_USER_JWT_DECODE_AUDIENCE: str
    SECURITY_ADMIN_JWT_SECRET_KEY: str
    SECURITY_ADMIN_JWT_ACCESS_COOKIE_NAME: str
    SECURITY_ADMIN_JWT_TOKEN_LOCATION: str
    SECURITY_ADMIN_JWT_DECODE_AUDIENCE: str

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        # DSN
        # postgresql+psycopg://postgres:postgres@localhost:5432/sa
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    # Пароль админа
    @property
    def ADMIN_psw(self):
        # admin psw
        return self.PSW_ADMIN
    # Настройки JWT для user
    @property
    def SECURITY_USER_JWT_secret_key(self):
        
        return self.SECURITY_USER_JWT_SECRET_KEY
    
    @property
    def SECURITY_USER_JWT_access_cookie_name(self):
        
        return self.SECURITY_USER_JWT_ACCESS_COOKIE_NAME
    
    @property
    def SECURITY_USER_JWT_token_location(self):
        
        return [self.SECURITY_USER_JWT_TOKEN_LOCATION]
    
    @property
    def SECURITY_USER_JWT_decode_audience(self):
        
        return [self.SECURITY_USER_JWT_DECODE_AUDIENCE]
    # Настройки JWT для admin 
    @property
    def SECURITY_ADMIN_JWT_secret_key(self):
        
        return self.SECURITY_ADMIN_JWT_SECRET_KEY
    
    @property
    def SECURITY_ADMIN_JWT_access_cookie_name(self):
        
        return self.SECURITY_ADMIN_JWT_ACCESS_COOKIE_NAME
    
    @property
    def SECURITY_ADMIN_JWT_token_location(self):
        
        return [self.SECURITY_ADMIN_JWT_TOKEN_LOCATION]
    
    @property
    def SECURITY_ADMIN_JWT_decode_audience(self):
        
        return [self.SECURITY_ADMIN_JWT_DECODE_AUDIENCE]
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()


