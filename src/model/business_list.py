import os
from dataclasses import dataclass, asdict, field
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from .business import Business

@dataclass
class BusinessList:
    """Manages collection of Business objects and handles data export"""
    business_list: list[Business] = field(default_factory=list)
    save_at: str = 'output'

    def dataframe(self) -> pd.DataFrame:
        """Convert business_list to pandas dataframe"""
        return pd.json_normalize(
            (asdict(business) for business in self.business_list), 
            sep="_"
        )

    def save_to_excel(self, filename: str) -> None:
        """Save data to Excel file, appending if exists"""
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
            
        file_path = f"{self.save_at}/{filename}.xlsx"
        df = self.dataframe()

        if os.path.exists(file_path):
            workbook = load_workbook(file_path)
            sheet = workbook.active
            for row in dataframe_to_rows(df, index=False, header=False):
                sheet.append(row)
            workbook.save(file_path)
        else:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)

    def save_to_csv(self, filename: str) -> None:
        """Save data to CSV file"""
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f"{self.save_at}/{filename}.csv", index=False)
