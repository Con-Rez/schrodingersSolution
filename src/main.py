import subprocess

def run_ai_fixed_response_test():
    result = subprocess.run(['python3', 'src/aiResponse.py'], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

if __name__ == "__main__":
    run_ai_fixed_response_test()