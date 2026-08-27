#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wraps N_parameters.xlsx: loads the global parameter, waste-fraction and
trade-parameter tables, and gives the calculations/*.py modules a single
lookup interface (.get(), .waste_N_frac(), .get_table()) that the Monte Carlo
engine can transparently override with perturbed values before each
simulation round (see override_global_params).
"""
import pandas as pd


class NParameters:
    def __init__(self, filename="N_parameters.xlsx"):
        # Stored for later use by get_table/get_trade_params/get_trade_mapping.
        self.filename = filename

        self.global_params = {}
        df = pd.read_excel(filename, sheet_name='global_parameters')
        for _, row in df.iterrows():
            param_id = row['parameter_id']
            value = row['value']
            self.global_params[param_id] = value

        self.waste_fractions = {}
        df = pd.read_excel(filename, sheet_name='waste_fractions')
        for _, row in df.iterrows():
            category = row['waste_category']
            n_frac = row['N_frac']
            self.waste_fractions[category] = n_frac

    def get(self, param_id):
        """Look up a global parameter. Raises KeyError if it doesn't exist."""
        if hasattr(self, param_id):
            return getattr(self, param_id)
        if param_id in self.global_params:
            return self.global_params[param_id]
        raise KeyError(f"[STOPP] Global parameter '{param_id}' mangler helt i systemet!")

    def waste_N_frac(self, category):
        """Look up a waste-category N fraction. Raises KeyError if it doesn't exist."""
        if hasattr(self, category):
            return getattr(self, category)
        if category in self.waste_fractions:
            return self.waste_fractions[category]
        raise KeyError(f"[STOPP] Avfallsfraksjon '{category}' mangler helt i waste_fractions!")

    def get_table(self, sheet_name):
        """
        Return a pandas DataFrame for the given sheet in N_parameters.xlsx.
        Assumes the first row is the header.
        """
        return pd.read_excel(self.filename, sheet_name=sheet_name)

    def get_trade_params(self):
        df = pd.read_excel(self.filename, sheet_name='trade_parameters')
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df['lower_bound'] = pd.to_numeric(df['lower_bound'], errors='coerce')
        df['upper_bound'] = pd.to_numeric(df['upper_bound'], errors='coerce')
        df = df.set_index('param_id')
        return df

    def get_trade_mapping(self):
        """
        Mapping from SSB trade codes (Varenr) to N-content parameters.
        Sheet: 'trade_mapping'
        Columns (at least): type, konv, Varenr, År fra, År til, Varebetegnelse
        'konv' holds the param_id used in trade_N_parameters.
        """
        df = self.get_table('trade_mapping')
        return df

    def override_global_params(self, custom_dict):
        """
        Lets the Monte Carlo engine push in simulated values before the
        calculations run. Handles both existing global parameters and new,
        flat MC keys (e.g. prod_ and weight_).
        """
        for param_id, new_value in custom_dict.items():
            if param_id in self.global_params:
                # Existing global parameter: update it in the dict.
                self.global_params[param_id] = new_value
            else:
                # New flat parameter (e.g. prod_ or weight_): set it directly
                # on the object so .get() finds it.
                setattr(self, param_id, new_value)
