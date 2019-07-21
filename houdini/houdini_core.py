try:
    import hou
except ImportError:
    pass


def create_alembic_single(paths):
    node = hou.node("/obj")
    hou.cd("/obj")
    pos_y = 0
    for key, value in paths.items():
        # Create Geo node
        pwd = hou.pwd().createNode("geo", node_name=key)
        pos_y += 1
        pwd.setPosition([2, pos_y])
        hou.cd("/obj/" + str(pwd))
        pwd.setColor(hou.Color(0, 0, 0))

        # Create alembic node
        alembic = hou.pwd().createNode("alembic")
        alembic.setName(key)

        # Set parameters
        alembic.setParms({"fileName": value, "curveFilter": 0, "NURBSFilter": 0})

        # Create Out node
        transform = alembic.createOutputNode("xform", node_name="ScaleSmaller")
        transform.parm("scale").set(0.01)
        out = transform.createOutputNode("null", node_name="OUT")
        out.setDisplayFlag(True)
        out.setRenderFlag(True)

        hou.cd("/obj")
    hou.ui.displayMessage("Creating a successful", ["Ok"])


def create_alembic_archive(paths):
    pos_x = 0
    pos_y = 5
    for key, value in paths.items():
        # Create Geo node
        pwd = hou.pwd().createNode("alembicarchive", node_name=key)
        pwd.parm("fileName").set(value)
        pwd.setName(key)
        # kwargs['node'].hdaModule().BuildHierarchyRoot(kwargs['node'])
        pwd.parm('buildHierarchy').pressButton()
        pwd.setColor(hou.Color(0, 0, 0))
        pwd.setPosition([pos_x, pos_y])
        pos_x += 2.2

        parnul = pwd.createInputNode(0, "null", "Scale")
        parnul.parm("scale").set(0.01)
        parnul.setColor(hou.Color(0, 0, 0))
        _tree(pwd)


    hou.ui.displayMessage("Creating a successful", ["Ok"])


def _tree(node):
    for child in node.children():
        if child.type().name() == "cam":
            child.parm("resx").set(1920)
            child.parm("resy").set(1080)

        _tree(child)
