import os
import bs4
import requests
import re
import time

# Todo: to scrape only English books
# Todo: to get book title
# Todo: to create folders separately in alphabetical way?

def main():
	alphabetical_list = "a"
	for char in alphabetical_list:
		try:
			url = "https://www.gutenberg.org/browse/titles/{}".format(char)
			site = pull_site(url)
			bookid_list = scrape_bookid(site)
			for book_id in bookid_list:
				book_data = download_books(book_id)
				save(book_id, book_data)

				time.sleep(2)
		except:
			continue


def pull_site(url):
		raw_site_page = requests.get(url)
		raw_site_page.raise_for_status()
		return raw_site_page


def scrape_bookid(site):
	soup = bs4.BeautifulSoup(site.text, 'html.parser')
	bookid_list = []
	for a in soup.find_all('a', href=True):
		# e.g. https://www.gutenberg.org/ebooks/14269
		link_to_text = re.search(r'^/ebooks/(\d+)$', a['href'])
		if link_to_text:
			bookid_list.append(link_to_text.group(1))
	return bookid_list


def download_books(book_id):
	# http://www.gutenberg.org/cache/epub/14269/pg14269.txt
	url = "https://www.gutenberg.org/cache/epub/{}/pg{}.txt".format(book_id, book_id)
	response = requests.get(url)
	response.raise_for_status()
	return response.text


def save(book_id, book_data):
	book_folder = "/Users/admin/Desktop/books"
	if not os.path.exists(book_folder):
		os.mkdir(book_folder)

	book_name = "book{}.txt".format(book_id)
	full_path = os.path.join(book_folder, book_name)
	with open(full_path, 'w', encoding='utf-8') as fout:
		fout.write(book_data)


if __name__ == '__main__':
	main()
