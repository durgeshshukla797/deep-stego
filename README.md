---
title: Deep-Stego Secure
emoji: 🔐
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
license: mit
---


# 🔐 Deep-Stego Secure

Military-grade neural image steganography with AES-256 encryption.
Hide secrets inside ordinary images — invisible and unbreakable.

## Features
- **Dual U-Net** neural architecture for hiding & revealing
- **AES-256-GCM** passphrase-based encryption
- **In-app messaging** — send encrypted stego images to other users
- **Decode tab** — upload any stego image to reveal hidden secrets

## Tech Stack
- PyTorch (Dual U-Net)
- Streamlit (UI)
- Supabase (Auth, DB, Storage)
- AES-256-GCM + PBKDF2 (Cryptography)