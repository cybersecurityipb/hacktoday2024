package com.gameobject;

import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.spec.KeySpec;
import java.util.ArrayList;
import java.util.Base64;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;

public class GiftManager {
    private String fakeflag="hacktoday{upsss_this_is_fake_flag_(again)_ehehehehehehehehehehe}";
    private String gift = "ibCwMf8C6lK2DpWlajcNClSJ4mkcTsISzA1CsYaSz/sFo7rLNiilZ61XTtYOiGAiTp4JyTCKyavvV71pMQKhwwSJPGpCvp6F/fw4jdMHTNecd8vs+MLfgRQu6CEzz+Z2";
    long[] ekhm = {9739771, 9748457, 9177139, 16481627, 16188631, 11192021, 9188887, 11438111, 15400867, 13872029, 12560267};
    long[] noo = {11495201, 20087279, 12279581, 15936241, 12195289, 9004517, 14319841, 14717887, 13550507, 16149437, 16353977};
    long[] what = {2317923, 6911077, 5987641, 2963639, 4617467, 628623, 9495313, 4673109, 412248, 5680062, 6028258};

    long[] ekhmm = {613141, 997463, 900283, 935413, 819563, 1026661, 727297, 1045391};
    long[] nonoo = {317825153, 162490421, 289363199, 417409397, 203977337, 269122423, 222951973, 203977337};
    long[] whatt = {159265919, 409493227, 198673187, 119711067, 144322529, 17404690, 90631929, 47048868};

    int[] apaini = {130, 136, 133, 131, 138, 129, 128, 137, 135, 132, 134};
    int[] apainii ={513, 517, 519, 520, 522, 521, 515, 512, 514, 518, 516};
    int[] apainiii = {1031, 1027, 1026, 1030, 1029, 1025, 1024, 1028};

    public boolean verify(BigInteger x, BigInteger y){
        String s = x.toString(0);
        int n=s.length();
        ArrayList<BigInteger> v = new ArrayList<>();
        
        for(int i=0;i<n;i+=7){
            int end= Math.min(i+7, n);
            String tmp = s.substring(i, end);
            v.add(new BigInteger(tmp));
        }

        n = v.size();
        for(int i=0; i<n; i++){
            BigInteger tmp = extract(v.get(i), ekhm[apaini[i] ^ 128], noo[apaini[i]^128]);
            tmp = extract(tmp, ekhm[apainii[i] ^ 512], noo[apainii[i]^512]);
            if(!tmp.equals(BigInteger.valueOf(what[i]))) return false;
        }

        if(n!=what.length) return false;

        s = y.toString(0);
        n=s.length();
        ArrayList<BigInteger> d1 = new ArrayList<>();

        for(int i=0;i<n;i+=2){
            int end= Math.min(i+2, n);
            String tmp = s.substring(i, end);
            int a = (int) tmp.charAt(0);
            int b = 0;
            if(tmp.length()>1) b = (int) tmp.charAt(1);
            tmp = Integer.toString(a) + Integer.toString(b);
            d1.add(new BigInteger(tmp));
        }

        n = d1.size();
        for(int i=0; i<n; i++){
            int urgent = apainiii[i] ^ 1024;
            if(urgent>n) urgent=0;
            BigInteger tmp = extract(d1.get(urgent), ekhmm[apainiii[i] ^ 1024], nonoo[apainiii[i]^1024]);
            if(!tmp.equals(BigInteger.valueOf(whatt[i]))) return false;
        }

        if(n != whatt.length) return false;

        return true;
    }

    

    public BigInteger extract(BigInteger x, Long y, Long m) {
        BigInteger hm;
        if (y==0)
            return BigInteger.ONE;
        hm = extract(x, y/2, m);
        hm = hm.mod(BigInteger.valueOf(m));

        if (y % 2 ==0)
            return (hm.multiply(hm)).mod(BigInteger.valueOf(m));
        else {
            return (x.multiply(hm).mod(BigInteger.valueOf(m)).multiply(hm)).mod(BigInteger.valueOf(m));
        }
    }

    public String printgift(BigInteger x, BigInteger y) {
        String xx =x.toString();
        String yy =y.toString();
        if(!verify(x, y)) return fakeflag;
        try {
            byte[] iv = yy.getBytes(StandardCharsets.UTF_8);
            IvParameterSpec ivspec = new IvParameterSpec(iv);

            SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
            KeySpec spec = new PBEKeySpec(xx.toCharArray(), xx.getBytes(), 65536, 256);
            SecretKey tmp = factory.generateSecret(spec);
            SecretKeySpec secretKeySpec = new SecretKeySpec(tmp.getEncoded(), "AES");

            Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5PADDING");
            cipher.init(Cipher.DECRYPT_MODE, secretKeySpec, ivspec);
            return new String(cipher.doFinal(Base64.getDecoder().decode(gift)));
        } catch (Exception e) {
            System.out.println("Error while decrypting: " + e.toString());
        }
        return null;
    }
}
