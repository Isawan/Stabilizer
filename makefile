# Directories
resources     :=resources
build         :=build
report        :=report

# File test
finalreport   :=$(build)/report.pdf
document      :=$(report)/report.tex
introduction  :=$(report)/introduction.tex
method        :=$(report)/method.tex
results       :=$(report)/results.tex
discussion    :=$(report)/discussion.tex
conclusion    :=$(report)/conclusion.tex
bibligraphy   :=$(report)/biblio.bib

texfiles      :=$(document) $(introduction) $(method) $(results) $(discussion) \
	$(conclusion)


all: $(finalreport)

$(finalreport): $(texfiles) $(bibliography)
	latexmk -pdf -outdir=$(build) -use-make $(document)


clean:
	rm -r $(build)/*
