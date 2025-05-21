from OpenSSL import crypto
import os

def generate_self_signed_cert():
    # Generate key
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)

    # Generate certificate
    cert = crypto.X509()
    cert.get_subject().C = "RU"
    cert.get_subject().ST = "Moscow"
    cert.get_subject().L = "Moscow"
    cert.get_subject().O = "STT Whisper"
    cert.get_subject().OU = "Development"
    cert.get_subject().CN = "localhost"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365*24*60*60)  # Valid for one year
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)

# Добавляем SAN
    san_list = "DNS:localhost, DNS:whisper-api, IP:192.168.6.28, IP:127.0.0.1"
    cert.add_extensions([
        crypto.X509Extension(
            b"subjectAltName", False, san_list.encode()
        )
    ])
    cert.sign(k, 'sha256')

    # Write certificate
    with open("cert.pem", "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    
    # Write private key
    with open("key.pem", "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

if __name__ == "__main__":
    generate_self_signed_cert()
    print("SSL certificates generated successfully!") 