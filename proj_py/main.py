from scraper import BMWScraper

def main():
    scraper = BMWScraper()
    try:
        scraper.run()
    except KeyboardInterrupt:
        print("\nScraping interrupted by user. Progress has been saved.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if scraper.driver:
            scraper.driver.quit()

if __name__ == "__main__":
    main() 