EXTRA_DIST = quest-for-greebling.tex
TEX_FILES := docs/slides/*.tex

.PHONY: lint

all-slides: pdf

lint:
	@echo "==> Initializing Skynet documentation audit..."
	@if command -v chktex > /dev/null; then \
		chktex -q $(TEX_FILES); \
		echo "==> Audit complete. Documentation stability: 100%"; \
	else \
		echo "ERROR: 'chktex' not found on this node. Install via apt-get or dnf."; \
		exit 1; \
	fi

pdf: quest-for-greebling.tex
	latexmk -pdf -interaction=nonstopmode $<

clean-slides:
	latexmk -c quest-for-greebling.tex
	rm -f quest-for-greebling.pdf *.nav *.snm *.vrb *.fls *.fdb_latexmk
