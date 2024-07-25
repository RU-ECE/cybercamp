all: 01slides_intro_cryptography.pdf 02slides_digital_logic.pdf 03slides_modern_crypto.pdf

01slides_intro_cryptography.pdf: 01slides_intro_cryptography.tex
	pdflatex --shell-escape $<

02slides_digital_logic.pdf: 02slides_digital_logic.tex
	pdflatex --shell-escape $<

03slides_modern_crypto.pdf: 03slides_modern_crypto.tex
	pdflatex --shell-escape $<

clean:
	rm *.log *.out *.snm *.toc *.nav *.aux *.vrb

