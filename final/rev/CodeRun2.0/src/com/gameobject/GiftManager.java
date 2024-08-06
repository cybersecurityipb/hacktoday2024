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
    private String fakeflag="hacktoday{upsss_this_is_fake_flag_(again)_ehehehe}";
    private String gift = "ibCwMf8C6lK2DpWlajcNClSJ4mkcTsISzA1CsYaSz/sFo7rLNiilZ61XTtYOiGAiTp4JyTCKyavvV71pMQKhwwSJPGpCvp6F/fw4jdMHTNecd8vs+MLfgRQu6CEzz+Z2";
    long[] e = {9739771, 9748457, 9177139, 16481627, 16188631, 11192021, 9188887, 11438111, 15400867, 13872029, 12560267};
    long[] en = {11495201, 20087279, 12279581, 15936241, 12195289, 9004517, 14319841, 14717887, 13550507, 16149437, 16353977};
    long[] ct = {2317923, 6911077, 5987641, 2963639, 4617467, 628623, 9495313, 4673109, 412248, 5680062, 6028258};

    long[] e1 = {613141, 997463, 900283, 935413, 819563, 1026661, 727297, 1045391};
    long[] n1 = {317825153, 162490421, 289363199, 417409397, 203977337, 269122423, 222951973, 203977337};
    long[] ct2 = {159265919, 409493227, 198673187, 119711067, 144322529, 17404690, 90631929, 47048868};

    int[] sn = {130, 136, 133, 131, 138, 129, 128, 137, 135, 132, 134};
    int[] sn2 ={513, 517, 519, 520, 522, 521, 515, 512, 514, 518, 516};
    int[] sn3 = {1031, 1027, 1026, 1030, 1029, 1025, 1024, 1028};

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
            BigInteger tmp = power(v.get(i), e[sn[i] ^ 128], en[sn[i]^128]);
            tmp = power(tmp, e[sn2[i] ^ 512], en[sn2[i]^512]);
            if(!tmp.equals(BigInteger.valueOf(ct[i]))) return false;
        }

        if(n!=ct.length) return false;

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
            int id = sn3[i] ^ 1024;
            if(id>n) id=0;
            BigInteger tmp = power(d1.get(id), e1[sn3[i] ^ 1024], n1[sn3[i]^1024]);
            if(!tmp.equals(BigInteger.valueOf(ct2[i]))) return false;
        }

        if(n != ct2.length) return false;

        return true;
    }

    

    public BigInteger power(BigInteger x, Long y, Long m) {
        BigInteger temp;
        if (y==0)
            return BigInteger.ONE;
        temp = power(x, y/2, m);
        temp = temp.mod(BigInteger.valueOf(m));

        if (y % 2 ==0)
            return (temp.multiply(temp)).mod(BigInteger.valueOf(m));
        else {
            return (x.multiply(temp).mod(BigInteger.valueOf(m)).multiply(temp)).mod(BigInteger.valueOf(m));
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
