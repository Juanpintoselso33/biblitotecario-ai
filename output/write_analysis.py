import sys
sys.stdout.reconfigure(encoding='utf-8')

content = open("/c/Users/trico/OneDrive/UBA/Analisis CIGOB/output/analysis_content.md", encoding='utf-8').read()
with open("/c/Users/trico/OneDrive/UBA/Analisis CIGOB/output/01_analisis_votometro_tecnico.md", 'w', encoding='utf-8') as f:
    f.write(content)
print("done")
