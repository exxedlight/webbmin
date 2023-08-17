from flask import Flask, render_template, request

app = Flask(__name__)


def combine(m, n):
    a = len(m)
    c = ''
    count = 0
    for i in range(a):
        if m[i] == n[i]:
            c += m[i]
        elif m[i] != n[i]:
            c += '-'
            count += 1

    if count > 1:
        return None
    else:
        return c


def find_minterms(data):
    newlist = list(data)
    size = len(newlist)
    imp = []
    im = []
    im2 = []
    mark = [0] * size
    m = 0
    for i in range(size):
        for j in range(i + 1, size):
            c = combine(str(newlist[i]), str(newlist[j]))
            if c is not None:
                im.append(str(c))
                mark[i] = 1
                mark[j] = 1
            else:
                continue

    mark2 = [0] * len(im)
    for p in range(len(im)):
        for n in range(p + 1, len(im)):
            if p != n and mark2[n] == 0:
                if im[p] == im[n]:
                    mark2[n] = 1

    for r in range(len(im)):
        if mark2[r] == 0:
            im2.append(im[r])

    for q in range(size):
        if mark[q] == 0:
            imp.append(str(newlist[q]))
            m = m + 1

    if m == size or size == 1:
        return imp
    else:
        return imp + find_minterms(im2)


def maketable(user_n):
    tablecreated = ''
    i = pow(2, int(user_n))
    j = 0
    while j < i:
        getbinary = lambda x, n: format(x, 'b').zfill(n)
        tablecreated += str(getbinary(j, int(user_n))) + "|" + "0\n"
        j += 1
    return tablecreated


def maketable_from_vector(data):
    tablecreated = ''
    list_dnf = list(data)
    user_n = len(list_dnf[1])
    i = pow(2, int(user_n))
    j = 0
    while j < i:
        flag = 0
        getbinary = lambda x, n: format(x, 'b').zfill(n)
        tablecreated += str(getbinary(j, int(user_n))) + "|"

        for a in range(len(list_dnf)):
            if str(getbinary(j, int(user_n))) == str(list_dnf[a]):
                flag = 1

        if flag == 1:
            tablecreated += "1\n"
        else:
            tablecreated += "0\n"
        j += 1
    return tablecreated


def make_list_vector(data):
    vectorlist = list(data)
    dig_map = map(int, vectorlist)
    dig_list = list(dig_map)
    size = len(dig_list)
    maxsizedind = 0

    for i in range(size):
        if dig_list[i] > maxsizedind:
            maxsizedind = dig_list[i]

    size_bin = len(str(bin(maxsizedind))) - 2

    str_list = []
    for i in range(size):
        getbinary = lambda x, n: format(x, 'b').zfill(n)
        str_list.append(str(getbinary(int(vectorlist[i]), size_bin)))

    return str_list


@app.route('/')
def mainpage():
    return render_template('index.html')


@app.route('/table', methods=["POST", "GET"])
def tablein():
    if request.method == "POST" and int(request.form.get("user_N")) > 0:
        user_n = request.form.get("user_N")
        return render_template('tablein.html', table_data=maketable(user_n))
    else:
        return render_template('tablein.html')


@app.route('/tablecreate', methods=["POST", "GET"])
def tableinn():
    user_n = request.form.get("user_N")
    return render_template('tablein1.html', table_data=maketable(user_n))


@app.route('/vector')
def vectorin():
    return render_template('vectorin.html')


@app.route('/minvector', methods=["POST"])
def min1():
    user_vector_data = request.form.get("user_vector_data").replace("\n", "")
    list_from_user_input = make_list_vector(user_vector_data.split(' '))
    min_users_data = find_minterms(list_from_user_input)
    string_res = ''.join([str(item + "\n") for item in min_users_data])
    return render_template('min.html', result_name_data="Funclion's vector form: " + user_vector_data.replace(" "," v ") + "\n\nTable:\n" + (maketable_from_vector(list_from_user_input)) + "\n\nResulted minterms:\n\n" + string_res)


@app.route('/mintable', methods=["POST"])
def min2():
    user_table_data = request.form.get("user_table_data").replace(" ", "")
    return render_template('min.html', result_name_data=user_table_data)
