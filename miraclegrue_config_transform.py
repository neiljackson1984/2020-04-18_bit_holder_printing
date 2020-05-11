import hjson

def transformMiraclegrueConfig(config: dict):
    # config['foo'] = "ahoy there!"
    # print("from within transformMiraclegrueConfig: globals().keys(): " + str(globals().keys()))		# globals().keys()
    # # print("math.cos(32): " + str(math.cos(32)))		# math.cos(32)
    # # the above will not work unless we import the math module
    # return config
    
    
    # return hjson.load(open("U:\\2020-04-18_bit_holder_printing\\miracle_config.hjson" ,'r'))

    try: 
        del config['baseLayer']
    except:
        pass
    config['baseLayerHeight'] = 0.4
    config['baseLayerWidth'] = 0.9
    config['bedZOffset'] = -0.25
    config['doFixedShellStart'] = False
    config['extruderProfiles'][0]['extrusionProfiles']['base_layer_surface']['extrusionVolumeMultiplier'] = 1.3
    config['extruderProfiles'][0]['extrusionProfiles']['base_layer_surface']['fanSpeed'] = 0
    config['extruderProfiles'][0]['extrusionProfiles']['base_layer_surface']['feedtrate'] = 4
    config['extruderProfiles'][0]['extrusionProfiles']['base_layer_surface']['temperature'] = 225
    config['fanLayer'] = 2
    config['modelFillProfiles']['base_layer_surface']['extrusionWidth'] = 1.5
    config['modelFillProfiles']['sparse']['density'] = 0.3
    config['modelShellProfiles']['base_layer_surface']['infillShellSpacingMultiplier'] = 0.1
    config['modelShellProfiles']['base_layer_surface']['innerExtrusionProfile'] = "base_layer_surface"
    config['modelShellProfiles']['base_layer_surface']['insetDistanceMultiplier'] = 0.9
    config['modelShellProfiles']['base_layer_surface']['numberOfShells'] = 2
    config['modelShellProfiles']['base_layer_surface']['outerExtrusionProfile'] = "base_layer_surface"
    config['paddedBaseWidth'] = 2
    config['raftModelShellsSpacing'] = 0.19
    config['doPaddedBase'] = True

    return config


    
