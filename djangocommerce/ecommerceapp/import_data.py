# import_data.py
import pandas as pd
from ecommerceapp.models import Product 

def import_data(file_path):
    try:
      
        df = pd.read_excel(file_path)

      
        for index, row in df.iterrows():
            Product.objects.create(
                name=row['Name'],
                description=row['Description'],
                price=row['Price'],
                image=row['Image'],
                category=row['Category'],
            
            )

        print("Import successful!")
    except Exception as e:
        print(f"Error during import: {e}")


if __name__ == "__main__":
    file_path = "path/to/your/excel/file.xlsx"
    import_data(file_path)
