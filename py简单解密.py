'''
运行前先看看脚本在加密代码前有没有定义变量，有的话自己复制到解密后的脚本里
运行前先看看脚本在加密代码前有没有定义变量，有的话自己复制到解密后的脚本里
运行前先看看脚本在加密代码前有没有定义变量，有的话自己复制到解密后的脚本里
'''
#要解密的文件填下面
name="可乐_1.6.py"
#脚本打印的字符里随便找两个字填下面
ser= "print"
import bz2, base64, lzma, zlib
file=name
namespace = {}
with open(file, "r", encoding="utf-8") as file:
  text =file.read()
  file.close
encoded = b' '
decoded = text.encode("utf-8")
print("读取到的文件内容是：\n"+decoded.decode("utf-8"))

find = b'exec('
find2 = b')'
find3 = ser
if isinstance(find3, str):
 find3 = find3.encode("utf-8")

while True :    
 
 if find in decoded:
    index = decoded.index(find)
    encoded = decoded[index + len(find):]
 if find2 in encoded[::-1]:
    index = encoded[::-1].index(find2[::-1])
    encoded = encoded[:len(encoded) - index - len(find2)]
    decoded2=b'import bz2, base64, lzma, zlib, gzip\ndecoded='+ encoded 
    exec(decoded2, namespace) 
    decoded=namespace['decoded']
    #print(decoded)
 if find3 in decoded:      
    byte_string_str = decoded.decode("utf-8")
    byte_string = byte_string_str.encode("utf-8")
    print("解出来的脚本是：\n"+byte_string_str)      
    with open("output"+name, "w", encoding="utf-8") as file:
        file.write(byte_string_str)
        file.close
        print("导出成功")
    break
   
    