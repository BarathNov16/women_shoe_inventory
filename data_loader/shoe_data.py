import kagglehub
import pandas as pd

# Download latest version
path = kagglehub.dataset_download("datafiniti/womens-shoes-prices")

print("Path to dataset files:", path)


path.to_csv("wshoe prices", index=False)
print("File saved successfully as my_local_copy.csv")
