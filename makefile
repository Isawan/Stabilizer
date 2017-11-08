# Directories
resources     :=resources
build         :=build
report        :=report

# File test
finalreport   :=$(build)/report.pdf
document      :=$(report)/report.tex
introduction  :=$(report)/introduction.tex
method        :=$(report)/method.tex
results       :=$(report)/result.tex
discussion    :=$(report)/discussion.tex
conclusion    :=$(report)/conclusion.tex

texfiles      :=$(document) $(introduction) $(method) $(result) $(discussion) \
	$(conclusion)


all: $(finalreport)

$(finalreport): $(texfiles)
	latexmk -pdf -outdir=$(build) -use-make $(document)


clean:
	rm -r $(build)/*
