import zipfile
import itertools
import queue
from concurrent.futures import ThreadPoolExecutor


class BoundedThreadPoolExecutor(ThreadPoolExecutor):
    # 将无界队列改成有界队列
    def __init__(self, max_workers=None, thread_name_prefix=''):
        super().__init__(max_workers, thread_name_prefix)
        self._work_queue = queue.Queue(self._max_workers * 2)  # 设置队列大小


def extract(file, password):
    if not flag:
        return
    file.extractall(path='.', pwd=''.join(password).encode('utf-8'))


def result(file):
    exception = file.exception()
    if not exception:
        # 如果获取不到异常说明破解成功
        print('密码为：', file.pwd)
        global flag
        flag = False


if __name__ == '__main__':
    # 创建一个标志用于判断密码是否破解成功
    flag = True
    # 创建一个线程池
    pool = ThreadPoolExecutor(100)
    nums = [str(i) for i in range(10)]  # 数字
    capital_letters = [chr(i) for i in range(65, 91)]  # 大写字母
    lower_letters = [chr(i) for i in range(65, 91)]  # 小写字母
    # 全排列暴力生成6位密码
    password_lst = itertools.permutations(nums + capital_letters + lower_letters, 6)

    # 创建文件句柄
    zip_file = zipfile.ZipFile("666.zip", 'r')
    for pwd in password_lst:
        # print(pwd)
        if not flag:
            break
        f = pool.submit(extract, zip_file, pwd)
        f.pwd = pwd
        f.pool = pool
        f.add_done_callback(result)
