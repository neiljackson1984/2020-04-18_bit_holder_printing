buildPath=build
getFullyQualifiedWindowsStylePath=$(shell cygpath --windows --absolute "$(1)")
pathOfMakePrintableScript=braids/makerbot_printable_maker/make_printable.py

default:
	mkdir -p ${buildPath}
	# cd "$(abspath $(dir ${pathOfMakePrintableScript}))"; \
		# pipenv install
	# cd "$(abspath $(dir ${pathOfMakePrintableScript}))"; \
	# pipenv run python \
		# "$(call getFullyQualifiedWindowsStylePath,${pathOfMakePrintableScript})" \
		# --makerware_path="C:\Program Files\MakerBot\MakerBotPrint\resources\app.asar.unpacked\node_modules\MB-support-plugin\mb_ir\MakerWare" \
		# --input_file="$(call getFullyQualifiedWindowsStylePath,bit_holder.thing)" \
		# --output_file="$(call getFullyQualifiedWindowsStylePath,${buildPath}/bit_holder.makerbot)" \
		# --miraclegrue_config_file="$(call getFullyQualifiedWindowsStylePath,miracle_config.hjson)" \
		# --miraclegrue_config_schema_file="$(call getFullyQualifiedWindowsStylePath,research/schema.json)" \
		# --output_annotated_miraclegrue_config_file="$(call getFullyQualifiedWindowsStylePath,${buildPath}/miracle_config_annotated.hjson)"
	cd "$(abspath $(dir ${pathOfMakePrintableScript}))"; \
	pipenv run python \
		"$(call getFullyQualifiedWindowsStylePath,${pathOfMakePrintableScript})" \
		--makerware_path="C:\Program Files\MakerBot\MakerBotPrint\resources\app.asar.unpacked\node_modules\MB-support-plugin\mb_ir\MakerWare" \
		--input_file="$(call getFullyQualifiedWindowsStylePath,bit_holder.thing)" \
		--output_file="$(call getFullyQualifiedWindowsStylePath,${buildPath}/bit_holder.makerbot)" \
		--miraclegrue_config_file="$(call getFullyQualifiedWindowsStylePath,miracle_config.hjson)" \
		--miraclegrue_config_schema_file="$(call getFullyQualifiedWindowsStylePath,research/schema.json)" \
		--output_annotated_miraclegrue_config_file="$(call getFullyQualifiedWindowsStylePath,${buildPath}/miracle_config_annotated.hjson)" \
		--old_miraclegrue_config_file="$(call getFullyQualifiedWindowsStylePath,original.json)" \
		--old_miraclegrue_config_schema_file="$(call getFullyQualifiedWindowsStylePath,research/miracle_grue_3.9.4_config_schema.json)" 
		


.SILENT:		