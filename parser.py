from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def get_program_params(prog_params):
    temp = list(prog_params)
    temp2 = list()
    n = 0
    for i in range(len(temp)):
        if temp[i - n] == ";":
            del temp[i - n]
            n += 1
        elif temp[i - n][-1] == ";":
            temp[i - n] = temp[i - n][:-1]

    for i in range(0, len(temp), 2):
        temp2.append(temp[i] + " " + temp[i + 1])

    return "\n".join(temp2)


def write_sweety_info(index, url, excel_path):
    result = requests.get(url)

    doc = BeautifulSoup(result.text, "html.parser")
    program_full_name = "Нет информации"
    program_name = "Нет информации"
    program_params = "Нет информации"
    program_about = "Нет информации"
    program_disciplines = "Нет информации"
    program_number = "Нет информации"
    points_info = "Нет информации"
    IDS = "Нет информации"
    try:
        program_full_name = " > ".join([i for i in doc.find("div", class_="real_breadcrumbs").stripped_strings])
    except Exception:
        pass
    try:
        program_name = program_full_name.split(">")[-1]
    except Exception:
        pass
    try:
        program_params = get_program_params(list(doc.find("div", class_="podrInfo").stripped_strings))
    except Exception:
        pass
    try:
        program_about = doc.find("div", class_="mainTitleBlTelo").find_next_sibling("p").string
    except Exception:
        pass
    try:
        program_disciplines = "\u2022".join(
            [i.string for i in
             doc.find("strong", string="Дисциплины, изучаемые в рамках профиля:").parent.find_next("ul")])[1:]
    except Exception:
        pass
    try:
        program_number = doc.find("div", class_="textOPisanieMidAfterTitle").find_all()[2].string.split()[-1][1:-1]
    except Exception:
        pass
    try:
        points_info = "".join([''.join([j for j in i.strings]) for i in doc.find("div", class_="zpForMabile")])[1:]
    except Exception:
        pass
    try:
        IDS = "\n".join([i.string for i in doc.find_all("div", style="margin:10px 0;font-size:16px")])
    except Exception:
        pass
    df = pd.DataFrame(
        {"url": url, "Code": program_number, "Program name": program_name, "Program full name": program_full_name,
         "Program parametrs": program_params, "Program about": program_about,
         "Program disciplines": program_disciplines, "Points info": points_info, "IDS": IDS}, index=[index])
    old_df = pd.read_excel(excel_path)
    old_df = pd.concat([df, old_df])
    for i in [url, program_name, program_full_name, program_params, program_about, program_disciplines, points_info, IDS]:
        if i == 'Нет информации':
            return
    old_df.to_excel(excel_path, index=False)

urls = [
    "https://vuzopedia.ru/vuz/1189",
    "https://vuzopedia.ru/vuz/1",
    "https://vuzopedia.ru/vuz/1239",
    "https://vuzopedia.ru/vuz/342",
    "https://vuzopedia.ru/vuz/1"
    "https://vuzopedia.ru/vuz/3211",
    "https://vuzopedia.ru/vuz/2600",
    "https://vuzopedia.ru/vuz/2550",
    "https://vuzopedia.ru/vuz/3855",
    "https://vuzopedia.ru/vuz/4251",
    "https://vuzopedia.ru/vuz/3005",
    "https://vuzopedia.ru/vuz/4257",
    "https://vuzopedia.ru/vuz/2913",
    "https://vuzopedia.ru/vuz/3713",
    "https://vuzopedia.ru/vuz/324",
    "https://vuzopedia.ru/vuz/3435",
    "https://vuzopedia.ru/vuz/2420",
    "https://vuzopedia.ru/vuz/2846",
    "https://vuzopedia.ru/vuz/3346",
    "https://vuzopedia.ru/vuz/3531",
    "https://vuzopedia.ru/vuz/2346",
    "https://vuzopedia.ru/vuz/1085",
    "https://vuzopedia.ru/vuz/3097",
    "https://vuzopedia.ru/vuz/3827",
    "https://vuzopedia.ru/vuz/3774",
    "https://vuzopedia.ru/vuz/4344"
]

n = 0
for i in urls:
    for k in range(1, 15):
        result = requests.get(i + f'/programs/bakispec?page={k}')
        doc = BeautifulSoup(result.text, "html.parser")
        if doc.find_all("a", class_='spectittle'):
            for j in doc.find_all("a", class_='spectittle'):
                write_sweety_info(n, "https://vuzopedia.ru" + j.attrs["href"],
                                  r"C:\Users\byari\OneDrive\Рабочий стол\Базированная база.xlsx")
                n += 1
                time.sleep(0.2)
        else:
            break
