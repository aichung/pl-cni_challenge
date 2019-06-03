#!/usr/bin/env python

import numpy as np

def rotate_matrix(instrRot, instrbvec, ostr):

	rots = np.loadtxt(instrRot)  # rots.shape = (nDirs, 16)
	bvecs = np.loadtxt(instrbvec)

	nDir = bvecs.shape[0]
	rotBvec = np.zeros((bvecs.shape))

	# eddy x-, y-, z- rotations (in radians) are store in columns 4-6 of this fsl edd output textfile
	# Cols 1:3 are the translations in x,y,z, 4:6 are rotations, and 7: are warp params
	rots = rots[:, 3:6]  # nDirs x [x,y,z]


	# An assumption is made here that the first volume is b0- and is that all other volumes were registered to by eddy
	for i in range(nDir):

		origVec = bvecs[i, :]  # Get original gradient
		rot = rots[i, :]  # Get rotations
		rotationMats = np.zeros((3, 3, 3))

		# For x-rotation
		rotationMats[0, 0, 0] = np.cos(rot[0])
		rotationMats[0, 1, 0] = np.sin(rot[0])
		rotationMats[1, 0, 0] = -np.sin(rot[0])
		rotationMats[1, 1, 0] = np.cos(rot[0])
		rotationMats[2, 2, 0] = 1

		# For y-rotation
		rotationMats[0, 0, 1] = np.cos(rot[1])
		rotationMats[0, 1, 1] = np.sin(rot[1])
		rotationMats[1, 0, 1] = -np.sin(rot[1])
		rotationMats[1, 1, 1] = np.cos(rot[1])
		rotationMats[2, 2, 1] = 1

		# For z-rotation
		rotationMats[0, 0, 2] = np.cos(rot[2])
		rotationMats[0, 1, 2] = np.sin(rot[2])
		rotationMats[1, 0, 2] = -np.sin(rot[2])
		rotationMats[1, 1, 2] = np.cos(rot[2])
		rotationMats[2, 2, 2] = 1

		# x' = (R_x R_y R_z)^-1 x
		temp = np.dot(np.linalg.inv(rotationMats[:, :, 0] * rotationMats[:, :, 1] * rotationMats[:, :, 2]), origVec)
		rotBvec[i,:] = temp

	# Output and save
	np.savetxt(ostr, rotBvec, fmt='%0.7f', delimiter='\t')

