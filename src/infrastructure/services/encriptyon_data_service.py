#Using RSA and AES encryption to encrypt sensitive data and decrypt it.
import rsa
from Crypto.Cipher import AES
import base64

class EncriptionDataService:
    def __init__(self):
        self.public_key, self.private_key = rsa.newkeys(1024)

    def encrypt_aes_key(self, aes_key: str) -> str:
        """Encrypt the AES key using RSA public key."""
        return base64.b64encode(self.public_key.encrypt(aes_key.encode(), rsa.PKCS1_OAEP)[0]).decode()

    def decrypt_aes_key(self, encrypted_aes_key: str) -> str:
        """Decrypt the AES key using RSA private key."""
        return self.private_key.decrypt(base64.b64decode(encrypted_aes_key.encode()), rsa.PKCS1_OAEP).decode()

    def encrypt_data(self, data: str, aes_key: str) -> str:
        """Encrypt data using AES key."""
        cipher = AES.new(aes_key.encode(), AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

    def decrypt_data(self, encrypted_data: str, aes_key: str) -> str:
        """Decrypt data using AES key."""
        data = base64.b64decode(encrypted_data.encode())
        cipher = AES.new(aes_key.encode(), AES.MODE_EAX, nonce=data[:16])
        return cipher.decrypt_and_verify(data[16:-16], data[-16:]).decode()
        
    def generate_aes_key(self) -> str:
        """Generate AES key."""
        return AES.generate_key().decode()