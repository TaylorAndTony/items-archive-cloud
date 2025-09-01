import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes


def encrypt_string(plaintext, password):
    # 生成随机salt和IV
    salt = get_random_bytes(16)
    iv = get_random_bytes(16)

    # 处理密码：使用SHA-256哈希将任意长度密码转换为32字节密钥
    key = hashlib.sha256((password + salt.hex()).encode('ascii')).digest()

    # 加密
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))

    # 返回salt(16字节) + iv(16字节) + 密文，均使用base64编码
    combined = salt + iv + ciphertext
    return base64.b64encode(combined).decode('utf-8')


def decrypt_string(encrypted, password):
    # 解码base64
    combined = base64.b64decode(encrypted)

    # 取出salt和iv
    salt = combined[:16]
    iv = combined[16:32]

    # 取出密文
    ciphertext = combined[32:]

    # 处理密码
    key = hashlib.sha256((password + salt.hex()).encode('ascii')).digest()

    # 解密
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    # 去除填充
    plaintext = plaintext.rstrip(b'\0')

    return plaintext.decode('utf-8')


# 示例用法
if __name__ == "__main__":
    password = "123"  # 支持任意长度的ASCII字符
    plaintext = "这是一个测试字符串，将被加密"

    encrypted = encrypt_string(plaintext, password)
    print(f"加密结果: {encrypted}")
    decrypted = decrypt_string(encrypted, password)
    print(f"解密结果: {decrypted}")
