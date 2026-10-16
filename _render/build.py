"""Render the GitHub profile README sections as images in the portfolio style.

GitHub profile READMEs accept Markdown only (no CSS or JavaScript), so each
section of the portfolio design is drawn here as HTML and captured with headless
Chrome. Edit the content below and run:

    python _render/build.py

Output PNGs go to assets/. Requires Google Chrome; fonts and icons load from
Google Fonts and cdnjs, so the render needs an internet connection.
"""
import shutil
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
IMG = (HERE / "img").as_uri()
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SCALE = 2
CARD_H = 500
LINK_LABEL = {"bridge-tf": "View protocol", "cell-seeding": "Open tool"}
COVER_POSITION = {"solubility": "center 54%"}

HEAD = f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600&family=Unbounded:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css">
<style>
:root {{
  --p: hsl(258, 62%, 66%); --p-alt: hsl(258, 80%, 58%); --p-light: hsl(258, 70%, 78%);
  --title: hsl(240, 8%, 95%); --text: hsl(240, 8%, 72%); --muted: hsl(240, 8%, 52%);
  --bg: hsl(240, 60%, 3%); --card: hsl(240, 10%, 7%); --card2: hsl(240, 10%, 10%); --line: hsl(240, 10%, 16%);
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ background: transparent; }}
body {{ font-family: Montserrat, sans-serif; color: var(--text); -webkit-font-smoothing: antialiased; }}
.frame {{ position: relative; overflow: hidden; background: var(--bg); border-radius: 22px; width: 100%; height: 100%; }}
h1, h2, h3 {{ font-family: Unbounded, sans-serif; color: var(--title); font-weight: 600; line-height: 1.15; }}
.title {{ text-align: center; font-size: 40px; }}
.title span {{ color: var(--p); }}
.glow {{ position: absolute; border-radius: 50%; pointer-events: none; }}
.chip {{ display: inline-block; font-size: 15px; font-weight: 500; color: var(--title); padding: 6px 14px;
        border-radius: 30px; border: 1px solid var(--line); background: var(--card); margin: 0 6px 8px 0; }}
.card {{ background: var(--card); border: 1px solid var(--line); border-radius: 18px; }}
.accent {{ color: var(--p); }}
</style></head><body>"""


def page(body, w, h):
    return f'{HEAD}<div class="frame" style="width:{w}px;height:{h}px">{body}</div></body></html>'


def hero():
    return page(f"""
<div class="glow" style="left:-160px;top:-200px;width:460px;height:460px;background:radial-gradient(circle,hsla(258,80%,58%,.45),transparent 65%)"></div>
<div style="position:absolute;top:30px;left:80px;right:80px;display:flex;justify-content:space-between;font-weight:600;color:var(--title);font-size:17px">
  <span style="font-family:Unbounded">Thaís</span>
  <span style="display:flex;gap:48px"><span>About</span><span>Projects</span><span>Experience</span><span>Contact</span></span>
</div>
<div class="glow" style="left:470px;top:150px;width:340px;height:440px;filter:blur(30px);background:radial-gradient(ellipse,hsl(258,80%,58%) 0%,hsla(258,80%,50%,.45) 40%,transparent 72%)"></div>
<img src="{IMG}/home-portrait.webp" style="position:absolute;left:430px;top:96px;width:420px;-webkit-mask-image:linear-gradient(#000 72%,transparent)">
<div style="position:absolute;left:80px;top:200px">
  <div class="accent" style="font-family:Unbounded;font-size:24px">Hello, I'm</div>
  <h1 style="font-size:66px;margin-top:6px">Thaís<br>Dolzany</h1>
</div>
<div style="position:absolute;right:80px;top:215px">
  <div class="accent" style="font-family:Unbounded;font-size:24px">Translational</div>
  <h2 style="font-size:40px;margin-top:6px"><span style="background:linear-gradient(90deg,var(--p-light),var(--p-alt));-webkit-background-clip:text;color:transparent">Oncology</span><br>&amp; Bioinformatics</h2>
  <div style="margin-top:22px;color:var(--muted);font-weight:600;letter-spacing:.1em;font-size:14px;line-height:1.8">PHARMACIST · PHD UNIVERSITÄT ZU KÖLN<br>SÃO PAULO, BRAZIL</div>
</div>
<div style="position:absolute;left:84px;bottom:56px;display:flex;flex-direction:column;gap:22px;font-size:26px;color:var(--title)">
  <i class="ri-github-line"></i><i class="ri-linkedin-box-line"></i><i class="ri-graduation-cap-line"></i>
