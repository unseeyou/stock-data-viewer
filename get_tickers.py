import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

def lookup_ticker(driver: webdriver.Edge, company: str) -> str | None:
    try:
        company = company.replace("Ltd", "Limited")
        URL = "https://www.asx.com.au/asx/research/codeLookup.do?by=searchByName&returnToFormIndex=&codeFormElement=&nameFormElement=&nameToSearch="
        driver.get(URL + company)
        t = driver.find_element(By.CLASS_NAME, "context").text
        return t + ".AX"
    except selenium.common.exceptions.NoSuchElementException:
        return None


def lookup_all_tickers(companies: list[str]) -> dict[str, str | None]:
    # make Edge headless
    edge_options = webdriver.EdgeOptions()
    edge_options.use_chromium = True  # if we miss this line, we can't make Edge headless
    # A little different from Chrome cause we don't need two lines before 'headless' and 'disable-gpu'
    edge_options.add_argument('headless')
    edge_options.add_argument('disable-gpu')
    driver = webdriver.Edge(options=edge_options)

    tickers = {c: None for c in companies}

    for company in companies:
        tickers[company] = lookup_ticker(driver, company)

    driver.close()
    return tickers
