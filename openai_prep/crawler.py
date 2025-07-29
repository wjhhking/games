# This is the HtmlParser's API interface.
# You should not implement it, or speculate about its implementation
# class HtmlParser(object):
#    def getUrls(self, url):
#      """
#      :type url: str
#      :rtype List[str]
#      """

from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import threading

# 假设 HtmlParser 类的定义已存在
# class HtmlParser(object):
#    def getUrls(self, url):
#      """
#      :type url: str
#      :rtype List[str]
#      """

# class Solution:
#     def crawl(self, startUrl: str, htmlParser: 'HtmlParser') -> list[str]:
#         # 提取起始 URL 的主机名
#         start_hostname = urlparse(startUrl).hostname

#         # 使用集合存储所有已访问（或已加入任务队列）的 URL
#         # 它是最终要返回的结果，也用于避免重复抓取
#         visited_urls = {startUrl}
#         # 需要一个锁来保护对 visited_urls 的并发访问
#         visited_lock = threading.Lock()

#         # 使用 ThreadPoolExecutor 管理线程池
#         with ThreadPoolExecutor(max_workers=8) as executor:
#             # 将初始任务提交给执行器
#             # tasks 字典用于追踪 Future 对象和其对应的 URL
#             tasks = {executor.submit(htmlParser.getUrls, startUrl): startUrl}

#             # 只要还有正在进行的任务，就继续循环
#             while tasks:
#                 # as_completed 会在任何一个 future 完成后立即返回它
#                 for future in as_completed(tasks):
#                     # 从 tasks 字典中移除已完成的 future
#                     # 这是关键一步，确保循环可以最终结束
#                     url = tasks.pop(future)

#                     try:
#                         # 获取爬取结果
#                         new_urls = future.result()
#                     except Exception as e:
#                         # 在实际应用中，这里应该有更完善的错误处理
#                         print(f"Error fetching {url}: {e}")
#                         continue

#                     # 遍历新发现的 URL
#                     for new_url in new_urls:
#                         # 检查主机名是否匹配
#                         if urlparse(new_url).hostname == start_hostname:
#                             # 加锁以保证线程安全地检查和添加 new_url
#                             with visited_lock:
#                                 # 检查是否已经访问过
#                                 if new_url not in visited_urls:
#                                     visited_urls.add(new_url)
#                                     # 将新的、未访问的、同主机的 URL 提交为新任务
#                                     new_future = executor.submit(htmlParser.getUrls, new_url)
#                                     tasks[new_future] = new_url

#         return list(visited_urls)



class Solutions:


    def crawl(self, startUrl: str, htmlParser: 'HtmlParse') -> list[str]:
        start_hostname = urlparse(startUrl).hostname

        visited = {startUrl}
        visited_lock = threading.Lock()

        with ThreadPoolExecutor(max_workers=8) as exector:
            tasks = {exector.submit(htmlParser.getUrls, startUrl): startUrl}

            while tasks:
                for future in as_completed(tasks):
                    url = tasks.pop(future)
                    # Task results.
                    try:
                        new_urls = future.result()
                    except Exception as e:
                        print(f'Error{url}:{e}')
                        continue

                # Add new urls.
                for new_url in new_urls:
                    if urlparse(new_url).hostname == start_hostname:
                        with visited_lock:
                            if new_url not in visited:
                                visited.add(new_url)
                                new_future = exector.submit(htmlParser.getUrls, new_url)
                                tasks[new_future] = new_url

        return list(visited)