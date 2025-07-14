import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# Mapping function to determine department code based on job title


def determine_department(job_title: str) -> str:
    if not isinstance(job_title, str):
        job_title = str(job_title)
    jt = job_title.lower()
    if any(
        keyword in jt
        for keyword in ["admin", "administrator", "don", "director of nursing"]
    ):
        return "BL1"
    elif any(
        keyword in jt for keyword in ["department head", "rn", "registered nurse"]
    ):
        return "BL2"
    else:
        return "BL3"


def process_workbook():
    input_path = filedialog.askopenfilename(
        title="Select Excel File", filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if not input_path:
        return

    output_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        title="Save Combined Workbook As",
        filetypes=[("Excel files", "*.xlsx *.xls")],
    )
    if not output_path:
        return

    try:
        xls = pd.ExcelFile(input_path)
        frames = []
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            frames.append(df)
        combined = pd.concat(frames, ignore_index=True)

        # Attempt to find a column that likely contains job titles
        job_title_col = None
        for col in combined.columns:
            if str(col).strip().lower() in ["job title", "title", "position"]:
                job_title_col = col
                break
        if job_title_col is None:
            # fallback to the first column
            job_title_col = combined.columns[0]

        department_values = combined[job_title_col].apply(determine_department)

        # Ensure there are at least 10 columns so we can place department at index 9
        while combined.shape[1] < 9:
            combined[f"Unnamed_{combined.shape[1]+1}"] = ""

        combined.insert(9, "Department", department_values)

        combined.to_excel(output_path, index=False)
        messagebox.showinfo("Success", f"Combined workbook saved to {output_path}")
    except Exception as exc:
        messagebox.showerror("Error", str(exc))


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    process_workbook()
