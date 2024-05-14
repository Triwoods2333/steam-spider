import os
import time

import pandas as pd
from DrissionPage import ChromiumPage, ChromiumOptions


def get_data(page, page_num, path):
    print(f'开始获取第{page_num+1}页数据')
    # 请求页面
    page.get(f'https://store.steampowered.com/specials?offset={page_num*12}')
    time.sleep(1)

    # 滚动到底部
    page.scroll.to_bottom()

    # 获取数据
    div_ls = page.eles('.y9MSdld4zZCuoQpRVDgMm')

    # 处理数据
    items = []
    if not div_ls:
        print('没有数据')
        return None
    for div in div_ls:
        item = {}
        item['游戏'] = div.ele('.:StoreSaleWidgetTitle').text
        item['标签'] = ','.join(div.ele('x:./div/div/div/div[2]/div[3]/div[1]').texts())
        item['原价'] = div.ele('t:div@|text()^¥@|text()^$@|text()^HK', index=2).text
        item['售价'] = div.ele('t:div@|text()^¥@|text()^$@|text()^HK', index=3).text
        item['折扣'] = div.ele('text:%').text
        item['详情页'] = div.ele('x:./div/div/div/div[2]/div[2]/a').attr('href')
        print(item)
        items.append(item)

    # 保存数据
    df = pd.DataFrame(items)
    df.to_csv(path, mode='a', header=False, index=False)
    print(f'第{page_num+1}页数据获取完成\n' + '='*100)
    return True


def main():
    # 实例化页面对象
    co = ChromiumOptions()
    co.incognito()  # 隐身模式
    co.no_imgs()  # 禁止加载图片
    co.headless()  # 无头模式
    page = ChromiumPage(co)

    # 开始获取数据
    file_path = 'steam_specials.csv'
    if not os.path.exists(file_path):
        pd.DataFrame(columns=['游戏', '标签', '原价', '售价', '折扣', '详情页']).to_csv(file_path, index=False)

    # 循环获取数据
    for i in range(1000):
        res = get_data(page, i, file_path)
        if res is None:
            break

    # 退出浏览器
    page.quit()

    print('数据获取完成')


if __name__ == '__main__':
    main()
