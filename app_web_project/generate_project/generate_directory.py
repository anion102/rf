# !usr/bin/env python
# coding=utf-8
# python version 2.7.10
# author: kanlijun
# system: windows7
import os, shutil
import xlrd
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#生成项目基本目录结构
def generateProject(project_path):
    dire = ["test", "MAP", "WorkFlow", "VAR", "config", "resource"]
    if os.path.exists(project_path):    # 文件:os.path.isfile(file)
        shutil.rmtree(project_path)
    os.mkdir(project_path)
    os.chdir(project_path)  # 进入生成的项目路径
    for i in dire:
        os.mkdir(i)
        if i == "config":
            f = open(i+"/config.txt", "a+")
            f.close()
    os.chdir(sys.path[0])   # 返回当前执行路径

#解析excel测试用例文件，将所有用例解析到数组list中；
def parse_excel(excelFile):
    # p = os.path.abspath(excelFile)
    book = xlrd.open_workbook(excelFile)
    sheet = book.sheets()[0]
    nr = sheet.nrows
    nc = sheet.ncols
    caseList = [ [0 for i in range(nc)] for i in range(nr-1)]
    for i in range(1, nr):
        for j in range(nc):
            caseList[i-1][j] = sheet.cell(i, j).value
    return caseList

#将用例数组数据进行分类存储
def data_classify(lists,path):
    os.chdir(path)
    case_module = ''
    case_suite = ''
    i = 0
    j = 1
    for row in lists:
        if row[0] != case_module:
            case_module = row[0]
            os.mkdir(row[0])
            os.chdir(row[0])
        if (case_suite != row[1]):
            i = i + 1
        f = open(str(i) + " %s.txt" % row[1], 'a+')
        if(case_suite!=row[1]):
            case_suite = row[1]
            f.write("*** Test Cases ***\n")
            j = 1
        f.write(str(j) + " " + row[3])
        j = j + 1
        f.write("\n")
        f.write("    [Documentation]    author=阚利君\n")
        row[5] = row[5].replace("\n","")
        f.write("    ...    【操作步骤】：%s" % row[5])
        f.write("\n")
        row[6] = row[6].replace("\n","")
        f.write("    ...    【预期结果】：%s" % row[6])
        f.write("\n")
        f.close()

#生成项目中test中的case
def generate_cases(project_path, excel_file):
    generateProject(project_path)
    lists = parse_excel(excel_file)
    data_classify(lists, project_path+"/test")

generate_cases("F:\\autotest_project\\python\\klj_rf_dubbo\\python_test\\project1", 'test.xlsx')