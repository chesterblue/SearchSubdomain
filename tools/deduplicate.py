# @Author: chesterblue
# @File Name:deduplicate.py

def remove_duplicate_data(items: list) -> list:
    """
    list: items
    return: list
    """
    return list(set(items))
