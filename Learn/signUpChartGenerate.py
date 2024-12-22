import xlrd
import xlwt

tableHead1 = ['考试时间', '开课院系', '课程编号', '课程名称', '班级号', '人数', '考场', '监考1', '监考2', '备注']
tableHead2 = ['学号', '姓名', '考试性质', '原始学期', '学生所在院系', '班级名称', '课程编号', '课程名称', '开课单位',
              '报名学期', '校区']
tableHead3 = ['学号', '姓名', '开课学院', '课程代码', '考试科目', '签名']


#学院简称
def simplfied(string):
    if string == '互联网金融与信息工程学院':
        return '互金学院'
    elif string == '金融数学与统计学院':
        return '数统学院'
    elif string == '外国语言与文化学院':
        return '外文学院'
    elif string == '财经与新媒体学院':
        return '财新学院'
    else:
        return string


def judgeclass(classes, oneclass):
    # 节省时间的
    if classes.find(oneclass) != -1 or classes == '':
        return True
    list = oneclass.split('-')
    profession = list[0]
    num = list[1][0]
    begin = classes.find(profession)
    if classes.find('级') != -1:
        grade = oneclass[0:2] + '级'
        if classes.find(grade) != -1:
            return True
    if begin != -1:
        begin += len(profession)
    else:
        return False
    end = classes[begin:].find('班')
    return classes[begin:begin + end].find(num) != -1


if __name__ == '__main__':
    print('开始生成')
    # 逐行遍历补考安排名单，找出考试教室
    result = xlwt.Workbook()
    schedule = xlrd.open_workbook('excels/附件2：2022-2023-2学期补考安排.xls').sheets()[0]
    names = xlrd.open_workbook('excels/附件1：2022-2023-2学期补考名单.xlsx').sheets()[0]
    room = ''
    sheet = ''
    rownum = 0
    session = 1
    time = 0;
    for i in range(1, schedule.nrows):
        row = schedule.row_values(i)
        # 是不是进入新的考场
        if row[tableHead1.index('考场')] != '':
            room = row[tableHead1.index('考场')]
            string = row[tableHead1.index('考试时间')][4:10]
            string = ''.join(filter(str.isalnum, string))
            if string != time:
                time = string
                session = 1
            sheetname = string + '（' + str(session) + '）' + '（' + room + '）'
            session += 1
            sheet = result.add_sheet(sheetname, cell_overwrite_ok=True)
            rownum = 0
            for column in range(0, len(tableHead3)):
                sheet.write(rownum, column, tableHead3[column])
            sheet.col(0).width = 256 * 11
            sheet.col(1).width = 256 * 9
            sheet.col(2).width = 256 * 14
            sheet.col(3).width = 256 * 10
            sheet.col(4).width = 256 * 20
            sheet.col(5).width = 256 * 9
            rownum += 1;
        subject = row[tableHead1.index('课程名称')]
        classes = row[tableHead1.index('班级号')]
        for j in range(1, names.nrows):
            row2 = names.row_values(j)
            # 匹配课程和班级
            if row2[tableHead2.index('课程名称')] == subject and judgeclass(classes,
                                                                            row2[tableHead2.index('班级名称')]):
                studentId = row2[tableHead2.index('学号')]
                name = row2[tableHead2.index('姓名')]
                faculty = row2[tableHead2.index('开课单位')]
                subjectCode = row2[tableHead2.index('课程编号')]
                row3 = [studentId, name, simplfied(faculty), subjectCode, subject]
                for column in range(0, len(tableHead3) - 1):
                    sheet.write(rownum, column, row3[column])
                rownum += 1;
    result.save('result2.xlsx')
    print("生成完毕！")
