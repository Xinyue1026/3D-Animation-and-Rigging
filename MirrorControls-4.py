import maya.cmds as cmds

# Duplicate selected curve controls and all its children, then mirror them across world X = 0
def mirror_controls(*args):
    controls = cmds.ls(selection=True, long=True)
    
     # If both a parent and its child are selected, copy the parent only once
    controls = [node for node in controls
                if not any(node.startswith(parent + '|') for parent in controls)]

    for control in controls:
        # Replace "L_" with "R_"
        name = control.split('|')[-1].replace('L_', 'R_', 1)
        copy = cmds.duplicate(control, name=name, returnRootsOnly=True)[0]
        if cmds.listRelatives(copy, parent=True):
            copy = cmds.parent(copy, world=True)[0]

        # Find all children
        children = cmds.listRelatives(copy, allDescendents=True, fullPath=True) or []

        # Rename children
        children.sort(key=lambda child: child.count('|'), reverse=True)
        for child in children:
            child_name = child.split('|')[-1]
            if 'L_' in child_name:
                cmds.rename(child, child_name.replace('L_', 'R_', 1))

        # Reflect the root's world matrix across X = 0
        matrix = cmds.xform(copy, query=True, worldSpace=True, matrix=True)
        for index in [0, 4, 8, 12]:
            matrix[index] *= -1
        cmds.xform(copy, worldSpace=True, matrix=matrix)

if cmds.window('mirrorControlsWindow', exists=True):
    cmds.deleteUI('mirrorControlsWindow')

cmds.window('mirrorControlsWindow', title='Mirror Controls', widthHeight=(350, 130))
cmds.columnLayout(adjustableColumn=True, rowSpacing=12)
cmds.text(label='Select controls.\n'
                'Mirrors across world X = 0.')
cmds.button(label='Mirror Controls', height=35, command=mirror_controls)
cmds.showWindow('mirrorControlsWindow')
