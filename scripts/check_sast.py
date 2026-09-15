import os
import sys
import subprocess

def run_quality_gate():
    print("[1/3] Запуск статического анализа кода Semgrep SAST...")
    print("[2/3] Сканирование на наличие критических уязвимостей (уровень ERROR)...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    app_dir = os.path.join(project_root, "app")
    
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    
    cmd = ["semgrep", "scan", "--config", "auto", "--severity", "ERROR", app_dir]
    # Попробуем использовать путь из semgrep-env
    semgrep_exe = os.path.join(project_root, "..", "semgrep-env", "Scripts", "semgrep.exe")
    if sys.platform == "win32" and os.path.exists(semgrep_exe):
        cmd[0] = semgrep_exe
        
    res = subprocess.run(cmd, env=env, cwd=project_root)
    print(f"[3/3] Код завершения анализатора: {res.returncode}")
    
    if res.returncode != 0:
        print("==================================================================")
        print("[FAIL] QUALITY GATE FAILED: Обнаружены критические уязвимости!")
        print("Сборка остановлена. Исправьте дефекты безопасности.")
        print("==================================================================")
        sys.exit(1)
    else:
        print("==================================================================")
        print("[+] QUALITY GATE PASSED: Критические уязвимости не обнаружены!")
        print("Сборка проекта и деплой разрешены для дальнейших этапов CI/CD.")
        print("==================================================================")
        sys.exit(0)

if __name__ == "__main__":
    run_quality_gate()
