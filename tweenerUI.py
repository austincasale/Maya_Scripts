from maya import cmds

def tween(percentage, obj=None, attrs=None, selection=True):
	if not obj and not selection:
		raise ValueError("No object given to tween")

	if not obj:
		obj = cmds.ls(selection=True)[0]

	if not attrs:
		attrs = cmds.listAttr(obj, keyable=True)

	currentTime = cmds.currentTime(query=True)
	
	for attr in attrs:
	
		attrFull ='%s.%s' % (obj, attr)
		keyframes = cmds.keyframe(attrFull, query=True)
		
		if not keyframes:
			continue
		
		previousKeyframes = []
		
		for frame in keyframes:
			if frame < currentTime:
				previousKeyframes.append(frame)
				
		laterKeyframes = [frame for frame in keyframes if frame > currentTime]
		
		if not previousKeyframes and not keyframes:
			continue
		
		if previousKeyframes:
			previousFrame = max(previousKeyframes)
		else:
			previousFrame = None
		
		nextFrame = min(laterKeyframes) if laterKeyframes else None
		
		if not previousFrame or not nextFrame:
			continue
		
		previousValue = cmds.getAttr(attrFull, time=previousFrame)
		nextValue = cmds.getAttr(attrFull, time=nextFrame)
		
		difference = nextValue - previousValue
		weightedDifference = (difference * percentage) / 100.0
		currentValue = previousValue + weightedDifference
		
		cmds.setKeyframe(attrFull, time=currentTime, value=currentValue)
		
