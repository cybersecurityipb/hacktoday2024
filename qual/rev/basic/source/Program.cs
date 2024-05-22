using System;
using System.Numerics;
using System.Text;
using System.IO;
using System.Security.Cryptography;
using System.Diagnostics;

namespace Basic
{
    public class RSA
    {
        private int e = 0x10001;
        private BigInteger PublicKey;
        public RSA(BigInteger PublicKey)
        {
            this.PublicKey = PublicKey;
        }
        public BigInteger Encrypt(BigInteger message)
        {
            return BigInteger.ModPow(message, e, PublicKey);
        }
    }
    public class ChaCha20
    {
        private uint[] state;

        public ChaCha20(byte[] key, byte[] nonce, uint counter)
        {
            state = new uint[16];
            state[0] = 0x61707865;
            state[1] = 0x3320646e;
            state[2] = 0x79622d32;
            state[3] = 0x6b206574;

            for (int i = 0; i < 8; i++)
            {
                state[i + 4] = BitConverter.ToUInt32(key, i * 4);
            }

            state[12] = counter;

            for (int i = 0; i < 3; i++)
            {
                state[i + 13] = BitConverter.ToUInt32(nonce, i * 4);
            }
        }

        private void QuarterRound(ref uint a, ref uint b, ref uint c, ref uint d)
        {
            a += b; d ^= a; d = (d << 16) | (d >> 16);
            c += d; b ^= c; b = (b << 12) | (b >> 20);
            a += b; d ^= a; d = (d << 8) | (d >> 24);
            c += d; b ^= c; b = (b << 7) | (b >> 25);
        }

        public byte[] Encrypt(byte[] plaintext)
        {
            byte[] ciphertext = new byte[plaintext.Length];
            byte[] block = new byte[64];

            int blockCount = plaintext.Length / 64;
            int remainder = plaintext.Length % 64;

            for (int i = 0; i < blockCount; i++)
            {
                ChaCha20Block(block);
                for (int j = 0; j < 64; j++)
                {
                    ciphertext[i * 64 + j] = (byte)(plaintext[i * 64 + j] ^ block[j]);
                }
            }

            if (remainder > 0)
            {
                ChaCha20Block(block);
                for (int j = 0; j < remainder; j++)
                {
                    ciphertext[blockCount * 64 + j] = (byte)(plaintext[blockCount * 64 + j] ^ block[j]);
                }
            }

            return ciphertext;
        }

        private void ChaCha20Block(byte[] block)
        {
            uint[] temp = new uint[16];
            state.CopyTo(temp, 0);

            for (int i = 0; i < 10; i++)
            {
                // Column round
                QuarterRound(ref temp[0], ref temp[4], ref temp[8], ref temp[12]);
                QuarterRound(ref temp[1], ref temp[5], ref temp[9], ref temp[13]);
                QuarterRound(ref temp[2], ref temp[6], ref temp[10], ref temp[14]);
                QuarterRound(ref temp[3], ref temp[7], ref temp[11], ref temp[15]);

                // Diagonal round
                QuarterRound(ref temp[0], ref temp[5], ref temp[10], ref temp[15]);
                QuarterRound(ref temp[1], ref temp[6], ref temp[11], ref temp[12]);
                QuarterRound(ref temp[2], ref temp[7], ref temp[8], ref temp[13]);
                QuarterRound(ref temp[3], ref temp[4], ref temp[9], ref temp[14]);
            }

            for (int i = 0; i < 16; i++)
            {
                temp[i] += state[i];
            }

            for (int i = 0; i < 16; i++)
            {
                Array.Copy(BitConverter.GetBytes(temp[i]), 0, block, i * 4, 4);
            }

            state[12]++;
        }
    }
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length != 1)
            {
                Console.WriteLine("Usage: ./program.exe <filename>");
                return; 
            }

            nodbg();
            string filename = args[0];

            if (File.Exists(filename))
            {
                string encryptedFileName = filename + ".Encrypted";

                try
                {
                    byte[] encryptedData = Encrypt(File.ReadAllBytes(filename));
                    File.WriteAllBytes(encryptedFileName, encryptedData);
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Error: " + ex.Message);
                }
            }
            else
            {
                Console.WriteLine("File not found: " + filename);
            }
        }

        static byte[] Encrypt(byte[] message)
        {
            byte[] key = GenerateRandomKey(32);
            byte[] nonce = GenerateRandomKey(12);
            RSA rsa = new RSA(BigInteger.Parse("167779367812792709915032707913032638382146251004558791142676786028501280044057627112826094280092505414510766384827088804978848108688648026981142540400168610823829003843442596437735093142183606826724002523744218048425313679193864739770021775952653310093258321014896182483000543295733022993925140727306455407233"));
            ChaCha20 chacha = new ChaCha20(key, nonce, 0);
            byte[] ciphertext = chacha.Encrypt(message);
            byte[] nonceEnc = rsa.Encrypt(new BigInteger(
                value : nonce,
                isUnsigned : true,
                isBigEndian: true
            )).ToByteArray();
            byte[] output = ciphertext.Concat(key).Concat(nonceEnc).ToArray();

            return output;
        }

        static byte[] GenerateRandomKey(int keySizeBytes)
        {
            byte[] key = new byte[keySizeBytes];
            using (RandomNumberGenerator rng = RandomNumberGenerator.Create())
            {
                rng.GetBytes(key);
            }
            return key;
        }

        static void nodbg()
        {
            try 
			{
				Process[] processes = Process.GetProcesses();
				foreach (Process process in processes)
				{
                    if (process.ProcessName == "dnSpy" || process.ProcessName == "ILSpy" || process.ProcessName == "ida64" || process.ProcessName == "ida32")
                    {
                        Console.WriteLine("Debugger detected!");
                        Environment.Exit(-1);
                    }
                    Console.WriteLine(process.ProcessName);
				}
            }
            catch (Exception) 
            {
                Environment.Exit(-1);
            }
        }
    }
}