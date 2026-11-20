# Toolkit sections and commands

## A. File browser / batch selection

    python -m neutrontoolkit browse data/reduced

Space marks files, A selects all visible, U clears selections, slash starts a filename filter, P saves plots using the currently selected view. Plot modes 1=I(Q), 2=Kratky, 3=Porod, 4=Guinier. Filtering only changes visibility; it never deletes a file.

## B. Data ingestion and QC

    python -m neutrontoolkit qc data/reduced/sample.dat

Reports points, Q limits, SHA-256, uncertainty availability and number of nonpositive intensity points. Accepts only 1D ASCII. Header lines before numbers are skipped; columns must be 2–4. Fails rather than guessing column order, sorting Q, or dropping invalid values.

## C. Plots and transformations

    python -m neutrontoolkit plot data/reduced/sample.dat --kind iq
    python -m neutrontoolkit plot data/reduced/sample.dat --kind kratky
    python -m neutrontoolkit plot data/reduced/sample.dat --kind porod
    python -m neutrontoolkit plot data/reduced/sample.dat --kind guinier

Results under outputs/plots. For log I(Q), nonpositive values are omitted from the displayed trace; QC reports their number. Guinier transformation is not a Guinier fit, and transforms should only be interpreted over physically appropriate Q ranges.

## D. Isotope contrast / SLD

    python -m neutrontoolkit sld C46H80O3 --density 0.96
    python -m neutrontoolkit mix-sld config/example_water_mixture.json

Formula and density supplied explicitly. periodictable returns coherent SLD in units of 10^-6 Å^-2. Mixture volume fractions are derived from mass fractions and component densities under ideal volume additivity. The command does not infer segregation, local layering contrast or an instrumental intensity enhancement.

Use config/cholesteric_template.json as a template with missing densities; fill each measured or clearly justified density before running.

## E. SasView-engine model previews

    python -m neutrontoolkit simulate config/example_sphere.json
    python -m neutrontoolkit simulate config/example_sphere.json --data data/reduced/sample.dat

Uses sasmodels directly. The sphere configuration is a software demonstration, **not** a proposed interpretation of a neat cholesteric mixture. No fit optimization, q-resolution correction, multi-contrast constraint or structural validation is performed. Fixed-parameter residuals are diagnostic only.

## F. Planned lab modules (not implemented)

- Instrument-aware USANS slit-smeared fitting with exact BL-1A resolution metadata
- EQ-SANS reduced 2D data and anisotropy under shear
- Model selection using residuals, hypothesis checks, and synthetic recovery
- Joint USANS/SANS fitting only when independent structural components require it
- Full H/D series with experimental density/volume, enrichment and contrast matching
- ORNL drtsans integration with provenance and institution-authorized data access
- Advanced filter commands by run number, wavelength, sample or metadata
