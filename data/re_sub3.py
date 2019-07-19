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
        path = "%s/%s.abc" % (abcPath, selectGeo[i])
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
        path = "%s/%s.abc" % (abcPath, name)
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
    path = "%s/%s.abc" % (abcPath, "All")
    startTime, endTime = getTime()
    command = commandline_exportall % (
        startTime, endTime, step_s, step, allOptions, path)
    try:
        cmds.AbcExport(j=command)
    except Exception:
        pass
