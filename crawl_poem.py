import requests
from bs4 import BeautifulSoup
import json


# 函数1：请求网页
def page_request(url, ua):
    response = requests.get(url, headers=ua)
    html = response.content.decode('utf-8')
    return html


# 函数2：解析主页面
def page_parse(html):
    soup = BeautifulSoup(html, 'lxml')
    
    # 提取诗词条目
    poem_items = soup.select('article.poem-item')
    
    sentence_list = []
    author_list = []
    href_list = []
    
    for item in poem_items:
        # 提取诗句
        poem_text = item.select_one('span.poem-text')
        if poem_text:
            sentence_list.append(poem_text.get_text().strip())
        
        # 提取作者
        poem_author = item.select_one('span.poem-author')
        if poem_author:
            author_list.append(poem_author.get_text().strip())
        else:
            author_list.append('')
        
        # 提取链接
        poem_link = item.select_one('a.poem-link')
        if poem_link:
            href = poem_link.get('href')
            href_list.append(href)
    
    return [href_list, sentence_list, author_list]


# 函数3：保存主页面爬取的古诗名句到txt
def save_txt(info_list):
    with open(r'sentence.txt', 'a', encoding='utf-8') as txt_file:
        for i in range(len(info_list[1])):
            data = {
                '编号': i + 1,
                '诗句': info_list[1][i],
                '作者': info_list[2][i],
                '链接': info_list[0][i]
            }
            txt_file.write(json.dumps(data, ensure_ascii=False) + '\n\n')


# 子网页处理函数：进入并解析子网页/请求子网页
def sub_page_request(info_list, base_url):
    subpage_urls = []
    for href in info_list[0]:
        subpage_urls.append(base_url + href)
    
    ua = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
    sub_html = []
    for url in subpage_urls:
        html = page_request(url, ua)
        sub_html.append(html)
    return sub_html


# 子网页处理函数：解析子网页，爬取完整古诗内容
def sub_page_parse(sub_html):
    poem_list = []
    for html in sub_html:
        soup = BeautifulSoup(html, 'lxml')
        # 提取古诗原文
        content_div = soup.select_one('div.content')
        if content_div:
            poem = content_div.get_text(separator='\n', strip=True)
            poem_list.append(poem)
        else:
            poem_list.append('无法提取古诗内容')
    return poem_list


# 子网页处理函数：保存完整古诗到txt
def sub_page_save(poem_list):
    with open(r'poems.txt', 'a', encoding='utf-8') as txt_file:
        for i, element in enumerate(poem_list):
            data = {
                '编号': i + 1,
                '完整古诗': element
            }
            txt_file.write(json.dumps(data, ensure_ascii=False) + '\n\n')


if __name__ == '__main__':
    print("**************开始爬取古诗词网站********************")
    
    # 网站URL
    base_url = 'https://sun-xt9527.github.io/'
    main_url = base_url + 'index.html'
    
    # User-Agent
    ua = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
    
    # 请求主页面
    print(f"请求主页面: {main_url}")
    html = page_request(main_url, ua)
    
    # 解析主页面
    print("解析主页面...")
    info_list = page_parse(html)
    
    # 保存主页面信息
    print("保存主页面古诗名句...")
    save_txt(info_list)
    
    # 开始处理子网页
    print("开始处理子网页...")
    sub_html = sub_page_request(info_list, base_url)
    poem_list = sub_page_parse(sub_html)
    
    # 保存完整古诗内容
    print("保存完整古诗内容...")
    sub_page_save(poem_list)
    
    print("****************爬取完成***********************")
    print("共爬取%d" % len(info_list[1]) + "个古诗词名句")
    print("共爬取%d" % len(poem_list) + "个完整古诗")
    print("\n生成的文件:")
    print("- sentence.txt (主页面古诗名句)")
    print("- poems.txt (完整古诗内容)")
