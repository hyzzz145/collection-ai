import os
import csv
# from scrape_copy import scatch,notice_request
import requests

##进入程序文件夹
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# #打开csv，以及初始化
# f = open("content_test.csv",'a',newline="",encoding='utf-8')
# writer = csv.writer(f)

# writer.writerow(["nihao"])

# f.close()

# f = open("content_test.csv",'a',newline="",encoding='utf-8')
# writer = csv.writer(f)

# writer.writerow(["nihao"])

# f.close()

a = ['\t附件名：附件1.福州大学国家级优秀教材培育项目立项申报书.docx']
print(str(a))
print("附件名" in str(a))
with open("test.txt","w") as f:
    f.write(a)

print(a)
print("附件名" in a)
