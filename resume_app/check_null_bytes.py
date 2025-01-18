with open('myproject/urls.py', 'rb') as file:
    content = file.read()
    if b'\0' in content:
        print("Null byte found!")
    else:
        print("File is clean!")
