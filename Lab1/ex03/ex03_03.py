def taotuplelist(lst):
    return lst[::-1]
input_list = input("Nhap danh sachc ac so ")
numbers - list(map(int, input_list.split(',')))

mytuple = taotuplelist(numbers)
print("list",numbers)
print("tuple", mytuple)