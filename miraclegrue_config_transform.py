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
    
    
    
    config['doRaft'] = True
    config['doSupport'] = True
    config['doSupportUnderBridges'] = True
    config['doBreakawaySupport'] = True
    
     #/* supportLayerHeight
     # * name: Support Layer Height
     # * description: Sets the layer height used for support structures. This layer height can be greater than the model layer height for faster printing.
     # * group: Support
     # * max: 0.4
     # * min: 0.05
     # * step: 0.01
     # * type: Scalar
     # * unit: mm
     # */
    config['supportLayerHeight'] = 0.2
    
     #/* supportLeakyConnections
     # * name: Leaky Connections
     # * default: true
     # * description: Select for less connected support structures which are easier to remove
     # * group: Support
     # * type: boolean
     # */
    config['supportLeakyConnections'] = True
    
    
    # /* supportMinRegionArea
     # * name: Support Minimum Region Area
     # * default: 10
     # * description: Anything smaller than this area gets expanded to a printable size roughly corresponding to 2 beadwidths so at least an enclosed shell can be extruded.  This value is what determines how much cascading effect our supports have.  Being that supports are drawn top down, the larger this value is, the thicker all downstream supports become through ripple effect.
     # * group: Support
     # * max: 100
     # * min: 0
     # * step: 1
     # * type: Scalar
     # */
    # // VALUE NOT SPECIFIED
    
    #/* supportModelSpacing
    # * name: Support to Model Spacing
    # * description: Distance between supports and the printed object in the horizontal plane
    # * group: Support
    # * max: 0.5
    # * min: 0.0
    # * step: 0.01
    # * type: Scalar
    # * unit: mm
    # */
    config['supportModelSpacing'] = 0.0
 
    return config


    
