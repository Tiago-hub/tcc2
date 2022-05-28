#!/usr/bin/env python3
import concurrent.futures
from multiprocessing import Process, Manager, Value


def add_to_list(my_list,index, add):
    print(add)
    my_list[index]+=add

def main():
    with Manager() as manager:
        my_list = manager.list([1, 2, 3, 4, 5])
        my_list2 = manager.list([1, 2, 3, 4, 5])
        my_list3 = manager.list([1, 2, 3, 4, 5])
        # my_list = 

        # Retrieve a single page and report the URL and contents


        print(my_list)
        procs = [Process(target=add_to_list, args=(my_list,my_list2[i],my_list3[i])) for i in range(4)]

        for p in procs: p.start()
        for p in procs: p.join()
        # p = Process(target=add_to_list, args=(my_list,my_list2,my_list3))
        # p.start()
        # p.join()
        # We can use a with statement to ensure threads are cleaned up promptly
        # with concurrent.futures.ProcessPoolExecutor(max_workers=5,initargs=(my_list, 'my_list')) as executor:
        #     # Start the load operations and mark each future with its URL
        #     indexes = [0,0,0,1,4]
        #     what_add = [1,1,1,2,5]
        #     results = executor.map(add_to_list,indexes,what_add)
        #     # for result in results:
            #     print(result)
        print(my_list)

if __name__=='__main__':
    main()