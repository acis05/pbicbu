import os, io, tempfile
from pathlib import Path
from datetime import datetime,date
from flask import Flask, render_template, request, jsonify
from openpyxl import load_workbook
app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH']=10*1024*1024
BASE=Path(__file__).parent
DATA=Path(os.environ.get('DATA_DIR',BASE/'data'))
DATA.mkdir(parents=True,exist_ok=True)
TARGET=DATA/'current.xlsx'
def parse(source):
    w=load_workbook(source,read_only=True,data_only=True)
    try:
        rows=iter(w.active.values); a=next(rows); b=next(rows)
        if str(a[0]).strip().lower()!='tanggal' or [str(x).strip().upper() for x in b[1:5]]!=['FG1','FG2','RW1','RW2']: raise ValueError('Header Excel tidak sesuai template.')
        result={}
        for row in rows:
            if not any(x is not None for x in row): continue
            d=row[0]
            if not isinstance(d,(date,datetime)): d=datetime.strptime(str(d),'%Y-%m-%d')
            key=d.strftime('%Y-%m-%d'); vals=row[1:5]
            if len(vals)!=4 or any(not isinstance(v,(int,float)) or isinstance(v,bool) or not __import__('math').isfinite(v) for v in vals): raise ValueError('Nilai FG/RW harus berupa angka lengkap.')
            old=result.get(key,[0]*4); result[key]=[x+y for x,y in zip(old,vals)]
        if not result: raise ValueError('Tidak ada data.')
        return [dict(zip(['date','FG1','FG2','RW1','RW2'],[k,*v])) for k,v in sorted(result.items())]
    finally: w.close()
@app.get('/')
def index(): return render_template('index.html')
@app.get('/api/data')
def data(): return jsonify(parse(TARGET if TARGET.exists() else BASE/'data/default.xlsx'))
@app.post('/api/upload')
def upload():
    f=request.files.get('file')
    if not f or not f.filename.lower().endswith('.xlsx'): return jsonify(error='Pilih file .xlsx'),400
    try:
        raw=f.read(); rows=parse(io.BytesIO(raw))
        with tempfile.NamedTemporaryFile(dir=DATA,delete=False) as tmp: tmp.write(raw); name=tmp.name
        os.replace(name,TARGET)
        return jsonify(rows)
    except Exception: return jsonify(error='Excel tidak valid. Gunakan template, tanggal Excel atau YYYY-MM-DD, dan angka lengkap.'),400
@app.get('/health')
def health(): return 'OK'
