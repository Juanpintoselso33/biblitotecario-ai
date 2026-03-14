import sys
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\Users\trico\OneDrive\UBA\Analisis CIGOB\output\01_analisis_votometro_tecnico.md'
with open(path, encoding='utf-8') as f:
    content = f.read()
print('length:', len(content))
