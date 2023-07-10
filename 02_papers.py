# %% [markdown]
# ENVIRONMENT SETTING

# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# %%
import pandas as pd

# %%
import os
import time
import urllib
from tqdm import tqdm, trange

# %%
tqdm.pandas()

# %%
options = webdriver.ChromeOptions()
# options.add_argument('no-sandbox')
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument('disable-gpu')

# %%
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)

# %% [markdown]
# GET LINK

# %%
conference_dfs = []

# %%
for filename in tqdm(os.listdir('./data/conferences/')):
    conference_dfs.append(pd.read_csv(f'./data/conferences/{filename}', index_col = 0))

# %%
conference_df = pd.concat(conference_dfs).reset_index(drop = True)

# %%
conference_df

# %% [markdown]
# CRAWL REVIEWS

# %%
progress = tqdm(total = len(conference_df))
dfs = []

# %%
for title, link in conference_df.loc:
    driver.get(link)
    time.sleep(2)

    reviews = driver.find_elements(By.CSS_SELECTOR, 'div.note_with_children')

    for review in reviews:
        review_title = [x.text for x in review.find_elements(By.CSS_SELECTOR, 'div.title_pdf_row > h2.note_content_title > span')][0]
        review_signature = [x.text for x in review.find_elements(By.CSS_SELECTOR, 'span.signatures')][0]
        review_date = [x.text for x in review.find_elements(By.CSS_SELECTOR, 'span.date.item')][0]
        review_meta = [x.text for x in review.find_elements(By.CSS_SELECTOR, 'div.meta_row.pull-left > span.item:nth-child(2)')][0]
        review_subtitles = [x.text[:-1] for x in review.find_elements(By.CSS_SELECTOR, 'div.note_contents > span.note_content_field')][:len(review.find_elements(By.CSS_SELECTOR, 'div.note_contents > span.note_content_field')) - len(review.find_elements(By.CSS_SELECTOR, 'div.children div.note_contents')) + 1]
        review_contents = [x.text for x in review.find_elements(By.CSS_SELECTOR, 'div.note_contents > span.note_content_value')][:len(review.find_elements(By.CSS_SELECTOR, 'div.note_contents > span.note_content_field')) - len(review.find_elements(By.CSS_SELECTOR, 'div.children div.note_contents')) + 1]

        dfs.append(pd.DataFrame(data = {'title': review_title, 'signature': review_signature, 'date': review_date, 'meta': review_meta, 'subtitles': review_subtitles, 'contents': review_contents}))

    progress.update(1)

# %%
df = pd.concat(dfs).reset_index(drop = True)

# %%
df

# %%



