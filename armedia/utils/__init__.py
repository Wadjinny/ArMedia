from rich.console import Console
import sys
console = Console()

# Now has his own url, and its episodes urls, for each provider
def debug(*argument, **kwarg):
    for arg in argument:
        console.log(arg, markup=False,end="")
    for key, val in kwarg.items():
        console.log(f"{key} = {val}", markup=False)


def download_from_server(server_link):
    return True


def join_list_of_list(list_of_list):
    result = []
    for l in list_of_list:
        result.extend(l)
    return result
            


def die(*argument, **kwarg):
    debug(*argument, **kwarg)
    exit()
    sys.exit()

def zip_extend(*args,no_none=False):
    """
    >>> list(zip_extend([1,2,3],[4,5,6,7]))
    [(1, 4), (2, 5), (3, 6), (None, 7)]
    """
    args = [iter(i) for i in args]
    cursor = [next(i, None) for i in args]
    while any(cursor):
        yield [i for i in cursor if i is not None] if no_none else cursor
        cursor = [next(i, None) for i in args]

def filter_list(l:list,filter_expression:str)-> list:
    """filter a list by a string of indexes:
    "1,3-6,8,-5" , [0,1,2,3,4,5,6,7,8,9] -> [1,3,4,6,8]
    """
    filter_expression = filter_expression.replace(" ", "")
    if filter_expression == "":
        return l
    bool_list = [False] * len(l)
    for exp in filter_expression.split(","):
        if "-" in exp:
            if exp[0] == "-":
                index = int(exp[1:])-1
                bool_list[index] = False
            else:
                start, end = exp.split("-")
                start, end = int(start)-1, int(end)-1
                if start > end:
                    start, end = end, start
                bool_list[start : end + 1] = [True] * (end - start + 1)
        else:
            index = int(exp)-1
            bool_list[index] = True
    return [item for item, boolean in zip(l, bool_list) if boolean]

wait = 1


if __name__ == "__main__":
    # l1 = [1, 2, 3]
    # l2 = [4, 5, 6, 7]
    # l3 = [8, 9]
    # debug(list(zip_extend(l1, l2,l3)))
    debug(filter_list([1,2,3,4,5,6,7,8,9],"1,3-6,8,-5"))
    