import re
import bs4
import urllib.request as req
import sys

'https://invoice.etax.nat.gov.tw/'


# 輸入網址(字串)，爬取發票號碼網頁，回傳網頁的html
def get_html(url):
    request = req.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42"
                                        })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    root = bs4.BeautifulSoup(data, "html.parser")
    return root


# 輸入網頁html，回傳當期發票中獎號碼
def take_number(html_):
    number_all = html_.find(id="area1").find("table").find_all("tr")
    lucky_num = []
    for row in number_all:
        col = row.find_all("td")
        if col:
            number_col = col[1].find("span", class_="t18Red")
            if number_col:
                for number_single in number_col.text.split("、"):
                    lucky_num.append((number_single))

    return lucky_num


# 輸入發票末三碼並判斷是否為三碼數字
def input_my3num():
    while True:
        this_one = input("請輸入發票末三碼: ")
        if this_one.isdigit() and len(this_one) == 3:
            break
        elif this_one == 'End':
            sys.exit("本程式結束，掰掰!")
        else:
            print("    末三碼數字!!!")

    return this_one


# 輸入發票號碼並判斷是否符合發票格式
def input_my8num():
    while True:
        this_one = input("請輸入發票號碼: ")
        if this_one.isdigit() and len(this_one) == 8:
            break
        else:
            print("    發票八碼數字!!!")

    return this_one


# 比對末三碼判斷是否有中獎，中獎則回傳True，沒有則回傳None
def win_3_num(my_num, targate):
    for each_ in targate:
        if my_num == each_[-3:]:
            print("    有中獎的希望!")
            return True


# 輸入發票號碼，比對中獎的類別
def win_8_num(my_all_num, targate):
    if my_all_num == targate[0]:
        print("    恭喜中獎1000萬元!!!")
    elif my_all_num[-3:] == targate[0][-3:] and my_all_num != targate[0]:
        print("    可惜未中獎1000萬元...")
    elif my_all_num == targate[1]:
        print("    恭喜中獎200萬元!!!")
    elif my_all_num[-3:] == targate[1][-3:] and my_all_num != targate[1]:
        print("    可惜未中獎200萬元...")
    elif my_all_num[-3:] == targate[5]:
        print("    恭喜中獎200元!")
    else:
        for each_ in targate[2:5]:
            if my_all_num == each_:
                print("    恭喜中獎20萬元!")
                break
            elif my_all_num[1:] == each_[1:]:
                print("    恭喜中獎4萬元!")
                break
            elif my_all_num[2:] == each_[2:]:
                print("    恭喜中獎1萬元!")
                break
            elif my_all_num[3:] == each_[3:]:
                print("    恭喜中獎4千元!")
                break
            elif my_all_num[4:] == each_[4:]:
                print("    恭喜中獎1千元!")
                break
            elif my_all_num[5:] == each_[5:]:
                print("    恭喜中獎200元!")
                break


# 主程式
def main():
    month_num = take_number(get_html('https://invoice.etax.nat.gov.tw/'))
    while True:
        my_num = input_my3num()
        if win_3_num(my_num, month_num) == None:
            print("    未中獎...")
        else:
            my_num = input_my8num()
            win_8_num(my_num, month_num)


if __name__ == "__main__":
    main()
