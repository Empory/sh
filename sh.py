import pyshorteners

def shorten_url(long_url):
    # Initialize the Shortener
    s = pyshorteners.Shortener()

    # Shorten the URL
    short_url = s.tinyurl.short(long_url)

    return short_url

if __name__ == "__main__":
    long_url = input("Enter the URL to shorten: ")
    short_url = shorten_url(long_url)
    print(f"Shortened URL: {short_url}")
