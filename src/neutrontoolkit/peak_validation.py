"""Empirical reduced I(Q) peak validation; no raw-event reduction or physical model claim.

Shares the same scipy/numpy dependencies as the scientific package. Report input
SHA256, residuals and alternative model fits; do not commit experimental outputs.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json

import numpy as np
from scipy.optimize import curve_fit
from .files import load


def baseline(q, c0, c1, c2):
    return c0 + c1*q + c2*q*q


def lorentz(q, c0, c1, c2, amp, q0, xi):
    return baseline(q,c0,c1,c2) + amp/(1 + ((q-q0)*xi)**2)


def gaussian(q, c0, c1, c2, amp, q0, sigma):
    return baseline(q,c0,c1,c2) + amp*np.exp(-0.5*((q-q0)/sigma)**2)


def powerlaw(q, amplitude, alpha, background):
    return amplitude*q**(-alpha) + background


def fit(x, y, dy, func, seed, bounds=(-np.inf, np.inf)):
    p,cov = curve_fit(func,x,y,p0=seed,sigma=dy,absolute_sigma=True,
                      bounds=bounds,maxfev=30000)
    residual = (y-func(x,*p))/dy
    n,k = len(x),len(p)
    if n <= k+1: raise ValueError("Insufficient data for AICc")
    chi2 = float(np.dot(residual,residual))
    stats = {
        "n":n,"k":k,"chi2":chi2,"reduced_chi2":chi2/(n-k),
        "aicc":chi2+2*k+2*k*(k+1)/(n-k-1),
        "residual_lag1":float(np.corrcoef(residual[:-1],residual[1:])[0,1])
    }
    return p,cov,stats,residual


def analyze(path, q_lower=0.06, q_upper=0.60):
    original = load(path)
    if original.di is None:
        raise ValueError("Measured positive dI column required for weighted model validation")
    valid = (original.intensity>0)&(original.di<0.5*original.intensity)
    q = original.q[valid];I=original.intensity[valid];dI=original.di[valid]
    m = (q>=q_lower)&(q<=q_upper)
    x,y,s = q[m],I[m],dI[m]
    if len(x)<18: raise ValueError("At least 18 points required in peak fit window")
    seed=[float(np.median(y)),0,0,0.05*float(np.median(y)),0.20,10.0]
    pl,cl,sl,rl=fit(x,y,s,lorentz,seed)
    pg,cg,sg,rg=fit(
        x,y,s,gaussian,[*seed[:5],0.05],
        bounds=([-np.inf]*3+[0,0.12,0.005],[np.inf]*3+[np.inf,0.30,0.20])
    )
    pn,cn,sn,rn=fit(x,y,s,baseline,seed[:3])
    if not q_lower<pl[4]<q_upper or pl[3]<=0 or pl[5]<=0:
        raise ValueError("Legacy unconstrained peak fit returned unphysical parameters")
    background=baseline(pl[4],*pl[:3])
    if background<=0:raise ValueError("Nonpositive fitted peak background")
    d_nm=float(2*np.pi/pl[4]/10)
    windows=[]
    for lo,hi in [(0.06,0.40),(0.08,0.45),(0.08,0.60),(0.10,0.40),(0.12,0.35)]:
        use=(q>=lo)&(q<=hi)
        if np.count_nonzero(use)<20:continue
        try:
            pp,_,st,_=fit(q[use],I[use],dI[use],lorentz,pl)
            if pp[4]>0 and pp[5]>0:
                windows.append({"q_min":lo,"q_max":hi,
                                "d_nm":float(2*np.pi/pp[4]/10),
                                "width_length_nm":float(pp[5]/10),
                                "reduced_chi2":st["reduced_chi2"]})
        except (RuntimeError, ValueError) as exc:
            windows.append({"q_min":lo,"q_max":hi,"fit_error":str(exc)})
    low=[]
    for hi in [0.010,0.015,0.025,0.040]:
        use=q<hi
        if np.count_nonzero(use)<=8:continue
        try:
            pp,cov,st,_=fit(q[use],I[use],dI[use],powerlaw,[1e-8,3.5,1.8])
            low.append({"q_upper":hi,"alpha":float(pp[1]),
                        "formal_sigma_alpha":float(np.sqrt(cov[1,1])),
                        "reduced_chi2":st["reduced_chi2"]})
        except (RuntimeError,ValueError) as exc:
            low.append({"q_upper":hi,"fit_error":str(exc)})
    result={
        "file_sha256":sha256(Path(path).read_bytes()).hexdigest(),
        "original_points":len(original.q),"retained_points":int(np.count_nonzero(valid)),
        "excluded_q_A_inv":[float(v) for v in original.q[~valid]],
        "legacy_filter":"I>0 and dI<0.5*I",
        "q_fit_range_A_inv":[q_lower,q_upper],
        "q0_A_inv":float(pl[4]),"d_nm":d_nm,
        "width_length_nm":float(pl[5]/10),
        "peak_height_percent":float(100*pl[3]/background),
        "formal_sigma_d_nm":float(d_nm*np.sqrt(cl[4,4])/pl[4]),
        "gaussian_d_nm":float(2*np.pi/pg[4]/10),
        "models":{"no_peak_quadratic":sn,"lorentz":sl,"gaussian":sg},
        "delta_aicc_null_minus_lorentz":sn["aicc"]-sl["aicc"],
        "window_sensitivity":windows,"lowq_window_sensitivity":low,
        "q_resolution":"dQ is not applied; ORNL dQ meaning must be verified",
        "warning":"Empirical fit only. Width length is not a validated physical correlation length.",
    }
    traces={"q":x,"I":y,"dI":s,"lorentz":lorentz(x,*pl),
            "gaussian":gaussian(x,*pg),"quadratic":baseline(x,*pn),
            "lorentz_residual":rl,"gaussian_residual":rg}
    return result,traces


def write_report(paths, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    paths=list(paths)
    if not paths:raise ValueError("No reduced data file supplied")
    out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
    report={
        "purpose":"Empirical model validation, not structural model identification",
        "utc":datetime.now(timezone.utc).isoformat(),
        "warnings":[
          "No event-mode re-reduction was performed.",
          "Merged dI may not represent independent Gaussian residual errors.",
          "No detector resolution correction was applied; dQ convention unknown.",
          "AICc is only screening; systematic residuals and physical validity take precedence.",
          "No experimental files should be committed to a public repository."
        ],"samples":{}
    }
    fig,axs=plt.subplots(len(paths),2,figsize=(11,3.2*len(paths)),squeeze=False)
    for i,path in enumerate(paths):
        stat,t=analyze(path)
        name=Path(path).stem
        if name in report["samples"]:raise ValueError("Duplicate sample names")
        report["samples"][name]=stat
        left,right=axs[i]
        left.errorbar(t["q"],t["I"],yerr=t["dI"],fmt=".",markersize=3,
                      capsize=1,label="Data")
        for model in ("lorentz","gaussian","quadratic"):
            left.plot(t["q"],t[model],label=model)
        left.set(title=name,ylabel="I(Q) [cm-1]")
        left.legend(fontsize=8)
        for model in ("lorentz","gaussian"):
            right.plot(t["q"],t[model+"_residual"],".-",label=model)
        right.axhline(0,color="gray",ls="--",lw=0.7)
        right.set(ylabel="(data-model)/dI")
        right.legend(fontsize=8)
        np.savetxt(out/(name+"_residuals.csv"),
                   np.column_stack([t["q"],t["I"],t["dI"],t["lorentz"],
                                    t["gaussian"],t["lorentz_residual"]]),
                   delimiter=",",comments="",
                   header="q_Ainv,I_cm1,dI_cm1,I_lorentz,I_gaussian,normalized_residual")
    axs[-1,0].set_xlabel("Q [Angstrom-1]")
    axs[-1,1].set_xlabel("Q [Angstrom-1]")
    fig.tight_layout()
    fig.savefig(out/"empirical_model_residuals.png",dpi=170)
    plt.close(fig)
    target=out/"audit.json"
    target.write_text(json.dumps(report,indent=2),encoding="utf-8")
    return target
