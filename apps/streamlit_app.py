"""Browser UI adapter: scientific calculations are delegated to neutrontoolkit."""
from pathlib import Path
import json
import tempfile

import pandas as pd
import streamlit as st

from neutrontoolkit.files import load, quality
from neutrontoolkit.plots import plot_files
from neutrontoolkit.model_rules import from_file
from neutrontoolkit.deuteration import sweep

ROOT = Path(__file__).resolve().parents[1]
st.set_page_config(page_title="NeutronToolKit", layout="wide")
st.title("NeutronToolKit")
st.caption("Guided neutron-scattering analysis of reduced 1D curves and isotopic scenarios")
st.warning(
    "Demo and exploratory science only. Upload files to third-party cloud platforms "
    "only when authorized. The isotope metric is a conditional SLD proxy, "
    "not a validated SANS peak prediction or purchasing-cost model."
)
data_tab, isotope_tab, model_tab, about_tab = st.tabs(
    ["Data browser and plots", "H/D isotope design", "Model guidance", "Limitations"]
)
with data_tab:
    source = st.radio(
        "Data source", ["Bundled synthetic example", "Upload approved reduced ASCII files"],
        horizontal=True
    )
    with tempfile.TemporaryDirectory(prefix="ntk-web-") as temp_dir:
        temp = Path(temp_dir)
        files = {}
        if source == "Bundled synthetic example":
            sample = ROOT/"data/examples/synthetic_iq.dat"
            files[sample.name] = sample
        else:
            uploaded = st.file_uploader(
                "Reduced 1D data: Q, I(Q), optional dI and dQ",
                type=["dat","txt","csv","iq"], accept_multiple_files=True
            )
            if len(uploaded) > 15 or sum(f.size for f in uploaded) > 20_000_000:
                st.error("This demo accepts at most 15 files and 20 MB total.")
            else:
                for i, item in enumerate(uploaded):
                    name = f"{i+1:02d}_{Path(item.name).name}"
                    path = temp/name
                    path.write_bytes(item.getvalue())
                    files[name] = path
        if files:
            term = st.text_input("Filter file names")
            visible = [name for name in files if term.casefold() in name.casefold()]
            selected = st.multiselect("Files to overlay", visible, default=visible[:1])
            view = st.selectbox("Plot", ["iq","kratky","porod","guinier"])
            st.caption("Kratky, Porod and Guinier are transforms, not automatic structural fits.")
            if selected:
                try:
                    paths = [files[name] for name in selected]
                    for name in selected:
                        with st.expander("QC: "+name):
                            st.json(quality(load(files[name])))
                    figure = plot_files(paths, kind=view, outdir=temp/"plots")
                    st.image(figure.read_bytes(), caption=view+" overlay")
                    st.download_button(
                        "Download plot PNG", figure.read_bytes(),
                        file_name="neutrontoolkit-"+view+".png", mime="image/png"
                    )
                    st.download_button(
                        "Download provenance JSON", figure.with_suffix(".json").read_bytes(),
                        file_name="neutrontoolkit-"+view+".json", mime="application/json"
                    )
                except (OSError, ValueError) as error:
                    st.error(str(error))
        else:
            st.info("Use the bundled synthetic example or upload approved reduced ASCII data.")
with isotope_tab:
    st.subheader("H/D site-labeling design")
    st.caption("Assumed H-state densities and partial-label fractions; no validated domain model.")
    use_example = st.checkbox("Use synthetic/example configuration", value=True)
    custom = None if use_example else st.file_uploader(
        "Supply your own JSON configuration", type=["json"], key="isotope"
    )
    if use_example or custom is not None:
        try:
            cfg = (json.loads((ROOT/"config/deuteration_design_example.json").read_text())
                   if use_example else json.loads(custom.getvalue().decode("utf-8")))
            result = sweep(cfg)
            names = [row["composition"] for row in result["summaries"]]
            selected_name = st.selectbox("Formulation", names)
            rows = [r for r in result["all_scenarios"] if r["composition"] == selected_name]
            table = pd.DataFrame([{
                "Label pattern": r["labeling"],
                "D atom mol per reference batch": r["D_atom_mol_per_reference_batch"],
                "Conditional SLD variance": r["component_variance_proxy"],
                "Cost USD if quoted": r["incremental_label_cost_usd_per_reference_batch"],
            } for r in rows])
            st.scatter_chart(
                table, x="D atom mol per reference batch",
                y="Conditional SLD variance"
            )
            st.dataframe(
                table.sort_values("Conditional SLD variance", ascending=False).head(60),
                use_container_width=True, hide_index=True
            )
            st.download_button("Download complete scenario CSV", table.to_csv(index=False),
                               file_name="neutrontoolkit-isotopes.csv", mime="text/csv")
            with st.expander("Scientific assumptions and caveats"):
                for note in result["limitations"]:
                    st.write("- "+note)
        except (OSError, ValueError, TypeError, KeyError) as error:
            st.error("Configuration invalid: "+str(error))
with model_tab:
    st.subheader("Evidence-gated model hypotheses")
    st.caption("Candidate suggestions are not identification of physical morphology.")
    try:
        st.json(from_file(ROOT/"config/model_guidance_cholesteric.json"))
    except (OSError, ValueError) as error:
        st.error(str(error))
with about_tab:
    st.write(
        "This interface reuses NeutronToolKit's existing file IO, plotting, "
        "PeriodicTable-backed deuteration screening, and model guidance. "
        "Instrument reduction, 2D fitting, and verified experimental model ranking "
        "are not included in this browser prototype."
    )
    st.markdown(
        "[Source and documentation](https://github.com/kbhalajiyadav/NeutronToolKit)"
    )
