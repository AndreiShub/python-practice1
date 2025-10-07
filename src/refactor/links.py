from datetime import datetime, date
from bs4 import BeautifulSoup
import logging

def parse_page_links(html: str, start_date: date, end_date: date) -> list[tuple[str, date]]:
    """
    Парсит ссылки на бюллетени с одной страницы:
    <a class="accordeon-inner__item-title link xls" href="/upload/reports/oil_xls/oil_xls_20240101_test.xls">link1</a>
    """
    results = []
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="accordeon-inner__item-title link xls")

    for link in links:
        href = link.get("href")
        if not href:
            continue

        href = href.split("?")[0]
        if "/upload/reports/oil_xls/oil_xls_" not in href or not href.endswith(".xls"):
            continue

        date_str = href.split("oil_xls_")[1][:8]
        try: 
            file_date = datetime.strptime(date_str, "%Y%m%d").date()
        except ValueError:
            logging.warning(f"Некорректная дата в ссылке: {href}")
            continue
        
        if start_date <= file_date <= end_date:
            full_url = href if href.startswith("http") else f"https://spimex.com{href}"
            results.append((full_url, file_date))
        else:
            logging.debug(f"Ссылка {href} вне диапазона дат")


    return results
