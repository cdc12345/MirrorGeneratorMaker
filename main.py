'''
 @encoding: utf-8
 @author: "cdc12345"
 @description: "生成镜像生成器"
'''

import zipfile
import sys

def getDictionary():
    return {"gradle-wrapper.properties":["services.gradle.org/distributions", "mirrors.cloud.tencent.com/gradle"]}


def findAndReplace(generator_zip_file:zipfile.ZipFile):
    dictionary = getDictionary()
    print("dictionary: ", dictionary)
    # 重新加个名字
    out = generator_zip_file.filename.replace("generator", "mirror-generator")
    with zipfile.ZipFile(out, mode='w') as output:
        for entry in generator_zip_file.infolist():
            # 获得文件名
            name = entry.filename.split('/').pop()
            # 转为文件类型方便读写
            with output.open(entry.filename, mode='w') as byNeed:
                byteContent = generator_zip_file.read(entry, None)
                if name in dictionary:
                        print("fileName: ", entry.filename)
                        # bytes.decode()
                        content = byteContent.decode()
                        map = dictionary[name]
                        modifiedText = content
                        for i in range(1, len(map) // 2 + 1):
                            # 兼容多个替换
                            modifiedText = modifiedText.replace(map[i - 1], map[i])
                        print(modifiedText)
                        byNeed.write(bytes(modifiedText, "utf-8"))
                else:
                    byNeed.write(byteContent)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        # 参数为1序列
        fileName = sys.argv[1]
        try:
            with zipfile.ZipFile(fileName, 'r') as generator_zip:
                findAndReplace(generator_zip)
        except zipfile.BadZipFile:
            print("Bad Zip: " + fileName)
        print("exit with ", fileName)
    else:
        print("Invalid args size: ", len(sys.argv))
        