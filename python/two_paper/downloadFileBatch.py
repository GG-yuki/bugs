import pandas as pd
import xlrd
from downloadFile import downloadFile


def downloadFromXls(xlsPath, localPath):
    df = pd.read_excel(xlsPath)
    df = pd.DataFrame(df)

    for i, row in df.iterrows():
        address = "https://www.ncbi.nlm.nih.gov" + getattr(row, "LInk")
        print(str(i) + ": " + address)
        try:
            downloadFile(address=address, localPath=localPath, local_file_name=i)
        except:
            print("ERROR" + str(i) + ' ' + address)
    return


if __name__ == "__main__":
    localPath = "F:/ZHL_download_files/"
    downloadFromXls(
        xlsPath=localPath + "PMC.xls",
        localPath=localPath,
    )
