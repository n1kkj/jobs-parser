import os
from dotenv import load_dotenv

load_dotenv('.env')

DB_HOST = os.getenv('DB_HOST', 'db')

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_DB = os.getenv('REDIS_DB', 0)

REDIS_DATABASE_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

FILE_NAME = os.getenv('FILE_NAME', 'result.xlsx')
GOOGLE_API_KEY = {
  "type": "service_account",
  "project_id": "jobs-parser-438410",
  "private_key_id": "9ce775b2c3de912162ce2a10ddd09853551c1b92",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCfJDQcAGpJD/y0\nZkmNJeq6T1l6VGizn6RI8bO4ZDSifnUsr1lxrMfqqnl7TMvt9a16qKx17SbFvCM6\nAkDAbGciGIDumGXAI4gWx++ECCgLXLw1K0xlT/S+rPmWwC7nlh84NOKEB9HqhUHC\nqBKUB4gRiqqEHBZwq4s0j3kCK6wyUU1UikzuRw6vUhVFY1HyZ2xaKYa+9n8Plg09\njbvOl6Gq7F04AnBJtVZdzXCCd6HKBD+ex9xVzfvQI+0dhiWZSzKQdRefzLx2aksC\n/cx0XFS095OECf61ghmzq4b5BqjfzB+2+IKl+Fd1bunTWJrGSTfKCKGcNIIGioPP\nuqRvaAs5AgMBAAECggEADLI6OAuubxLH8eqBLrIaNm/zLwfB7KatWCZ0VJ8l9drJ\n5V098Qw8TNP56iTX1i21/+WqEKRxZfAbDVs1qERdvAIhcyeUYo5TIqIj0TBHZZSp\n7UH9j82ftICfTvAZLd+zsOvDMI5hKGkmNG3tQYMST3f1H6IQBkAhVHmnyU0LqV3j\n6ONjdqewZdvIt9IjUPqDkQvnyKOuW3ugbuEv5Tx/ggHTiy7xC8zW16Qcw83d6pmP\nNSw3LMeXUdOn6M7YLlfWpxB+efSfpIfVraiG0OYnVcXTEAD5cW0dEl/J9g4jMMv2\nojwWFQ+lC8rL8kbM/X4kmmQFTO530MFA0WpHTOmqawKBgQDQfP/QgBnirf3Hr+25\nwdn8Msj0NmcisHjzeyKC3lMvzsLpuBoAxFe1QJUvCwGJcK8wKSM27u9Qy4PYWSXe\nbFo0Q75PZ3GsV4QmzV3uCIazwFvsGjyJATVKnJyFKQ3x58gYt40VDXRQ7Xjwg7Ac\nk8A/+DzGW1C2/aHxzbBAuJvhjwKBgQDDaFtwwC5YKr4baqxaLE0TJZEmw9Sq02Zz\nT7fu3LZLf2kmFu7pczTP7FU+/4V7pXhSn+bG/YOeGJQlr3TqjdAEcv7UDAoyXMOc\n2mwE1fyK2kIooi5Vo4cTBqm8g4MLxmKA9BL2RGMeFcnGCz7eMsX4dFIs7NUqbVn8\n+4xfyaZStwKBgQC88IrkaTMMOqHCVa0aqpLh+yQiLStKRKNYBD9CWjkJGleJd04Z\nY9YYbG7GMzMxWu1ot98x6Vb34XeamS+4Ynlc5AeT7isWBDm+8F4vWYq5W5nyXdR+\nVJn3A/bUtl/s2iB8RduVOJwwuwTe8ninbT7MuipZmGeNbk1U1RLllGewAQKBgQCs\nLkEcWYq8j3URzW3uyshjTZ/Xy4iRuVK12pGU/I/4eF0bfeuocqYfa/w1VYu1xrj9\n/P2pa2rVHI01o6PepXSc5wMZrz4w4EJQ7LlvjWpIo0bWbQls1nnHzwAzJqKK9pSH\nUgl/TAUWVlaDlhcgTRbZ9Q0PnuO5zb8URkaLhLB0gwKBgHqdKIACtZVQxyaEUFcg\nPx/RkRAPGHZqFSYxLl+yj6oYmMxDgdAjJwMaEuDVRCgrvY1/H3ThI9+rL62bmQPS\nkTvOut9YiImSChVqaHsnVdUJtxSOudUKRFO3xlHaZckOGZtbNJBO+h0QvJuGnovT\n77spsprnQFfIkDFlUZpd8+AR\n-----END PRIVATE KEY-----\n",
  "client_email": "prom-154@jobs-parser-438410.iam.gserviceaccount.com",
  "client_id": "115981825621299350238",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/prom-154%40jobs-parser-438410.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
GOOGLE_SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID', '1RZYaxU30CqtQEMGBKXbNyEZBMY6i4yS0RSKteD0Loxg')
GOOGLE_SPREADSHEET_ID_VACANCIES = os.getenv(
    'GOOGLE_SPREADSHEET_ID_VACANCIES', '1QCQ_RbCV7bj2dNFqW2HHru6xyXa_1yQaDZcQOgIt7vc'
)

# BOT_TOKEN = '7357401151:AAE8Q17dpROq1szPxchFmu-Tjo0-pzipoxI'
BOT_TOKEN = '7357401151:AAGz3IHeF1QYen2e37ZvQiMT2YpE9RhVdgQ'

DELETE_ALL = False
INCLUDE_PREVIOUS = False

API_ID = '10606035'
API_HASH = '1c23dd853c00089eaa875fb2cb4f9a3b'

donors_id = [
    -1001648398214,
    -1001648398214,
    -1001721582614,
    -1001561915720,
]
