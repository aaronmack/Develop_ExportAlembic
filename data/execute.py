# ################################## Sub1 ############################################### #
import maya.cmds as cmds
import maya.mel as mel
cmds.loadPlugin('AbcExport.mll')
# ################################## Sub2 ############################################### #
name = ""
maya_namespace = ""
sel_file_name = "XHQS_EP001_SC009_0037_ANI_V001"
frameMode = 0
endTimeSet = ""
step = 1
mode = 0
allOptions = "-writeColorSets -worldSpace -writeUVSets -writeVisibility -autoSubd -writeFaceSets -uvWrite -dataFormat ogawa"
abcPath = "C:\\Users\\Drock_Li\\Desktop\\abc"
type = "SHOT_CAMERA"
selectGeo = [u'SHOT_CAMERA']
startTimeSet = ""

# ################################## Sub3 ############################################### #
step_s = "-step"
lights = ["Om"]
ref = maya_namespace
findName = "%s%s" % (ref, name)
name_complete = "%s%s|%s%s" % (ref, type, ref, name)

commandline = "-frameRange %d %d %s %s %s -root |%s -file %s"
commandline_exportall = "-frameRange %d %d %s %s %s -file %s"

# By name
"Prop|sub|pCube1"
#selectGeo = cmds.ls(sl=True)


def getTime():
    if frameMode == 0:
        startTime = cmds.playbackOptions(q=True, min=True)
        endTime = cmds.playbackOptions(q=True, max=True)
        return startTime, endTime
    if frameMode == 1:
        startTime = startTimeSet
        endTime = endTimeSet
        return startTime, endTime


# Export select option
if mode == 0:
    startTime, endTime = getTime()

    for i in range(len(selectGeo)):
        m1_export_name = "%s%s" % (ref, selectGeo[i])
        path = "%s/%s_%s.abc" % (abcPath, selectGeo[i], sel_file_name)
        command = commandline % (
        startTime, endTime, step_s, step, allOptions,
        m1_export_name, path)
        try:
            cmds.AbcExport(j=command)
        except Exception:
            pass

# export by name
if mode == 1:
    if cmds.objExists(findName):
        path = "%s/%s_%s.abc" % (abcPath, name, sel_file_name)
        startTime, endTime = getTime()

        command = commandline % (
            startTime, endTime, step_s, step, allOptions,
            name_complete, path)
        try:
            cmds.AbcExport(j=command)
        except Exception:
            pass
    else:
        pass

# export all
if mode == 2:
    path = "%s/%s_%s.abc" % (abcPath, "All", sel_file_name)
    startTime, endTime = getTime()
    command = commandline_exportall % (
        startTime, endTime, step_s, step, allOptions, path)
    try:
        cmds.AbcExport(j=command)
    except Exception:
        pass
