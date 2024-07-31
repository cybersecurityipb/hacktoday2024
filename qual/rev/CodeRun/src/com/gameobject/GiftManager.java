package com.gameobject;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

public class GiftManager {
    private String fakeflag="hacktoday{upsss_this_is_fake_flag_hehehe}";
    private String gift = "KHh19flIeUhU/3JYD7dnrIlkG2G9i7/YPHMpRgk1sim+MG3ZdwqTc44lvQVaojKH";
    long apaini[]={15125, 25570, 8745, 4148, 467, 4148, 15125, 467};
    long apaan = 34393;
    long apeni = 3217;

    public boolean check(int x){
        String v = Integer.toString(x);
        long[] data = new long[v.length()];
        for (int i = 0; i < v.length(); i++) {
            char c = v.charAt(i);
            long value = (c + 7) * 99;
            long res = 1;
            long apeni2=apeni;
            while (apeni2 > 0) {
                if ((apeni2 & 1) == 1) {
                    res = (res * value) % apaan;
                }
    
                apeni2 = apeni2 >> 1;
                value = (value * value) % apaan;
            }
            data[i] = res;
        }

        int pjg = data.length;
        for (int i = 0; i < pjg; i++) {
            int j = (i * 9 + 9) % pjg; 
            long temp = data[i];
            data[i] = data[j];
            data[j] = temp;
        }

        if(pjg != apaini.length) return false;
        for (int i = 0; i < pjg; i++) {
            if(data[i] != apaini[i]) return false;
        }

        return true;
    }

    public String printgift(int x){
        String key = Integer.toString(x);
        String rkey = new StringBuilder(key).reverse().toString();
        key+=rkey;
        try{
            byte[] keyData = key.getBytes("UTF-8");
            SecretKeySpec secretKeySpec = new SecretKeySpec(keyData, "AES");
            Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
            cipher.init(Cipher.DECRYPT_MODE, secretKeySpec);
            byte[] decodedData = Base64.getDecoder().decode(gift);
            byte[] decrypted = cipher.doFinal(decodedData);
            return new String(decrypted, "UTF-8");
        }catch (Exception e) {
            e.printStackTrace();
            return fakeflag;
        }
    }
}
