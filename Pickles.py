import pickle

file = open("pickleJar", "wb")
class example_class:
    a_number = 35
    a_string = "hey"
    a_list = [1, 2, 3]
    a_dict = {"first": "a", "second": 2, "third": [1, 2, 3]}
    a_tuple = (22, 23)


my_object = example_class()

pickle.dump(my_object,open("pickleJar","wb"))

obji = pickle.load(open("pickleJar", "rb"))

print(obji.a_dict)
