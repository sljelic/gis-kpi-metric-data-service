"""Prepare one semantic release's metadata, distributions and documentation."""
from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import sys
from packaging.version import Version

ROOT=Path(__file__).resolve().parents[1]
PROJECT_ROOT=ROOT/os.environ.get("PYTHON_PROJECT_DIR", ".")


def set_version(value, root=PROJECT_ROOT):
    version=str(Version(value))
    path=root/'pyproject.toml';content=path.read_text()
    start=content.index('[project]');end=content.find('\n[',start+1)
    if end<0:end=len(content)
    section,count=re.subn(r'(?m)^version\s*=\s*"[^"]+"',f'version = "{version}"',content[start:end],count=1)
    if count!=1:raise ValueError('Expected one static project version')
    path.write_text(content[:start]+section+content[end:])
    if (root/'VERSION').exists():(root/'VERSION').write_text(version+'\n')
    if (root/'provider.yaml').exists():
        import yaml
        path=root/'provider.yaml';provider=yaml.safe_load(path.read_text())
        provider.pop('version',None)
        provider['versions']=[version,*[str(v) for v in provider.get('versions',[]) if str(v)!=version]]
        path.write_text(yaml.safe_dump(provider,sort_keys=False))
    return version


def main():
    version=set_version(sys.argv[1])
    for path in (ROOT/'dist',ROOT/'build',ROOT/'docs/_build'):
        if path.exists():shutil.rmtree(path)
    subprocess.run([sys.executable,'-m','build',str(PROJECT_ROOT),'--outdir',str(ROOT/'dist')],cwd=ROOT,check=True)
    subprocess.run([sys.executable,'scripts/registry.py','validate'],cwd=ROOT,check=True)
    source=os.environ.get('DOCS_SOURCE','docs')
    subprocess.run(['sphinx-build','-W','-b','html',source,'docs/_build/html'],cwd=ROOT,check=True)
    shutil.make_archive(str(ROOT/'dist'/f'docs-html-{version}'),'zip',ROOT/'docs/_build/html')
    if os.environ.get('BUILD_PDF','0')=='1':
        subprocess.run(['sphinx-build','-W','-b','simplepdf',source,'docs/_build/pdf'],cwd=ROOT,check=True)
        for pdf in (ROOT/'docs/_build/pdf').rglob('*.pdf'):shutil.copy2(pdf,ROOT/'dist'/pdf.name)


if __name__=='__main__':main()
