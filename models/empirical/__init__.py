"""
PyMuTT.models.statmech.basethermo
Vlachos group code for thermodynamic models.
Created on Tues Jul 10 12:40:00 2018
"""

import inspect
from matplotlib import pyplot as plt
import numpy as np
from PyMuTT import _pass_expected_arguments
from PyMuTT import constants as c
from pprint import pprint

class BaseThermo:
	"""
	The Thermodynamic Parent class. Holds properties of a specie, the 
	statistical-mechanical thermodynamic model.

	Attributes
		name - str
			Name of the specie
		phase - str
			Phase of the specie
				G - gas
				S - surface
		elements - dict
			Composition of the species. Keys of dictionary are elements, 
			values are stoichiometric values in a formula unit
			e.g. CH3OH can be represented as:
			{
				'C': 1,
				'H': 4,
				'O': 1,
			}
		thermo_model - PyMuTT.thermo_model class or custom class
			Class should have the following methods:
				get_CpoR
				get_HoRT
				get_SoR
				get_GoRT
		T_ref - float
			Temperature (in K) at which HoRT_dft was calculated. Only used for fitting empirical coefficients.
		HoRT_dft - float
			Dimensionless enthalpy calculated using DFT that corresponds to T_dft. Only used for fitting empirical
			coefficients.
		HoRT_ref - float
			Reference dimensionless enthalpy corresponding to T_ref. 
		references - PyMuTT.models.empirical.References object
			Contains references to calculate HoRT_ref. If not specified then HoRT_dft will be used without adjustment.
		notes - str
			Any additional details you would like to include such as computational set up.
	"""

	def __init__(self, name, phase=None, elements=None, thermo_model=None, T_ref=c.T0('K'), HoRT_dft=None, HoRT_ref=None, references=None, notes=None, **kwargs):
		self.name = name
		self.phase = phase
		self.elements = elements
		self.T_ref = T_ref
		self.references = references
		self.notes = notes

		#Assign self.thermo_model
		if inspect.isclass(thermo_model):
			#If you're passing a class. Note that the required arguments will be guessed.
			self.thermo_model = _pass_expected_arguments(thermo_model, **kwargs)
		else:
			#If it's an object that has already been initialized
			self.thermo_model = thermo_model
		
		#Calculate dimensionless DFT energy using thermo model
		if (HoRT_dft is None) and (self.thermo_model is not None):
			self.HoRT_dft = self.thermo_model.get_HoRT(Ts=self.T_ref)
		else:
			self.HoRT_dft = HoRT_dft

		#Assign self.HoRT_ref
		if HoRT_ref is None:
			if (references is None) or (self.HoRT_dft is None):
				self.HoRT_ref = self.HoRT_dft
			else:
				self.HoRT_ref = self.HoRT_dft + references.get_HoRT_offset(elements=elements, Ts=self.T_ref)
		else:
			self.HoRT_ref = HoRT_ref

	def plot_empirical(self, T_low = None, T_high = None, Cp_units = None, H_units = None, S_units = None, G_units = None):
		"""
		Plots the thermodynamic profiles between T_low and T_high using empirical relationship
		Parameters
			T_low - float
				Lower temperature in K. If not specified, T_low attribute used
			T_high - float
				Upper temperature in K. If not specified, T_high attribute used
			Cp_units - str
				Units to plot heat capacity. See PyMuTT.constants.R for accepted units. 
				If not specified, dimensionless units used.
			H_units - str
				Units to plot enthalpy. See PyMuTT.constants.R for accepted units but omit the '/K' (e.g. J/mol).
				If not specified, dimensionless units used.
			S_units - str
				Units to plot entropy. See PyMuTT.constants.R for accepted units. 
				If not specified, dimensionless units used.
			G_units - str
				Units to plot Gibbs free energy. See PyMuTT.constants.R for accepted units but omit the '/K' (e.g. J/mol).
				If not specified, dimensionless units used.
		"""
		if T_low is None:
			T_low = self.T_low
		if T_high  is None:
			T_high = self.T_high
		Ts = np.linspace(T_low, T_high)

		plt.figure()
		'''
		Heat Capacity
		'''
		plt.subplot(411)
		plt.title('Specie: {}'.format(self.name))
		plt.xlabel('Temperature (K)')
		Cp_plot = self.get_CpoR(Ts=Ts)
		if Cp_units is None:
			plt.ylabel('Cp/R')
		else:
			plt.ylabel('Cp ({})'.format(Cp_units))
			Cp_plot = Cp_plot * c.R(Cp_units)
		plt.plot(Ts, Cp_plot, 'r-')

		'''
		Enthalpy
		'''
		plt.subplot(412)
		plt.xlabel('Temperature (K)')
		H_plot = self.get_HoRT(Ts=Ts)
		if H_units is None:
			plt.ylabel('H/RT')
		else:
			plt.ylabel('H ({})'.format(H_units))
			H_plot = H_plot * c.R('{}/K'.format(H_units)) * Ts
		plt.plot(Ts, H_plot, 'g-')

		'''
		Entropy
		'''
		plt.subplot(413)
		plt.xlabel('Temperature (K)')
		S_plot = self.get_SoR(Ts=Ts)
		if S_units is None:
			plt.ylabel('S/R')
		else:
			plt.ylabel('S ({})'.format(S_units))
			S_plot = S_plot * c.R(S_units)
		plt.plot(Ts, S_plot, 'b-')

		'''
		Gibbs energy
		'''
		plt.subplot(414)
		plt.xlabel('Temperature (K)')
		G_plot = self.get_GoRT(Ts=Ts)
		if G_units is None:
			plt.ylabel('G/RT')
		else:
			plt.ylabel('G ({})'.format(G_units))
			G_plot = G_plot * c.R('{}/K'.format(G_units)) * Ts
		plt.plot(Ts, G_plot, 'k-')

	def plot_thermo_model(self, T_low = None, T_high = None, Cp_units = None, H_units = None, S_units = None, G_units = None):
		"""
		Plots the thermodynamic profiles between T_low and T_high using statistical mechanics thermodynamic model
		Parameters
			T_low - float
				Lower temperature in K. If not specified, T_low attribute used
			T_high - float
				Upper temperature in K. If not specified, T_high attribute used
			Cp_units - str
				Units to plot heat capacity. See PyMuTT.constants.R for accepted units. 
				If not specified, dimensionless units used.
			H_units - str
				Units to plot enthalpy. See PyMuTT.constants.R for accepted units but omit the '/K' (e.g. J/mol).
				If not specified, dimensionless units used.
			S_units - str
				Units to plot entropy. See PyMuTT.constants.R for accepted units. 
				If not specified, dimensionless units used.
			G_units - str
				Units to plot Gibbs free energy. See PyMuTT.constants.R for accepted units but omit the '/K' (e.g. J/mol).
				If not specified, dimensionless units used.
		"""
		if T_low is None:
			T_low = self.T_low
		if T_high  is None:
			T_high = self.T_high
		Ts = np.linspace(T_low, T_high)

		plt.figure()
		'''
		Heat Capacity
		'''
		plt.subplot(411)
		plt.title('Specie: {}'.format(self.name))
		plt.xlabel('Temperature (K)')
		Cp_plot = self.thermo_model.get_CpoR(Ts=Ts)
		if Cp_units is None:
			plt.ylabel('Cp/R')
		else:
			plt.ylabel('Cp ({})'.format(Cp_units))
			Cp_plot = Cp_plot * c.R(Cp_units)
		plt.plot(Ts, Cp_plot, 'r-')

		'''
		Enthalpy
		'''
		plt.subplot(412)
		plt.xlabel('Temperature (K)')

		H_plot = self.thermo_model.get_HoRT(Ts=Ts)
		if self.references is not None:
			H_plot += self.references.get_HoRT_offset(elements=self.elements, Ts=Ts)

		if H_units is None:
			plt.ylabel('H/RT')
		else:
			plt.ylabel('H ({})'.format(H_units))
			H_plot = H_plot * c.R('{}/K'.format(H_units)) * Ts
		plt.plot(Ts, H_plot, 'g-')

		'''
		Entropy
		'''
		plt.subplot(413)
		plt.xlabel('Temperature (K)')
		S_plot = self.thermo_model.get_SoR(Ts=Ts)
		if S_units is None:
			plt.ylabel('S/R')
		else:
			plt.ylabel('S ({})'.format(S_units))
			S_plot = S_plot * c.R(S_units)
		plt.plot(Ts, S_plot, 'b-')

		'''
		Gibbs energy
		'''
		plt.subplot(414)
		plt.xlabel('Temperature (K)')
		G_plot = self.thermo_model.get_GoRT(Ts=Ts)
		if self.references is not None:
			G_plot += self.references.get_HoRT_offset(elements=self.elements, Ts=Ts)

		if G_units is None:
			plt.ylabel('G/RT')
		else:
			plt.ylabel('G ({})'.format(G_units))
			G_plot = G_plot * c.R('{}/K'.format(G_units)) * Ts
		plt.plot(Ts, G_plot, 'k-')

	def plot_thermo_model_and_empirical(self, T_low = None, T_high = None, Cp_units = None, H_units = None, S_units = None, G_units = None):
		"""
		Plots the thermodynamic profiles between T_low and T_high
		Parameters
			T_low - float
				Lower temperature in K. If not specified, T_low attribute used
			T_high - float
				Upper temperature in K. If not specified, T_high attribute used
			Cp_units - str
				Units to plot heat capacity. See PyMuTT.constants.R for accepted units. 
				If not specified, dimensionless units used.
			H_units - str
				Units to plot enthalpy. See PyMuTT.constants.R for accepted units but omit the '/K' (e.g. J/mol).
				If not specified, dimensionless units used.
			S_units - str
				Units to plot entropy. See PyMuTT.constants.R for accepted units. 
				If not specified, dimensionless units used.
			G_units - str
				Units to plot Gibbs free energy. See PyMuTT.constants.R for accepted units but omit the '/K' (e.g. J/mol).
				If not specified, dimensionless units used.
		"""
		if T_low is None:
			T_low = self.T_low
		if T_high  is None:
			T_high = self.T_high
		Ts = np.linspace(T_low, T_high)

		plt.figure()
		'''
		Heat Capacity
		'''
		plt.subplot(411)
		plt.title('Specie: {}'.format(self.name))
		plt.xlabel('Temperature (K)')
		Ts, Cp_plot_thermo_model, Cp_plot_empirical = self.compare_CpoR(Ts=Ts)
		if Cp_units is None:
			plt.ylabel('Cp/R')
		else:
			plt.ylabel('Cp ({})'.format(Cp_units))
			Cp_plot_thermo_model = Cp_plot_thermo_model * c.R(Cp_units)
			Cp_plot_empirical = Cp_plot_empirical * c.R(Cp_units)

		plt.plot(Ts, Cp_plot_thermo_model, 'r-', label = 'Stat Mech Model')
		plt.plot(Ts, Cp_plot_empirical, 'b-', label = 'Empirical Model')
		plt.legend()
		
		'''
		Enthalpy
		'''
		plt.subplot(412)
		plt.xlabel('Temperature (K)')
		Ts, H_plot_thermo_model, H_plot_empirical = self.compare_HoRT(Ts=Ts)

		if H_units is None:
			plt.ylabel('H/RT')
		else:
			plt.ylabel('H ({})'.format(H_units))
			H_plot_thermo_model = H_plot_thermo_model * c.R('{}/K'.format(H_units)) * Ts
			H_plot_empirical = H_plot_empirical * c.R('{}/K'.format(H_units)) * Ts
		plt.plot(Ts, H_plot_thermo_model, 'r-')
		plt.plot(Ts, H_plot_empirical, 'b-')

		'''
		Entropy
		'''
		plt.subplot(413)
		plt.xlabel('Temperature (K)')
		Ts, S_plot_thermo_model, S_plot_empirical = self.compare_SoR(Ts=Ts)
		if S_units is None:
			plt.ylabel('S/R')
		else:
			plt.ylabel('S ({})'.format(S_units))
			S_plot_thermo_model = S_plot_thermo_model * c.R(S_units)
			S_plot_empirical = S_plot_empirical * c.R(S_units)
		plt.plot(Ts, S_plot_thermo_model, 'r-')
		plt.plot(Ts, S_plot_empirical, 'b-')

		'''
		Gibbs energy
		'''
		plt.subplot(414)
		plt.xlabel('Temperature (K)')
		Ts, G_plot_thermo_model, G_plot_empirical = self.compare_GoRT(Ts=Ts)
		if G_units is None:
			plt.ylabel('G/RT')
		else:
			plt.ylabel('G ({})'.format(G_units))
			G_plot_thermo_model = G_plot_thermo_model * c.R('{}/K'.format(G_units)) * Ts
			G_plot_empirical = G_plot_empirical * c.R('{}/K'.format(G_units)) * Ts
		plt.plot(Ts, G_plot_thermo_model, 'r-')
		plt.plot(Ts, G_plot_empirical, 'b-')

	def compare_CpoR(self, Ts = None):
		"""
		Returns the dimensionless heat capacity of the statistical model and the empirical model 
		Parameters
			Ts - (N,) ndarray, float, or None
				Temperatures (in K) to calculate CpoR. If None, generates a list of temperatures between self.T_low and self.T_high
		Returns
			tuple of length 3
			Element 0:
				Temperature in K
			Element 1: 
				CpoR_statmech Dimensionless heat capacity of statistical thermodynamic model
			Element 2: 
				CpoR_empirical Dimensionless heat capacity of empirical model
		"""

		if Ts is None:
			Ts = np.linspace(self.T_low, self.T_high)

		try:
			iter(Ts)
		except TypeError:
			CpoR_statmech = self.thermo_model.get_CpoR(Ts=Ts)
			CpoR_empirical = self.get_CpoR(Ts=Ts)
		else:
			CpoR_statmech = np.zeros_like(Ts)
			CpoR_empirical = np.zeros_like(Ts)
			for i, T in enumerate(Ts):
				CpoR_statmech[i] = self.thermo_model.get_CpoR(Ts=T)
				CpoR_empirical[i] = self.get_CpoR(Ts=T)
		return (Ts, CpoR_statmech, CpoR_empirical)

	def compare_HoRT(self, Ts = None):
		"""
		Returns the dimensionless enthalpy of the statistical model and the empirical model 
		Parameters
			Ts - (N,) ndarray, float, or None
				Temperatures (in K) to calculate HoRT. If None, generates a list of temperatures between self.T_low and self.T_high
		Returns
			tuple of length 3
			Element 0:
				Temperature in K
			Element 1: 
				HoRT_statmech Dimensionless enthalpy of statistical thermodynamic model
			Element 2: 
				HoRT_empirical Dimensionless enthalpy capacity of empirical model
		"""

		if Ts is None:
			Ts = np.linspace(self.T_low, self.T_high)

		if self.references is not None:
			H_offset = self.references.get_HoRT_offset(elements=self.elements, Ts=Ts)

		try:
			iter(Ts)
		except TypeError:
			HoRT_statmech = self.thermo_model.get_HoRT(Ts=Ts) + H_offset
			HoRT_empirical = self.get_HoRT(Ts=Ts)
		else:
			HoRT_statmech = np.zeros_like(Ts)
			HoRT_empirical = np.zeros_like(Ts)
			for i, T in enumerate(Ts):
				HoRT_statmech[i] = self.thermo_model.get_HoRT(Ts=T) + H_offset[i]
				HoRT_empirical[i] = self.get_HoRT(Ts=T)
		return (Ts, HoRT_statmech, HoRT_empirical)

	def compare_SoR(self, Ts = None):
		"""
		Returns the dimensionless entropy of the statistical model and the empirical model 
		Parameters
			Ts - (N,) ndarray, float, or None
				Temperatures (in K) to calculate SoR. If None, generates a list of temperatures between self.T_low and self.T_high
		Returns
			tuple of length 3
			Element 0:
				Temperature in K
			Element 1: 
				SoR_statmech Dimensionless entropy of statistical thermodynamic model
			Element 2: 
				SoR_empirical Dimensionless entropy of empirical model
		"""

		if Ts is None:
			Ts = np.linspace(self.T_low, self.T_high)

		try:
			iter(Ts)
		except TypeError:
			SoR_statmech = self.thermo_model.get_SoR(Ts=Ts)
			SoR_empirical = self.get_SoR(Ts=Ts)
		else:
			SoR_statmech = np.zeros_like(Ts)
			SoR_empirical = np.zeros_like(Ts)
			for i, T in enumerate(Ts):
				SoR_statmech[i] = self.thermo_model.get_SoR(Ts=T)
				SoR_empirical[i] = self.get_SoR(Ts=T)
		return (Ts, SoR_statmech, SoR_empirical)

	def compare_GoRT(self, Ts = None):
		"""
		Returns the dimensionless Gibbs energy of the statistical model and the empirical model 
		Parameters
			Ts - (N,) ndarray, float, or None
				Temperatures (in K) to calculate GoRT. If None, generates a list of temperatures between self.T_low and self.T_high
		Returns
			tuple of length 3
			Element 0:
				Temperature in K
			Element 1: 
				GoRT_statmech Dimensionless Gibbs energy of statistical thermodynamic model
			Element 2: 
				GoRT_empirical Dimensionless Gibbs energy of empirical model
		"""

		if Ts is None:
			Ts = np.linspace(self.T_low, self.T_high)

		if self.references is not None:
			G_offset = self.references.get_HoRT_offset(elements=self.elements, Ts=Ts)

		try:
			iter(Ts)
		except TypeError:
			GoRT_statmech = self.thermo_model.get_GoRT(Ts=Ts) + G_offset
			GoRT_empirical = self.get_GoRT(Ts=Ts)
		else:
			GoRT_statmech = np.zeros_like(Ts)
			GoRT_empirical = np.zeros_like(Ts)
			for i, T in enumerate(Ts):
				GoRT_statmech[i] = self.thermo_model.get_GoRT(Ts=T) + G_offset[i]
				GoRT_empirical[i] = self.get_GoRT(Ts=T)
		return (Ts, GoRT_statmech, GoRT_empirical)