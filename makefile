getFullyQualifiedWindowsStylePath=$(shell cygpath --windows --absolute "$(1)")
unslashedDir=$(patsubst %/,%,$(dir $(1)))
pathOfThisMakefile=$(call unslashedDir,$(lastword $(MAKEFILE_LIST)))
pathOfMakePrintableScript:=braids/makerbot_printable_maker/make_printable.py
buildFolder:=${pathOfThisMakefile}/build
sources:=$(wildcard ${pathOfThisMakefile}/*.thing)
targets:=$(foreach source,${sources},${buildFolder}/$(basename $(notdir ${source})).makerbot)
uploadTargets:=$(foreach source,${sources},upload_$(basename $(notdir ${source})))
makerwarePath:=C:\Program Files\MakerBot\MakerBotPrint\resources\app.asar.unpacked\node_modules\MB-support-plugin\mb_ir\MakerWare
uploadPrefix:=$(shell date +%Y%m%d_%H%M%S)--
destinationDirectoryOnTheMakerbot:=/home/usb_storage/
# miraclegrueConfigFile=miracle_config.hjson
miraclegrueConfigFile:=default_miracle_config.json
venv:=$(shell cd "$(abspath $(dir ${pathOfMakePrintableScript}))" > /dev/null 2>&1; pipenv --venv || echo initializeVenv)
# the variable 'venv' will evaluate to the path of the venv, if it exists, or else will evaluate to 'initializeVenv', which is a target that we have created below.
# in either case, we want to use venv as a prerequisite for default.

# default:
	# @echo venv: ${venv}
	# @echo venv: ${venv}

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

${buildFolder}/%.makerbot: ${pathOfThisMakefile}/%.thing ${pathOfMakePrintableScript} | ${buildFolder} ${venv} 
	@echo "====== BUILDING $@ from $< ======= "
	cd "$(abspath $(dir ${pathOfMakePrintableScript}))"; \
	pipenv run python \
		"$(call getFullyQualifiedWindowsStylePath,${pathOfMakePrintableScript})" \
		--makerware_path="${makerwarePath}" \
		--input_model_file="$(call getFullyQualifiedWindowsStylePath,$<)" \
		--input_miraclegrue_config_file="$(call getFullyQualifiedWindowsStylePath,${miraclegrueConfigFile})" \
		--output_annotated_miraclegrue_config_file="$(call getFullyQualifiedWindowsStylePath,${buildFolder}/miracle_config_annotated.hjson)" \
		--output_makerbot_file="$(call getFullyQualifiedWindowsStylePath,$@)" \
		--output_gcode_file="$(call getFullyQualifiedWindowsStylePath, $(dir $@)$(basename $(notdir $@)).gcode)"
upload_%: ${buildFolder}/%.makerbot
	pscp "$(call getFullyQualifiedWindowsStylePath,$<)" "root@makerbot.ad.autoscaninc.com:${destinationDirectoryOnTheMakerbot}${uploadPrefix}$(notdir $<)"

# ${venv}: $(dir ${pathOfMakePrintableScript})/Pipfile $(dir ${pathOfMakePrintableScript})/Pipfile.lock
${venv}: 
	cd "$(abspath $(dir ${pathOfMakePrintableScript}))"; pipenv install

.SILENT:		

.PHONY: default initializeVenv
# SHELL=sh	
	