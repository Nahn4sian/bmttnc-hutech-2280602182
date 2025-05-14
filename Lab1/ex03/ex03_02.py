def daonguoclist (lst):
    return lst[::-1]
input_list = input("nhap danh sach cac so ")
numbers = list(map(int, input_list.split(',')))
listdaonguoc = daonguoclist(numbers)
print(("list sau khi dao nguoc ",listdaonguoc))