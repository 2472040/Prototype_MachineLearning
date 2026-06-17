import requests

API_URL = "http://127.0.0.1:8000/predict"

def detect_cyberbullying(text: str) -> dict:
    response = requests.post(API_URL, json={"text": text})
    return response.json()

def run_agent():
    print("=" * 50)
    print("  Cyberbullying Detection Agent")
    print("  Ketik 'exit' untuk keluar")
    print("=" * 50)
    
    while True:
        user_input = input("\nMasukkan teks: ").strip()
        
        if user_input.lower() == 'exit':
            print("Agent berhenti.")
            break
            
        if not user_input:
            print("Teks tidak boleh kosong!")
            continue
        
        print("\nMenganalisis teks...")
        result = detect_cyberbullying(user_input)
        
        print("\n--- Hasil Analisis ---")
        print(f"Teks      : {result['input_text']}")
        print(f"Kategori  : {result['prediction']}")
        
        if result['is_cyberbullying']:
            print(f"Status    : ⚠ CYBERBULLYING TERDETEKSI")
        else:
            print(f"Status    : ✓ Aman - Bukan cyberbullying")
        print("-" * 22)

if __name__ == "__main__":
    run_agent()