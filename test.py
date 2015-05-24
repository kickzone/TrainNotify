#!C:\Python34\python.exe

import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("Content-Type: text/plain")
print()

plugin = "jreast"
module = __import__(plugin)
result = module.notify(["中央線快速電車"])
print(result)