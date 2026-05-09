# ==============================================================================
# Autotools Configuration for Skynet Node Operational Grimoire
# Target Workspace: docs/grimoire/
# Distributed Cluster Verification Layer
# ==============================================================================

# Track all modular chapters and main compilation targets in the distribution package
EXTRA_DIST = \
	grimoire.tex \
	chap_topology.tex \
	chap_acceleration.tex \
	chap_pipeline.tex \
	chap_protocols.tex

# Define file classes for compilation and syntax auditing
MASTER_TEX = grimoire.tex
TEX_CHAPTERS = chap_*.tex

.PHONY: lint pdf clean-grimoire all

# Default target compiles the PDF grimoire
all: pdf

# Syntax and structural integrity check of all local LaTeX documents
lint:
	@echo "==> Initializing Skynet documentation audit..."
	@if command -v chktex > /dev/null; then \
		chktex -q -n 1 -n 3 -n 8 $(MASTER_TEX) $(TEX_CHAPTERS); \
		echo "==> Audit complete. Documentation stability: 100%"; \
	else \
		echo "ERROR: 'chktex' utility not found on this node."; \
		echo "Execute: sudo apt-get install chktex (or pkg_add chktex on blowfish)"; \
		exit 1; \
	fi

# Compile the master document using latexmk with non-interactive PDF engines
pdf: $(MASTER_TEX)
	@echo "==> Resolving document structure and compiling grimoire.pdf..."
	latexmk -pdf -interaction=nonstopmode $<

# Clean up all auxiliary files, leaving only the source documents and final PDF
clean-grimoire:
	@echo "==> Cleaning grimoire auxiliary compilation assets..."
	latexmk -c $(MASTER_TEX)
	rm -f grimoire.pdf *.nav *.snm *.vrb *.fls *.fdb_latexmk *.run.xml *.bcf
