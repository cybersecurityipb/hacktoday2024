use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn check(input: &str) -> bool {
    let enc: [u32; 14] = [3839659437,1341186360,573349873,593025942,3480065291,2419960532,319440920,435129863,4041771554,1937840669,329441504,3208216387,3406776571,2845364712];
    let mut input_bytes = prepare_input(input);
    let key: [u32; 4] = [2037477999, 1903325039, 1919905641, 1869572462];
    for chunk in input_bytes.chunks_mut(2) {
        let enc = tea_enc(key, chunk);
        chunk[0] = enc[0];
        chunk[1] = enc[1];
    }
    input_bytes == enc
}

fn prepare_input(input: &str) -> Vec<u32> {
    let mut input_bytes: Vec<u32> = Vec::new();
    
    for chunk in input.as_bytes().chunks(4) {
        let mut tmp: u32 = 0;
        for (i, &byte) in chunk.iter().enumerate() {
            tmp |= (byte as u32) << (i * 8);
        }
        input_bytes.push(tmp);
    }
    
    if input_bytes.len() % 2 != 0 {
        input_bytes.push(0);
    }
    
    input_bytes
}

fn tea_enc(key: [u32; 4], v: &mut [u32]) -> [u32; 2] {
    let mut v0 = v[0];
    let mut v1 = v[1];
    let mut sum: u32 = 0;
    let delta: u32 = 0x9e3779b9;
    let k = key;
    
    for _ in 0..32 {
        sum = sum.wrapping_add(delta);
        v0 = v0.wrapping_add((v1 << 4).wrapping_add(k[0]) ^ v1.wrapping_add(sum) ^ (v1 >> 5).wrapping_add(k[1]));
        v1 = v1.wrapping_add((v0 << 4).wrapping_add(k[2]) ^ v0.wrapping_add(sum) ^ (v0 >> 5).wrapping_add(k[3]));
    }
    
    [v0, v1]
}
