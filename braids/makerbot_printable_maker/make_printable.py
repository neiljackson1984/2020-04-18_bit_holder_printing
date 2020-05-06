import argparse
import os
import re
import json
import pathlib
import sys
import math
# import numpy
import subprocess
import hjson
import tempfile


parser = argparse.ArgumentParser(description="Generate a .makerbot toolpath file from a .thing file and a mircale_grue configuration file.")
parser.add_argument("--makerware_path", action='store', nargs=1, required=True, 
    help=
        "the path of the MakerWare folder, which comes with Makerbot Print.  Typically, on a " 
        + "Windows machine, the MakerWare path is " 
        + "\"" 
        + "C:\\Program Files\\MakerBot\\MakerBotPrint\\resources\\app.asar.unpacked\\node_modules\\MB-support-plugin\\mb_ir\\MakerWare"
        + "\""
        + "."
)
parser.add_argument("--input_model_file", action='store', nargs=1, required=True, help="the .thing file to be sliced.")
parser.add_argument("--input_miraclegrue_config_file", action='store', nargs=1, required=True, help="The miraclegrue config file.  This may be either a plain old .json file, or an hjson file, which is json with more relaxed syntax, and allows comments.")
parser.add_argument("--output_annotated_miraclegrue_config_file", action='store', nargs=1, required=False, help="An hjson file to be created by inserting the descriptions from the schema, as comments, interspersed within the miracle_grue_config json entries.")
parser.add_argument("--output_makerbot_file", action='store', nargs=1, required=False, help="the .makerbot file to be created.")
parser.add_argument("--output_gcode_file", action='store', nargs=1, required=False, help="the .gcode file to be created.")


args, unknownArgs = parser.parse_known_args()

#resolve all of the paths passed as arguments to fully qualified paths:
input_model_file_path = pathlib.Path(args.input_model_file[0]).resolve()
output_makerbot_file_path = (pathlib.Path(args.output_makerbot_file[0]).resolve() if args.output_makerbot_file else None)
output_gcode_file_path = (pathlib.Path(args.output_gcode_file[0]).resolve() if args.output_gcode_file else None)
makerware_path = pathlib.Path(args.makerware_path[0]).resolve()
input_miraclegrue_config_file_path = pathlib.Path(args.input_miraclegrue_config_file[0]).resolve()



#the path of the python executable included with makerware:
makerware_python_executable_path = makerware_path.joinpath("python3.4.exe").resolve()
makerware_python_working_directory_path = makerware_path.joinpath("python34").resolve()
miracle_grue_executable_path = makerware_path.joinpath("miracle_grue.exe").resolve()

#the path of the makerware sliceconfig python script:
makerware_sliceconfig_path = makerware_path.joinpath("sliceconfig").resolve()

miraclegrueConfig = hjson.load(open(input_miraclegrue_config_file_path ,'r'))

def tabbedWrite(file, content, tabLevel=0, tabString="    ", linePrefix=""):
    file.write(
        "\n".join(
            map( 
                lambda y: tabString*tabLevel + linePrefix + y,
                str(content).splitlines()
            )
        ) + "\n"
    )

def prefixAllLines(x, prefix):
    return "\n".join(
        map( 
            lambda y: prefix + y,
            str(x).splitlines()
        )
    )

def indentAllLines(x, indentString="    "):
    return prefixAllLines(x, indentString)

def makeBlockComment(x):
    lines = str(x).splitlines()  
    return "\n".join(
        ["/* " + lines[0]]
        + list(
            map(
                lambda y: " * " + y,
                lines[1:]
            )
        )
        + [" */"]
    )

def addParentheticalRemarkAtEndOfFirstLine(x, remark=None): 
    lines = str(x).splitlines()
    return "\n".join(
        [lines[0] + (" (" + str(remark) + ")" if remark else "")]
        + lines[1:]
    )


# path is expected to be a list (of keys)
def getSchemedTypeName(path, schema):
    if len(path) == 0:
        return '__top__'
    schemedTypeOfParent = getSchemedType(path[:-1],schema)
    if schemedTypeOfParent:
        if schemedTypeOfParent['mode'] == "aggregate":
            memberSpec = (
                    list(
                        filter(
                            lambda x: x['id'] == path[-1],
                            schemedTypeOfParent["members"]
                        )
                    ) or [None]
                )[0]
            if memberSpec:
                return memberSpec['type']
        elif schemedTypeOfParent['json_type'] == "object":
            return schemedTypeOfParent['value_type']
        elif schemedTypeOfParent['json_type'] == "array":
            return schemedTypeOfParent['element_type']
    return None

def getSchemedType(path, schema):
    # print("getSchemedType() was called with path " + str(path))
    schemedTypeName = getSchemedTypeName(path, schema)
    if schemedTypeName:
        return schema.get(schemedTypeName)
    return None

def getMemberIds(schemedType):
    return (
        map(
            lambda x: x['id'],
            schemedType['members']
        )
        if (schemedType and schemedType.get('mode') == "aggregate" )
        else None
    )


#returns the annotation text that is to appear immediately
# before the entry having the specified path.
def getAnnotationForEntry(path, schema):
    schemedTypeOfParent = getSchemedType(path[:-1],schema)
    if schemedTypeOfParent and schemedTypeOfParent['mode'] == "aggregate":
        memberSpec = (
                list(
                    filter(
                        lambda x: x['id'] == path[-1],
                        schemedTypeOfParent["members"]
                    )
                ) or [None]
            )[0]
        if memberSpec:
            return "\n".join(
                [path[-1]]
                + (["name: " + memberSpec.get('name')] if (memberSpec.get('name') and (memberSpec.get('name') != path[-1])) else [])
                + list(
                    map(
                        lambda k: k + ": " + hjson.dumps(memberSpec[k]),
                        filter(
                            lambda k: k not in ['id','name'],
                            memberSpec.keys()
                        )
                    )
                )   
            )
        else:
            return "THIS ELEMENT IS NOT SPECIFIED IN THE SCHEMA."
    else:
        return None

