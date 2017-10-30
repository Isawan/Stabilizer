# Directories
resources     :=resources
build         :=build
report        :=report

# File test
finalreport   :=$(build)/report.pdf
document      :=$(report)/report.tex


all: $(finalreport)

$(finalreport): 
	latexmk -pdf -outdir=$(build) -use-make $(document)


clean:
	rm -r $(build)/*