</div>
""", 1280, 600)


def about():
    stats = "".join(f'<div class="card" style="padding:16px 10px;text-align:center"><div style="font-family:Unbounded;color:var(--p);font-size:26px;font-weight:600">{a}</div><div style="font-size:14px;color:var(--muted);margin-top:2px">{b}</div></div>'
                    for a, b in [("10+", "years in research"), ("5", "publications"), ("PhD", "Universität zu Köln")])
    chips = "".join(f'<span class="chip">{t}</span>' for t in
                    ["R", "Python", "Seurat", "Scanpy", "pySCENIC", "DESeq2", "RDKit", "XGBoost", "scikit-learn", "GEO · TCGA · cBioPortal"])
    return page(f"""
<h2 class="title" style="padding-top:48px">About <span>me</span></h2>
<div style="position:absolute;left:110px;top:150px;width:330px;height:410px;border-radius:170px 170px 18px 18px;overflow:hidden;border:1px solid var(--line);box-shadow:0 0 0 8px var(--card),0 0 70px hsla(258,80%,58%,.35)">
  <img src="{IMG}/about-portrait.webp" style="width:100%;height:100%;object-fit:cover">
  <div style="position:absolute;inset:0;background:linear-gradient(to top,hsla(258,70%,20%,.45),transparent 45%)"></div>
</div>
<div style="position:absolute;left:530px;right:90px;top:150px">
  <h3 style="font-size:26px;margin-bottom:14px">From the bench to the network.</h3>
  <p style="font-size:17px;line-height:1.6">Pharmacist with a PhD in Biochemistry from the University of Cologne, where I studied
  extracellular vesicles and Lyn kinase signalling in chronic lymphocytic leukaemia. Today I work on
  <b style="color:var(--title)">single-cell and bulk transcriptomics</b>, <b style="color:var(--title)">target prioritisation</b>
  and <b style="color:var(--title)">drug repurposing</b> in cancer, built on public data and reproducible pipelines.</p>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:24px 0 20px">{stats}</div>
  <div>{chips}</div>
