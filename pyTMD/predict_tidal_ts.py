#!/usr/bin/env python
u"""
predict_tidal_ts.py (08/2018)
Predict tidal time series at a location using harmonic constants

CALLING SEQUENCE:
	ht = predict_tidal_ts(time,hc,con)

INPUTS:
	time: days relative to Jan 1, 1992 (48622mjd)
	hc: harmonic constant vector (complex)
	constituents: tidal constituent IDs

OUTPUT:
	ht: time series reconstructed using the nodal corrections

OPTIONS:
	DELTAT: time correction for converting to Ephemeris Time (days)
	CORRECTIONS: use nodal corrections from OTIS/ATLAS or GOT models

PYTHON DEPENDENCIES:
	numpy: Scientific Computing Tools For Python
		http://www.numpy.org
		http://www.scipy.org/NumPy_for_Matlab_Users

PROGRAM DEPENDENCIES:
	load_constituent.py: loads parameters for a given tidal constituent
	load_nodal_corrections.py: loads nodal corrections for tidal constituents

UPDATE HISTORY:
	Updated 08/2018: added correction option ATLAS for localized OTIS solutions
	Updated 07/2018: added option to use GSFC GOT nodal corrections
	Updated 09/2017: Rewritten in Python
"""
import numpy as np
from pyTMD.load_constituent import load_constituent
from pyTMD.load_nodal_corrections import load_nodal_corrections

def predict_tidal_ts(time,hc,constituents,DELTAT=0.0,CORRECTIONS='OTIS'):
	nt = len(time)
	#-- load the nodal corrections
	pu,pf,G = load_nodal_corrections(time + 48622.0, constituents,
		DELTAT=DELTAT, CORRECTIONS=CORRECTIONS)
	#-- allocate for output time series
	ht = np.zeros((nt))
	#-- for each constituent
	for k,c in enumerate(constituents):
		if CORRECTIONS in ('OTIS','ATLAS'):
			#-- load parameters for each constituent
			amp,ph,omega,alpha,species = load_constituent(c)
			#-- add component for constituent to output tidal time series
			th = omega*time*86400.0 + ph + pu[:,k]
		elif (CORRECTIONS == 'GOT'):
			th = G[:,k]*np.pi/180.0 + pu[:,k]
		#-- sum over all tides at location
		ht += pf[:,k]*hc.real[0,k]*np.cos(th) - pf[:,k]*hc.imag[0,k]*np.sin(th)
	#-- return the tidal time series
	return ht
