# Deep-Stego: Neural Image Steganography with Cryptographic Verification

An end-to-end deep learning framework for imperceptible image-into-image steganography coupled with authenticated AES-256-GCM payload encryption and verifiable routing.

---

## 1. Abstract

Steganography is the practice of concealing secret information within an ordinary, non-suspicious carrier medium. Traditional spatial steganography techniques (such as Least Significant Bit substitution) are susceptible to statistical steganalysis and exhibit low payload capacity.

**Deep-Stego** introduces a dual deep neural network pipeline based on U-Net architectures:
1. A **Hiding Network** that embeds a full-resolution secret image into a cover carrier image, minimizing spatial and frequency-domain perceptual artifacts.
2. A **Reveal Network** that reconstructs the secret payload from the stego image.

To mitigate the vulnerability of weight-leakage and unauthorized extraction inherent to standard neural steganography, Deep-Stego implements an **AES-256-GCM cryptographic layer** with PBKDF2-HMAC-SHA256 key derivation. Even if an adversary obtains the complete model weights, the reconstructed payload remains mathematically undecryptable without the ephemeral secret passphrase.

---

## 2. System Architecture

```
Cover Image (3x128x128)  ──┐
                           ├─► [Hiding Network: U-Net] ─► Stego Image (3x128x128)
Secret Image (3x128x128) ──┘                                      │
                                                                  ▼
                                                      [AES-256-GCM Encryption]
                                                                  │
                                                                  ▼
                                                       Encrypted Transmission
                                                                  │
                                                                  ▼
                                                      [AES-256-GCM Decryption]
                                                                  │
                                                                  ▼
                                                      [Reveal Network: U-Net]
                                                                  │
                                                                  ▼
                                                     Reconstructed Secret (3x128x128)
```

### 2.1 Neural Network Specifications
- **Input Resolution**: 128 x 128 pixels (RGB, 3 channels, normalized to [0, 1]).
- **Hiding Network**:
  - Input: 6 channels (Concatenation of 3-channel Cover and 3-channel Secret).
  - Architecture: 5-level encoder-decoder U-Net with skip connections.
  - Encoder Channels: 6 -> 64 -> 128 -> 256 -> 512.
  - Decoder Channels: 512 -> 256 -> 128 -> 64 -> 3.
  - Activation: LeakyReLU (slope = 0.2) in encoder, ReLU in decoder, Sigmoid output.
- **Reveal Network**:
  - Input: 3 channels (Synthesized Stego Image).
  - Architecture: 5-level encoder-decoder U-Net with skip connections.
  - Output: 3 channels (Reconstructed Secret Image).
- **Model Checkpoint**: Pretrained weights stored in `best.pt` (~66 MB), tracked via Git LFS.

### 2.2 Cryptographic Defense-in-Depth
- **Cipher**: AES-256-GCM (Authenticated Encryption with Associated Data).
- **Key Derivation Function (KDF)**: PBKDF2-HMAC-SHA256 with 480,000 iterations.
- **Initialization Vector (IV)**: 96-bit cryptographically secure pseudorandom nonce per transmission.
- **Salt**: 128-bit cryptographically random salt per payload.
- **Integrity Guarantee**: 128-bit authentication tag ensures ciphertext tampering detection prior to neural reconstruction.

---

## 3. Evaluation & Steganographic Metrics

The framework evaluates concealment fidelity and reconstruction accuracy using standard computer vision metrics:

| Metric | Formulation / Criterion | Target Value | Description |
| :--- | :--- | :--- | :--- |
| **PSNR** | $10 \log_{10}\left(\frac{MAX^2}{MSE}\right)$ | > 30 dB | Quantifies peak signal-to-noise ratio between cover and stego carrier. |
| **SSIM** | $\frac{(2\mu_x\mu_y + c_1)(2\sigma_{xy} + c_2)}{(\mu_x^2 + \mu_y^2 + c_1)(\sigma_x^2 + \sigma_y^2 + c_2)}$ | > 0.95 | Evaluates structural luminance and contrast fidelity against human perception. |
| **Detection Resistance** | $0.7 \times \text{SSIM}_{\text{norm}} + 0.3 \times \text{PSNR}_{\text{norm}}$ | > 90% | Composite index quantifying robustness against statistical steganalysis. |

---

## 4. Platform Components

- **Application Layer**: Streamlit Python framework styled with a minimalist monochrome interface.
- **Deep Learning Runtime**: PyTorch (CPU-optimized for standard production and cloud inference).
- **Database & Identity**: Supabase (PostgreSQL with Row Level Security for authenticated user profiles and message routing).
- **Encrypted Storage**: Supabase S3-compatible Object Storage for encrypted binary payloads.
- **Network Routing**: Peer-to-peer Stego-ID identifier addressing (`DSS-XXXXXX`).

---

## 5. Repository Structure

```
├── .gitattributes          # Git LFS configuration for best.pt weights
├── .gitignore              # Exclusion rules for bytecode, cache, and secrets
├── README.md               # Technical project documentation
├── app.py                  # Primary Streamlit application and inference pipeline
├── best.pt                 # Pretrained PyTorch model state dictionary (Git LFS)
├── crypto_utils.py         # AES-256-GCM, PBKDF2, and Stego-ID generation
├── requirements.txt        # Python package dependencies
└── supabase_schema.sql     # Database DDL schema, foreign keys, and RLS policies
```

---

## 6. Installation & Local Execution

### Prerequisites
- Python 3.10+
- Git and Git LFS

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/durgeshshukla797/deep-stego.git
   cd deep-stego
   ```

2. **Pull model weights via Git LFS**:
   ```bash
   git lfs pull
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application**:
   ```bash
   streamlit run app.py
   ```

5. Open `http://localhost:8501` in your browser.

---

## 7. License

This project is licensed under the MIT License.