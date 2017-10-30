# Directories
resources     :=resources
build         :=build
report        :=report

# File test
document      :=$(report)/document.tex


all: $(finalreport)

$(finalreport): 
	latexmk -pdf -outdir=$(build) -use-make $(document)


clean:
	rm -r $(build_dir)
