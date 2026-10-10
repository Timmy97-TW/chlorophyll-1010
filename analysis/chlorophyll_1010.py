import sys, json, openpyxl, statistics as st
wb=openpyxl.load_workbook(sys.argv[1],data_only=True)
V=4.0
def grp(ws,rows,names,blank,fwrow0=22,alt=None):
    out=[]
    for i,(r,n) in enumerate(zip(rows,names)):
        a645=[ws.cell(r,c).value for c in (1,2,3)]
        a663=[ws.cell(r,c).value for c in (4,5,6)]
        if alt and r in alt: a645=alt[r]
        fw=ws.cell(fwrow0+i,6).value
        sheet=ws.cell(fwrow0+i,5).value
        reps=[]
        for x,y in zip(a645,a663):
            x_,y_=x-blank,y-blank
            tot=8.02*y_+20.2*x_           # ug/mL
            ca=12.7*y_-2.69*x_; cb=22.9*x_-4.68*y_
            reps.append(dict(a645=x,a663=y,tot=tot,mgg=tot*V/1000/fw,ug=tot*V,ab=ca/cb))
        m=lambda k:[q[k] for q in reps]
        d=dict(name=n,fw=fw,sheet=sheet,a645=a645,a663=a663,
               mgg=m('mgg'),mean=st.mean(m('mgg')),sd=st.stdev(m('mgg')),
               ug=st.mean(m('ug')),ab=st.mean(m('ab')),max663=max(a663),mean663=st.mean(a663))
        d['cv']=d['sd']/d['mean']*100
        out.append(d)
    return out
b=wb['20261010 Bopep4 Salinity']
bn=[f"{t}|{c}" for t in ("Control","Pre","Co","Post") for c in (0,75,100)]
B=grp(b,range(6,18),bn,0.037)
a=wb['20261010 ACCD SOIL SALINITY']
an=["TB|0","TB|300","Pre|300","Co|300","Post|300"]
A=grp(a,range(6,11),an,0.037)
A2=grp(a,range(6,11),an,0.037,alt={6:[0.224,0.214,0.223]})
for lab,G in (("BOPEP",B),("ACCD",A),("ACCD alt",A2)):
    print(lab)
    for d in G:
        print(f"{d['name']:12s} fw={d['fw']:.4f} mgg={d['mean']:.3f}±{d['sd']:.3f} cv={d['cv']:.1f}% sheet={d['sheet']:.4f} ratio={d['mean']/d['sheet']:.3f} ug={d['ug']:.1f} a/b={d['ab']:.2f} A663mean={d['mean663']:.3f} max={d['max663']:.3f}")
def corr(x,y):
    mx,my=st.mean(x),st.mean(y)
    return sum((p-mx)*(q-my) for p,q in zip(x,y))/ (sum((p-mx)**2 for p in x)*sum((q-my)**2 for q in y))**.5
for lab,G in (("B",B),("A",A)):
    print(lab,"r(fw,mgg)=",round(corr([d['fw'] for d in G],[d['mean'] for d in G]),3),"r(fw,ug)=",round(corr([d['fw'] for d in G],[d['ug'] for d in G]),3), "r(1/fw,mgg)", round(corr([1/d['fw'] for d in G],[d['mean'] for d in G]),3))
json.dump(dict(bopep=B,accd=A,accd_alt=A2),open(sys.argv[2],'w'),indent=1)
