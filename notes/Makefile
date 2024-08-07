all: 01slides_intro_cryptography.pdf 02slides_digital_logic.pdf 03slides_modern_crypto.pdf 04slides_attacks.pdf

01slides_intro_cryptography.pdf: 01slides_intro_cryptography.tex
	pdflatex --shell-escape $<

02slides_digital_logic.pdf: 02slides_digital_logic.tex
	pdflatex --shell-escape $<

03slides_modern_crypto.pdf: 03slides_modern_crypto.tex
	pdflatex --shell-escape $<

04slides_attacks.pdf: 04slides_attacks.tex
	pdflatex --shell-escape $<

01slides_intro_cryptography.tex: preamble.tex
	touch 01slides_intro_cryptography.tex

02slides_digital_logic.tex: preamble.tex
	touch 02slides_digital_logic.tex

03slides_modern_crypto.tex: preamble.tex
	touch 03slides_modern_crypto.tex

04slides_attacks.tex: preamble.tex
	touch 04slides_attacks.tex

clean:
	rm *.log *.out *.snm *.toc *.nav *.aux *.vrb

rebuild:
	rm 0[1234]*.pdf
	make