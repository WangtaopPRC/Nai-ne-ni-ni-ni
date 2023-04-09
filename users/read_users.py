import pandas as pd
import gradio as gr
import copy
import os
def get_current_user():
    users = dict()
    users['wangzitao1999'] = {'passward': str(406406406), 'counts': 1e9}
    # users['1999'] = {'passward': str(4), 'counts': 1}
    df = pd.read_csv('users/checkpoint.csv')
    # df = pd.read_csv('users/202304061758502305.csv')
    for item in df.itertuples():
        # print(item)
        try:
            user = str(item[5]).split('\t')[-1]
        except:
            user = str(item[5])
        try:
            passward = item[3].split('\t')[-1]
        except:
            passward = str(item[3])
        counts = item[6]
        # print(counts)
        # if user in users.keys():
        #     users[user] = {'passward': passward, 'counts': counts + users[user]['counts']}
        # else:
        users[user] = {'passward': passward, 'counts': counts}
        # break
    # print(users)

    return users


import global_var

all_user = get_current_user()
print(all_user)
global_var.set_value('all_user', all_user)


def read_user(user, password):
    all_user = copy.deepcopy(global_var.get_value('all_user'))
    # print(user)
    if user in all_user.keys():
        print(user, password)

        user, password = str(user), str(password)

        if password == all_user[user]['passward']:
            cridit = f"登陆成功, 剩余积分：{all_user[user]['counts']}"
            if all_user[user]['counts'] < 0:
                return cridit, False, user, gr.update(visible=True), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)


            if user == 'wangzitao1999':
                return cridit, True, user, gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)

            return cridit, True, user, gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=False)



    else:
        return "用户名或密码错误", False, None, gr.update(visible=True), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)



def save_user():
    all_user = global_var.get_value('all_user')

    df = pd.DataFrame(
        {"序号": [], "所属平台": [], "订单号": [], "收件人": [], "收件人电话": [], "总金额": [], "运费": [], "快递单号": [], "快递公司": []})
    for k, v in all_user.items():
        # print(k)
        new_row = {"序号": len(df) + 1, "所属平台": "", "订单号": f"{v['passward']}", "收件人": "", "收件人电话": f"{k}", "总金额": str(v['counts']), "运费": "", "快递单号": "",
                   "快递公司": ""}
        df.loc[len(df)] = new_row
    # print(df)
    df.to_csv('users/checkpoint.csv', index=False)


def update_user(csv_path):

    df = pd.read_csv(f'{csv_path}')
    all_user = copy.deepcopy(global_var.get_value('all_user'))
    for item in df.itertuples():
        try:
            user = str(item[5]).split('\t')[-1]
        except:
            user = str(item[5])
        try:
            passward = item[3].split('\t')[-1]
        except:
            passward = str(item[3])
        counts = item[6]
        # print(counts)
        # print(user)
        if user in all_user.keys():
            all_user[user] = {'passward': passward, 'counts': counts + all_user[user]['counts']}
        else:
            all_user[user] = {'passward': passward, 'counts': counts}
    print(all_user)
    global_var.set_value('all_user', all_user)

def change_single_user(username, points):

    # df = pd.read_csv(f'{csv_path}', encoding='gb18030')
    all_user = copy.deepcopy(global_var.get_value('all_user'))

    if username in all_user.keys():
        all_user[username]['counts'] = int(points)

        global_var.set_value('all_user', all_user)

    print(all_user)
    # os.remove('users/202304042003593893.csv')
if __name__ == '__main__':
    get_current_user()