#entryFormat shall be a streing that is either "dictEntry" or "listEntry"
# def dumpsAnnotatedHjsonEntry(value, path, schema, entryFormat):
#     # print("dumpsAnnotatedHjsonEntry was called with path: " + str(path))
#     entry = (str(path[-1]) + ": "  if entryFormat == "dictEntry" else "") + dumpsAnnotatedHjsonValue(value, path, schema)
#     annotation = getAnnotationForEntry(path, schema)
#     return ("\n" + prefixAllLines(annotation, "// ") + "\n" if annotation else "") + entry


def dumpsAnnotatedHjsonValue(value, path, schema):
    # print("now working on path: " + str(path))
    returnValue=""
    schemedType = getSchemedType(path, schema)
    
    isIterable = (
        isinstance(value, dict)
        or isinstance(value, list)
        or (schemedType and schemedType.get('mode') == "aggregate" )
        or (schemedType and schemedType.get('json_type') == "object") 
        or (schemedType and schemedType.get('json_type') == "array" )
    )
    if isIterable:
        if isinstance(value, dict):
            braces=["{","}"]
            keysInValue=set(value.keys())
            keysInSchema=set(getMemberIds(schemedType) or [])
            subentryFormat="dictEntry"
        else:
            braces=["[","]"]
            keysInValue=set(range(len(value)))
            keysInSchema=set([])
            subentryFormat="listEntry"
        returnValue += braces[0] + "\n"
        for key in sorted(list(keysInValue.union(keysInSchema))):
            annotation = getAnnotationForEntry(path + [key], schema)
            
            if key in keysInValue:
                subValue = value[key]
                entry = (key + ": "  if subentryFormat == "dictEntry" else "") + dumpsAnnotatedHjsonValue(subValue, path + [key], schema)
            else:
                subValue = None
                entry = "// VALUE NOT SPECIFIED"
            
            returnValue += indentAllLines(
                (
                    "\n" + makeBlockComment(annotation) + "\n" 
                    if annotation else ""
                ) 
                + entry
            ) + "\n"
        returnValue += braces[1] + "\n"
    else:
        returnValue += hjson.dumps(value) + "\n"
    return returnValue    

# if args.miraclegrue_config_schema_file and args.output_annotated_miraclegrue_config_file:
if args.output_annotated_miraclegrue_config_file:
    # generate an annotated hjson version of the config file, by
    # adding the descriptions in the schema as comments.
    # schema = json.load(open(pathlib.Path(args.miraclegrue_config_schema_file[0]).resolve() ,'r'))
    process = subprocess.run(
        args=[
            str(miracle_grue_executable_path),
            "--config-schema"   
        ],
        capture_output = True,
        text=True
    )
    schema = json.loads(process.stdout)
    # oldSchema = json.load(open(pathlib.Path(args.old_miraclegrue_config_schema_file[0]).resolve(),'r'))
    # oldMiraclegrueConfig = json.load(open(pathlib.Path(args.old_miraclegrue_config_file[0]).resolve(),'r'))
    
    with open(pathlib.Path(args.output_annotated_miraclegrue_config_file[0]).resolve() ,'w') as annotatedConfigFile:
        annotatedConfigFile.write(
            dumpsAnnotatedHjsonValue(
                value=miraclegrueConfig,
                schema=schema,
                path=[]
            )
        )

with tempfile.NamedTemporaryFile(mode='w', delete=False) as temporary_miraclegrue_config_file:
    json.dump(miraclegrueConfig, temporary_miraclegrue_config_file, sort_keys=True, indent=4)
    temporary_miraclegrue_config_file_path = pathlib.Path(temporary_miraclegrue_config_file.name).resolve()

outputToolpathFilePaths = [output_makerbot_file_path]
if output_gcode_file_path: 
    #TO DO: fill in the gcode generation process here.
    pass

if output_makerbot_file_path:
    subprocessArgs = [
        str(makerware_python_executable_path),
        str(makerware_sliceconfig_path),
        "--status-updates",
        "--input=" + str(input_model_file_path) +  "",
        "--output=" + str(output_makerbot_file_path) +  "",
        "--machine_id=" + miraclegrueConfig['_bot'] + "",
        "--extruder_ids=" + ",".join(miraclegrueConfig['_extruders']) + "",
        "--material_ids=" + ",".join(miraclegrueConfig['_materials']) + "",
        "--profile=" + str(temporary_miraclegrue_config_file_path) + "" ,
        "slice"
    ]

    process = subprocess.Popen(
        cwd=makerware_python_working_directory_path,
        args=subprocessArgs,
        # capture_output = True,
        text=True,
        stdout=subprocess.PIPE
    )
    for line in iter(process.stdout.readline, 'b'):
        if line:
            sys.stdout.write(line)
        else:
            break

    print("\n")
    print("process.args: " + str(process.args))
    print("\n")
    print("process.stdout: " + str(process.stdout))
    print("\n")
    print("process.stderr: " + str(process.stderr))
    print("\n")
    print("process.returncode: " + str(process.returncode))
    print("\n")
    print("temporary_miraclegrue_config_file_path: " + str(temporary_miraclegrue_config_file_path))
    print("\n")
    print("temporary_miraclegrue_config_file_path: " + str(temporary_miraclegrue_config_file_path))
    print("\n")
    print("temporary_miraclegrue_config_file_path: " + str(temporary_miraclegrue_config_file_path))
    print("\n")

# print("process.stderr: " + json.dumps(json.loads(str(process.stderr))) )




