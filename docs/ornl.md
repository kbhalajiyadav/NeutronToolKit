# ORNL software: what we can and cannot identify

ORNL supports Mantid for neutron data reduction and visualization and drtsans for reduction of EQ-SANS, GP-SANS and Bio-SANS. SasView analyzes reduced scattering curves with analytical models. The ORNL Neutron Science Remote Analysis Service provides workstations for authorized users.

References:
- https://neutrons-user-facilities.ornl.gov/data-management/
- https://analysis.neutrons.ornl.gov/
- https://github.com/neutrons/drtsans
- https://www.sasview.org/docs/
- https://github.com/neutrons/usansred

A specifically relevant open-source project is EQSANS-CLI (https://github.com/cw-do/eqsanscli), an interactive terminal application for EQ-SANS reduction. Its documented commands include:

    /load ipts 35884
    /show catalog
    /matchruns
    /reduce all
    /list iq
    /plot *_Iq.dat --save plot.png
    /stitch smart
    /session save myexperiment

The number above is an example from upstream documentation. Its documented shortcuts do not confirm the precise P/U keyboard behavior remembered from a visit. We should not claim that this is certainly the software seen without a screenshot or program name.

NeutronToolKit borrows only the **interface pattern**, not EQSANS-CLI's instrument reduction capability. It does not authenticate to ONCat, load raw detector events, reduce absolute scattering intensity, correct masking/transmission, or impersonate ORNL processing.

Correct scientific separation:
1. Raw experimental events -> ORNL drtsans / Mantid or qualified reduction software.
2. Reduced I(Q), dI, dQ and provenance -> NeutronToolKit quality checks and figures.
3. Model evaluation and constrained fits -> sasmodels / SasView with independently justified geometry and real instrument resolution.
4. Experimental reporting -> data version, code commit, config, uncertainties, correction history and hypothesis tests.

Do not copy personal ORNL account passwords, ONCat tokens, beamtime data or unpublished raw run data into public GitHub. Use your assigned ORNL rights and approved lab storage.
