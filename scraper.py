import logging
import os
import time
import requests
from selenium import webdriver

# Set up logging
logging.basicConfig(filename='img_scrap.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='w')
logger = logging.getLogger()


def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    # build the Google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    logger.info(f"Loading search URL for query '{query}'")
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0

    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)

        logger.info(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception as e:
                logger.error(f'Could\'nt click the thumbnail due to {e}')
                continue

            # extract image urls
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                logger.info(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            logger.info("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)

            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls


def persist_image(folder_path: str, url: str, counter):
    try:
        image_content = requests.get(url).content
    except Exception as e:
        logger.error(f"ERROR - Could not download {url} - {e}")

    try:
        f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
        f.write(image_content)
        f.close()
        logger.info(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        logger.error(f"ERROR - Could not save {url} - {e}")


def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images=10):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    logger.info(f"Starting search and download for '{search_term}'")

    with webdriver.Chrome(executable_path=driver_path) as wd:
        logger.info(f"Webdriver started with path {driver_path}")
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)

    logger.info(f"Fetching {len(res)} image URLs for '{search_term}'")

    counter = 0
    for elem in res:
        persist_image(target_folder, elem, counter)
        counter += 1

    logger.info(f"Downloaded {counter} images to {target_folder}")


if __name__ == '__main__':
    DRIVER_PATH = r'chromedriver.exe'
    search_term = 'gwynne shotwell'
    # num of images you can pass it from here  by default it's 10 if you are not passing
    # number_images = 50
    search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_images=10)
