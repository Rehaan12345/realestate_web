from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse 

# Source: https://www.youtube.com/watch?v=tp_B5tpJS3c&t=40s 

@dataclass 
class Business:
    name: str = None
    address: str = None
    website: str = None
    phone_number_1: str = None
    phone_number_2: str = None # Two phone numbers because sometimes the div for phone_number_1 is not the phone number. 

@dataclass
class BusinessList:
    business_list: list[Business] = field(default_factory=list)

    def dataframe(self):
        return pd.json_normalize((asdict(business) for business in self.business_list), sep="_")
    
    def save_to_excel(self, filename):
        self.dataframe().to_excel(f"{filename}.xlsx", index=False)

    def save_to_csv(self, filename):
        self.dataframe().to_csv(f"{filename}.csv", index=False)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Change headless to true when in production mode
        page = browser.new_page()

        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_timeout(1000) # Can remove in production / change to one second

        page.locator('//*[@id="searchboxinput"]').fill(search_for) # I copied the XPath
        page.wait_for_timeout(3000)

        page.keyboard.press("Enter")
        page.wait_for_timeout(8000)

        listings = page.locator('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[5]/div').all()
        print(len(listings))

        business_list = BusinessList()

        for listing in listings: # Looping through the first five. Need to scroll down to get the rest because they only show up when you scroll.
            listing.click()
            page.wait_for_timeout(5000)

            name_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1'
            address_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[3]/button/div/div[2]/div[1]'
            website_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[5]/a/div/div[2]/div[1]'
            phone_number_1_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[7]/button/div/div[2]/div[1]'
            phone_number_2_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[6]/button/div/div[2]/div[1]'

            business = Business()
            business.name = page.locator(name_xpath).text_content()
            print(business.name)
            business.address = page.locator(address_xpath).inner_text()
            print(business.address)
            business.website = page.locator(website_xpath).inner_text()
            print(business.website)
            business.phone_number_1 = page.locator(phone_number_1_xpath).inner_text()
            print(business.phone_number_1)
            business.phone_number_2 = page.locator(phone_number_2_xpath).inner_text()
            print(business.phone_number_2)
            

            business_list.business_list.append(business)
        
        business_list.save_to_excel("google_maps_data")
        business_list.save_to_csv("google_maps_data")


        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-l", "--location", type=str)
    args = parser.parse_args()

    if args.location and args.search:
        search_for = f"{args.search} {args.location}"
    else:
        search_for = "real estate boston"
    
    main()