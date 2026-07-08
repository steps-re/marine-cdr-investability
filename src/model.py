"""
Core air-sea CO2 equilibration model for marine CDR viability scoping.

Central quantity: the KINETIC efficiency f_kin -- the fraction of the potential
CO2 uptake that is actually realized across the air-sea interface within a policy
horizon. This is pathway-agnostic: it is a property of the water column (wind,
mixed-layer depth, carbonate chemistry, surface residence time), not of the
intervention. It applies to every "atmosphere-coupled" marine CDR pathway
(OAE, direct ocean capture, marine-grown biomass sinking, iron fertilization).

It does NOT apply to "storage-only" pathways (terrestrial biomass sunk into the
ocean), where the carbon was already removed from the atmosphere on land and the
ocean is only a vault. For those, f_kin = 1 by construction (see is_air_sea_gated).

Physics note (corrected vs the common heuristic):
    tau_eq = (h / k) * (R_ion / R_f)
where R_ion = DIC/[CO2(aq)] is the ionization fraction (~100-200) and R_f is the
Revelle/buffer factor (~8-15). The net CO2 slowdown vs an inert gas is R_ion/R_f
(~10-20x). The Revelle factor is in the DENOMINATOR: a higher R_f drives the flux
harder and SPEEDS equilibration. (Jones et al. 2014, GBC, doi:10.1002/2014GB004813)
"""

import numpy as np
import PyCO2SYS as pyco2


# ----------------------------------------------------------------------------
# Gas transfer velocity (Wanninkhof 2014)
# ----------------------------------------------------------------------------
def schmidt_co2_seawater(sst_c):
    """Schmidt number for CO2 in seawater, salinity ~35 (Wanninkhof 2014, Table 1)."""
    t = sst_c
    return 2116.8 - 136.25 * t + 4.7353 * t**2 - 0.092307 * t**3 + 0.0007555 * t**4


def k_wanninkhof2014(u10_sq, sst_c):
    """
    Gas transfer (piston) velocity, m/day.
    u10_sq : second moment of 10 m wind speed <U^2>, (m/s)^2
    Returns k in m/day.
    k[cm/hr] = 0.251 * <U^2> * (Sc/660)^-0.5   (Wanninkhof 2014, L&O Methods)
    """
    sc = schmidt_co2_seawater(sst_c)
    k_cm_hr = 0.251 * u10_sq * (sc / 660.0) ** (-0.5)
    return k_cm_hr * 0.24  # cm/hr -> m/day


# ----------------------------------------------------------------------------
# Carbonate chemistry (PyCO2SYS)
# ----------------------------------------------------------------------------
def carbonate_properties(dic, talk, sst_c, sal=35.0, pco2_atm=420.0):
    """
    Returns (revelle_factor, ionization_fraction, eta_max).

    revelle_factor R_f          : dimensionless
    ionization_fraction R_ion   : DIC / [CO2(aq)]
    eta_max                     : equilibrium mol CO2 uptake per mol alkalinity
                                  added, = dDIC/dTAlk at fixed atmospheric pCO2.
                                  (the carbonate-chemistry ceiling; ~0.8 warm,
                                  ~0.9 cold)
    dic, talk in umol/kg.
    """
    # State at given DIC/TAlk for Revelle + aqueous CO2
    res = pyco2.sys(par1=talk, par2=dic, par1_type=1, par2_type=2,
                    salinity=sal, temperature=sst_c)
    r_f = float(res["revelle_factor"])
    co2aq = float(res["CO2"])          # umol/kg aqueous CO2
    r_ion = dic / co2aq

    # eta_max: equilibrium ratio dDIC/dTAlk at fixed atmospheric pCO2
    d = 1.0  # umol/kg alkalinity perturbation
    s0 = pyco2.sys(par1=talk,     par2=pco2_atm, par1_type=1, par2_type=4,
                   salinity=sal, temperature=sst_c)
    s1 = pyco2.sys(par1=talk + d, par2=pco2_atm, par1_type=1, par2_type=4,
                   salinity=sal, temperature=sst_c)
    eta_max = (float(s1["dic"]) - float(s0["dic"])) / d
    return r_f, r_ion, eta_max


# ----------------------------------------------------------------------------
# Equilibration timescale and realized kinetic efficiency
# ----------------------------------------------------------------------------
def tau_eq_days(mld_m, k_m_day, r_ion, r_f):
    """CO2 e-folding equilibration timescale, days."""
    return (mld_m / k_m_day) * (r_ion / r_f)


def realized_kinetic_efficiency(tau_eq_yr, tau_res_yr, horizon_yr):
    """
    Expected fraction of POTENTIAL uptake realized via air-sea flux within a
    policy horizon, given competition between equilibration and subduction.

    Model: a surface parcel relaxes toward equilibrium as (1 - exp(-t/tau_eq)).
    It is removed from the surface (subducted/advected) at exponential rate
    1/tau_res. Realized fraction at horizon H, averaging over subduction time:

        f_kin(H) = 1 - [ tau_res/(tau_res+tau_eq) * exp(-H*(1/tau_eq + 1/tau_res))
                         + tau_eq/(tau_res+tau_eq) ]              ... derivation:

    E over t_sub~Exp(1/tau_res) of (1 - exp(-min(H, t_sub)/tau_eq)).
    Closed form below. This is the SURFACE-realized fraction; it ignores the
    slow re-emergence of subducted disequilibrium (Zhou et al. 2024), so it is a
    conservative lower bound at long horizons -- appropriate for a viability test.
    """
    te = np.asarray(tau_eq_yr, dtype=float)
    tr = np.asarray(tau_res_yr, dtype=float)
    H = float(horizon_yr)
    a = 1.0 / te
    b = 1.0 / tr
    # E[1 - exp(-min(H,tsub)/te)]
    #  = 1 - [ P(tsub>=H)*exp(-H/te) + E[exp(-tsub/te); tsub<H] ]
    # P(tsub>=H) = exp(-bH)
    # E[exp(-tsub/te)*1{tsub<H}] = b/(a+b) * (1 - exp(-(a+b)H))
    term_ge = np.exp(-b * H) * np.exp(-a * H)
    term_lt = (b / (a + b)) * (1.0 - np.exp(-(a + b) * H))
    return 1.0 - (term_ge + term_lt)


def is_air_sea_gated(pathway):
    """
    True if the pathway creates a marine carbon deficit the atmosphere must
    back-fill (air-sea gated). False for storage-only (terrestrial biomass sunk
    into the ocean), where f_kin = 1 by construction.
    """
    storage_only = {"terrestrial_biomass_sinking"}
    return pathway not in storage_only
