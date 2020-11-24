# encoding: utf-8  

import os

def del_temp_file(path):
    """
    删除目录下的临时文件
    :param path:
    :return:
    """
    # 删除临时文件
    g = os.walk(path)

    for path, dir_list, file_list in g:
        print(path)
        for file_name in file_list:
            print(file_name)
            if file_name.startswith('temp'):
                os.remove(path +os.sep+file_name)



