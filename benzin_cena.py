import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
from datetime import date
url = "https://erc.org.mk/ceni.aspx"

header = {
    "Referer": "https://erc.org.mk/pages.aspx?id=156",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
}

r = requests.post(url, data="e=1", headers=header)
soup = BeautifulSoup(r.text.encode('utf-8').strip(), "html.parser")
cur_cena = float(soup.find('span', id="ceniGrid_Label1_0").text.replace(",", "."))
prev_cena = None

with open("b_95.txt", "rt") as ptr:
    last_line = None
    while True:
        chunk = ptr.readline()
        if chunk == '':
            break
        last_line = chunk
    line = float(last_line.split(",")[0])
    prev_cena = line

toaster = ToastNotifier()
if prev_cena > cur_cena:
    toaster.show_toast(
        "Цената на бензинот падна",
        str(cur_cena),
        icon_path=None,
        duration=30,
        threaded=True
    )
    with open("b_95.txt", "a") as ptr:
        ptr.write("\n" + str(cur_cena) + "," + str(date.today()))
elif cur_cena > prev_cena:
    toaster.show_toast(
        "Цената на бензинот е качена",
        str(cur_cena),
        icon_path=None,
        duration=30,
        threaded=True
    )
    with open("b_95.txt", "a") as ptr:
        ptr.write("\n" + str(cur_cena) + "," + str(date.today()))
else:
    toaster.show_toast(
        "Нема промена во цената на БС 95",
        icon_path=None,
        duration=30,
        threaded=True
    )


