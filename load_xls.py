import xlrd
import xlwt


def read_excel():
    work_book = xlrd.open_workbook('./咪咕音乐效果测试.xls')
    sheet = work_book.sheet_by_name('test1')
    print('sheet_name:{},sheet_rows:{},sheet_cols:{}'.format(sheet.name, sheet.nrows, sheet.ncols))
    rows_num = sheet.nrows
    cols_num = sheet.ncols
    type_list = sheet.col_values(2)[1::]
    song_list = sheet.col_values(3)[1::]
    # print(type_list)
    # print(song_list)
    # 获取要查询的类型和查询串
    search_list = []
    for i in range(len(song_list)):
        search_list.append((type_list[i], song_list[i]))
    # print(search_list)

    # 第二种获取要查询的类型和查询串
    search_list1 = []
    for i in range(1, rows_num):
        search_list1.append((sheet.cell_value(i, 2), sheet.cell_value(i, 3)))
    # print(search_list1)
    return search_list


if __name__ == '__main__':
    a = read_excel()
    print(a)
