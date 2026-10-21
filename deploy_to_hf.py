"""
Deploy Deep-Stego Secure to Hugging Face Spaces automatically.
"""
import os
import sys
from huggingface_hub import HfApi

def deploy():
    token = os.environ.get("HF_TOKEN")
    if not token:
        token = input("Enter your Hugging Face Write Token (get from https://huggingface.co/settings/tokens): ").strip()
        if not token:
            print("Error: Hugging Face token is required.")
            sys.exit(1)

    username = input("Enter your Hugging Face username: ").strip()
    if not username:
        print("Error: Username is required.")
        sys.exit(1)

    space_name = input("Enter Space name [default: deep-stego-deploy]: ").strip() or "deep-stego-deploy"
    repo_id = f"{username}/{space_name}"

    api = HfApi(token=token)
    print(f"\n🚀 Connecting to Hugging Face Space: {repo_id}...")
    try:
        api.create_repo(
            repo_id=repo_id,
            repo_type="space",
            space_sdk="docker",
            private=False,
            exist_ok=True
        )
        print("✅ Space created/verified successfully as Docker Space!")
    except Exception as e:
        print(f"Repository creation message: {e}")
        # Verify if repository actually exists
        try:
            api.repo_info(repo_id=repo_id, repo_type="space")
            print("✅ Verified: Space repository exists.")
        except Exception:
            print(f"❌ Error: Could not find or create repository {repo_id}. Check token permissions.")
            sys.exit(1)

    print("\n📦 Uploading project files and model weights (best.pt ~66MB)...")
    print("This may take 1-3 minutes depending on your internet connection...")

    api.upload_folder(
        folder_path=".",
        repo_id=repo_id,
        repo_type="space",
        ignore_patterns=[
            "deep-stego.ipynb",
            "src/*",
            "deploy_to_hf.py",
            "__pycache__/*",
            "*.pyc"
        ]
    )

    print(f"\n🎉 All files uploaded successfully!")
    print(f"👉 Your Space is building and will be live at: https://huggingface.co/spaces/{repo_id}")
    print("\nHugging Face will build the Docker container in about 2-3 minutes.")

if __name__ == "__main__":
    deploy()
