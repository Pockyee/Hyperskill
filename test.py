list = [1, 7, 3, 6, 0, 8, 6, 7, 5, 3]


def mergesort_list(x):
    if len(x) <= 1:
        return x
    else:
        mid = len(x) // 2
        left = mergesort_list(x[:mid])
        right = mergesort_list(x[mid:])
        return merge(left,right)


def merge(left, right):
    new = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            new.append(left[i])
            i += 1
        else:
            new.append(right[j])
            j += 1
    new.extend(left[i:])
    new.extend(right[j:])
    return new

new_list = mergesort_list(list)
print("".join(new_list))
