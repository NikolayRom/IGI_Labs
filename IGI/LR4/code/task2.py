from zipfile import ZipFile

filename = "task2.txt"
filename_result = "task2_result.txt"
zipname = "task2.zip"
data = ""

with open(filename, encoding="utf-8") as fh:
    data = fh.read()

print(data)

result = "Test Result: " + data

with open(filename_result, "w", encoding="utf-8") as fh:
    print(result, file=fh)

with ZipFile(zipname, "w") as zip:
    zip.write(filename_result)

with ZipFile(zipname, "r") as zip:
    print(zip.getinfo(filename_result))

