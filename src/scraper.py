from playwright.sync_api import sync_playwright, Page
from typing import Tuple
from .model.business import Business
from .model.business_list import BusinessList

def extract_coordinates_from_url(url: str) -> Tuple[float, float]:
    """Extract latitude and longitude from Google Maps URL"""
    coordinates = url.split('/@')[-1].split('/')[0]
    return float(coordinates.split(',')[0]), float(coordinates.split(',')[1])

class GoogleMapsScraper:
    def __init__(self):
        self.xpaths = {
            'name': '//h1[@class="DUwDvf lfPIob"]',
            'address': '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]',
            'website': '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]',
            'phone': '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]',
            'review_count': '//button[@class="HHrUdb fontTitleSmall rqjGif"]//span',
            'reviews_avg': '//div[@jsaction="pane.reviewChart.moreReviews"]//div[@role="img"]'
        }

    def _scroll_and_collect_listings(self, page: Page, total: int) -> list:
        page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')
        previously_counted = 0
        
        while True:
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(3000)
            
            current_count = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count()
            
            if current_count >= total:
                listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()[:total]
                return [listing.locator("xpath=..") for listing in listings]
            
            if current_count == previously_counted:
                listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()
                return [listing.locator("xpath=..") for listing in listings]
                
            previously_counted = current_count
            print(f"Currently Scraped: {current_count}")

    def _extract_business_data(self, page: Page) -> Business:
        business = Business()
        
        business.map_url = page.url
        
        if page.locator(self.xpaths['name']).count() > 0:
            business.name = page.locator(self.xpaths['name']).inner_text()
        
        if page.locator(self.xpaths['address']).count() > 0:
            business.address = page.locator(self.xpaths['address']).all()[0].inner_text()
            
        if page.locator(self.xpaths['website']).count() > 0:
            business.website = page.locator(self.xpaths['website']).all()[0].inner_text()
            
        if page.locator(self.xpaths['phone']).count() > 0:
            business.phone_number = page.locator(self.xpaths['phone']).all()[0].inner_text()
            
        if page.locator(self.xpaths['review_count']).count() > 0:
            business.reviews_count = int(
                page.locator(self.xpaths['review_count']).inner_text()
                .split()[0]
                .replace('.', '')
                .strip()
            )
            
        if page.locator(self.xpaths['reviews_avg']).count() > 0:
            business.reviews_average = float(
                page.locator(self.xpaths['reviews_avg']).get_attribute("aria-label")
                .split()[0]
                .replace(',', '.')
                .strip()
            )
            
        business.latitude, business.longitude = extract_coordinates_from_url(page.url)
        
        return business

    def scrape(self, search_term: str, total_results: int = 10000) -> BusinessList:
        business_list = BusinessList()
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            page.goto("https://www.google.com/maps", timeout=60000)
            page.wait_for_timeout(5000)
            
            page.locator('//input[@id="searchboxinput"]').fill(search_term)
            page.wait_for_timeout(3000)
            page.keyboard.press("Enter")
            page.wait_for_timeout(5000)
            
            listings = self._scroll_and_collect_listings(page, total_results)
            print(f"Total Listings Found: {len(listings)}")
            
            for listing in listings:
                try:
                    listing.click()
                    page.wait_for_timeout(5000)
                    
                    business = self._extract_business_data(page)
                    business_list.business_list.append(business)
                    print(f"Scraped: {business.name}")
                    
                except Exception as e:
                    print(f"Error scraping listing: {e}")
            
            browser.close()
            
        return business_list
