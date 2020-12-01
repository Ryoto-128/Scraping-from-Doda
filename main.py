
import time
import multiprocessing
from multiprocessing import Pool

from modules.fileIO import Csv
from modules.webdriver import Chrome

target_url = 'https://doda.jp/DodaFront/View/JobSearchList.action?ss=1&op=20&pic=1&ds=0&tp=1&bf=1&mpsc_sid=10&oldestDayWdtno=0&leftPanelType=1'
fileIO = Csv()
output_path = './out/out.csv'
process_num = multiprocessing.cpu_count()
# process_num = 2


def get_detail(detail_page_url):
    page_ch = Chrome()
    with page_ch.driver as page_driver:
        page_driver.get(detail_page_url)
        detail_page = page_driver.find_element_by_xpath(
            '//*[@id="shStart"]//*[@class="_canonicalUrl"]')
        detail_page.click()
        time.sleep(2)

        url = page_driver.current_url
        name = page_driver.find_element_by_xpath(
            '//*[@class="head_title"]//h1').text
        detatil = page_driver.find_element_by_xpath(
            '//*[@id="application_method_table"]//*[@class="band_title"]/dd/p').text
        corp_url = page_driver.find_element_by_xpath(
            '//*[@id="company_profile_table"]//a').get_attribute("href")
        period = page_driver.find_element_by_xpath(
            '//*[@class="meta_head"]//*[@class="publishingSchegulePeriod"]/*[@class="meta_text"]').text

        content = [name, period, url, detatil, corp_url]
        print(content)
        fileIO.addCsv(output_path, content)


def main(target_url):
    ch = Chrome()
    with ch.driver as driver:
        process = Pool(process_num)
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
                        corp_page = driver.find_element_by_xpath(
                            f'//*[@id="{item_count}"]')
                        detail_page_url = corp_page.get_attribute("href")

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
                process.close()
                process.join()
                break
    return


if __name__ == "__main__":
    main(target_url)
