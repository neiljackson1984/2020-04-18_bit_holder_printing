getFullyQualifiedWindowsStylePath=$(shell cygpath --windows --absolute "$(1)")
unslashedDir=$(patsubst %/,%,$(dir $(1)))
pathOfThisMakefile=$(call unslashedDir,$(lastword $(MAKEFILE_LIST)))
pathOfMakePrintableScript=braids/makerbot_printable_maker/make_printable.py
buildFolder=${pathOfThisMakefile}/build
sources=$(wildcard ${pathOfThisMakefile}/*.thing)
targets=$(foreach source,${sources},${buildFolder}/$(basename $(notdir ${source})).makerbot)
uploadTargets=$(foreach source,${sources},upload_$(basename $(notdir ${source})))
makerwarePath=C:\Program Files\MakerBot\MakerBotPrint\resources\app.asar.unpacked\node_modules\MB-support-plugin\mb_ir\MakerWare
uploadPrefix=$(shell date +%Y%m%d_%H%M%S)--
destinationDirectoryOnTheMakerbot=/home/usb_storage/
miraclegrueConfigFile=miracle_config.hjson

# default:
	# @echo pathOfThisMakefile: $(pathOfThisMakefile)
	# @echo test: $(foreach source,${sources},$(notdir ${source}))
	# @echo sources: $(sources)
	# @echo targets: $(targets)

default: $(targets) $(uploadTargets)

${buildFolder}:
	mkdir --parents "${buildFolder}"
#buildFolder, when included as a prerequisite for rules, should be declared as an order-only prerequisites (by placing it to the right of a "|" character in the 
# list of prerequisites.  See https://www.gnu.org/software/make/manual/html_node/Prerequisite-Types.html 

${buildFolder}/%.makerbot: ${pathOfThisMakefile}/%.thing  | ${buildFolder}
	@echo "====== BUILDING $@ from $< ======= "
	cd "$(abspath $(dir ${pathOfMakePrintableScript}))"; \
	pipenv install; \
	pipenv run python \
		"$(call getFullyQualifiedWindowsStylePath,${pathOfMakePrintableScript})" \
		--makerware_path="${makerwarePath}" \
		--input_file="$(call getFullyQualifiedWindowsStylePath,$<)" \
		--output_makerbot_file="$(call getFullyQualifiedWindowsStylePath,$@)" \
		--output_gcode_file="$(call getFullyQualifiedWindowsStylePath, $(dir $@)$(basename $(notdir $@)).gcode)" \
		--miraclegrue_config_file="$(call getFullyQualifiedWindowsStylePath,${miraclegrueConfigFile})" \
		--miraclegrue_config_schema_file="$(call getFullyQualifiedWindowsStylePath,research/schema.json)" \
		--output_annotated_miraclegrue_config_file="$(call getFullyQualifiedWindowsStylePath,${buildFolder}/miracle_config_annotated.hjson)" \
		--old_miraclegrue_config_file="$(call getFullyQualifiedWindowsStylePath,original.json)" \
		--old_miraclegrue_config_schema_file="$(call getFullyQualifiedWindowsStylePath,research/miracle_grue_3.9.4_config_schema.json)" 	
	

upload_%: ${buildFolder}/%.makerbot
	pscp -v "$(call getFullyQualifiedWindowsStylePath,$<)" "root@makerbot.ad.autoscaninc.com:${destinationDirectoryOnTheMakerbot}${uploadPrefix}$(notdir $<)"


.SILENT:		


# SHELL=sh	
	