# main.py

from etl.load.load import run_pipeline

def main():
    print("Iniciando pipeline de Data Warehouse...")
    run_pipeline()
    print("✅ Pipeline completada con éxito!")

if __name__ == "__main__":
    main()
