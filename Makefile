.PHONY: build html clean

build:
	typst compile --root . book/attapl-uk.typ attapl-uk.pdf

# HTML-видання по розділах -> site/ (експериментальний експорт Typst)
html:
	mkdir -p build
	typst compile --root . --features html --format html book/attapl-uk.typ build/book.html
	python3 tools/split_html.py build/book.html site
	typst compile --root . book/attapl-uk.typ site/attapl-uk.pdf

clean:
	rm -rf attapl-uk.pdf build site
