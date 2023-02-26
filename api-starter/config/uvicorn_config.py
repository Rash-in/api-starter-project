import os, uvicorn

'''
Ciphers: Provided from EIS in AppSec Teams Channel

Disallowed ciphers prefixs:   ALL:!aNULL:!ADH:!eNULL:!LOW:!EXP:!NULL:!RC4:!RC2:!DES:!3DES:!SHA:!SHA256:!SHA384:!MD5+HIGH:+MEDIUM

Specific insecure ciphers (TLSv1_2) that appear in openssl:
    AES256-SHA256
    AES128-SHA256
    ECDHE-RSA-AES256-SHA384
    ECDHE-RSA-AES128-SHA256
'''

ssl_ciphers = "ALL:!aNULL:!ADH:!eNULL:!LOW:!EXP:!NULL:!RC4:!RC2:!DES:!3DES:!SHA:!SHA256:!SHA384:!MD5+HIGH:+MEDIUM"
bad_ciphers = [
    "AES256-SHA256",
    "AES128-SHA256",
    "ECDHE-RSA-AES256-SHA384",
    "ECDHE-RSA-AES128-SHA256"
]

for bad_cipher in bad_ciphers:
    ssl_ciphers += f":!{bad_cipher}" 

uvi_config = uvicorn.Config(
    app= "main:tccapi",
    host= "0.0.0.0",
    port= 4443,
    reload= False,
    workers= int(os.environ['UVICORN_WORKERS']),
    access_log= True,
    log_level= "debug",
    proxy_headers= True,
    server_header= False,
    ssl_cert_reqs= 0,
    ssl_ca_certs= os.environ['SSL_CA_PATH'],
    ssl_certfile= os.environ['SSL_CRT_PATH'],
    ssl_keyfile= os.environ['SSL_KEY_PATH'],
    ssl_ciphers= ssl_ciphers,
    ssl_version= 5
)