# how to augment:

# scale: [Bad, not useful, potentially usefull, usefull, important, mandatory] 

# augment complete image
	# mirror 			(Bad)
		# hor/ver axis
	# crop				(mandatory, make sure to crop to a of 32 and that the table is in there)
	# rotate 	 		(Bad)
	# shear	 	 		(not usefull)
	# brightness 		( usefull )
	# exposure  	 	(potentially usefull)
	# blur		 		(potentially usefull)
	# noise(gaussioan)	(potentially usefull)

# augment bounding box (card)
	# overlap			(mandatory)
	# mirror			( not usefull)
		# hor/ver axis
	# rotations			( important)
	# scale				( potentially usefull)
	# crop				( not usefull)
	# shear 			( important )
	# warp 				( important )
	# Brightness 		( not usefull )
	# exposure			( not usefull)
	# blur				( not usefull )
	# noise				( )