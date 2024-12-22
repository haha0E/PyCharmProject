import xlrd as x
import xlwt

d = []
d.append(['招考单位', '单位代码', '招考职位', '职位代码', '职位简介', '职位类型', '录用人数', '学历', '学位', \
          '研究生专业名称及代码', '本科专业名称及代码', '大专专业名称及代码', '是否要求2年以上基层工作经历', \
          '是否开展心理素质测试', '是否限应届毕业生报考', '其他要求', '考区'])
def select(city, scholar, degree, experience, graduation, profession, section):
    """
    :param scholar: 学历 list
    :param degreee: 学位 list
    :param experience: 是否要求2年以上基层工作经历 list
    :param graduation 是否限应届毕业生报考 list
    :param profession: 专业 str
    :param city: 部门所属城市
    :param section:考区 list
    :return:
    """
    workbook = x.open_workbook('附件2：广东省县级以上机关和珠三角地区乡镇机关2023年考试录用公务员职位表.xls')
    nums = len(workbook.sheet_names())
    # 加表头
    # 遍历表内部，找到符合筛选条件的加入
    for i in range(0, nums):
        table = workbook.sheets()[i]
        for j in range(0, table.nrows):
            list = table.row_values(j)
            if judge(list, city, scholar, degree, experience, graduation, profession, section):
                d.append(list)
                continue
    '''
    存进excel表格
    '''
    w = xlwt.Workbook()
    sheet1 = w.add_sheet('sheet1', cell_overwrite_ok=True)
    row = 0
    for colours in d:
        for i in range(0, len(colours)):
            sheet1.write(row, i, colours[i])
        row = row + 1
    w.save('xxx.xlsx')


# 筛选条件判断函数
def judge(list, city, scholar, degreee, experience, graduation, profession, section):
    if list[d[1].index("本科专业名称及代码")].find(profession) != -1 or profession == '':
        if judgecity(city, list[0]) or city == []:
            if list[-1] in section or section == '':
                if list[7] in scholar or scholar == []:
                    if list[-5] == experience or experience == '':
                        if list[-3] in graduation or graduation == []:
                            if list[-9] in degree or degreee == []:
                                return True
    return False


def judgecity(city, department):
    for i in city:
        if department.find(i) != -1:
            return True
    return False


if __name__ == '__main__':
    city = ['湛江', '吴川']
    # 部门所属城市
    scholar = []
    # 学历
    # ['研究生','本科以上','本科','大专以上','大专、本科']
    degree = []
    # 学位
    # ['博士','硕士以上','硕士','学士以上','学士、硕士','学士','不限']
    experience = ''
    # 是否要求2年以上基层工作经历
    # '是' '否'
    graduation = ['应届毕业生', '2023届高校毕业生']
    # 是否要求应届毕业生
    # ['否','应届毕业生','2023届高校毕业生']
    profession = '土木'
    # 本科专业
    section = ['湛江']
    # 考区
    '''
    ['省直','广州','深圳','珠海','汕头','佛山','韶关','河源','梅州','惠州',\
     '汕尾','东莞','中山','江门','阳江','湛江','茂名','肇庆','清远','潮州',\
     '揭阳','云浮']
    '''
    select(city, scholar, degree, experience, graduation, profession, section)
