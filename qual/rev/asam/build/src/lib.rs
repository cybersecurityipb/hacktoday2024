use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn check(input: &str) -> bool {
    let enc = [3839659437, 1341186360, 2258978845, 287028135, 3773907231, 3148196059, 1919102421, 487438519, 3441371210, 3761107162, 4089870006, 1296473502, 2468068580, 3433399734, 2091112295, 3305929185, 3300395815, 4116423227, 844991392, 1536208801];
    let mut input_bytes = prepare_input(input);
    let key: [u32; 4] = [2037477999, 1903325039, 1919905641, 1869572462];
    for chunk in input_bytes.chunks_mut(2) {
        let enc = tea_enc(key, chunk);
        chunk[0] = enc[0];
        chunk[1] = enc[1];
    }
    if input_bytes != enc {
        return false;
    }
    let transformed_input: Vec<u8> = input[13..].chars()
    .map(|c| (c as u8 ^ 0x69) as u8)
    .collect();
    let cheese: Vec<u8> = vec![54, 0, 7, 54, 30, 8, 26, 4, 54, 11, 28, 29, 54, 0, 36, 8, 13, 12, 54, 12, 8, 26, 16, 54, 26, 89, 54, 28, 42, 89, 28, 5, 13, 54, 10, 1, 12, 12, 26, 12, 54, 0, 29, 54, 11, 28, 29, 54, 88, 33, 89, 25, 12, 54, 16, 6, 28, 54, 7, 89, 29, 20];

    transformed_input == cheese
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
