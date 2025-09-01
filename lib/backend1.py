import base64

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from rich.console import Console

console = Console()

# 加密函数
def encrypt(plaintext, password):
    salt = get_random_bytes(16)  # 随机盐
    iv = get_random_bytes(16)  # 随机IV
    console.print(f"salt: [bold cyan]{salt.hex()}")
    console.print(f"iv:   [bold cyan]{iv.hex()}")
    # 用PBKDF2生成密钥（32字节用于AES-256）
    key = PBKDF2(password, salt, dkLen=32, count=100000)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    return salt + iv + ciphertext  # 组合盐、IV和密文


# 解密函数
def decrypt(ciphertext, password):
    salt = ciphertext[:16]  # 提取盐
    iv = ciphertext[16:32]  # 提取IV
    console.print(f"salt: [bold cyan]{salt.hex()}")
    console.print(f"iv:   [bold cyan]{iv.hex()}")
    actual_ciphertext = ciphertext[32:]
    key = PBKDF2(password, salt, dkLen=32, count=100000)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(actual_ciphertext), AES.block_size)
    return decrypted.decode('utf-8')


def bytes_to_base64(data):
    return base64.b64encode(data).decode('utf-8')


if __name__ == '__main__':
    # 使用示例
    password = "123"
    plaintext = "需要加密的字符串"
    encrypted = encrypt(plaintext, password)
    print("加密后:", bytes_to_base64(encrypted))
    decrypted = decrypt(encrypted, password)
    print("解密后:", decrypted)