</div>""", 1280, 640)


def section_title(first, accent, sub=None):
    sub_html = f'<p style="text-align:center;margin-top:12px;font-size:17px">{sub}</p>' if sub else ""
    h = 170 if sub else 130
    return page(f'<h2 class="title" style="padding-top:42px">{first} <span>{accent}</span></h2>{sub_html}', 1280, h)


ART_NETWORK = """<svg viewBox="0 0 320 180" style="width:78%;color:var(--p-light)"><g fill="none" stroke="currentColor" stroke-width="1.3" opacity=".75">
<path d="M40 140 L110 70 L190 110 L270 40"/><path d="M110 70 L150 30 L190 110"/><path d="M40 140 L190 110"/><path d="M150 30 L270 40"/><path d="M190 110 L250 150"/></g>
<g fill="currentColor"><circle cx="40" cy="140" r="6"/><circle cx="110" cy="70" r="9"/><circle cx="190" cy="110" r="11"/><circle cx="270" cy="40" r="7"/><circle cx="150" cy="30" r="5"/><circle cx="250" cy="150" r="6"/></g></svg>"""


def glyph(icon, label):
    return (f'<div style="display:grid;justify-items:center;gap:10px"><i class="{icon}" style="font-size:64px;color:var(--title)"></i>'
            f'<span style="font-family:Unbounded;font-size:17px;color:var(--p-light)">{label}</span></div>')


PROJECTS = [
    ("bridge-tf", "art", ART_NETWORK, "Pre-registered", "Breast cancer · scRNA-seq · Regulons", "BRIDGE-TF",
     "Conserved transcription-factor modules behind malignant cell-state plasticity. Two scRNA-seq atlases, validated in metastasis and TCGA-BRCA. Protocol published before the analysis."),
    ("solubility", "img", "proj-solubility.webp", None, "ADME · Cheminformatics · Machine learning", "Solubility under scaffold shift",
     "9,145 curated molecules. XGBoost reaches RMSE 0.85 on a random split but 1.23 log units on unseen scaffolds; error grows as similarity to training falls."),
    ("melanoma-resistance", "img", "proj-melanoma-resistance.webp", None, "Melanoma · scRNA-seq · Immunotherapy", "Malignant resistance program",
     "7,186 cells from 31 tumours. A tumour-level pseudobulk reanalysis cut 5,384 cell-level hits to 117; EMP1 loss after treatment is the robust signal."),
    ("trials-brazil", "img", "proj-trials-brazil.webp", None, "Clinical operations · Python · API", "Oncology trials in Brazil",
     "1,908 interventional trials and 11,387 Brazilian sites from ClinicalTrials.gov. 72% industry-sponsored, 73% multinational."),
    ("melanoma-biomarkers", "img", "proj-volcano.webp", "In progress", "Melanoma · Smart-seq2 · Biomarkers", "Response to checkpoint blockade",
     "16,291 CD45+ cells from 48 biopsies. Cell states and signatures that separate responders from non-responders to anti-PD-1 and anti-CTLA-4."),
    ("scanpy-lowmem", "art", glyph("ri-cpu-line", "16 GB"), None, "Scanpy · Harmony · pySCENIC", "scanpy-lowmem",
     "Patterns and patches to integrate ~486k single cells on a 16 GB laptop, each tied to the error it solved."),
    ("omics-fetch", "art", glyph("ri-database-2-line", "GEO · cBioPortal · GDC"), None, "Python · Public data", "omics-fetch",
     "Download scripts for public cancer data that keep working on large cohorts, straight from NCBI FTP and the cBioPortal API."),
    ("cell-seeding", "art", glyph("ri-test-tube-line", "Cell seeding"), "Live", "Wet lab · HTML · No dependencies", "Cell seeding calculator",
     "Bench tool that turns a counted cell suspension into a master-mix recipe for plates and flasks."),
]


def project_card(kind, cover, badge, subtitle, title, desc, link_label="View on GitHub", position="center"):
    if kind == "img":
        cover_html = f'<div style="height:300px;background:#fff;overflow:hidden"><img src="{IMG}/{cover}" style="width:100%;height:100%;object-fit:cover;object-position:{position}"></div>'
    else:
        cover_html = ('<div style="height:300px;display:grid;place-items:center;background:radial-gradient(circle at 75% 20%,hsla(258,80%,58%,.55),transparent 55%),'
                      f'radial-gradient(circle at 15% 90%,hsla(200,80%,50%,.25),transparent 50%),var(--card2)">{cover}</div>')
    badge_html = (f'<span style="position:absolute;top:16px;left:16px;padding:5px 13px;border-radius:30px;font-size:14px;font-weight:600;color:#fff;'
                  f'background:{"hsla(240,10%,10%,.88)" if badge == "In progress" else "var(--p-alt)"}">{badge}</span>') if badge else ""
    body = f"""<div style="position:absolute;inset:0;border:1px solid var(--line);border-radius:22px;overflow:hidden;background:var(--card);display:flex;flex-direction:column">
{cover_html}{badge_html}
<div style="padding:22px 26px;display:flex;flex-direction:column;gap:9px;flex:1">
  <span style="font-size:14px;color:var(--p);font-weight:600;letter-spacing:.02em">{subtitle}</span>
  <h3 style="font-size:23px">{title}</h3>
  <p style="font-size:15.5px;line-height:1.55;flex:1">{desc}</p>
  <span style="color:var(--title);font-weight:600;font-size:15px">{link_label} <i class="ri-arrow-right-up-line"></i></span>
</div></div>"""
    return page(body, 620, CARD_H)


def expertise():
    items = [("01", "Single-cell &amp; bulk transcriptomics", "QC, multi-cohort integration, malignant cell states, regulons, pseudobulk DE."),
             ("02", "Target prioritisation &amp; drug repurposing", "Linking expression programs to druggable targets and existing compounds."),
             ("03", "ADME &amp; cheminformatics", "RDKit featurisation, scaffold-aware validation, applicability domain."),
             ("04", "Clinical &amp; regulatory landscape", "Trial-registry feasibility, medical affairs and ANVISA regulatory work.")]
    cards = "".join(f"""<div class="card" style="padding:24px 26px;display:grid;grid-template-columns:34px 1fr;column-gap:14px;row-gap:6px;align-content:start">
<span style="font-family:Unbounded;color:var(--p);font-size:16px;grid-row:span 2;padding-top:4px">{n}</span>
<h3 style="font-size:19px">{t}</h3><p style="font-size:15.5px">{d}</p></div>""" for n, t, d in items)
    return page(f"""<h2 class="title" style="padding-top:44px">What I <span>work on</span></h2>
<div style="position:absolute;left:90px;right:90px;top:140px;display:grid;grid-template-columns:1fr 1fr;gap:18px">{cards}</div>""", 1280, 450)


def experience():
    def col(title, entries):
        rows = "".join(f"""<div class="card" style="position:relative;padding:18px 22px;margin-bottom:14px">
