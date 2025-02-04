from src.scraper import GoogleMapsScraper

def main():
    try:
        search_input = input("Enter the search term: ")
        total_input = input("Enter the total number of results to scrape (press Enter for default): ")
        total = int(total_input) if total_input.strip() else 10000

        scraper = GoogleMapsScraper()
        
        for term in search_input.split(","):
            print(f"Scraping results for: {term}")
            business_list = scraper.scrape(term.strip(), total)
            
            filename = f"google_maps_data_{term}".replace(' ', '_')
            business_list.save_to_excel(filename)
            business_list.save_to_csv(filename)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
