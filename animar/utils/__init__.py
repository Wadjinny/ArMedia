from rich.console import Console
import sys
console = Console()

# Now has his own url, and its episodes urls, for each provider
def debug(*argument, **kwarg):
    for arg in argument:
        console.log(arg, markup=False)
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

def zip_extend(*args):
    """
    >>> list(zip_extend([1,2,3],[4,5,6,7]))
    [(1, 4), (2, 5), (3, 6), (None, 7)]
    """
    args = [iter(i) for i in args]
    cursor = [next(i, None) for i in args]
    while any(cursor):
        yield cursor
        cursor = [next(i, None) for i in args]

wait = 1


if __name__ == "__main__":
    l1 = [1, 2, 3]
    l2 = [4, 5, 6, 7]
    l3 = [8, 9]
    debug(list(zip_extend(l1, l2,l3)))