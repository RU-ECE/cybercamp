#include <iostream>
#include <string>
#include <vector>
#include <openssl/ec.h>
#include <openssl/ecdh.h>
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <openssl/rand.h>
#include <openssl/err.h>

// Helper function to handle OpenSSL errors
void handleErrors() {
    ERR_print_errors_fp(stderr);
    abort();
}

// Generate ECC key pair and save to PEM files
void generateKeyPair() {
    EC_KEY* ecKey = EC_KEY_new_by_curve_name(NID_X9_62_prime256v1);
    if (ecKey == nullptr) handleErrors();

    if (EC_KEY_generate_key(ecKey) != 1) handleErrors();

    // Save private key
    FILE* privFile = fopen("ecc_private_key.pem", "wb");
    if (privFile == nullptr) handleErrors();
    if (PEM_write_ECPrivateKey(privFile, ecKey, nullptr, nullptr, 0, nullptr, nullptr) != 1) handleErrors();
    fclose(privFile);

    // Save public key
    FILE* pubFile = fopen("ecc_public_key.pem", "wb");
    if (pubFile == nullptr) handleErrors();
    if (PEM_write_EC_PUBKEY(pubFile, ecKey) != 1) handleErrors();
    fclose(pubFile);

    EC_KEY_free(ecKey);
    std::cout << "ECC key pair generated and saved in PEM format." << std::endl;
}

// Encrypt a message using ECC
std::vector<unsigned char> encryptMessage(const std::string& message, EC_KEY* publicKey) {
    // Generate an ephemeral key pair
    EC_KEY* ephemeralKey = EC_KEY_new_by_curve_name(NID_X9_62_prime256v1);
    if (EC_KEY_generate_key(ephemeralKey) != 1) handleErrors();

    // Perform ECDH key exchange
    int sharedKeyLen = 32;  // 256 bits
    unsigned char* sharedKey = new unsigned char[sharedKeyLen];
    if (ECDH_compute_key(sharedKey, sharedKeyLen, EC_KEY_get0_public_key(publicKey), ephemeralKey, nullptr) != sharedKeyLen) handleErrors();

    // Use shared key for AES encryption
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    if (ctx == nullptr) handleErrors();

    unsigned char iv[16];
    if (RAND_bytes(iv, sizeof(iv)) != 1) handleErrors();

    if (EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), nullptr, sharedKey, iv) != 1) handleErrors();

    std::vector<unsigned char> ciphertext(message.size() + EVP_CIPHER_block_size(EVP_aes_256_cbc()));
    int len;
    if (EVP_EncryptUpdate(ctx, ciphertext.data(), &len, reinterpret_cast<const unsigned char*>(message.data()), message.size()) != 1) handleErrors();
    int ciphertextLen = len;

    if (EVP_EncryptFinal_ex(ctx, ciphertext.data() + len, &len) != 1) handleErrors();
    ciphertextLen += len;

    ciphertext.resize(ciphertextLen + sizeof(iv) + EC_KEY_get0_public_key(ephemeralKey)->encoded_size);
    memcpy(ciphertext.data() + ciphertextLen, iv, sizeof(iv));
    unsigned char* pubKeyBytes = ciphertext.data() + ciphertextLen + sizeof(iv);
    i2o_ECPublicKey(ephemeralKey, &pubKeyBytes);

    EVP_CIPHER_CTX_free(ctx);
    EC_KEY_free(ephemeralKey);
    delete[] sharedKey;

    return ciphertext;
}

// Decrypt a message using ECC
std::string decryptMessage(const std::vector<unsigned char>& ciphertext, EC_KEY* privateKey) {
    // Extract IV and ephemeral public key from ciphertext
    const unsigned char* iv = ciphertext.data() + ciphertext.size() - 16 - EC_KEY_get0_public_key(privateKey)->encoded_size;
    const unsigned char* ephemeralPubKeyBytes = iv + 16;
    EC_KEY* ephemeralKey = EC_KEY_new_by_curve_name(NID_X9_62_prime256v1);
    o2i_ECPublicKey(&ephemeralKey, &ephemeralPubKeyBytes, EC_KEY_get0_public_key(privateKey)->encoded_size);

    // Perform ECDH key exchange
    int sharedKeyLen = 32;  // 256 bits
    unsigned char* sharedKey = new unsigned char[sharedKeyLen];
    if (ECDH_compute_key(sharedKey, sharedKeyLen, EC_KEY_get0_public_key(ephemeralKey), privateKey, nullptr) != sharedKeyLen) handleErrors();

    // Use shared key for AES decryption
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    if (ctx == nullptr) handleErrors();

    if (EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), nullptr, sharedKey, iv) != 1) handleErrors();

    std::vector<unsigned char> plaintext(ciphertext.size() - 16 - EC_KEY_get0_public_key(privateKey)->encoded_size);
    int len;
    if (EVP_DecryptUpdate(ctx, plaintext.data(), &len, ciphertext.data(), ciphertext.size() - 16 - EC_KEY_get0_public_key(privateKey)->encoded_size) != 1) handleErrors();
    int plaintextLen = len;

    if (EVP_DecryptFinal_ex(ctx, plaintext.data() + len, &len) != 1) handleErrors();
    plaintextLen += len;

    EVP_CIPHER_CTX_free(ctx);
    EC_KEY_free(ephemeralKey);
    delete[] sharedKey;

    return std::string(reinterpret_cast<char*>(plaintext.data()), plaintextLen);
}

int main() {
    // Initialize OpenSSL
    ERR_load_crypto_strings();
    OpenSSL_add_all_algorithms();

    // Generate key pair
    generateKeyPair();

    // Load public key for encryption
    FILE* pubFile = fopen("ecc_public_key.pem", "rb");
    if (pubFile == nullptr) handleErrors();
    EC_KEY* publicKey = PEM_read_EC_PUBKEY(pubFile, nullptr, nullptr, nullptr);
    fclose(pubFile);

    // Load private key for decryption
    FILE* privFile = fopen("ecc_private_key.pem", "rb");
    if (privFile == nullptr) handleErrors();
    EC_KEY* privateKey = PEM_read_ECPrivateKey(privFile, nullptr, nullptr, nullptr);
    fclose(privFile);

    // Example usage
    std::string message = "Hello, ECC!";
    std::cout << "Original message: " << message << std::endl;

    std::vector<unsigned char> ciphertext = encryptMessage(message, publicKey);
    std::string decryptedMessage = decryptMessage(ciphertext, privateKey);

    std::cout << "Decrypted message: " << decryptedMessage << std::endl;

    // Clean up
    EC_KEY_free(publicKey);
    EC_KEY_free(privateKey);
    EVP_cleanup();
    ERR_free_strings();

    return 0;
}