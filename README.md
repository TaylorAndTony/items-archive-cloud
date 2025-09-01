# 物品归档加密与解密工具

> [!WARNING]
> 本 Readme 由 AI 生成，请勿直接修改。如需修改，请联系 AI 工程师。（这句话也是 AI 写的）

## 项目概述

此项目旨在提供一个简单的加密工具，用于将CSV文件中的物品归档数据加密，并通过一个网页界面进行解密展示。项目包含两个主要部分：加密与写入文件部分，以及通过网页解密和展示数据部分。

## 项目结构
- `main.py`: 主程序，用于加密CSV文件内容，并将加密后的字符串写入`static/data.js`文件。
- `config.example.yml`: 配置文件示例，包含CSV文件路径、加密密码及需要过滤的私有关键词。自行部署需要更名为`config.yml`。
- `lib/__init__.py`: 包含加密和解密功能的库。
- `index.html`: 网页界面，用于解密和展示数据。

## 使用方法

### 1. 配置文件

首先，复制`config.example.yml`为`config.yml`，并根据需要修改配置文件中各项参数：

- `csv_file`: 指定需要加密的CSV文件路径。
- `password`: 设置加密密码，该密码需与解密时使用的密码一致。
- `private`: 列出希望在加密时过滤掉的关键词，包含该关键词的行将被跳过。

### 2. 加密CSV文件

运行`main.py`脚本，程序将读取配置文件中的CSV文件内容，过滤掉包含私有关键词的行，然后使用AES CBC模式加密剩余内容，并将结果写入`static/data.js`文件。最后，程序会提示是否将加密后的文件提交到本地git仓库，并进一步推送到远程仓库。

```python
def encrypt_string(plaintext: str, password: str):
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
```

### 3. 解密和展示数据

打开`index.html`文件，通过浏览器访问。界面将加载`data.js`中的加密数据，并提供解密功能。用户需输入正确的密码以解密数据。解密后的数据将按照每页30项进行分页展示，并支持搜索功能。

```javascript
function decrypt(encryptedText, password) {
    try {
        // 解码base64
        const combined = CryptoJS.enc.Base64.parse(encryptedText);
        const combinedBytes = combined.toString(CryptoJS.enc.Latin1);
        
        // 提取salt(前16字节)、iv(接下来16字节)和密文
        const salt = combinedBytes.substr(0, 16);
        const iv = combinedBytes.substr(16, 16);
        const ciphertext = combinedBytes.substr(32);
        
        // 处理密码：与Python端相同的方式生成密钥
        const saltHex = CryptoJS.enc.Latin1.parse(salt).toString(CryptoJS.enc.Hex);
        const key = CryptoJS.SHA256(password + saltHex);
        
        // 解密
        const decrypted = CryptoJS.AES.decrypt(
            { ciphertext: CryptoJS.enc.Latin1.parse(ciphertext) },
            key,
            {
                iv: CryptoJS.enc.Latin1.parse(iv),
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            }
        );
        
        return decrypted.toString(CryptoJS.enc.Utf8);
    } catch (e) {
        throw new Error("解密失败: " + e.message);
    }
```

## 依赖库

项目依赖于以下Python库：
- `pyyaml`
- `rich`

网页端依赖于以下JavaScript库：
- `CryptoJS`
- `Vue.js`
- `PapaParse`
- `TailwindCSS`
- `Font Awesome`

## 注意事项

- 确保在运行`main.py`前安装了所有依赖库。
- 项目假设CSV文件的第一行是表头。
- 私有关键词过滤是基于行内容的简单字符串匹配。
- 在解密过程中，如果密码不正确，将无法解析数据。