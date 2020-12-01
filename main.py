import time
import multiprocessing
from multiprocessing import Pool

from modules.fileIO import Csv
from modules.webdriver import Chrome

target_url = 'https://doda.jp/DodaFront/View/JobSearchList/j_op__20/'
fileIO = Csv()
output_path = './out/out.csv'
process_num = multiprocessing.cpu_count()
# process_num = 2

def get_detail(detail_page_url):
    page_ch = Chrome()
    try:
        with page_ch.driver as page_driver:
            page_driver.get(detail_page_url)
            try:
                detail_page = page_driver.find_element_by_xpath(
                    '//*[@id="shStart"]//*[@class="_canonicalUrl"]')
                detail_page.click()
            except Exception as e:
                print(detail_page_url)
                print(e)
            time.sleep(2)

            url = page_driver.current_url
            try:
                name = page_driver.find_element_by_xpath(
                '//*[@class="head_title"]//h1').text
            except Exception as e:
                name = None
                print(e)
            try:
                detatil = page_driver.find_element_by_xpath(
                '//*[@id="application_method_table"]//*[@class="band_title"]/dd/p').text
            except Exception as e:
                detatil = None
                print(e)
            try:
                corp_url = page_driver.find_element_by_xpath(
                '//*[@id="company_profile_table"]//a').get_attribute("href")
            except Exception as e:
                corp_url = None
                print(e)
            try:
                period = page_driver.find_element_by_xpath(
                '//*[@class="meta_head"]//*[@class="publishingSchegulePeriod"]/*[@class="meta_text"]').text
            except Exception as e:
                period = None
                print(e)

            content = [name, period, url, detatil, corp_url]
            # print(content)
            fileIO.addCsv(output_path, content)
            
    except Exception as e:
        print(e)

def main(target_url):
    ch = Chrome()
    process = Pool(process_num)
    with ch.driver as driver:
        driver.get(target_url)
        time.sleep(2)
        while True:
            try:
                current_url = driver.current_url
                print(current_url)

                item_count = 1
                detail_page_url_list = []
                while True:
                    try:
                        corp_page = driver.find_elements_by_xpath(f'//h2[@class="title clrFix"]//a')[item_count]
                        detail_page_url = corp_page.get_attribute("href")

                        # print(detail_page_url)
                        detail_page_url_list.append(detail_page_url)

                        item_count += 1
                    except Exception as e:
                        print('None item')
                        print(e)
                        break
                process.map(get_detail, detail_page_url_list)
                next_bottom = driver.find_element_by_xpath(
                    '//*[@class="btn_r last"]/a')
                next_bottom.click()
            except Exception as e:
                print('None list')
                print(e)
                break
    process.close()
    process.join()
    return


if __name__ == "__main__":
    main(target_url)
