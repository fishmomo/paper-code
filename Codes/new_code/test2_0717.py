import concurrent.futures
import numpy as np
import time

def process_task(argument):
    # 执行任务的函数
    # 这里可以根据需要进行任务的处理
    result = argument+1  # 执行任务的结果
    return result

def main():
    arguments = [i*np.ones([3, 3]) for i in range(10000)]  # 要传递给任务的参数列表

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # 提交任务并获取 Future 对象列表
        futures = [executor.submit(process_task, argument) for argument in arguments]

        # 获取每个任务的结果
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()  # 获取任务的结果
            results.append(result)
        # print(results)
        # 在这里可以对结果进行进一步处理或保存
        # ...

if __name__ == '__main__':
    st = time.time()
    main()
    et = time.time()
    print("cost:", et-st)
