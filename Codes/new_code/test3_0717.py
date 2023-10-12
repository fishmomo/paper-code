import concurrent.futures
import numpy as np
import time
def process_task(argument):
    # 执行任务的函数
    # 这里可以根据需要进行任务的处理
    result = argument+1  # 执行任务的结果
    return result

def main():
    arguments = [i*np.ones([3, 3]) for i in range(10000)]   # 要传递给任务的参数列表

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # 并行地提交任务并处理结果
        results = executor.map(process_task, arguments)

        # 在这里对结果进行处理或保存
        arr = []
        for x in results:
            arr.append(x)
        # print(arr)

if __name__ == '__main__':
    st = time.time()
    main()
    et = time.time()
    print("cost:", et-st)


