from pydantic import BaseSettings


class AppSettings(BaseSettings):
    debug: bool = False
    dev_server_address: str = '0.0.0.0'
    dev_server_port: int = 8080
    secret_key: str = 'INSECURE-CHANGE-ME-6up8zksTD6mi4N3z3zFk'
    db_url: str = 'mysql://pda:pda@127.0.0.1:3306/pda'
    db_host: str = '127.0.0.1'
    db_port: int = 3306
    db_user: str = 'pda'
    db_password: str = 'pda'
    db_name: str = 'pda'
    config: str = 'conf/config.yml'

    class Config:
        env_prefix = 'pda_'