<span style="position:absolute;left:-31px;top:24px;width:14px;height:14px;border-radius:50%;background:var(--bg);border:2px solid var(--p);box-shadow:0 0 12px hsla(258,80%,58%,.6)"></span>
<h3 style="font-size:17px">{t}</h3><div style="color:var(--p);font-weight:600;font-size:14.5px;margin-top:4px">{p}</div>
{f'<p style="font-size:14.5px;margin-top:6px">{d}</p>' if d else ''}</div>""" for t, p, d in entries)
        return f"""<div><div style="display:inline-block;padding:9px 22px;border-radius:30px;background:var(--p-alt);color:#fff;font-weight:600;font-size:15px;margin-bottom:22px">{title}</div>
<div style="position:relative;padding-left:30px"><div style="position:absolute;left:6px;top:8px;bottom:22px;width:1px;background:linear-gradient(var(--p),var(--line))"></div>{rows}</div></div>"""
    exp = [("Responsible Pharmacist · Medical Affairs &amp; Scientific Lead", "Medra Brasil · São Paulo", "Technical responsibility, regulatory affairs and scientific content."),
           ("University Lecturer · Pharmacy", "Afya Universidade Unigranrio", "Online Pharmacy programme; member of the Structuring Teaching Core (NDE)."),
           ("Research collaboration", "LABEC · Universidade de Mogi das Cruzes", "Computational oncology and drug repurposing."),
           ("Doctoral researcher", "Universität zu Köln · Germany", "Extracellular vesicles and Lyn kinase signalling in CLL.")]
    edu = [("PhD in Biochemistry", "Universität zu Köln · Germany", "Recognised in Brazil by UFRGS."),
           ("MSc in Biotechnology", "Universidade de Mogi das Cruzes", "PLGA nanoparticles and peptides for drug delivery."),
           ("Postgraduate specialisations", "Pharmacology · Regulatory Affairs", None),
           ("Pharmacy degree", "Registered pharmacist, CRF-SP", None)]
    return page(f"""<h2 class="title" style="padding-top:44px">Experience &amp; <span>education</span></h2>
<div style="position:absolute;left:90px;right:90px;top:140px;display:grid;grid-template-columns:1fr 1fr;gap:56px">{col("Experience", exp)}{col("Education", edu)}</div>""", 1280, 760)


def contact_card(icon, label, value):
    return page(f"""<div style="position:absolute;inset:0;border:1px solid var(--line);border-radius:22px;background:var(--card);display:grid;place-content:center;justify-items:center;gap:6px">
<i class="{icon}" style="font-size:40px;color:var(--p);margin-bottom:6px"></i>
<span style="font-family:Unbounded;color:var(--title);font-weight:600;font-size:20px">{label}</span>
<span style="font-size:15px;color:var(--muted)">{value}</span></div>""", 400, 210)


def render(html, name, w, h, tmp):
    src = tmp / f"{name}.html"
    src.write_text(html, encoding="utf8")
    out = ASSETS / f"{name}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--default-background-color=00000000", f"--force-device-scale-factor={SCALE}",
                    "--virtual-time-budget=8000", f"--window-size={w},{h}", f"--screenshot={out}", src.as_uri()],
                   check=True, capture_output=True)
    print("wrote", out.name)


def main():
    ASSETS.mkdir(exist_ok=True)
    tmp = Path(tempfile.mkdtemp())
    try:
        render(hero(), "hero", 1280, 600, tmp)
        render(about(), "about", 1280, 640, tmp)
        render(section_title("Selected", "projects"), "title-projects", 1280, 130, tmp)
        for key, kind, cover, badge, sub, title, desc in PROJECTS:
            card = project_card(kind, cover, badge, sub, title, desc,
                                LINK_LABEL.get(key, "View on GitHub"), COVER_POSITION.get(key, "center"))
            render(card, f"card-{key}", 620, CARD_H, tmp)
        render(expertise(), "expertise", 1280, 450, tmp)
        render(experience(), "experience", 1280, 760, tmp)
        render(section_title("Selected", "publications"), "title-publications", 1280, 130, tmp)
        render(section_title("Let's", "talk", "Open to collaborations in computational oncology, postdoctoral positions "
                             "and translational research roles in industry."), "title-contact", 1280, 170, tmp)
        for key, icon, label, value in [("portfolio", "ri-global-line", "Portfolio", "thaisdolzany.github.io"),
                                        ("linkedin", "ri-linkedin-box-line", "LinkedIn", "Send a message"),
                                        ("orcid", "ri-graduation-cap-line", "ORCID", "Publication record")]:
            render(contact_card(icon, label, value), f"contact-{key}", 400, 210, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
