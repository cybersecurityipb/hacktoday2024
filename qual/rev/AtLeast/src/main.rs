use aes::Aes128;
use block_modes::{BlockMode, Cbc};
use block_modes::block_padding::Pkcs7;
use hex_literal::hex;
use std::io;

type Aes128Cbc = Cbc<Aes128, Pkcs7>;

const ENC: [u8; 96] = [237, 148, 244, 113, 73, 102, 31, 250, 225, 229, 80, 16, 30, 160, 201, 51, 94, 130, 168, 224, 126, 59, 248, 236, 31, 150, 252, 67, 39, 244, 36, 102, 225, 36, 95, 199, 129, 172, 203, 54, 147, 200, 166, 175, 101, 170, 232, 16, 192, 245, 16, 104, 174, 232, 210, 141, 246, 22, 228, 209, 56, 243, 146, 6, 7, 81, 58, 197, 212, 123, 109, 201, 129, 200, 105, 13, 59, 234, 181, 75, 171, 37, 162, 240, 18, 210, 219, 39, 90, 24, 35, 240, 107, 38, 80, 177];

fn main() {
    // let message: String = String::from("hacktoday{Fucking_rust_B1naRy_ru_kidding_M3?!?_bUt_AtLeast_it's_Easy,Do_you_think+it's_Easy??}");
    let mut message: String = String::new();
    io::stdin().read_line(&mut message).expect("masukin apa bang");
    let plaintext: &[u8] = message.trim().as_bytes();

    let iv: [u8; 16] = hex!("01c35d9de24cdab152ce94db6c0b9103");
    let key:[u8; 16] = hex!("c01ebc5b30a8d42d0b08bfd5c38b9513");

    let cipher: Cbc<Aes128, Pkcs7> = Aes128Cbc::new_from_slices(&key, &iv).unwrap();
    let pos: usize = plaintext.len();

    let mut buffer: [u8; 128] = [0u8; 128];
    buffer[..pos].copy_from_slice(plaintext);

    let ciphertext: &[u8] = cipher.encrypt(&mut buffer, pos).unwrap();

    if ciphertext == ENC {
        println!("yep");
    } else {
        println!("nah");
    }
}