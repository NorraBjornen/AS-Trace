import subprocess
import re
import sys

ip_r = r'\d+\.\d+\.\d+\.\d+'
as_r = r'AS\d+'


def get_as_list(ips):
    as_list = []

    print("Поиск номеров автономных систем")

    for ip in ips:
        args = ["curl", "http://api.whois.vu/?q=" + ip]
        result = subprocess.run(args, stdout=subprocess.PIPE, encoding='utf-8').stdout
        asn = re.findall(as_r, result)

        if len(asn) >= 1:
            asn = asn[0]
        else:
            asn = ""

        as_list.append(asn)

    print("Номера автономных систем найдены")

    return as_list


def get_ips(addr):
    print("Поиск маршрута...")
    args = ["tracert", addr]
    result = subprocess.run(args, stdout=subprocess.PIPE, encoding='cp1251').stdout

    ips = re.findall(ip_r, result)
    del ips[0]
    del ips[-1]

    print("Маршрут найден")

    return ips


def print_fancy_table(list_of_pairs):
    i = 1

    common_str = ""
    max_len = 0

    for pair in list_of_pairs:
        this_str = str(i) + "\t\t" + pair[0] + "\t\t" + pair[1] + "\n"
        csl = len(this_str)
        if csl > max_len:
            max_len = csl
        common_str += this_str
        i += 1

    print("\n\n№\t\t\tip\t\tas\n")

    print(common_str)

    print("\nТаблица построена")


def print_help():
    print("Справка по запуску\n")
    print("В качестве единственного параметра укажите ip адрес или доменное имя\n")
    print("\tПримеры запуска:\n")
    print("\t\tpython as_route.py vk.com")
    print("\t\tpython as_route.py 87.240.190.78\n")


def main():
    if len(sys.argv) != 2:
        print_help()
        return

    addr = sys.argv[1]

    if addr == "-h" or addr == "--help":
        print_help()
        return

    ips = get_ips(addr)
    as_list = get_as_list(ips)

    list_of_pairs = list(zip(ips, as_list))
    print_fancy_table(list_of_pairs)


if __name__ == '__main__':
    main()
