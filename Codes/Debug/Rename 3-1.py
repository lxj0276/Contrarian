import os; path = os.getcwd()

os.chdir("Result")
file_name_list = os.listdir()

# for old_file_name in file_name_list:
#     if "-" not in old_file_name:
#         print(old_file_name)
#         splitted_file_name = old_file_name.split()
#         splitted_file_name.insert(-1, "3-1")
#         new_file_name = " ".join(splitted_file_name)
#         try:
#             os.rename(old_file_name, new_file_name)
#         except FileExistsError:
#             pass
#     elif "6-1 " in old_file_name:
#         print(old_file_name)
#         splitted_file_name = old_file_name.split()
#         splitted_file_name.remove("6-1")
#         new_file_name = " ".join(splitted_file_name)
#         try:
#             os.rename(old_file_name, new_file_name)
#         except FileExistsError:
#             pass

# for old_file_name in file_name_list:
#     if "3-1 " in old_file_name:
#         splitted_file_name_list = old_file_name.split()
#         index_of_3_1 = splitted_file_name_list.index("3-1")
#         splitted_file_name_list[index_of_3_1], splitted_file_name_list[index_of_3_1+1] \
#             = splitted_file_name_list[index_of_3_1+1], splitted_file_name_list[index_of_3_1]
#         new_file_name = " ".join(splitted_file_name_list)
#         try:
#             os.rename(old_file_name, new_file_name)
#             print("把%s重命名为%s" % (old_file_name, new_file_name))
#         except FileExistsError:
#             pass

for old_file_name in file_name_list:
    if "3-1" in old_file_name:
        os.remove(old_file_name) 

os.chdir(path)